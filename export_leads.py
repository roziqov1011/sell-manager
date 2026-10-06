"""
Arizalarni (lidlarni) Excel va matn formatida ko'rish hamda yuklab olish moduli.
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from config import DATABASE_PATH

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_leads_data():
    """Barcha arizalarni olish"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, full_name, phone_number, course_interest, note, status, created_at
        FROM leads
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def export_leads_to_excel(output_path: str = "arizalar.xlsx") -> str:
    """Arizalarni chiroyli formatlangan Excel faylga eksport qilish"""
    leads = get_leads_data()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Arizalar Ro'yxati"

    # Sarlavhalar
    headers = ["ID", "Ism Familiya", "Telefon Raqam", "Kurs / Qiziqish", "Telegram / Izoh", "Holati", "Sana va Vaqt"]
    ws.append(headers)

    # Dizayn: Sarlavha uslubi
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Qatorlarni kiritish
    for row_idx, lead in enumerate(leads, start=2):
        ws.append([
            lead["id"],
            lead["full_name"],
            lead["phone_number"],
            lead["course_interest"],
            lead["note"] or "",
            lead["status"],
            lead["created_at"]
        ])
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_num)
            cell.border = thin_border
            if col_num in [1, 3, 6, 7]:
                cell.alignment = Alignment(horizontal="center", vertical="center")

    # Ustunlar kengligini avtomatik moslash
    column_widths = {
        "A": 8,   # ID
        "B": 24,  # Ism
        "C": 20,  # Telefon
        "D": 30,  # Kurs
        "E": 25,  # Izoh
        "F": 14,  # Holati
        "G": 22   # Sana
    }
    for col_letter, width in column_widths.items():
        ws.column_dimensions[col_letter].width = width

    file_path = Path(output_path).resolve()
    wb.save(file_path)
    return str(file_path)

def print_leads_table():
    """Terminalda arizalarni jadval ko'rinishida ko'rsatish"""
    leads = get_leads_data()
    if not leads:
        print("Hozircha hech qanday ariza mavjud emas.")
        return

    print("=" * 80)
    print(f"{'ID':<4} | {'ISM':<18} | {'TELEFON':<16} | {'KURS':<22} | {'SANA':<12}")
    print("=" * 80)
    for lead in leads:
        print(f"{lead['id']:<4} | {lead['full_name'][:18]:<18} | {lead['phone_number']:<16} | {lead['course_interest'][:22]:<22} | {str(lead['created_at'])[:16]:<12}")
    print("=" * 80)
    print(f"Jami arizalar soni: {len(leads)}")

if __name__ == "__main__":
    print_leads_table()
    excel_file = export_leads_to_excel()
    print(f"\n✅ Excel fayl saqlandi: {excel_file}")
