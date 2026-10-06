# 📚 Online Kurslar AI Sotuv Menejeri Boti — To'liq Texnik Hujjat (Documentation)

Ushbu hujjat **Online Kurslar Sotuv Menejeri Telegram Boti**ning ichki arxitekturasi, modullari, ma'lumotlar bazasi tuzilishi, AI integratsiyalari va deploy qilish yo'riqnomasini o'z ichiga oladi.

---

## 📌 Mundarija
1. [Loyiha Haqida](#1-loyiha-haqida)
2. [Tizim Arxitekturasi (Gibrid AI)](#2-tizim-arxitekturasi-gibrid-ai)
3. [Modullar va Fayllar Vazifasi](#3-modullar-va-fayllar-vazifasi)
4. [Ma'lumotlar Bazasi Sxemasi (Database Schema)](#4-malumotlar-bazasi-sxemasi-database-schema)
5. [AI Modellari Integratsiyasi](#5-ai-modellari-integratsiyasi)
   - [Amazon Strands Decider 2B (Lokal Model)](#amazon-strands-decider-2b-lokal-model)
   - [Google Gemini 3.5 Flash (Bulutli LLM)](#google-gemini-35-flash-bulutli-llm)
6. [Sotuv Voronkasi va Lidlar Boshqaruvi (Lead Management)](#6-sotuv-voronkasi-va-lidlar-boshqaruvi-lead-management)
7. [Buyruqlar va Telegram Hodisalari (Handlers & Commands)](#7-buyruqlar-va-telegram-hodisalari-handlers--commands)
8. [O'rnatish va Serverda Ishga Tushirish (Deployment)](#8-ornatish-va-serverda-ishga-tushirish-deployment)

---

## 1. Loyiha Haqida

Ushbu bot online ta'lim markazlari va akademiyalar uchun mo'ljallangan bo'lib, uning asosiy maqsadi:
* Yangi mijozlarga kurslar haqida professional maslahat berish;
* Mijozning qiziqishi, darajasi va ehtiyojlarini aniqlash (Consultative / SPIN selling);
* Kurslarning narxlari, muddatli to'lov va kafolatlari bo'yicha e'tirozlarni yechish;
* Har bir murojaatdan aniq **Lid (Ariza)** shakllantirish, mijozning telefon raqami va u tanlagan aniq kurs nomini bazaga saqlash hamda adminga uzatish.

---

## 2. Tizim Arxitekturasi (Gibrid AI)

Loyiha eng zamonaviy **Gibrid Agentik AI Arxitekturasi (Dual-Model Architecture)** asosida ishlaydi:

```
[ Foydalanuvchi (Telegram) ]
            │
            ▼
   ┌─────────────────┐
   │   handlers.py   │  ──▶ [ bot_database.db ] (Suhbat konteksti va lidlar)
   └─────────────────┘
            │
   ┌────────┴─────────────────────────────────────────┐
   ▼                                                  ▼
[ 1-BOSQICH: LOKAL ANALITIKA ]            [ 2-BOSQICH: PROFESSIONAL MULOQOT ]
 Amazon Strands Decider 2B                   Google Gemini 3.5 Flash
 (open-weight model)                         (Bulutli multimodal LLM)
 • Niyatni aniqlash (Intent)                 • Xushmuomala sotuvchi xarakteri
 • Kursni avtomatik biriktirish              • Ehtiyojga mos tavsiya
 • Lid harorati (Sovuq/Iliq/Qaynoq)          • E'tirozlar bilan ishlash
 • E'tirozlarni sezish                       • Bepul dars/telefon olish (CTA)
   └────────┬─────────────────────────────────────────┘
            ▼
[ To'liq va Tugallangan Javob ] ──▶ Foydalanuvchiga yuboriladi
```

---

## 3. Modullar va Fayllar Vazifasi

| Fayl | Vazifasi |
|---|---|
| `main.py` | Botni ishga tushiruvchi markaziy modul, dispatcherni yoqish, Strands Decider 2B modelini orqa fonda oldindan yuklash (pre-warm). |
| `config.py` | `.env` faylidan tokenlar, API kalitlar, model nomlari va doimiy parametrlarni yuklash. |
| `courses_data.py` | Barcha online kurslar haqidagi batafsil bilimlar bazasi (Knowledge Base) va ta'lim dasturlari. |
| `database.py` | `aiosqlite` orqali asinxron SQLite ma'lumotlar bazasi (foydalanuvchilar, suhbat xotirasi, lidlar). |
| `decider_service.py` | Amazon Strands Decider 2B modelini boshqarish (Singleton), matndan niyat va kursni avtomatik aniqlash. |
| `ai_service.py` | Google Gemini API bilan asinxron aloqa, professional Sales Manager tizimli prompti, token limitlari va model fallback. |
| `keyboards.py` | Reply va Inline klaviaturalar (kurslar ro'yxati, bitta bosishda kontakt ulashish, ariza tugmalari). |
| `handlers.py` | Telegram xabarlarini, tugma bosilishlarini va kontaktlarni qayta ishlovchi biznes mantiq. |
| `export_leads.py` | Tushgan arizalarni chiroyli formatlangan Microsoft Excel (`.xlsx`) faylga eksport qilish moduli. |
| `.env` | Maxfiy kalitlar: `telegram_bot_token`, `gemini_api_key`, `ADMIN_ID`. |
| `.gitignore` | Xavfsizlik fayli: `.env`, ma'lumotlar bazasi (`*.db`) va Excel fayllarni Gitga chiqib ketishidan himoyalaydi. |

---

## 4. Ma'lumotlar Bazasi Sxemasi (Database Schema)

Loyiha SQLite ma'lumotlar bazasidan foydalanadi (`bot_database.db`).

### 1. `users` jadvali
Foydalanuvchilar profili va ularning oxirgi tanlagan kursi:
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    selected_course TEXT, -- Foydalanuvchi oxirgi qiziqqan/tanlagan kurs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. `messages` jadvali
AI muloqot xotirasi (Conversation Memory). AI ga oxirgi 10-12 ta xabar kontekst sifatida uzatiladi:
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role TEXT, -- 'user' yoki 'model'
    text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

### 3. `leads` jadvali
Menejerlar uchun sotuv arizalari (Leads):
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT,
    phone_number TEXT,
    course_interest TEXT, -- Aniq yozilgan kurs nomi (masalan: 🐍 Python & Backend)
    note TEXT,
    status TEXT DEFAULT 'yangi', -- 'yangi', 'boglanildi', 'yopildi'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 5. AI Modellari Integratsiyasi

### Amazon Strands Decider 2B (Lokal Model)
* **Model ID:** `StrandsAgents/strands-decider-2B-hobson-v19`
* **Vazifasi:** Matn generatsiya qilmaydi, balki foydalanuvchi xabarini 1 ta inferensiyada skan qilib, 4 ta qarorni qabul qiladi:
  1. `course_topic`: Qaysi kursga qiziqmoqda? (`frontend`, `backend`, `fullstack`, `ai_data`, `design`, `marketing`).
  2. `is_lead_intent`: Xarid qilish yoki ro'yxatdan o'tish niyati bormi? (Ha/Yo'q).
  3. `is_objection`: Narx, vaqt yoki ishonch bo'yicha e'tiroz bormi?
  4. `lead_warmth`: Mijozning harorati (0: Sovuq, 1: Iliq, 2: Qaynoq).
* **Tezlik va Asinxronlik:** Model bot bloklanib qolmasligi uchun `asyncio.to_thread` orqali alohida oqimda ishlaydi.

### Google Gemini 3.5 Flash (Bulutli LLM)
* **Model:** `gemini-3.5-flash` (Zaxirada: `gemini-3.1-flash-lite`)
* **Sozlamalar:**
  * `maxOutputTokens: 4096` — javoblar hech qachon chala uzilmasligi kafolatlangan.
  * `thinkingConfig: {"thinkingBudget": 0}` — ichki fikrlashga behuda token ketkazmasdan, darhol to'liq va ravon matn qaytaradi.
* **Vazifasi:** Haqiqiy professional sotuvchi (Aziza) sifatida samimiy suhbatlashish, kurslarning afzalliklarini tushuntirish va har bir javob oxirida harakatga chaqirish (Call to Action).

---

## 6. Sotuv Voronkasi va Lidlar Boshqaruvi (Lead Management)

1. **Kursni tanlash:**
   * Foydalanuvchi kurs ichidagi **"✍️ Ushbu kursga yozilish / Sinov darsi"** tugmasini bosganda yoki matnda kurs haqida so'raganda, uning tanlovi bazadagi `selected_course` ustuniga saqlanadi.
2. **Kontakt ulashish:**
   * Foydalanuvchi **"📱 Telefon raqamimni ulashish"** tugmasini bosganida yoki matnda telefon raqamini yozganda (`+998901234567`), tizim buni tutib oladi.
3. **Lid yaratish:**
   * `leads` jadvaliga mijozning ismi, telefoni va **u tanlagan aniq kursi** yoziladi.
4. **Adminga tezkor bildirishnoma:**
   * Agar `.env` faylida `ADMIN_ID` ko'rsatilgan bo'lsa, adminga darhol yangi ariza haqida quyidagi xabarnoma boradi:
     ```
     🚨 Yangi Ariza (Lead #2)!
     👤 Ism: Anvar Aliyev
     🎯 Kurs: 🐍 Python & Backend Dasturlash
     📞 Tel: +998901234567
     🔗 Telegram: @anvar (ID: 12345678)
     ```

---

## 7. Buyruqlar va Telegram Hodisalari (Handlers & Commands)

| Buyruq / Tugma | Kim uchun | Vazifasi |
|---|---|---|
| `/start` | Foydalanuvchi | Botni ishga tushirish, salomlashish va asosiy menyuni chiqarish. |
| `/help` | Foydalanuvchi | Botdan qanday foydalanish bo'yicha yo'riqnoma. |
| `📚 Kurslarimiz` | Foydalanuvchi | Barcha online kurslar ro'yxatini inline tugmalar bilan ko'rsatish. |
| `🎯 Kurs tanlashda maslahat` | Foydalanuvchi | AI orqali foydalanuvchining maqsadi va darajasini aniqlash. |
| `💰 Narxlar va to'lov` | Foydalanuvchi | Bo'lib to'lash shartlari va chegirmalar haqida to'liq ma'lumot. |
| `📞 Menejer bilan bog'lanish` | Foydalanuvchi | Qaysi kursga yozilishini tanlash va telefon raqam qoldirish. |
| `🔄 Yangi suhbat boshlash` | Foydalanuvchi | Suhbat xotirasini tozalash va yangi muloqot boshlash. |
| `/leads` | **Admin** | So'nggi kelib tushgan barcha arizalar ro'yxatini matn ko'rinishida ko'rish. |
| `/export` yoki `/excel` | **Admin** | Barcha kursga yozilganlar ro'yxatini **Excel (.xlsx)** fayl qilib Telegramga yuklab olish. |

---

## 8. O'rnatish va Serverda Ishga Tushirish (Deployment)

### 1. Talablar
* Python 3.10 yoki undan yuqori (Tavsiya: Python 3.11 - 3.14)
* Git

### 2. Loyihani yuklab olish va paketlarni o'rnatish
```bash
git clone https://github.com/roziqov1011/sell-manager.git
cd sell-manager
pip install -r requirements.txt
```

### 3. `.env` faylini sozlash
`.env` faylini yarating va kalitlaringizni kiriting:
```env
gemini_api_key=AIzaSy...Sizning_Gemini_Kalitingiz
telegram_bot_token=1234567890:AA...Sizning_Bot_Tokeningiz
ADMIN_ID=801372981
```

### 4. Botni ishga tushirish

**Oddiy rejimda:**
```bash
python main.py
```

**Linux (Ubuntu VPS) da Systemd xizmati sifatida (24/7 ishlab turishi uchun):**
`/etc/systemd/system/sell-manager.service`:
```ini
[Unit]
Description=Telegram AI Sales Manager Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/sell-manager
ExecStart=/usr/bin/python3 /var/www/sell-manager/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Xizmatni yoqish:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sell-manager
sudo systemctl start sell-manager
sudo systemctl status sell-manager
```
