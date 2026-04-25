# CleanState AI — Korrupsiyani Oldindan Ko'radigan Tizim

## 🎯 Loyiha haqida
Amaldorlarning daromadi va hayot tarzi o'rtasidagi nomuvofiqlikni aniqlaydigan AI platforma.

## 🛠️ Texnologiyalar
- **Backend:** Django 5.0
- **Frontend:** Bootstrap 5 + Chart.js + vis.js (network graph)
- **Database:** PostgreSQL
- **Python:** 3.11+

## 📦 O'rnatish

### 1. Virtual environment yaratish
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. PostgreSQL sozlash
```bash
# PostgreSQL'da database yarating
createdb cleanstate_db
```

### 4. `.env` faylini sozlang
```
DB_NAME=cleanstate_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
```

### 5. Migration va seed data
```bash
python manage.py migrate
python manage.py seed_data  # Fake data yuklash
python manage.py createsuperuser
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

## 📋 Modullar
1. **Dashboard** — Ochiqlik Indeksi 2025
2. **Risk Score** — Har bir amaldor uchun
3. **Lifestyle Analyzer** — Daromad vs hayot tarzi
4. **Network Detector** — Yashirin bog'lanishlar
