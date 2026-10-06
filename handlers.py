"""
Telegram bot hodisalari (handlers) va mantiqi.
Foydalanuvchi buyruqlari, matnli xabarlar, AI javoblari va sotuv voronkasi (funnel).
"""

import re
import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import MANAGER_NAME, ACADEMY_NAME, ADMIN_ID
from courses_data import (
    COURSES,
    get_course_by_id,
    get_courses_list_text
)
import database as db
from ai_service import get_ai_sales_response
from keyboards import (
    get_main_reply_keyboard,
    get_contact_request_keyboard,
    get_courses_inline_keyboard,
    get_course_detail_keyboard,
    get_apply_course_selection_keyboard
)
from decider_service import analyze_user_message

logger = logging.getLogger(__name__)
router = Router()

# Telefon raqami regex patterni
PHONE_REGEX = re.compile(r"(\+?998\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{2}\s?[0-9]{2}|0?[0-9]{9})")


@router.message(CommandStart())
async def handle_start(message: Message):
    """Start buyrug'i: foydalanuvchini kutib olish va sotuv muloqotini boshlash"""
    user = message.from_user
    await db.save_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    greeting_text = (
        f"Assalomu alaykum, **{user.first_name}**! 👋\n\n"
        f"Men — **{MANAGER_NAME}**, **{ACADEMY_NAME}**ning katta sotuv menejeri va ta'lim maslahatchisiman.\n\n"
        "🎯 Zamonaviy, daromadli kasb egalari (Dasturlash, Sun'iy Intellekt, Dizayn, Marketing) "
        "safiga qo'shilishga qaror qilganingizdan juda xursandman!\n\n"
        "Sizga o'zingizga eng mos kursni tanlashda, bepul sinov darsiga yozilishda "
        "va barcha savollaringizga batafsil javob berishda yordam beraman.\n\n"
        "💬 **Menga istalgan savolingizni yozishingiz** yoki quyidagi tugmalardan birini tanlashingiz mumkin:"
    )

    await message.answer(
        text=greeting_text,
        reply_markup=get_main_reply_keyboard(),
        parse_mode="Markdown"
    )


@router.message(Command("help"))
async def handle_help(message: Message):
    """Yordam buyrug'i"""
    help_text = (
        "💡 **Botdan foydalanish bo'yicha qo'llanma:**\n\n"
        "• Shunchaki matn yozing — AI sotuv menejeri savollaringizga to'liq javob beradi.\n"
        "• 📚 **Kurslarimiz** — Barcha zamonaviy ta'lim dasturlarimiz ro'yxati.\n"
        "• 🎯 **Kurs tanlashda maslahat** — Qobiliyatingiz va maqsadingizga qarab yo'nalish tanlash.\n"
        "• 💰 **Narxlar va to'lov** — Narxlar, chegirmalar va bo'lib to'lash shartlari.\n"
        "• 📞 **Menejer bilan bog'lanish** — Telefon raqam qoldirish va bepul sinov darsi.\n"
        "• 🔄 **Yangi suhbat** — Muloqot tarixini yangilash.\n"
        "• `/leads` — Adminlar uchun kelib tushgan arizalarni ko'rish."
    )
    await message.answer(help_text, parse_mode="Markdown")


@router.message(F.text == "📚 Kurslarimiz")
async def show_courses_menu(message: Message):
    """Kurslar ro'yxatini ko'rsatish"""
    try:
        await message.answer(
            get_courses_list_text(),
            reply_markup=get_courses_inline_keyboard(),
            parse_mode="Markdown"
        )
    except Exception:
        await message.answer(
            get_courses_list_text(),
            reply_markup=get_courses_inline_keyboard(),
            parse_mode=None
        )


