"""
SQLite ma'lumotlar bazasi boshqaruvi (aiosqlite orqali asinxron).
Foydalanuvchilar, suhbat tarixi va sotuv arizalarini (lidlarni) saqlash.
"""

import aiosqlite
from datetime import datetime
from config import DATABASE_PATH


async def init_db():
    """Ma'lumotlar bazasi va jadvallarni initsializatsiya qilish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Foydalanuvchilar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Suhbat tarixi jadvali (AI konteksti uchun)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role TEXT, -- 'user' yoki 'model'
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        # Sotuv arizalari (Leads) jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                full_name TEXT,
                phone_number TEXT,
                course_interest TEXT,
                note TEXT,
                status TEXT DEFAULT 'yangi', -- 'yangi', 'boglanildi', 'yopildi'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Foydalanuvchilar jadvaliga selected_course ustunini qo'shish (agar bo'lmasa)
        try:
            await db.execute("ALTER TABLE users ADD COLUMN selected_course TEXT")
        except Exception:
            pass

        await db.commit()


async def save_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None, phone_number: str = None):
    """Foydalanuvchini saqlash yoki oxirgi faolligini yangilash"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, phone_number, last_active)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                username = COALESCE(excluded.username, users.username),
                first_name = COALESCE(excluded.first_name, users.first_name),
                last_name = COALESCE(excluded.last_name, users.last_name),
                phone_number = COALESCE(excluded.phone_number, users.phone_number),
                last_active = CURRENT_TIMESTAMP
        """, (user_id, username, first_name, last_name, phone_number))
        await db.commit()


async def update_user_phone(user_id: int, phone_number: str):
    """Foydalanuvchi telefon raqamini yangilash"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE users SET phone_number = ?, last_active = CURRENT_TIMESTAMP WHERE user_id = ?
        """, (phone_number, user_id))
        await db.commit()


async def save_message(user_id: int, role: str, text: str):
    """Suhbat xabarini saqlash (user yoki model)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO messages (user_id, role, text)
            VALUES (?, ?, ?)
        """, (user_id, role, text))
        await db.commit()


async def get_user_chat_history(user_id: int, limit: int = 12):
    """Foydalanuvchining oxirgi suhbat tarixini olish (AI konteksti uchun)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT role, text FROM (
                SELECT id, role, text, created_at FROM messages
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
            ) ORDER BY id ASC
        """, (user_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [{"role": row["role"], "text": row["text"]} for row in rows]


async def clear_user_chat_history(user_id: int):
    """Foydalanuvchi suhbat tarixini tozalash (yangi muloqot boshlash)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        await db.commit()


async def save_lead(user_id: int, full_name: str, phone_number: str, course_interest: str = "Umumiy", note: str = "") -> int:
    """Yangi sotuv arizasini (lead) bazaga kiritish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO leads (user_id, full_name, phone_number, course_interest, note)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, full_name, phone_number, course_interest, note))
        await db.commit()
        return cursor.lastrowid


async def get_all_leads(limit: int = 20):
    """Oxirgi tushgan arizalarni olish (admin uchun)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT id, user_id, full_name, phone_number, course_interest, note, status, created_at
            FROM leads
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def set_user_selected_course(user_id: int, course_title: str):
    """Foydalanuvchi qiziqqan yoki tanlagan kursini saqlash"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE users SET selected_course = ?, last_active = CURRENT_TIMESTAMP WHERE user_id = ?
        """, (course_title, user_id))
        await db.commit()


async def get_user_selected_course(user_id: int) -> str | None:
    """Foydalanuvchi tanlagan kursini olish"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT selected_course FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row and row[0]:
                return row[0]
            return None
