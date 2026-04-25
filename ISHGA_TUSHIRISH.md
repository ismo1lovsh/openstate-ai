# 🚀 CleanState AI — To'liq Ishga Tushirish Yo'riqnomasi

## 📦 1-QADAM: Kutubxonalarni o'rnatish

```bash
# Loyiha papkasiga o'ting
cd cleanstate

# Virtual environment yarating
python -m venv venv

# Activate qiling (OS ga qarab)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Kutubxonalarni o'rnating
pip install -r requirements.txt
```

## 🗄️ 2-QADAM: PostgreSQL sozlash

### Variant A — PostgreSQL (professional)
```bash
# PostgreSQL o'rnating (agar yo'q bo'lsa)
# Windows: https://www.postgresql.org/download/windows/
# Linux: sudo apt install postgresql
# Mac: brew install postgresql

# Database yarating
psql -U postgres
CREATE DATABASE cleanstate_db;
\q
```

Keyin `.env` fayl yarating (`.env.example` ni nusxa qiling):
```
DB_NAME=cleanstate_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-cleanstate-secret-key
DEBUG=True
```

### Variant B — SQLite (agar PostgreSQL yo'q bo'lsa, tez variant)

`cleanstate/settings.py` faylini oching, `DATABASES` qismini topib, quyidagicha o'zgartiring:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🔨 3-QADAM: Migration va Seed Data

```bash
# Migration yaratish (agar yo'q bo'lsa)
python manage.py makemigrations

# Database jadvallarini yaratish
python manage.py migrate

# 🌟 ENG MUHIM QADAM — demo ma'lumotlar yuklash
python manage.py seed_data
```

Bu buyruq quyidagilarni yaratadi:
- ✅ 72 ta real tashkilot (Ochiqlik Indeksi 2025)
- ✅ 95+ ta demo amaldor
- ✅ 400+ aktivlar
- ✅ 145+ qarindoshlar
- ✅ 180+ tenderlar
- ⭐ **Alisher Karimov** — demo pitch uchun eng kuchli case (Risk: 94.5/100)

## 👤 4-QADAM: Admin foydalanuvchi yaratish

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@cleanstate.uz
# Password: (o'zingizga qulay qilib yozing)
```

## 🚀 5-QADAM: Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerda oching:
- **http://127.0.0.1:8000/** — Dashboard
- **http://127.0.0.1:8000/admin/** — Admin panel

## 🎯 DEMO SCENARIY (hakaton uchun)

### 1. Dashboard'dan boshlang
http://127.0.0.1:8000/
- Ochiqlik Indeksi 2025 statistikasi
- Yuqori riskli amaldorlar ro'yxati

### 2. Eng kuchli case'ni ko'rsating
http://127.0.0.1:8000/officials/ → **Alisher Karimov** ni toping (yuqorida)

Bu sahifada quyidagilarni ko'rasiz:
- 🚨 Risk Score: **94.5/100** (KRITIK)
- 💰 Daromadi 150 mln, lekin aktivlari 16.8 mlrd (108x ortiq!)
- 💎 7 ta red flags (Rolex, Londondagi kvartira, offshor hisoblar...)
- 📊 Radar chart (4 o'lchovli risk breakdown)
- 👨‍👩‍👧 Qarindoshlar bloki (qaynonasi, kuyovi, qizi)
- 📋 Tenderlar bog'liqliklar

### 3. Network Graph'ni ochib ko'rsating
http://127.0.0.1:8000/network/97/
- Interaktiv grafik (drag & drop)
- Amaldor → Qarindoshlar → Biznes → Tenderlar zanjirasi
- Shubhali bog'lanishlar qizil chiziq bilan ko'rsatilgan

### 4. Lifestyle Analyzer (4-slayd uchun)
http://127.0.0.1:8000/analysis/
- Scatter plot: Daromad vs Aktivlar
- Har bir nuqta — bitta amaldor
- Log scale — anomaliyalar yaqqol ko'rinadi

## 🎨 BRANDING QO'SHISH (ixtiyoriy)

`static/img/` papkaga logotipingizni qo'ying va `templates/base.html` da `logo-icon` qismini o'zgartiring.

## 🐛 MUAMMOLARNI HAL QILISH

### "psycopg2 error"
```bash
pip install psycopg2-binary
```

### "no module named 'decouple'"
```bash
pip install python-decouple
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### Stil buzuq ko'rinsa
```bash
python manage.py collectstatic --noinput
```

## 📋 LOYIHA STRUKTURASI

```
cleanstate/
├── cleanstate/          # Django asosiy sozlamalar
│   ├── settings.py
│   └── urls.py
├── core/                # Umumiy apps va management commands
│   └── management/
│       └── commands/
│           └── seed_data.py  ⭐ ENG MUHIM
├── dashboard/           # Bosh sahifa
├── officials/           # Amaldorlar (eng muhim app!)
│   ├── models.py        # Official, Asset, Relative, Tender
│   └── views.py
├── organizations/       # Tashkilotlar (Ochiqlik Indeksi)
├── analysis/           # Lifestyle analyzer, tender anomaly
├── network/            # Network graph
├── templates/          # Barcha HTML'lar
│   ├── base.html       # Layout
│   ├── dashboard/
│   ├── officials/
│   │   └── detail.html  ⭐ ENG MUHIM SAHIFA
│   └── network/
│       └── graph.html   ⭐ vis.js network graph
└── static/             # CSS, JS, images
```

## 🎯 KEYINGI QADAMLAR

1. ✅ Loyihani ishga tushiring
2. ✅ Seed data yuklang
3. ✅ Alisher Karimov sahifasini demo qiling
4. 📝 Pitch deck tayyorlang (keyingi bosqich)
5. 🎬 Video demo tayyorlang

---

## 💡 PITCH UCHUN ASOSIY NUQTALAR

1. **Muammo:** Bugungi tizim reaktiv (jurnalist yozgandan keyin)
2. **Yechim:** AI proaktiv risk aniqlovchi
3. **Farq:** Ochiqlik Indeksi tashkilot darajasi → Biz shaxs darajasiga tushamiz
4. **Demo:** Alisher Karimov — Risk 94.5/100, 16.8 mlrd aktivlar
5. **Xalqaro tajriba:** UK UWO, Singapore, Estonia modellari

**Hakaton g'olibligiga tayyor! 🚀**
