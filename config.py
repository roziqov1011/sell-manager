import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylini joriy papkadan yoki uning atrofidan yuklash
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

# Tokenlar va kalitlar
TELEGRAM_BOT_TOKEN = os.getenv("telegram_bot_token") or os.getenv("TELEGRAM_BOT_TOKEN") or ""
GEMINI_API_KEY = os.getenv("gemini_api_key") or os.getenv("GEMINI_API_KEY") or ""

# AI Modellari
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.1-flash-lite")

# Ma'lumotlar bazasi yo'li
DATABASE_PATH = BASE_DIR / "bot_database.db"

# Admin ID (agar .env da berilsa, arizalar haqida xabar borishi uchun)
ADMIN_ID = os.getenv("ADMIN_ID", "")

# Maktab / Akademiya nomi
ACADEMY_NAME = "Online IT Academy"
MANAGER_NAME = "Aziza"  # AI Sotuv Menejeri ismi
SUPPORT_USERNAME = "@academy_support"
SUPPORT_PHONE = "+998 71 200 00 00"
