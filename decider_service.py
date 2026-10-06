"""
Amazon Strands Decider 2B Model integratsiyasi.
Lokal open-weight qaror qabul qiluvchi model: StrandsAgents/strands-decider-2B-hobson-v19
Foydalanuvchi niyatini (intent), qiziqqan kursini va lid haroratini (lead score) aniqlaydi.
"""

import asyncio
import logging
import torch
from courses_data import COURSES

logger = logging.getLogger(__name__)

# Strands Decider kutubxonasi mavjudligini tekshirish
try:
    from strands_decider.infer import load_engine, SystemOneEngine
    from strands_decider.schema import ChoiceQuestion, NoulQuestion, ScoreQuestion
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False
    logger.warning("strands_decider paketi topilmadi. Decider xizmati o'chirilgan rejimda ishlaydi.")


# Kurs identifikatorlarini tushunarli nomlarga xaritalash
TOPIC_TO_COURSE_TITLE = {
    "backend": "🐍 Python & Backend Dasturlash",
    "frontend": "⚛️ Frontend & React Dasturlash",
    "fullstack": "🚀 Fullstack Web Dasturlash (Python + React)",
    "ai_data": "🧠 Data Science & Sun'iy Intellekt (AI)",
    "design": "🎨 UI/UX & Grafik Dizayn",
    "marketing": "📱 SMM & Target Reklama",
    "general": None
}


class StrandsDeciderManager:
    """Strands Decider 2B modelini boshqaruvchi Singleton sinfi"""
    _engine = None
    _is_loading = False

    @classmethod
    def get_engine(cls):
        """Modelni xotiraga faqat bir marta (lazy loading) yuklash"""
        if not STRANDS_AVAILABLE:
            return None

        if cls._engine is None and not cls._is_loading:
            cls._is_loading = True
            try:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"Strands Decider 2B modeli xotiraga yuklanmoqda ({device})...")
                cls._engine = load_engine("StrandsAgents/strands-decider-2B-hobson-v19", device=device)
                logger.info("Strands Decider 2B modeli muvaffaqiyatli yuklandi!")
            except Exception as e:
                logger.error(f"Strands Decider 2B modelini yuklashda xatolik: {e}")
                cls._engine = None
            finally:
                cls._is_loading = False

        return cls._engine


def _sync_analyze_message(user_text: str) -> dict:
    """Model inferensiyasini sinxron bajarish"""
    engine = StrandsDeciderManager.get_engine()
    if engine is None:
        return {}

    questions = {
        # 1. Qaysi kurs yo'nalishiga qiziqayotganini aniqlash
        "course_topic": ChoiceQuestion(
            instructions="Mijoz qaysi ta'lim yo'nalishi yoki kasbga qiziqmoqda?",
            criteria={
                "backend": "Python, backend, server, ma'lumotlar bazasi, Django, FastAPI, bot yaratish",
                "frontend": "Frontend, sayt yaratish, HTML, CSS, JavaScript, React, web dizayn interfeysi",
                "fullstack": "Fullstack, to'liq dasturchi, ham frontend ham backend",
                "ai_data": "Sun'iy intellekt, Data Science, AI, Machine Learning, tahlil",
                "design": "UI/UX, grafik dizayn, Figma, Photoshop, ilovalar ko'rinishi",
                "marketing": "SMM, Target, reklama, Instagram marketing, sotuv",
                "general": "Umumiy ta'lim, maslahat, narxlar yoki noaniq savol"
            }
        ),
        # 2. Xarid yoki ro'yxatdan o'tish niyati (Lead Intent)
        "is_lead_intent": NoulQuestion(
            instructions="Foydalanuvchi kursga yozilish, narxi, dars boshlanishi yoki ro'yxatdan o'tish haqida so'ramoqdami?"
        ),
        # 3. E'tiroz bormi (Objection)
        "is_objection": NoulQuestion(
            instructions="Mijozda e'tiroz bormi (qimmat, vaqtim yo'q, o'rganolmasam-chi, ishonchsizlik)?"
        ),
        # 4. Lid harorati (Lead Temperature / Warmth)
        "lead_warmth": ScoreQuestion(
            instructions="Mijozning xaridga tayyorlik darajasi",
            criteria=[
                "0: Sovuq (shunchaki ma'lumot qidiryapti)",
                "1: Iliq (kurslar va shartlar bilan qiziqmoqda)",
                "2: Qaynoq (kursga yozilishga yoki telefon qoldirishga tayyor)"
            ]
        )
    }

    try:
        response = engine.ask(state=user_text, questions=questions)
        topic_ans = response.answers.get("course_topic")
        intent_ans = response.answers.get("is_lead_intent")
        objection_ans = response.answers.get("is_objection")
        warmth_ans = response.answers.get("lead_warmth")

        detected_topic = topic_ans.choice if topic_ans else "general"
        topic_conf = topic_ans.confidence if topic_ans else 0.0
        course_name = TOPIC_TO_COURSE_TITLE.get(detected_topic) if topic_conf >= 0.35 else None

        return {
            "detected_topic": detected_topic,
            "topic_confidence": topic_conf,
            "matched_course_title": course_name,
            "is_lead_intent": intent_ans.noul > 0.5 if intent_ans else False,
            "lead_intent_prob": intent_ans.noul if intent_ans else 0.0,
            "is_objection": objection_ans.noul > 0.5 if objection_ans else False,
            "lead_warmth_score": warmth_ans.score if warmth_ans else 0.0
        }
    except Exception as e:
        logger.error(f"Strands Decider tahlilida xatolik: {e}")
        return {}


async def analyze_user_message(user_text: str) -> dict:
    """
    Foydalanuvchi xabarini asinxron fonda (non-blocking) Strands Decider 2B orqali tahlil qilish.
    """
    if not STRANDS_AVAILABLE:
        return {}

    # Event loopni to'sib qo'ymaslik uchun alohida oqimda ishga tushirish
    try:
        return await asyncio.to_thread(_sync_analyze_message, user_text)
    except Exception as e:
        logger.error(f"Async decider execution error: {e}")
        return {}
