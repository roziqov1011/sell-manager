# 🚀 Online Kurslar Sotuv Menejeri Telegram Boti (AI Sales Manager)

Ushbu loyiha online ta'lim akademiyalari va o'quv markazlari uchun mo'ljallangan professional **AI Sotuv Menejeri** Telegram boti hisoblanadi. Bot foydalanuvchilar bilan xuddi haqiqiy tajribali sotuv xodimidek (Sales Representative) suhbatlashadi, mijozlarning ehtiyojlarini aniqlaydi, ularga eng mos kurslarni taklif qiladi, e'tirozlarni professional tarzda yechadi va ularni bepul sinov darsiga yoki ariza qoldirishga yo'naltiradi.

---

## 🌟 Asosiy Xususiyatlari

1. **🧠 Gibrid AI Arxitekturasi (Strands Decider 2B + Google Gemini 3.5 Flash):**
   - **Amazon Strands Decider 2B (Lokal Model):** Foydalanuvchi qaysi kursga qiziqayotganini (`frontend`, `backend`, `ai_data`, `design`, `marketing`), xarid niyatini va lid haroratini (sovuq, iliq, qaynoq) real vaqtda aniqlaydi.
   - **Google Gemini 3.5 Flash (Bulutli LLM):** Tabiiy, samimiy va professional sotuvchi sifatida mukammal o'zbek tilida muloqot qiladi.
   - **Tugallangan Javoblar:** `thinkingBudget: 0` va `maxOutputTokens: 4096` sozlamalari orqali javoblar hech qachon chala uzilmaydi.

2. **🎓 Kurslar Bilimlar Bazasi (Knowledge Base):**
   - 🐍 Python & Backend Dasturlash (Django, FastAPI, Docker)
   - ⚛️ Frontend & React Dasturlash
   - 🚀 Fullstack Web Dasturlash (Python + React)
   - 🧠 Data Science & Sun'iy Intellekt (AI)
   - 🎨 UI/UX & Grafik Dizayn
   - 📱 SMM & Target Reklama
   - Narxlar, oylik bo'lib to'lash (0% ustama), 14 kunlik kafolat va bonuslar.

3. **🎯 Kurslarni Avtomatik Kuzatish (Course Tracking):**
   - Foydalanuvchi qaysi kursni ko'rsa yoki qaysi kurs haqida yozsa, bu ma'lumot uning profiliga biriktiriladi.
   - Foydalanuvchi telefon raqamini yuborishi bilan, ro'yxatda u tanlagan **aniq kurs nomi** saqlanadi.

4. **📊 Lidlar va Excel Eksport:**
   - Foydalanuvchi telefonini bitta tugma orqali ulashishi mumkin (`📱 Telefon raqamimni ulashish`).
   - Adminlar uchun `/leads` komandasi (chatda ko'rish) va `/export` yoki `/excel` komandasi orqali barcha arizalarni **Microsoft Excel (.xlsx)** formatida Telegramga yuklab olish imkoniyati.
   - Yangi ariza kelganda adminga bir zumda xabarnoma boradi.

5. **💾 Xotira va Suhbat Tarixi (Conversation Memory):**
   - Asinxron SQLite ma'lumotlar bazasi (`bot_database.db`) orqali har bir foydalanuvchi suhbati saqlanadi.
   - Istalgan vaqtda "🔄 Yangi suhbat boshlash" tugmasi orqali xotirani tozalash mumkin.

---

## 📁 Loyiha Tuzilmasi

```
sell-manager/
├── .env                  # Telegram bot token, Gemini API kalit va Admin ID
├── .env.example          # Namunaviy konfiguratsiya fayli
├── config.py             # Loyiha konfiguratsiyasi
├── courses_data.py       # Kurslar bazasi va ta'lim dasturlari
├── database.py           # SQLite ma'lumotlar bazasi (Users, Messages, Leads)
├── decider_service.py    # Amazon Strands Decider 2B modeli integratsiyasi
├── ai_service.py         # Google Gemini AI integratsiyasi
├── export_leads.py       # Arizalarni Excel (.xlsx) ga eksport qilish
├── keyboards.py          # Reply va Inline tugmalar
├── handlers.py           # Telegram hodisalari va xabarlar logikasi
├── main.py               # Botni ishga tushiruvchi markaziy modul
├── DOCUMENTATION.md      # To'liq texnik hujjat (Technical Documentation)
├── requirements.txt      # Kutubxonalar ro'yxati
└── README.md             # Qo'llanma
```

---

## 📖 To'liq Texnik Hujjat

Loyiha arxitekturasi, ma'lumotlar bazasi jadvallari, AI modellarining ishlash mexanizmi va serverga deploy qilish bo'yicha to'liq ma'lumot olish uchun quyidagi hujjatni o'qing:
👉 **[DOCUMENTATION.md](DOCUMENTATION.md)**

---

## ⚙️ Sozlash va Ishga Tushirish

### 1. `.env` faylini tekshirish
Loyihaning ildiz papkasidagi `.env` fayliga ma'lumotlarni kiriting:
```env
gemini_api_key=Sizning_Gemini_API_Kalitingiz
telegram_bot_token=Sizning_Telegram_Bot_Tokeningiz
ADMIN_ID=Sizning_Telegram_ID_Raqamingiz
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Botni ishga tushirish
```bash
python main.py
```

Telegramda botingizga kiring (masalan: **[@rrtsellmanagerbot](https://t.me/rrtsellmanagerbot)**) va `/start` buyrug'ini bosing!