@router.message(F.text == "💰 Narxlar va to'lov")
async def show_pricing(message: Message):
    """Narxlar va bo'lib to'lash haqida ma'lumot"""
    pricing_text = (
        "💳 **Kurslarimiz narxlari va to'lov qulayliklari:**\n\n"
        "Bizda barcha kurslar uchun **0% ustamasiz oylik bo'lib to'lash** tizimi mavjud:\n\n"
        "• 🐍 **Python & Backend**: 800 000 so'm/oy (Jami 4 800 000 so'm)\n"
        "• ⚛️ **Frontend & React**: 840 000 so'm/oy (Jami 4 200 000 so'm)\n"
        "• 🚀 **Fullstack Web**: 800 000 so'm/oy (Jami 6 400 000 so'm)\n"
        "• 🧠 **Data Science & AI**: 900 000 so'm/oy (Jami 5 400 000 so'm)\n"
        "• 🎨 **UI/UX & Grafik Dizayn**: 900 000 so'm/oy (Jami 3 600 000 so'm)\n"
        "• 📱 **SMM & Target**: 900 000 so'm/oy (Jami 2 700 000 so'm)\n\n"
        "🎁 **Maxsus imtiyozlar:**\n"
        "1. Bir yo'la to'lov qilganda **10-15% gacha chegirma**!\n"
        "2. **14 kunlik kafolat**: Darslar ma'qul kelmasa, to'lov 100% qaytariladi.\n"
        "3. Birinchi dars — **MUTLAQO BEPUL**!\n\n"
        "Qaysi yo'nalish sizga ma'qul kelmoqda? Men sizga batafsil ma'lumot beraman!"
    )
    await message.answer(pricing_text, parse_mode="Markdown")


@router.message(F.text == "🎯 Kurs tanlashda maslahat")
async def advise_course(message: Message, bot: Bot):
    """Kurs tanlashda maslahat berishni boshlash"""
    prompt_text = (
        "🎯 **Keling, sizga eng mos keladigan kasbni birgalikda tanlaymiz!**\n\n"
        "Menga quyidagilar haqida qisqacha yozib bering:\n"
        "1️⃣ Hozirgi kasbingiz yoki mashg'ulotingiz nima?\n"
        "2️⃣ Dasturlash yoki dizayn bo'yicha ozgina bo'lsa ham tajribangiz bormi yoki noldan boshlaysizmi?\n"
        "3️⃣ Sizga ko'proq qaysi soha qiziqroq: mantiq va dasturlashmi, chiroyli dizaynmi yoki sun'iy intellektmi?\n\n"
        "Javobingizni kutaman! 😊"
    )
    await message.answer(prompt_text, parse_mode="Markdown")


@router.message(F.text == "📞 Menejer bilan bog'lanish / Ariza")
async def request_lead_contact(message: Message):
    """Foydalanuvchidan qaysi kursga yozilishini so'rash va telefon olish"""
    text = (
        "📞 **Kursga yozilish va Bepul konsultatsiya:**\n\n"
        "Iltimos, avval o'zingiz qiziqqan **kurs yo'nalishini tanlang**:\n"
        "(Mutaxassisimiz 15 daqiqa ichida bog'lanib, tanlangan kursingiz bo'yicha joy band qilib beradi!)"
    )
    await message.answer(
        text,
        reply_markup=get_apply_course_selection_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "❌ Bekor qilish")
async def cancel_contact(message: Message):
    """Kontakt so'rovini bekor qilish"""
    await message.answer(
        "Tushundim. Bemalol kurslar bo'yicha savollaringizni yozishingiz mumkin!",
        reply_markup=get_main_reply_keyboard()
    )


@router.message(F.text == "🔄 Yangi suhbat boshlash")
@router.message(Command("clear"))
async def clear_chat(message: Message):
    """Suhbat tarixini tozalash"""
    await db.clear_user_chat_history(message.from_user.id)
    await message.answer(
        "🔄 Muloqot tarixingiz yangilandi!\n"
        "Endi siz bilan yangi mavzuda suhbatlashishga tayyorman. Qanday savolingiz bor?",
        reply_markup=get_main_reply_keyboard()
    )


