from django.db import models


class Organization(models.Model):
    """Davlat tashkiloti (Ochiqlik Indeksi 2025 asosida)"""
    
    CATEGORY_CHOICES = [
        ('green', '🟢 Yashil (71-100)'),
        ('yellow', '🟡 Sariq (55-71)'),
        ('red', '🔴 Qizil (0-55)'),
    ]
    
    TYPE_CHOICES = [
        ('ministry', 'Vazirlik'),
        ('committee', 'Qo\'mita'),
        ('agency', 'Agentlik'),
        ('company', 'Korxona'),
        ('bank', 'Bank'),
        ('hokimlik', 'Hokimlik'),
        ('other', 'Boshqa'),
    ]
    
    name = models.CharField("Tashkilot nomi", max_length=300)
    short_name = models.CharField("Qisqa nomi", max_length=100, blank=True)
    org_type = models.CharField("Turi", max_length=20, choices=TYPE_CHOICES, default='other')
    
    # Ochiqlik Indeksi
    openness_score = models.DecimalField("Ochiqlik balli", max_digits=5, decimal_places=2, default=0)
    category = models.CharField("Kategoriya", max_length=10, choices=CATEGORY_CHOICES, default='yellow')
    rank = models.IntegerField("Reyting o'rni", default=0)
    
    # Trend
    score_2024 = models.DecimalField("2024-yil ball", max_digits=5, decimal_places=2, default=0)
    score_2023 = models.DecimalField("2023-yil ball", max_digits=5, decimal_places=2, default=0)
    trend = models.CharField("Trend", max_length=10, choices=[
        ('up', '📈 O\'sish'),
        ('down', '📉 Pasayish'),
        ('stable', '➡️ Stabil'),
    ], default='stable')
    
    # Risk
    risk_score = models.DecimalField("Risk balli (AI)", max_digits=5, decimal_places=2, default=0)
    employees_count = models.IntegerField("Xodimlar soni", default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tashkilot"
        verbose_name_plural = "Tashkilotlar"
        ordering = ['rank', '-openness_score']
    
    def __str__(self):
        return f"{self.name} ({self.openness_score})"
    
    @property
    def category_color(self):
        colors = {'green': '#22c55e', 'yellow': '#eab308', 'red': '#ef4444'}
        return colors.get(self.category, '#6b7280')
    
    @property
    def risk_level(self):
        if self.risk_score >= 70:
            return 'critical'
        elif self.risk_score >= 40:
            return 'high'
        elif self.risk_score >= 20:
            return 'medium'
        return 'low'
    
    def save(self, *args, **kwargs):
        # Avtomatik kategoriya
        score = float(self.openness_score)
        if score >= 71:
            self.category = 'green'
        elif score >= 55:
            self.category = 'yellow'
        else:
            self.category = 'red'
        
        # Trend hisoblash
        if self.score_2024 > 0:
            diff = float(self.openness_score) - float(self.score_2024)
            if diff > 1:
                self.trend = 'up'
            elif diff < -1:
                self.trend = 'down'
            else:
                self.trend = 'stable'
        
        super().save(*args, **kwargs)
