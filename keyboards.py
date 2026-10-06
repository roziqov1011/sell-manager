"""
Telegram bot klaviaturalari va tugmalari (Reply va Inline klaviaturalar).
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from courses_data import COURSES


def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy pastki menyu klaviaturasi"""
    keyboard = [
        [
            KeyboardButton(text="📚 Kurslarimiz"),
            KeyboardButton(text="🎯 Kurs tanlashda maslahat")
        ],
        [
            KeyboardButton(text="💰 Narxlar va to'lov"),
            KeyboardButton(text="📞 Menejer bilan bog'lanish / Ariza")
        ],
        [
            KeyboardButton(text="🔄 Yangi suhbat boshlash")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Savolingizni yozing yoki tugmani tanlang..."
    )


def get_contact_request_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqamni bitta tugma bilan yuborish klaviaturasi"""
    keyboard = [
        [
            KeyboardButton(text="📱 Telefon raqamimni ulashish", request_contact=True)
        ],
        [
            KeyboardButton(text="❌ Bekor qilish")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_courses_inline_keyboard() -> InlineKeyboardMarkup:
    """Kurslarni tanlash uchun inline tugmalar"""
    inline_keyboard = []
    for cid, c in COURSES.items():
        inline_keyboard.append([
            InlineKeyboardButton(text=c["title"], callback_data=f"course_info:{cid}")
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_course_detail_keyboard(course_id: str) -> InlineKeyboardMarkup:
    """Alohida kurs haqida batafsil ko'rilgandagi amallar tugmasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Ushbu kursga yozilish / Sinov darsi", callback_data=f"apply_course:{course_id}")
            ],
            [
                InlineKeyboardButton(text="❓ AI Menejerdan so'rash", callback_data=f"ask_ai:{course_id}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Barcha kurslarga qaytish", callback_data="back_to_courses")
            ]
        ]
    )


def get_apply_course_selection_keyboard() -> InlineKeyboardMarkup:
    """Ariza qoldirishda qaysi kursga yozilishini tanlash inline klaviaturasi"""
    inline_keyboard = []
    for cid, c in COURSES.items():
        inline_keyboard.append([
            InlineKeyboardButton(text=c["title"], callback_data=f"apply_course:{cid}")
        ])
    inline_keyboard.append([
        InlineKeyboardButton(text="🎯 Umumiy maslahat (Barcha kurslar)", callback_data="apply_course:general")
    ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
