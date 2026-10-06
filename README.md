# 🚀 Online Kurslar Sotuv Menejeri Telegram Boti (AI Sales Manager)

Ushbu loyiha online ta'lim akademiyalari va o'quv markazlari uchun mo'ljallangan professional **AI Sotuv Menejeri** Telegram boti hisoblanadi. Bot foydalanuvchilar bilan xuddi haqiqiy tajribali sotuv xodimidek (Sales Representative) suhbatlashadi, mijozlarning ehtiyojlarini aniqlaydi, ularga eng mos kurslarni taklif qiladi, e'tirozlarni professional tarzda yechadi va ularni bepul sinov darsiga yoki ariza qoldirishga yo'naltiradi.

---

## 🌟 Asosiy Xususiyatlari

1. **🧠 Gemini AI integratsiyasi:**
   - Google Gemini modeli orqali ishlaydi (`gemini-3.5-flash` va zaxirada `gemini-3.1-flash-lite`).
   - Professional sotuvchi xarakteri (SPIN / Consultative selling texnikasi).
   - O'zbek, Rus va boshqa tillarda erkin va ravon muloqot.
   - Har bir javob oxirida aniq harakatga chaqiruv (Call to Action / Savol).

2. **🎓 Kurslar Bilimlar Bazasi (Knowledge Base):**
   - Python & Backend Dasturlash (Django, FastAPI, Docker)
   - Frontend & React Dasturlash
   - Fullstack Web Dasturlash
   - Data Science & Sun'iy Intellekt (AI)
   - UI/UX & Grafik Dizayn
   - SMM & Target Reklama
   - Narxlar, oylik bo'lib to'lash (0% ustama), kafolatlar va bonuslar.

3. **💾 Xotira va Suhbat Tarixi (Conversation Memory):**
   - SQLite ma'lumotlar bazasi (`bot_database.db`) orqali har bir foydalanuvchi bilan oxirgi muloqot xotirada saqlanadi.
   - AI foydalanuvchi qaysi soha yoki tajribaga ega ekanligini eslab qoladi.
   - Istalgan vaqtda "🔄 Yangi suhbat boshlash" tugmasi orqali xotirani tozalash mumkin.

4. **📱 Sotuv Voronkasi va Lidlar (Lead Generation):**
   - Foydalanuvchi bitta tugma orqali o'z telefon raqamini yuborishi mumkin (`📱 Telefon raqamimni ulashish`).
   - Shuningdek, matn ichida yozilgan telefon raqamlarini ham avtomatik aniqlaydi va arizalar bazasiga saqlaydi.
   - Adminlar uchun `/leads` komandasi orqali tushgan arizalar ro'yxatini ko'rish imkoniyati.

5. **⚡ Asinxron va Ishonchli Arxitektura:**
   - Aiogram 3.x va aiohttp asinxron kutubxonalari asosida qurilgan.
   - Xabarlar kelganda Telegramda "yozmoqda..." (`typing`) animatsiyasi ko'rsatiladi.
   - Model uzilishi yoki yuklama yuqori bo'lganda avtomatik fallback mexanizmi mavjud.

---

## 📁 Loyiha Tuzilmasi

```
sell-manager/
├── .env                  # Telegram bot token va Gemini API kaliti
├── config.py             # Loyiha konfiguratsiyasi
├── courses_data.py       # Kurslar bazasi va ta'lim dasturlari
├── database.py           # SQLite ma'lumotlar bazasi (Users, Messages, Leads)
├── ai_service.py         # Gemini AI Sales Manager tizimi
├── keyboards.py          # Reply va Inline tugmalar
├── handlers.py           # Bot hodisalari va xabarlarni qayta ishlash
├── main.py               # Botni ishga tushiruvchi asosiy fayl
├── requirements.txt      # Kutubxonalar ro'yxati
└── README.md             # Qo'llanma
```

---

## ⚙️ Sozlash va Ishga Tushirish

### 1. `.env` faylini tekshirish
Loyihaning ildiz papkasidagi `.env` faylida kalitlar mavjudligiga ishonch hosil qiling:
```env
gemini_api_key=Sizning_Gemini_API_Kalitingiz
telegram_bot_token=Sizning_Telegram_Bot_Tokeningiz
ADMIN_ID=Sizning_Telegram_ID_Raqamingiz  # Ixtiyoriy (arizalarni ko'rish uchun)
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Botni ishga tushirish
```bash
python main.py
```

Ishga tushgandan so'ng, Telegramda o'z botingizga kiring (masalan, `@rrtsellmanagerbot`) va `/start` buyrug'ini yuboring!
