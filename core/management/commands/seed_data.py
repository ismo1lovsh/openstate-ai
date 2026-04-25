"""
CleanState AI - Seed Data
Ochiqlik Indeksi 2025 asosida real tashkilotlar va demo amaldorlar
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import date, timedelta
import random

from organizations.models import Organization
from officials.models import Official, Asset, Relative, Tender


# Ochiqlik Indeksi 2025 — real tashkilotlar
ORGANIZATIONS_DATA = [
    # 🟢 YASHIL ZONA (71-100) — 66 ta
    ("O'zbekgidroenergo AJ", "company", 94.4, 94.1, 85.0, 1),
    ("Navoiy kon-metallurgiya kombinati", "company", 94.4, 92.3, 81.5, 2),
    ("Moliya vazirligi", "ministry", 93.2, 91.0, 78.4, 3),
    ("Adliya vazirligi", "ministry", 92.5, 89.6, 82.1, 4),
    ("Davlat soliq qo'mitasi", "committee", 91.8, 88.2, 79.5, 5),
    ("Markaziy bank", "bank", 91.3, 89.8, 85.2, 6),
    ("Prezident Administratsiyasi", "agency", 90.5, 87.4, 80.3, 7),
    ("Iqtisodiyot va moliya vazirligi", "ministry", 89.7, 86.5, 75.8, 8),
    ("Davlat statistika qo'mitasi", "committee", 89.2, 85.3, 77.1, 9),
    ("Raqamli texnologiyalar vazirligi", "ministry", 88.6, 84.9, 72.4, 10),
    ("Oliy ta'lim vazirligi", "ministry", 87.5, 83.2, 78.6, 11),
    ("Maktabgacha va maktab ta'limi vazirligi", "ministry", 86.8, 82.5, 76.3, 12),
    ("Sog'liqni saqlash vazirligi", "ministry", 85.9, 81.7, 74.2, 13),
    ("O'zbekiston havo yo'llari", "company", 85.3, 82.0, 73.5, 14),
    ("Qishloq xo'jaligi vazirligi", "ministry", 84.7, 80.3, 72.8, 15),
    ("Suv xo'jaligi vazirligi", "ministry", 84.2, 79.6, 71.3, 16),
    ("Energetika vazirligi", "ministry", 83.8, 78.9, 70.5, 17),
    ("Transport vazirligi", "ministry", 83.1, 78.4, 69.8, 18),
    ("Tashqi ishlar vazirligi", "ministry", 82.6, 79.2, 75.4, 19),
    ("Mehnat va ijtimoiy himoya vazirligi", "ministry", 82.1, 78.0, 71.2, 20),
    ("Uyg'algan iqtisodiyot va mehnat vazirligi", "ministry", 81.5, 77.3, 70.6, 21),
    ("Oilani qo'llab-quvvatlash qo'mitasi", "committee", 80.9, 76.8, 68.5, 22),
    ("Milliy gvardiya", "agency", 80.3, 76.1, 69.2, 23),
    ("Bojxona qo'mitasi", "committee", 79.8, 75.5, 67.4, 24),
    ("O'zavtosanoat AJ", "company", 79.2, 74.8, 66.9, 25),
    ("O'ztransgaz AJ", "company", 78.7, 74.2, 65.8, 26),
    ("Uzbekneftegaz", "company", 78.1, 73.6, 64.7, 27),
    ("O'zbekiston temir yo'llari", "company", 77.5, 73.0, 65.3, 28),
    ("Paxta vazirligi", "ministry", 77.0, 72.5, 64.2, 29),
    ("Milliy Televideniye va radio", "company", 76.4, 71.9, 63.5, 30),
    ("Sudlar Oliy Kengashi", "agency", 75.9, 71.3, 62.8, 31),
    ("Prokuratura bosh idorasi", "agency", 75.3, 70.8, 62.2, 32),
    ("Mudofaa vazirligi", "ministry", 74.8, 70.2, 61.5, 33),
    ("Ichki ishlar vazirligi", "ministry", 74.2, 69.7, 60.8, 34),
    ("Davlat xavfsizlik xizmati", "agency", 73.7, 69.1, 60.1, 35),
    ("O'zbekinvest", "company", 73.1, 68.6, 59.4, 36),
    ("O'zbekiston pochta", "company", 72.6, 68.0, 58.7, 37),
    ("Fargona viloyati hokimligi", "hokimlik", 72.1, 67.5, 58.0, 38),
    ("Samarqand viloyati hokimligi", "hokimlik", 71.8, 67.1, 57.4, 39),
    ("Buxoro viloyati hokimligi", "hokimlik", 71.5, 66.8, 57.1, 40),
    ("Jizzax viloyati hokimligi", "hokimlik", 71.3, 66.5, 56.8, 41),
    
    # 🟡 SARIQ ZONA (55-71) — 22 ta
    ("Surxondaryo viloyati hokimligi", "hokimlik", 70.5, 65.2, 55.8, 42),
    ("Xorazm viloyati hokimligi", "hokimlik", 69.8, 64.5, 55.2, 43),
    ("Namangan viloyati hokimligi", "hokimlik", 69.1, 63.8, 54.6, 44),
    ("Qashqadaryo viloyati hokimligi", "hokimlik", 68.4, 63.1, 53.9, 45),
    ("Sirdaryo viloyati hokimligi", "hokimlik", 67.7, 62.4, 53.2, 46),
    ("Qoraqalpog'iston Respublikasi", "hokimlik", 67.0, 61.7, 52.5, 47),
    ("Navoiy viloyati hokimligi", "hokimlik", 66.3, 61.0, 51.8, 48),
    ("Turizm va madaniyat vazirligi", "ministry", 65.6, 60.3, 51.1, 49),
    ("Sport vazirligi", "ministry", 64.9, 59.6, 50.4, 50),
    ("Ekologiya va atrof-muhitni muhofaza qilish", "ministry", 64.2, 58.9, 49.7, 51),
    ("Qurilish vazirligi", "ministry", 63.5, 58.2, 49.0, 52),
    ("Uy-joy-kommunal xo'jaligi vazirligi", "ministry", 62.8, 57.5, 48.3, 53),
    ("Davlat aktivlarini boshqarish agentligi", "agency", 62.1, 56.8, 47.6, 54),
    ("O'zagroeksport", "company", 61.4, 56.1, 46.9, 55),
    ("O'zbekiston aero-kosmik agentligi", "agency", 60.7, 55.4, 46.2, 56),
    ("Davlat patent idorasi", "agency", 60.0, 54.7, 45.5, 57),
    ("Ko'chmas mulk kadastri qo'mitasi", "committee", 59.3, 54.0, 44.8, 58),
    ("Innovatsiyalar agentligi", "agency", 58.6, 53.3, 44.1, 59),
    ("O'zbekiston yoshlar ittifoqi", "agency", 57.9, 52.6, 43.4, 60),
    ("O'zbekiston savdo-sanoat palatasi", "agency", 57.2, 51.9, 42.7, 61),
    ("Ma'naviyat va ma'rifat markazi", "agency", 56.5, 51.2, 42.0, 62),
    ("O'zbekiston diniy idorasi", "agency", 55.8, 50.5, 41.3, 63),
    
    # 🔴 QIZIL ZONA (0-55) — 9 ta
    ("Toshkent shahar hokimligi", "hokimlik", 54.2, 48.5, 38.7, 64),
    ("Toshkent viloyati hokimligi", "hokimlik", 52.6, 47.1, 37.4, 65),
    ("Andijon viloyati hokimligi", "hokimlik", 51.8, 46.3, 36.8, 66),
    ("Davlat mulki qo'mitasi (rayonlar)", "committee", 49.5, 44.2, 34.5, 67),
    ("Yer resurslari agentligi", "agency", 47.3, 42.0, 32.6, 68),
    ("Toshkent shahar prokuraturasi", "agency", 45.8, 40.5, 31.2, 69),
    ("Tuman hokimliklari o'rtacha", "hokimlik", 43.5, 38.2, 29.8, 70),
    ("Ba'zi tuman sudlari", "agency", 41.2, 35.9, 27.4, 71),
    ("Kichik davlat korxonalari", "company", 38.7, 33.5, 25.1, 72),
]


# Fake amaldor ismlari
FIRST_NAMES = [
    "Alisher", "Bekzod", "Doniyor", "Eldor", "Farrux", "G'ayrat", "Hasan", "Ibrohim",
    "Jahongir", "Komil", "Laziz", "Mirzohid", "Nodir", "Olim", "Pulat", "Qahramon",
    "Rustam", "Sardor", "Tohir", "Umid", "Vali", "Xurshid", "Yusuf", "Zafar",
    "Anvar", "Bahrom", "Davron", "Elyor", "Feruz", "Ghulom"
]

LAST_NAMES = [
    "Karimov", "Rahimov", "Yusupov", "Abdullayev", "Mirzayev", "Islomov", "Toshmatov",
    "Qodirov", "Umarov", "Xolmatov", "Jo'rayev", "Nabiyev", "O'zbekov", "Rasulov",
    "Salomov", "Tursunov", "Vohidov", "Yoqubov", "Zokirov", "Eshonov", "Qobilov"
]

POSITIONS = {
    'top': [
        "Vazir", "Gubernator", "Raisning birinchi o'rinbosari",
        "Bosh direktor", "Prezident Administratsiyasi rahbari",
    ],
    'senior': [
        "Vazir o'rinbosari", "Viloyat hokimi o'rinbosari",
        "Bosh boshqarma boshlig'i", "Moliya direktori",
        "Bosh direktor o'rinbosari",
    ],
    'middle': [
        "Bo'lim boshlig'i", "Departament boshlig'i",
        "Bosh mutaxassis", "Viloyat vakili",
        "Mintaqa boshlig'i",
    ],
    'regular': [
        "Yetakchi mutaxassis", "Katta inspektor",
        "Bosh inspektor", "Ekspert",
    ]
}

REGIONS = [
    "Toshkent shahar", "Toshkent viloyati", "Samarqand", "Buxoro",
    "Fargona", "Andijon", "Namangan", "Surxondaryo", "Qashqadaryo",
    "Xorazm", "Navoiy", "Jizzax", "Sirdaryo", "Qoraqalpog'iston"
]


class Command(BaseCommand):
    help = 'CleanState AI uchun seed data yuklash'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n🚀 CleanState AI — Seed Data Yuklash\n"))
        
        with transaction.atomic():
            self.clear_data()
            orgs = self.create_organizations()
            self.create_demo_officials(orgs)
            self.create_hero_case(orgs)  # Alisher Karimov — pitch uchun
        
        self.stdout.write(self.style.SUCCESS("\n✅ Seed data muvaffaqiyatli yuklandi!\n"))
        self.print_summary()
    
    def clear_data(self):
        """Eski ma'lumotlarni tozalash"""
        self.stdout.write("🧹 Eski ma'lumotlar tozalanmoqda...")
        Tender.objects.all().delete()
        Relative.objects.all().delete()
        Asset.objects.all().delete()
        Official.objects.all().delete()
        Organization.objects.all().delete()
    
    def create_organizations(self):
        """Ochiqlik Indeksi 2025 tashkilotlarini yaratish"""
        self.stdout.write(f"🏛️  {len(ORGANIZATIONS_DATA)} ta tashkilot yaratilmoqda...")
        
        orgs = []
        for name, org_type, score_2025, score_2024, score_2023, rank in ORGANIZATIONS_DATA:
            org = Organization.objects.create(
                name=name,
                short_name=name.split()[0] if len(name.split()) > 0 else name,
                org_type=org_type,
                openness_score=Decimal(str(score_2025)),
                score_2024=Decimal(str(score_2024)),
                score_2023=Decimal(str(score_2023)),
                rank=rank,
                employees_count=random.randint(50, 5000),
                risk_score=Decimal(str(max(0, 100 - score_2025 + random.uniform(-10, 10))))
            )
            orgs.append(org)
        
        self.stdout.write(self.style.SUCCESS(f"   ✓ {len(orgs)} ta tashkilot yaratildi"))
        return orgs
    
    def create_demo_officials(self, orgs):
        """Demo amaldorlar yaratish"""
        self.stdout.write("👥 Demo amaldorlar yaratilmoqda...")
        
        count = 0
        # Qizil va sariq zonaga ko'proq amaldor
        red_orgs = [o for o in orgs if o.category == 'red']
        yellow_orgs = [o for o in orgs if o.category == 'yellow']
        green_orgs = [o for o in orgs if o.category == 'green']
        
        # Har bir qizil zonada 3-5 ta amaldor (yuqori risk bilan)
        for org in red_orgs:
            for _ in range(random.randint(3, 5)):
                self.create_official(org, risk_bias='high')
                count += 1
        
        # Sariq zonada 2-3 ta
        for org in yellow_orgs[:15]:
            for _ in range(random.randint(2, 3)):
                self.create_official(org, risk_bias='medium')
                count += 1
        
        # Yashil zonadan ba'zilarda 1-2 ta
        for org in random.sample(green_orgs, min(20, len(green_orgs))):
            for _ in range(random.randint(1, 2)):
                self.create_official(org, risk_bias='low')
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f"   ✓ {count} ta amaldor yaratildi"))
    
    def create_official(self, org, risk_bias='medium'):
        """Bitta amaldor yaratish"""
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES) + "ov"
        full_name = f"{first} {last}"
        
        # Lavozim tanlash
        if org.org_type in ['ministry', 'agency']:
            level = random.choice(['top', 'senior', 'middle'])
        else:
            level = random.choice(['senior', 'middle', 'regular'])
        
        position = random.choice(POSITIONS[level])
        
        # Maosh
        salary_ranges = {
            'top': (20_000_000, 50_000_000),
            'senior': (10_000_000, 25_000_000),
            'middle': (5_000_000, 15_000_000),
            'regular': (3_000_000, 8_000_000),
        }
        monthly = random.randint(*salary_ranges[level])
        yearly_income = monthly * 12 + random.randint(0, 50_000_000)
        
        # Aktivlarni risk_bias asosida hisoblash
        if risk_bias == 'high':
            multiplier = random.uniform(8, 25)
        elif risk_bias == 'medium':
            multiplier = random.uniform(3, 8)
        else:
            multiplier = random.uniform(1, 3)
        
        declared_assets = yearly_income * random.uniform(0.5, 2.0)
        
        official = Official.objects.create(
            full_name=full_name,
            organization=org,
            position=position,
            position_level=level,
            monthly_salary=Decimal(str(monthly)),
            declared_income=Decimal(str(yearly_income)),
            declared_assets=Decimal(str(declared_assets)),
            appointed_date=date.today() - timedelta(days=random.randint(30, 2000)),
        )
        
        # Aktivlar yaratish
        total_hidden_assets = yearly_income * multiplier
        self.create_assets(official, total_hidden_assets, risk_bias)
        
        # Qarindoshlar
        if risk_bias in ['high', 'medium']:
            self.create_relatives(official, org, risk_bias)
        
        # Risk hisoblash
        official.calculate_risk()
        return official
    
    def create_assets(self, official, total_value, risk_bias):
        """Aktivlar yaratish"""
        assets_types = []
        
        if risk_bias == 'high':
            # Ko'p hashamatli aktivlar
            assets_types = [
                ('real_estate', 'Villa Toshkentda', True, 0.35),
                ('real_estate', 'Xorijdagi kvartira (Dubai)', True, 0.25),
                ('vehicle', 'Range Rover', True, 0.08),
                ('vehicle', 'Mercedes S-Class', True, 0.07),
                ('luxury', 'Rolex Daytona soat', True, 0.05),
                ('real_estate', 'Dala hovli', False, 0.15),
                ('foreign', 'Xorijiy hisob (BVI)', False, 0.05),
            ]
        elif risk_bias == 'medium':
            assets_types = [
                ('real_estate', 'Kvartira markazda', False, 0.45),
                ('vehicle', 'Toyota Camry', True, 0.15),
                ('real_estate', 'Dala hovli', False, 0.30),
                ('luxury', 'Brendli soat', False, 0.10),
            ]
        else:
            assets_types = [
                ('real_estate', 'Kvartira', True, 0.70),
                ('vehicle', 'Chevrolet Cobalt', True, 0.30),
            ]
        
        for asset_type, name, is_luxury, ratio in assets_types:
            value = int(total_value * ratio * random.uniform(0.8, 1.2))
            Asset.objects.create(
                official=official,
                asset_type=asset_type,
                name=name,
                value=Decimal(str(value)),
                location=random.choice(REGIONS),
                is_declared=random.random() > (0.6 if risk_bias == 'high' else 0.3),
                is_luxury=is_luxury,
                owner_name=official.full_name if random.random() > 0.3 else random.choice(FIRST_NAMES) + " qarindoshi",
                source=random.choice(['Kadastr', 'OSINT', 'Soc. tarmoq', 'Deklaratsiya']),
            )
    
    def create_relatives(self, official, org, risk_bias):
        """Qarindoshlar yaratish"""
        num_relatives = random.randint(2, 4) if risk_bias == 'high' else random.randint(1, 2)
        
        for _ in range(num_relatives):
            rel_type = random.choice(['spouse', 'child', 'in_law', 'sibling'])
            rel_name = random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES) + "ov"
            
            has_business = risk_bias == 'high' and random.random() > 0.3
            has_tenders = has_business and random.random() > 0.4
            
            relative = Relative.objects.create(
                official=official,
                full_name=rel_name,
                relation_type=rel_type,
                has_business=has_business,
                business_name=f'"{rel_name.split()[0]} Biznes" MChJ' if has_business else '',
                business_value=Decimal(str(random.randint(500_000_000, 10_000_000_000))) if has_business else 0,
                has_government_tenders=has_tenders,
                total_tenders_won=random.randint(3, 30) if has_tenders else 0,
                total_tender_value=Decimal(str(random.randint(1_000_000_000, 50_000_000_000))) if has_tenders else 0,
            )
            
            # Tenderlar
            if has_tenders:
                num_tenders = random.randint(3, 8)
                for i in range(num_tenders):
                    Tender.objects.create(
                        title=f"Qurilish/ta'mirlash ishlari №{random.randint(100,999)}",
                        organization=org,
                        company_name=relative.business_name,
                        company_owner=rel_name,
                        value=Decimal(str(random.randint(500_000_000, 5_000_000_000))),
                        announced_date=date.today() - timedelta(days=random.randint(30, 1800)),
                        awarded_date=date.today() - timedelta(days=random.randint(30, 1800)),
                        is_suspicious=random.random() > 0.5,
                        price_vs_market=Decimal(str(random.uniform(15, 45))),
                        linked_relative=relative,
                    )
    
    def create_hero_case(self, orgs):
        """Pitch uchun eng muhim case — Alisher Karimov"""
        self.stdout.write("\n⭐ Pitch case yaratilmoqda: Alisher Karimov...")
        
        # Toshkent shahar hokimligi (qizil zona)
        hokimlik = Organization.objects.filter(name__icontains="Toshkent shahar hokimligi").first()
        if not hokimlik:
            hokimlik = orgs[-1]
        
        # Eski bo'lsa o'chirish
        Official.objects.filter(full_name="Alisher Karimov").delete()
        
        official = Official.objects.create(
            full_name="Alisher Karimov",
            organization=hokimlik,
            position="Viloyat hokimi o'rinbosari",
            position_level='senior',
            monthly_salary=Decimal('12000000'),
            declared_income=Decimal('150000000'),
            declared_assets=Decimal('200000000'),
            appointed_date=date(2019, 3, 15),
        )
        
        # 🏠 Aktivlar — bu juda ham realistik va shok qiluvchi
        assets_data = [
            ('real_estate', 'Villa (Bog\'i Shamol)', 1_200_000_000, 'Toshkent shahar', False, True, 'Qaynonasi Mohira Karimova'),
            ('real_estate', 'Villa (Yunusobod)', 900_000_000, 'Toshkent shahar', False, True, 'Qaynonasi Mohira Karimova'),
            ('real_estate', 'Villa (Chimgan)', 700_000_000, 'Toshkent viloyati', False, True, 'Qaynonasi Mohira Karimova'),
            ('real_estate', 'Kvartira London (Knightsbridge)', 4_500_000_000, 'London, UK', False, True, 'Qizi Nilufar Karimova'),
            ('vehicle', 'Mercedes-Maybach S680', 2_500_000_000, 'Toshkent', False, True, 'O\'z nomida'),
            ('vehicle', 'Range Rover Autobiography', 1_800_000_000, 'Toshkent', True, True, 'O\'z nomida'),
            ('luxury', 'Rolex Daytona (Platinum)', 380_000_000, 'Toshkent', False, True, 'O\'z nomida (Instagram postida)'),
            ('luxury', 'Patek Philippe Nautilus', 420_000_000, 'Toshkent', False, True, 'O\'z nomida'),
            ('foreign', 'Xorijiy bank hisobi (BVI)', 2_300_000_000, 'British Virgin Islands', False, False, 'Oila nomida'),
            ('business', 'Restoran (markazda)', 1_100_000_000, 'Toshkent', False, False, 'Kuyovi Jahongir'),
        ]
        
        for asset_type, name, value, location, is_declared, is_luxury, owner in assets_data:
            Asset.objects.create(
                official=official,
                asset_type=asset_type,
                name=name,
                value=Decimal(str(value)),
                location=location,
                is_declared=is_declared,
                is_luxury=is_luxury,
                owner_name=owner,
                source=random.choice(['Kadastr', 'OSINT (Instagram)', 'Xorijiy reestr', 'Anonim manba']),
            )
        
        # 👨‍👩‍👧 Qarindoshlar
        mohira = Relative.objects.create(
            official=official,
            full_name="Mohira Karimova (qaynonasi)",
            relation_type='in_law',
            has_business=True,
            business_name='"Mohira Invest" MChJ',
            business_value=Decimal('2800000000'),
            has_government_tenders=False,
        )
        
        jahongir = Relative.objects.create(
            official=official,
            full_name="Jahongir Nabiyev (kuyovi)",
            relation_type='in_law',
            has_business=True,
            business_name='"Jahongir Construction" MChJ',
            business_value=Decimal('12000000000'),
            has_government_tenders=True,
            total_tenders_won=47,
            total_tender_value=Decimal('89000000000'),
        )
        
        nilufar = Relative.objects.create(
            official=official,
            full_name="Nilufar Karimova (qizi)",
            relation_type='child',
            has_business=False,
            notes="Londonda tahsil olmoqda — yillik xarajat 450 mln so'm",
        )
        
        # 📋 Tenderlar — kuyovining kompaniyasi yutgan
        tender_titles = [
            "Tuman hokimligi binosi ta'mirlash",
            "Maktab-litsey qurilishi",
            "Ko'cha yoritish tizimi",
            "Suv ta'minoti ta'miri",
            "Kasalxona binosi qurilishi",
            "Sport kompleksi qurilishi",
            "Yo'l qoplamasi ta'mirlash",
            "Bolalar bog'chasi qurilishi",
        ]
        
        for title in tender_titles:
            Tender.objects.create(
                title=title,
                organization=hokimlik,
                company_name='"Jahongir Construction" MChJ',
                company_owner="Jahongir Nabiyev",
                value=Decimal(str(random.randint(1_500_000_000, 8_000_000_000))),
                announced_date=date.today() - timedelta(days=random.randint(100, 1500)),
                awarded_date=date.today() - timedelta(days=random.randint(50, 1400)),
                is_suspicious=True,
                price_vs_market=Decimal(str(random.uniform(25, 48))),
                linked_relative=jahongir,
            )
        
        # AI risk hisoblash
        official.calculate_risk()
        
        # Manual override — dramatik effekt uchun
        official.risk_score = Decimal('94.5')
        official.risk_level = 'critical'
        official.income_mismatch_score = Decimal('98')
        official.lifestyle_score = Decimal('95')
        official.network_score = Decimal('92')
        official.wealth_growth_score = Decimal('88')
        
        official.red_flags = [
            "Topilgan aktivlar yillik daromadidan 108 marta ko'p (16.8 mlrd vs 150 mln)",
            "Qaynonasi nomida 3 ta villa (2.8 mlrd so'm)",
            "Kuyovining kompaniyasi 5 yilda 47 ta tender yutgan (89 mlrd so'm)",
            "Qizi Londonda, yillik xarajat 450 mln so'm",
            "Instagram'da 380 mln so'mlik Rolex soat aniqlangan",
            "Xorijda 2.3 mlrd so'mlik bank hisobi (BVI — offshor zona)",
            "47 ta tenderdan 43 tasi bozor narxidan 25%+ yuqori",
        ]
        
        official.risk_explanation = """🚨 BU AMALDOR KRITIK RISK DARAJASIDA

AI tizim quyidagi jiddiy anomaliyalarni aniqladi:

💰 Daromad nomuvofiqligi (98/100):
Rasmiy yillik daromadi 150 mln so'm, lekin topilgan aktivlar umumiy qiymati 16.8 mlrd so'm. Bu daromaddan 108 marta ko'p!

💎 Hayot tarzi anomaliyasi (95/100):
Instagram postlarida 380 mln so'mlik Rolex Daytona soat aniqlangan. Mercedes-Maybach S680 (2.5 mlrd so'm) shaxsiy transporti.

🕸️ Yashirin tarmoq (92/100):
• Qaynonasi "Mohira Invest" MChJ egasi — 2.8 mlrd so'm biznes
• Kuyovining kompaniyasi "Jahongir Construction" 5 yilda 47 ta davlat tenderini yutgan (89 mlrd so'm)
• 43 ta tenderda bozor narxi 25%+ yuqori (aniq kartel belgilari)

📈 Boylik o'sishi (88/100):
Aktivlar 2019-2026 orasida 200 mln so'mdan 16.8 mlrd so'mga oshgan (84 marta!)

🌍 Offshor signallar:
London (Knightsbridge)da 4.5 mlrd so'mlik kvartira, BVI (British Virgin Islands)da xorijiy hisoblar mavjud.

📊 Tavsiya: SHOSHILINCH PROKURATURA TEKSHIRUVI talab etiladi.
UK UWO (Unexplained Wealth Order) mexanizmiga o'xshash chora — amaldor aktivlarini qonuniy yo'l bilan orttirganini isbot qilishi kerak."""
        
        official.save()
        
        self.stdout.write(self.style.SUCCESS(f"   ⭐ {official.full_name} yaratildi — Risk: {official.risk_score}/100"))
    
    def print_summary(self):
        """Yakuniy statistika"""
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("📊 YAKUNIY STATISTIKA"))
        self.stdout.write("="*50)
        self.stdout.write(f"🏛️  Tashkilotlar: {Organization.objects.count()}")
        self.stdout.write(f"    🟢 Yashil: {Organization.objects.filter(category='green').count()}")
        self.stdout.write(f"    🟡 Sariq: {Organization.objects.filter(category='yellow').count()}")
        self.stdout.write(f"    🔴 Qizil: {Organization.objects.filter(category='red').count()}")
        self.stdout.write(f"\n👥 Amaldorlar: {Official.objects.count()}")
        self.stdout.write(f"    🔴 Kritik: {Official.objects.filter(risk_level='critical').count()}")
        self.stdout.write(f"    🟠 Yuqori: {Official.objects.filter(risk_level='high').count()}")
        self.stdout.write(f"    🟡 O'rta: {Official.objects.filter(risk_level='medium').count()}")
        self.stdout.write(f"    🟢 Past: {Official.objects.filter(risk_level='low').count()}")
        self.stdout.write(f"\n🏠 Aktivlar: {Asset.objects.count()}")
        self.stdout.write(f"👨‍👩‍👧 Qarindoshlar: {Relative.objects.count()}")
        self.stdout.write(f"📋 Tenderlar: {Tender.objects.count()}")
        self.stdout.write(f"    ⚠️  Shubhali: {Tender.objects.filter(is_suspicious=True).count()}")
        self.stdout.write("\n" + "="*50 + "\n")
