"""
Asosiy ishga tushirish fayli (Main Entry Point).
Telegram botni ishga tushiradi va AI Sotuv Menejeri xizmatini yoqadi.
"""

import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, ACADEMY_NAME, MANAGER_NAME
import database as db
from handlers import router

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("SalesManagerBot")


async def main():
    # 1. Sozlamalarni tekshirish
    if not TELEGRAM_BOT_TOKEN:
        logger.error("XATOLIK: .env faylida 'telegram_bot_token' topilmadi!")
        sys.exit(1)

    if not GEMINI_API_KEY:
        logger.warning("DIQQAT: .env faylida 'gemini_api_key' topilmadi. AI javoblari ishlamasligi mumkin!")

    # 2. Ma'lumotlar bazasini initsializatsiya qilish
    logger.info("Ma'lumotlar bazasi initsializatsiya qilinmoqda...")
    await db.init_db()

    # 3. Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    # 4. Routerni ulash
    dp.include_router(router)

    # 5. Bot ma'lumotlarini tekshirish
    bot_info = await bot.get_me()
    logger.info(f"=== {ACADEMY_NAME} SOTUV MENEJERI BOTI ISHGA TUSHDI ===")
    logger.info(f"Bot Username: @{bot_info.username}")
    logger.info(f"Bot Nomi: {bot_info.first_name}")
    logger.info(f"Virtual Menejer: {MANAGER_NAME}")
    logger.info("Bot yangi xabarlarni tinglamoqda (Polling rejimida)...")

    # 6. Eski xabarlarni (pending updates) o'tkazib yuborish va polling boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
