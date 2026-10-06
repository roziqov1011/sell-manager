"""
Online kurslar ma'lumotlar bazasi va ta'lim dasturlari tavsifi.
Ushbu ma'lumotlar AI Sotuv Menejeri uchun asosiy bilimlar bazasi (Knowledge Base) sifatida xizmat qiladi.
"""

COURSES = {
    "python_backend": {
        "id": "python_backend",
        "title": "🐍 Python & Backend Dasturlash",
        "short_desc": "Noldan kuchli backend dasturchi bo'ling: Python, Django, FastAPI, PostgreSQL, Docker.",
        "duration": "6 oy (haftada 3 kun, jonli darslar + amaliyot)",
        "level": "Noldan boshlovchilar va boshlang'ich bilimi borlar uchun",
        "price_total": "4 800 000 so'm",
        "price_monthly": "800 000 so'm / oyiga (bo'lib to'lash imkoniyati)",
        "discount_price": "4 200 000 so'm (bir yo'la to'langanda 12% chegirma)",
        "skills": [
            "Python asoslari va OOP tamoyillari",
            "Algoritmlar va ma'lumotlar tuzilmalari",
            "PostgreSQL va ma'lumotlar bazalari bilan ishlash",
            "Django va Django REST Framework orqali API yaratish",
            "FastAPI zamonaviy asinxron mikroservislar",
            "Docker, Git, GitHub va CI/CD asoslari",
            "Telegram botlar va sun'iy intellekt API integratsiyasi",
            "Real 4 ta portfolio loyihalar"
        ],
        "bonuses": [
            "O'qish yakunida rasmiy sertifikat",
            "Karyera markazi: Rezyume tayyorlash va intervyuga tayyorlov",
            "Eng yaxshi talabalarga IT kompaniyalarda amaliyot va ishga joylashish ko'magi",
            "Mentorlar tomonidan 24/7 kod tekshiruvi va konsultatsiya"
        ]
    },
    "frontend_react": {
        "id": "frontend_react",
        "title": "⚛️ Frontend & React Dasturlash",
        "short_desc": "Zamonaviy veb-saytlar va interaktiv interfeyslar yaratish: HTML, CSS, JavaScript, React, Next.js.",
        "duration": "5 oy (haftada 3 kun)",
        "level": "Noldan boshlovchilar uchun",
        "price_total": "4 200 000 so'm",
        "price_monthly": "840 000 so'm / oyiga (bo'lib to'lash)",
        "discount_price": "3 700 000 so'm (bir yo'la to'langanda)",
        "skills": [
            "HTML5, CSS3, Flexbox, CSS Grid",
            "TailwindCSS va zamonaviy UI freymvorklar",
            "JavaScript (ES6+) chuqurlashtirilgan darajada",
            "React.js (Hooks, State Management, Redux Toolkit)",
            "Next.js (SSR, SSG, SEO optimizatsiya)",
            "REST API bilan ishlash va ma'lumotlarni ulash",
            "5 ta real portfolio veb-sayt va ilovalar"
        ],
        "bonuses": [
            "Xalqaro standartdagi sertifikat",
            "Freelance platformalarida (Upwork, Fiverr) buyurtma olish bo'yicha maxsus dars",
            "Shaxsiy mentor va kod tahlili"
        ]
    },
    "fullstack_web": {
        "id": "fullstack_web",
        "title": "🚀 Fullstack Web Dasturlash (Python + React)",
        "short_desc": "To'liq veb-dasturchi bo'ling: Frontenddan tortib Backend va server boshqaruvigacha.",
        "duration": "8 oy",
        "level": "Noldan professional darajagacha",
        "price_total": "6 400 000 so'm",
        "price_monthly": "800 000 so'm / oyiga",
        "discount_price": "5 600 000 so'm (bir yo'la to'lovda)",
        "skills": [
            "Frontend (HTML, CSS, JS, React.js)",
            "Backend (Python, Django, FastAPI)",
            "Database (PostgreSQL, Redis)",
            "DevOps asoslari (Docker, Linux, Nginx, Deploy)",
            "Katta startap va korporativ darajadagi 6 ta loyiha"
        ],
        "bonuses": [
            "Kafolatlangan amaliyot (Internship)",
            "Ishga joylashish kafolati (shartnoma asosida)",
            "1 yil davomida barcha kurs yangilanishlariga bepul kirish"
        ]
    },
    "data_science_ai": {
        "id": "data_science_ai",
        "title": "🧠 Data Science & Sun'iy Intellekt (AI)",
        "short_desc": "Katta ma'lumotlar tahlili, Machine Learning va AI modellar yaratish.",
        "duration": "6 oy",
        "level": "Matematika va mantiqqa qiziqishi bor noldan boshlovchilar",
        "price_total": "5 400 000 so'm",
        "price_monthly": "900 000 so'm / oyiga",
        "discount_price": "4 800 000 so'm",
        "skills": [
            "Python data kutubxonalari: NumPy, Pandas, Matplotlib, Seaborn",
            "Ehtimollar nazariyasi va statistik tahlil",
            "Machine Learning (Scikit-learn, tasniflash, regressiya)",
            "Deep Learning va Nefron to'rlar asoslari (PyTorch)",
            "LLM, Prompt Engineering va Gemini/OpenAI API integratsiyasi",
            "Biznes uchun ma'lumotlar tahlili va dashboardlar (Power BI)"
        ],
        "bonuses": [
            "Data Science bo'yicha xalqaro sertifikat",
            "Kaggle musobaqalarida qatnashish va portfolio yaratish",
            "Data Analyst va AI muhandisi sifatida ish topish ko'magi"
        ]
    },
    "ui_ux_design": {
        "id": "ui_ux_design",
        "title": "🎨 UI/UX & Grafik Dizayn",
        "short_desc": "Saytlar va mobil ilovalarning qulay hamda chiroyli dizaynini yarating.",
        "duration": "4 oy",
        "level": "Ijodkor va kompyuterda ishlashni xohlovchilar",
        "price_total": "3 600 000 so'm",
        "price_monthly": "900 000 so'm / oyiga",
        "discount_price": "3 100 000 so'm",
        "skills": [
            "Figma: Auto-layout, komponentlar, prototiplash, dizayn tizimlari",
            "UX tadqiqotlar: User Persona, Wireframe, User Journey",
            "Mobil ilovalar (iOS / Android) dizayni",
            "Photoshop va Illustrator dasturlarida grafik elementlar yaratish",
            "Behance va Dribbble uchun professional portfolio"
        ],
        "bonuses": [
            "Behance profili tayyorlab berish",
            "Buyurtmachilar bilan ishlash va narx belgilash bo'yicha maslahat",
            "Rasmiy sertifikat"
        ]
    },
    "smm_target": {
        "id": "smm_target",
        "title": "📱 SMM & Target Reklama",
        "short_desc": "Ijtimoiy tarmoqlarda biznesni rivojlantirish va to'g'ri auditoriyaga reklama yoqish.",
        "duration": "3 oy",
        "level": "Har kim uchun mos",
        "price_total": "2 700 000 so'm",
        "price_monthly": "900 000 so'm / oyiga",
        "discount_price": "2 300 000 so'm",
        "skills": [
            "Instagram, Telegram va TikTok marketing strategiyalari",
            "Meta Ads Manager: Facebook va Instagramda professional targeting",
            "Kopirayting va sotuv matnlari yozish sirlari",
            "Vizual kontent va qisqa videolar (Reels, Shorts) suratga olish/montaj",
            "Auditoriyani tahlil qilish va sotuv voronkalari (funnels)"
        ],
        "bonuses": [
            "Haqiqiy biznes loyihada amaliy byudjet bilan reklama yoqish",
            "Mijoz topish va shartnoma tuzish bo'yicha darslar",
            "Sertifikat"
        ]
    }
}


