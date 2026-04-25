from django.db import models
from organizations.models import Organization


class Official(models.Model):
    """Davlat amaldori"""
    
    POSITION_LEVEL = [
        ('top', 'Yuqori lavozim (vazir, gubernator)'),
        ('senior', 'Yuqori amaldor (o\'rinbosar, bosh)'),
        ('middle', 'O\'rta lavozim (bo\'lim boshlig\'i)'),
        ('regular', 'Oddiy xodim'),
    ]
    
    RISK_LEVEL = [
        ('low', '🟢 Past risk'),
        ('medium', '🟡 O\'rta risk'),
        ('high', '🟠 Yuqori risk'),
        ('critical', '🔴 Kritik risk'),
    ]
    
    # Shaxsiy ma'lumotlar
    full_name = models.CharField("To'liq ismi", max_length=200)
    photo = models.ImageField("Rasm", upload_to='officials/', blank=True, null=True)
    birth_date = models.DateField("Tug'ilgan sana", null=True, blank=True)
    
    # Lavozim
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='officials')
    position = models.CharField("Lavozim", max_length=200)
    position_level = models.CharField("Daraja", max_length=20, choices=POSITION_LEVEL, default='middle')
    appointed_date = models.DateField("Tayinlangan sana", null=True, blank=True)
    
    # Daromad
    monthly_salary = models.DecimalField("Oylik maosh (so'm)", max_digits=15, decimal_places=2, default=0)
    declared_income = models.DecimalField("Deklaratsiya daromadi (yillik)", max_digits=15, decimal_places=2, default=0)
    declared_assets = models.DecimalField("Deklaratsiya aktivlari", max_digits=15, decimal_places=2, default=0)
    
    # AI Risk Analysis
    risk_score = models.DecimalField("Risk balli (0-100)", max_digits=5, decimal_places=2, default=0)
    risk_level = models.CharField("Risk darajasi", max_length=20, choices=RISK_LEVEL, default='low')
    
    # Risk component scores
    income_mismatch_score = models.DecimalField("Daromad nomuvofiqligi", max_digits=5, decimal_places=2, default=0)
    lifestyle_score = models.DecimalField("Hayot tarzi riski", max_digits=5, decimal_places=2, default=0)
    network_score = models.DecimalField("Tarmoq riski", max_digits=5, decimal_places=2, default=0)
    wealth_growth_score = models.DecimalField("Boylik o'sishi riski", max_digits=5, decimal_places=2, default=0)
    
    # AI Explanation
    risk_explanation = models.TextField("AI tushuntirish", blank=True)
    red_flags = models.JSONField("Red flags", default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Amaldor"
        verbose_name_plural = "Amaldorlar"
        ordering = ['-risk_score']
    
    def __str__(self):
        return f"{self.full_name} — {self.position}"
    
    @property
    def total_assets(self):
        """Haqiqiy topilgan aktivlar (AI)"""
        return sum(asset.value for asset in self.assets.all())
    
    @property
    def assets_to_income_ratio(self):
        """Aktivlar / Daromad"""
        if self.declared_income > 0:
            return float(self.total_assets) / float(self.declared_income)
        return 0
    
    def calculate_risk(self):
        """AI Risk hisoblash"""
        # 1. Income mismatch (0-100)
        ratio = self.assets_to_income_ratio
        if ratio > 20:
            income_score = 100
        elif ratio > 10:
            income_score = 80
        elif ratio > 5:
            income_score = 60
        elif ratio > 3:
            income_score = 40
        else:
            income_score = 20
        
        # 2. Lifestyle (luxury items)
        luxury_count = self.assets.filter(is_luxury=True).count()
        lifestyle_score = min(luxury_count * 20, 100)
        
        # 3. Network (relatives with tenders)
        relatives_with_tenders = self.relatives.filter(has_government_tenders=True).count()
        network_score = min(relatives_with_tenders * 25, 100)
        
        # 4. Wealth growth
        wealth_score = 50  # Placeholder
        
        self.income_mismatch_score = income_score
        self.lifestyle_score = lifestyle_score
        self.network_score = network_score
        self.wealth_growth_score = wealth_score
        
        # Final: weighted average
        self.risk_score = (
            income_score * 0.35 +
            lifestyle_score * 0.25 +
            network_score * 0.30 +
            wealth_score * 0.10
        )
        
        # Risk level
        if self.risk_score >= 75:
            self.risk_level = 'critical'
        elif self.risk_score >= 50:
            self.risk_level = 'high'
        elif self.risk_score >= 25:
            self.risk_level = 'medium'
        else:
            self.risk_level = 'low'
        
        # Red flags generation
        flags = []
        if ratio > 10:
            flags.append(f"Aktivlar daromaddan {ratio:.1f} marta ko'p")
        if luxury_count > 0:
            flags.append(f"{luxury_count} ta hashamatli aktiv aniqlangan")
        if relatives_with_tenders > 0:
            flags.append(f"{relatives_with_tenders} ta qarindoshi davlat tenderi yutgan")
        
        self.red_flags = flags
        
        # Explanation
        self.risk_explanation = self._generate_explanation()
        self.save()
    
    def _generate_explanation(self):
        """AI-style tushuntirish"""
        parts = []
        
        if self.income_mismatch_score >= 60:
            parts.append(f"⚠️ Topilgan aktivlar rasmiy daromadidan {self.assets_to_income_ratio:.1f} marta ko'p.")
        
        if self.lifestyle_score >= 40:
            luxury = self.assets.filter(is_luxury=True)
            parts.append(f"💎 Hashamatli aktivlar: {', '.join([a.name for a in luxury[:3]])}.")
        
        if self.network_score >= 50:
            parts.append(f"🕸️ Yaqin qarindoshlari davlat tenderlari bilan bog'liq.")
        
        if not parts:
            return "✅ Sezilarli anomaliyalar topilmadi. Amaldor risk darajasi past."
        
        conclusion = f"\n\n📊 Umumiy xulosa: Bu amaldor {self.get_risk_level_display()} toifasida."
        return "\n".join(parts) + conclusion


class Asset(models.Model):
    """Amaldor aktivlari"""
    
    ASSET_TYPE = [
        ('real_estate', '🏠 Ko\'chmas mulk'),
        ('vehicle', '🚗 Transport vositasi'),
        ('luxury', '💎 Hashamatli buyum'),
        ('business', '🏢 Biznes'),
        ('foreign', '🌍 Xorijiy aktiv'),
        ('other', '📦 Boshqa'),
    ]
    
    official = models.ForeignKey(Official, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField("Turi", max_length=20, choices=ASSET_TYPE)
    name = models.CharField("Nomi", max_length=300)
    value = models.DecimalField("Qiymati (so'm)", max_digits=15, decimal_places=2, default=0)
    location = models.CharField("Joylashuvi", max_length=200, blank=True)
    
    is_declared = models.BooleanField("Deklaratsiyada", default=False)
    is_luxury = models.BooleanField("Hashamatli", default=False)
    owner_name = models.CharField("Rasmiy egasi", max_length=200, blank=True, 
                                   help_text="Agar qarindoshi nomida bo'lsa")
    
    discovered_date = models.DateField("Aniqlangan sana", auto_now_add=True)
    source = models.CharField("Manba", max_length=200, blank=True, 
                              help_text="Kadastr, OSINT, soc. tarmoq va h.k.")
    notes = models.TextField("Izohlar", blank=True)
    
    class Meta:
        verbose_name = "Aktiv"
        verbose_name_plural = "Aktivlar"
        ordering = ['-value']
    
    def __str__(self):
        return f"{self.name} — {self.value:,.0f} so'm"


class Relative(models.Model):
    """Amaldor qarindoshlari"""
    
    RELATION_TYPE = [
        ('spouse', 'Turmush o\'rtoq'),
        ('child', 'Farzand'),
        ('parent', 'Ota-ona'),
        ('sibling', 'Aka-uka/opa-singil'),
        ('in_law', 'Qayin qarindosh'),
        ('other', 'Boshqa'),
    ]
    
    official = models.ForeignKey(Official, on_delete=models.CASCADE, related_name='relatives')
    full_name = models.CharField("Ismi", max_length=200)
    relation_type = models.CharField("Qarindoshlik", max_length=20, choices=RELATION_TYPE)
    
    # Business
    has_business = models.BooleanField("Biznesi bor", default=False)
    business_name = models.CharField("Biznes nomi", max_length=300, blank=True)
    business_value = models.DecimalField("Biznes qiymati", max_digits=15, decimal_places=2, default=0)
    
    # Government connections
    has_government_tenders = models.BooleanField("Davlat tenderlari", default=False)
    total_tenders_won = models.IntegerField("Yutgan tenderlar soni", default=0)
    total_tender_value = models.DecimalField("Umumiy tender qiymati", max_digits=15, decimal_places=2, default=0)
    
    notes = models.TextField("Izohlar", blank=True)
    
    class Meta:
        verbose_name = "Qarindosh"
        verbose_name_plural = "Qarindoshlar"
    
    def __str__(self):
        return f"{self.full_name} ({self.get_relation_type_display()})"


class Tender(models.Model):
    """Davlat tenderlari"""
    
    title = models.CharField("Tender nomi", max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tenders')
    
    company_name = models.CharField("Yutgan kompaniya", max_length=300)
    company_owner = models.CharField("Kompaniya egasi", max_length=200, blank=True)
    
    value = models.DecimalField("Qiymati (so'm)", max_digits=18, decimal_places=2)
    
    announced_date = models.DateField("E'lon qilingan sana")
    awarded_date = models.DateField("G'olib bo'lgan sana")
    
    # Anomalies
    is_suspicious = models.BooleanField("Shubhali", default=False)
    price_vs_market = models.DecimalField("Bozor narxidan %", max_digits=6, decimal_places=2, default=0,
                                           help_text="Masalan 35% yuqori bo'lsa shubhali")
    
    # Linked relative
    linked_relative = models.ForeignKey(Relative, on_delete=models.SET_NULL, 
                                         null=True, blank=True, related_name='tenders')
    
    class Meta:
        verbose_name = "Tender"
        verbose_name_plural = "Tenderlar"
        ordering = ['-awarded_date']
    
    def __str__(self):
        return f"{self.title[:50]} — {self.value:,.0f} so'm"