@router.message(Command("leads"))
async def show_leads(message: Message):
    """Adminlar uchun tushgan so'nggi arizalarni ko'rish"""
    # Xavfsizlik: agar ADMIN_ID sozlangan bo'lsa tekshirish
    if ADMIN_ID and str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("Ushbu buyruq faqat administratorlar uchun mo'ljallangan.")
        return

    leads = await db.get_all_leads(limit=15)
    if not leads:
        await message.answer("Hozircha hech qanday ariza kelib tushmagan.")
        return

    report = "📋 **So'nggi kelib tushgan sotuv arizalari:**\n\n"
    for idx, lead in enumerate(leads, 1):
        report += (
            f"**{idx}. {lead['full_name']}**\n"
            f"📞 Tel: `{lead['phone_number']}`\n"
            f"🎯 Qiziqish: {lead['course_interest']}\n"
            f"🕒 Vaqt: {lead['created_at']}\n"
            f"📝 Izoh: {lead['note'] or '-'}\n"
            "----------------------------\n"
        )
    report += "\n📊 Excel formatida yuklab olish uchun: /export yoki /excel"
    await message.answer(report, parse_mode="Markdown")


@router.message(Command("export"))
@router.message(Command("excel"))
async def handle_export(message: Message):
    """Arizalarni Excel (.xlsx) fayl ko'rinishida yuborish"""
    if ADMIN_ID and str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("Ushbu buyruq faqat administratorlar uchun mo'ljallangan.")
        return

    from aiogram.types import FSInputFile
    from export_leads import export_leads_to_excel

    await message.answer("⏳ Excel fayl tayyorlanmoqda...")
    try:
        excel_path = export_leads_to_excel("arizalar.xlsx")
        file_to_send = FSInputFile(excel_path, filename="Kursga_yozilganlar_arizalar.xlsx")
        await message.answer_document(
            document=file_to_send,
            caption="📊 **Kursga yozilgan barcha foydalanuvchilar va arizalar ro'yxati (Excel)**",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Excel fayl yuborishda xatolik: {e}")
        await message.answer(f"Excel faylni tayyorlashda xatolik yuz berdi: {e}")


@router.message(F.contact)
async def handle_contact(message: Message, bot: Bot):
    """Foydalanuvchi kontakt yuborganida arizani (lead) qabul qilish"""
    contact = message.contact
    user = message.from_user
    phone = contact.phone_number

    if not phone.startswith("+"):
        phone = "+" + phone

    await db.update_user_phone(user.id, phone)

    # Foydalanuvchi tanlagan kursini bazadan olish
    selected_course = await db.get_user_selected_course(user.id) or "Umumiy ta'lim konsultatsiyasi"

    lead_id = await db.save_lead(
        user_id=user.id,
        full_name=contact.first_name + (f" {contact.last_name}" if contact.last_name else ""),
        phone_number=phone,
        course_interest=selected_course,
        note=f"Username: @{user.username}" if user.username else ""
    )

    # Foydalanuvchiga professional javob
    success_text = (
        f"Ajoyib, **{contact.first_name}**! 🎉\n\n"
        f"🎯 Tanlangan kurs: **{selected_course}**\n"
        f"📞 Raqamingiz qabul qilindi: `{phone}`\n\n"
        "Katta mutaxassisimiz 15 daqiqa ichida siz bilan bog'lanadi va:\n"
        "✅ Kurs dasturini to'liq taqdim etadi;\n"
        "✅ Bepul sinov darsiga kirish huquqini beradi;\n"
        "✅ Siz uchun shaxsiy chegirma band qiladi!\n\n"
        "Ungacha agar qandaydir savollaringiz bo'lsa, bemalol bu yerda so'rashingiz mumkin. 😊"
    )

    await message.answer(
        success_text,
        reply_markup=get_main_reply_keyboard(),
        parse_mode="Markdown"
    )

    # Agar ADMIN_ID bo'lsa, xabarnoma yuborish
    if ADMIN_ID:
        try:
            admin_msg = (
                f"🚨 **Yangi Ariza (Lead #{lead_id})!**\n\n"
                f"👤 Ism: {contact.first_name} {contact.last_name or ''}\n"
                f"🎯 Kurs: **{selected_course}**\n"
                f"📞 Tel: `{phone}`\n"
                f"🔗 Telegram: @{user.username or 'yoq'} (ID: `{user.id}`)\n"
            )
            await bot.send_message(chat_id=int(ADMIN_ID), text=admin_msg, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Admin xabarnomasi yuborilmadi: {e}")


@router.callback_query(F.data.startswith("course_info:"))
async def handle_course_info(callback: CallbackQuery):
    """Kurs haqida batafsil ma'lumot inline callback"""
    course_id = callback.data.split(":")[1]
    course = get_course_by_id(course_id)

    if not course:
        await callback.answer("Kurs ma'lumotlari topilmadi.", show_alert=True)
        return

    if course:
        await db.set_user_selected_course(callback.from_user.id, course["title"])

    skills_text = "\n".join([f"• {s}" for s in course["skills"]])
    bonuses_text = "\n".join([f"🎁 {b}" for b in course["bonuses"]])

    detail_text = (
        f"🎓 **{course['title']}**\n\n"
        f"📝 **Tavsif:** {course['short_desc']}\n\n"
        f"⏳ **Davomiyligi:** {course['duration']}\n"
        f"🎯 **Daraja:** {course['level']}\n\n"
        f"💰 **Narxi:**\n"
        f"— Oylik bo'lib to'lash: **{course['price_monthly']}**\n"
        f"— Jami kurs narxi: **{course['price_total']}**\n"
        f"— Bir yo'la to'lovda chegirma: **{course['discount_price']}**\n\n"
        f"🛠 **Nimalarni o'rganasiz:**\n{skills_text}\n\n"
        f"🌟 **Imtiyoz va bonuslar:**\n{bonuses_text}\n\n"
        "Birinchi sinov darsi — mutlaqo bepul! Ro'yxatdan o'tmoqchimisiz?"
    )

    await callback.message.edit_text(
        text=detail_text,
        reply_markup=get_course_detail_keyboard(course_id),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("apply_course:"))
async def handle_apply_course(callback: CallbackQuery):
    """Muayyan kursga yozilish inline callback"""
    course_id = callback.data.split(":")[1]
    if course_id == "general":
        course_title = "🎯 Umumiy ta'lim maslahati / Barcha kurslar"
    else:
        course = get_course_by_id(course_id)
        course_title = course["title"] if course else "Kurs"

    # Foydalanuvchi tanlagan aniq kursni bazada saqlash
    await db.set_user_selected_course(callback.from_user.id, course_title)

    text = (
        f"🎯 Siz **{course_title}** yo'nalishini tanladingiz!\n\n"
        "Bepul 1-darsga kirish va chegirma joyini band qilish uchun "
        "pastdagi **'📱 Telefon raqamimni ulashish'** tugmasini bosing yoki raqamingizni yozib yuboring:"
    )

    await callback.message.answer(
        text,
        reply_markup=get_contact_request_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer(f"{course_title} tanlandi!")


@router.callback_query(F.data.startswith("ask_ai:"))
async def handle_ask_ai_course(callback: CallbackQuery):
    """Kurs bo'yicha AI ga savol berish callback"""
    course_id = callback.data.split(":")[1]
    course = get_course_by_id(course_id)
    course_title = course["title"] if course else "kurs"

    await callback.message.answer(
        f"💬 **{course_title}** bo'yicha o'zingizni qiziqtirgan har qanday savolni yozing! "
        "Masalan: 'Ushbu kursdan keyin qanday ish topsa bo'ladi?' yoki 'Darslar qaysi kunlari o'tiladi?'"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_courses")
async def handle_back_to_courses(callback: CallbackQuery):
    """Kurslar ro'yxatiga qaytish"""
    await callback.message.edit_text(
        get_courses_list_text(),
        reply_markup=get_courses_inline_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(F.text)
async def handle_user_text(message: Message, bot: Bot):
    """
    Foydalanuvchining barcha matnli xabarlarini qabul qilish.
    AI Sotuv Menejeri (Gemini) orqali professional javob qaytarish.
    """
    user_id = message.from_user.id
    user_text = message.text.strip()

    # 1. Matnda telefon raqami bor-yo'qligini tekshirish
    phone_match = PHONE_REGEX.search(user_text)
    if phone_match and len(user_text) < 40:
        phone_number = phone_match.group(0)
        await db.update_user_phone(user_id, phone_number)
        selected_course = await db.get_user_selected_course(user_id) or "Matnda telefon qoldirilgan"
        lead_id = await db.save_lead(
            user_id=user_id,
            full_name=message.from_user.first_name,
            phone_number=phone_number,
            course_interest=selected_course,
            note=user_text
        )
        response_text = (
            f"Rahmat, **{message.from_user.first_name}**! Raqamingiz qabul qilindi: `{phone_number}` ✅\n\n"
            f"🎯 Tanlangan kurs: **{selected_course}**\n\n"
            "Tez orada katta mutaxassisimiz siz bilan bog'lanadi va batafsil ma'lumot beradi. "
            "Yana biror savolingiz bo'lsa, bemalol so'rashingiz mumkin!"
        )
        await message.answer(response_text, parse_mode="Markdown")

        if ADMIN_ID:
            try:
                admin_msg = (
                    f"🚨 **Yangi Ariza (Lead #{lead_id})!**\n\n"
                    f"👤 Ism: {message.from_user.first_name}\n"
                    f"🎯 Kurs: **{selected_course}**\n"
                    f"📞 Tel: `{phone_number}`\n"
                    f"🔗 Telegram: @{message.from_user.username or 'yoq'} (ID: `{user_id}`)\n"
                )
                await bot.send_message(chat_id=int(ADMIN_ID), text=admin_msg, parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Admin xabarnomasi yuborilmadi: {e}")
        return

    # 2. Telegram 'typing' holatini ko'rsatish
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # 3. Strands Decider 2B modeli orqali niyat va qiziqqan kursni tahlil qilish
    decider_info = await analyze_user_message(user_text)
    if decider_info and decider_info.get("matched_course_title"):
        # Agar mijoz ma'lum kursga qiziqayotgani aniqlansa, bazada unga kursni biriktiramiz
        await db.set_user_selected_course(user_id, decider_info["matched_course_title"])

    # 4. Oldingi suhbat tarixini bazadan olish
    history = await db.get_user_chat_history(user_id=user_id, limit=10)

    # 5. Gemini AI orqali sotuv menejeri javobini olish (Decider xulosalari bilan)
    ai_reply = await get_ai_sales_response(
        user_id=user_id,
        user_message=user_text,
        chat_history=history,
        decider_info=decider_info
    )

    # 6. Suhbatni bazaga saqlash
    await db.save_message(user_id=user_id, role="user", text=user_text)
    await db.save_message(user_id=user_id, role="model", text=ai_reply)

    # 7. Javobni foydalanuvchiga to'liq va uzilmasdan yuborish
    if len(ai_reply) <= 4000:
        try:
            await message.answer(ai_reply, parse_mode="Markdown")
        except Exception as e:
            logger.warning(f"Markdown format xatosi: {e}. Oddiy matnda yuborilmoqda.")
            await message.answer(ai_reply, parse_mode=None)
    else:
        # 4000 belgidan oshsa, qismlarga bo'lib to'liq yuborish
        for i in range(0, len(ai_reply), 4000):
            chunk = ai_reply[i:i+4000]
            try:
                await message.answer(chunk, parse_mode="Markdown")
            except Exception:
                await message.answer(chunk, parse_mode=None)