def get_course_by_id(course_id: str):
    return COURSES.get(course_id)


def get_courses_list_text() -> str:
    """Foydalanuvchi menyusi uchun kurslar ro'yxati matni"""
    text = "🎓 **Bizning Zamonaviy Online Kurslarimiz:**\n\n"
    for idx, (cid, c) in enumerate(COURSES.items(), 1):
        text += (
            f"**{idx}. {c['title']}**\n"
            f"⏳ Davomiyligi: {c['duration']}\n"
            f"💰 Narxi: {c['price_monthly']}\n"
            f"💡 {c['short_desc']}\n\n"
        )
    text += "👉 *Har bir kurs bo'yicha batafsil ma'lumot olish yoki bepul darsga yozilish uchun menga yozing yoki tugmalardan foydalaning!*"
    return text


def get_knowledge_base_for_ai() -> str:
    """Gemini AI uchun kurslar haqida to'liq bilimlar bazasi matni"""
    kb = "=== AKADEMIYA ONLINE KURSLARI BILIMLAR BAZASI ===\n\n"
    for cid, c in COURSES.items():
        kb += f"--- Kurs: {c['title']} (ID: {c['id']}) ---\n"
        kb += f"Tavsif: {c['short_desc']}\n"
        kb += f"Davomiyligi: {c['duration']}\n"
        kb += f"Daraja: {c['level']}\n"
        kb += f"Jami narx: {c['price_total']}\n"
        kb += f"Oylik to'lov: {c['price_monthly']}\n"
        kb += f"Bir yo'la to'langandagi chegirma: {c['discount_price']}\n"
        kb += "O'rgatiladigan ko'nikmalar:\n" + "\n".join([f"  - {s}" for s in c['skills']]) + "\n"
        kb += "Afzalliklar va bonuslar:\n" + "\n".join([f"  - {b}" for b in c['bonuses']]) + "\n\n"

    kb += """
UMUMIY AKADEMIYA AFZALLIKLARI:
- O'qish formati: 100% online, jonli darslar, barcha darslarning videoyozuvi shaxsiy kabinetda umrbod qoladi.
- Mentorlik tizimi: Har bir talabaga shaxsiy kurator/mentor biriktiriladi.
- Amaliyot: Nazariya faqat 20%, 80% amaliyot va real loyihalar ustida ishlash.
- Bepul sinov: Har bir yangi mijozga 1 ta bepul ochiq dars / sinov darsi taqdim etiladi.
- Bo'lib to'lash: 0% ustamasiz oylik bo'lib to'lash imkoniyati bor.
- Kafolat: 14 kun ichida agar dars ma'qul kelmasa, pulni to'liq qaytarib berish kafolati mavjud!
- Aloqa / Bog'lanish: Agar mijoz telefon raqamini qoldirsa, katta menejer 15 daqiqa ichida qo'ng'iroq qilib, kurs dasturini yuboradi va bepul konsultatsiya beradi.
"""
    return kb
