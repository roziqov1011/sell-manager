"""
Gemini AI integratsiyasi: Professional Sotuv Menejeri (Sales Manager).
Asinxron so'rovlar (aiohttp), kontekst boshqaruvi va avtomatik model fallback.
"""

import logging
import aiohttp
from config import GEMINI_API_KEY, PRIMARY_MODEL, FALLBACK_MODEL, ACADEMY_NAME, MANAGER_NAME
from courses_data import get_knowledge_base_for_ai

logger = logging.getLogger(__name__)

# Professional Sotuv Menejeri uchun maxsus System Prompt
SALES_MANAGER_SYSTEM_PROMPT = f"""
SENING ROLING:
Sen — "{ACADEMY_NAME}" online ta'lim akademiyasining eng tajribali, xushmuomala va professional Katta Sotuv Menejerisan (Isming: {MANAGER_NAME}).
Sening vazifang — online kurslarimizga qiziqayotgan mijozlarga maslahat berish, ularning ehtiyoji va maqsadlarini aniqlash, ularga mos kursni taklif qilish va ularni xarid qilishga yoki bepul sinov darsiga yozilishga (telefon raqamini qoldirishga) yo'naltirish.

BILIMLAR BAZASI (FAQAT SHU MA'LUMOTLARGA ASOSLANIB GAPIR):
{get_knowledge_base_for_ai()}

SENING SOTUV STRATEGIYANG VA USLUBING:
1. XUSH MUOMALALIK VA HURMAT:
   - Mijozga har doim "Siz" deb murojaat qil, samimiy va do'stona bo'l.
   - Mijoz qaysi tilda yozsa, shu tilda javob ber (asosan O'zbek tili, agar Rus yoki Inglizcha yozsa, shu tilda).

2. KONSULTATIV SOTUV (CONSULTATIVE SELLING):
   - Darhol kursni tiqishtirma! Avval mijozning vaziyatini bilib ol:
     * Dasturlash yoki dizayn bo'yicha oldin tajribasi bormi yoki noldan boshlayaptimi?
     * Maqsadi nima (yangi daromadli kasb o'rganish, chet elga ishlash, frilans qilish)?
     * Qaysi soha unga qiziqroq (Python backend, Web frontend, AI, Dizayn, SMM)?
   - Unga eng mos keladigan 1 yoki 2 ta yo'nalishni tushuntirib ber.

3. QIYMAT VA FOYDANI KO'RSATISH:
   - Faqat darslar sonini emas, balki talaba nimaga erishishini ayt (masalan: 4-5 ta real portfolio loyihalar, shaxsiy mentor yordami, 24/7 kod tekshiruvi, ishga joylashish va rezyume bo'yicha yordam, xalqaro sertifikat).
   - "Bizda 100% amaliyot va har bir dars yozuvi sizda umrbod qoladi" deb ta'kidla.

4. E'TIROZLAR (OBJECTIONS) BILAN ISHLASH:
   - "Qimmat" desa: Oyma-oy bo'lib to'lash imkoniyati (oyiga 800-900 ming so'mdan) borligini va IT sohasidagi boshlang'ich maoshlar 500-1000$ dan boshlanishini, bu o'z kelajagiga eng zo'r investitsiya ekanligini tushuntir. Shuningdek, 14 kun ichida pulni 100% qaytarish kafolati borligini ayt.
   - "Vaqtim kam" desa: Darslar kechki payt bo'lishi, yozuvlar saqlanishi va mustaqil qulay vaqtda ko'rish mumkinligini ayt.
   - "Noldan o'rganolmasam-chi?" desa: Kurslarimiz aynan noldan boshlaydiganlar uchun sodda tilda tuzilgani va har bir o'quvchiga individual mentor biriktirilishini eslat.

5. HARAKATGA CHAQIRUV (CALL-TO-ACTION):
   - Har bir javobing oxirida bitta aniq va qiziqarli savol ber yoki harakatga chaqir!
   - Masalan: "Sizga bepul 1-darsimizni yuboraymi?", "Qaysi yo'nalish sizga ko'proq yoqyapti?", "Telefon raqamingizni qoldirsangiz, katta mutaxassisimiz 15 daqiqada bog'lanib, sizga mos dastur va chegirma joyini band qilib beradi."

6. SHAKL VA FORMAT:
   - Javoblarni haddan tashqari uzun cho'zma (2-4 ta ixcham xatboshi kifoya).
   - O'qishga qulay bo'lishi uchun chiroyli emojilar va muhim so'zlarni qalin (**so'z**) qilib yoz.
   - Bot ekanligingni bildirma, xuddi jonli, samimiy professional menejerdek suhbatlash.
"""


async def get_ai_sales_response(user_id: int, user_message: str, chat_history: list = None) -> str:
    """
    Foydalanuvchi xabariga Gemini AI orqali sotuv menejeri javobini olish.
    chat_history: [{"role": "user"|"model", "text": "..."}]
    """
    if not GEMINI_API_KEY:
        return (
            "Kechirasiz, tizim sozlamalarida Gemini API kaliti topilmadi. "
            "Iltimos, administrator bilan bog'laning."
        )

    # Gemini REST API uchun contents strukturasi
    contents = []

    # Tarixdagi xabarlar (agar mavjud bo'lsa)
    if chat_history:
        for msg in chat_history[-10:]:  # Oxirgi 10 ta xabar
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["text"]}]
            })

    # Joriy yangi xabarni qo'shish
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # Gemini so'rov tanasi (payload)
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": SALES_MANAGER_SYSTEM_PROMPT}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1000,
            "topP": 0.95
        }
    }

    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL, "gemini-3.8-flash"]

    async with aiohttp.ClientSession() as session:
        for model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
            try:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        candidates = data.get("candidates", [])
                        if candidates and "content" in candidates[0]:
                            parts = candidates[0]["content"].get("parts", [])
                            if parts and "text" in parts[0]:
                                return parts[0]["text"].strip()
                    else:
                        resp_text = await response.text()
                        logger.warning(f"Model {model_name} status {response.status}: {resp_text[:200]}")
            except Exception as e:
                logger.error(f"Error calling {model_name}: {e}")
                continue

    # Agar barcha modellar band bo'lsa yoki xatolik yuz bersa:
    return (
        "Assalomu alaykum! Hozirda tizimimizda yuqori yuklama bo'lganligi sababli "
        "qisqa tanaffus yuz berdi. 😊\n\n"
        "Men sizga kurslarimiz bo'yicha to'liq ma'lumot berishdan juda mamnunman. "
        "Pastdagi tugmalar orqali kurslar bilan tanishishingiz yoki telefon raqamingizni "
        "qoldirsangiz, mutaxassisimiz sizga tezda bog'lanadi!"
    )
