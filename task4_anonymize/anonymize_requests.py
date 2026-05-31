import re
from pathlib import Path

# Папка, где лежит сам скрипт — используем как базу для путей
BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "test.txt"
OUTPUT_FILE = BASE_DIR / "test_V2.txt"


def load_lines():
    """Загружаем строки из исходного файла."""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def save_lines(lines):
    """Сохраняем результат в отдельный файл (перезапись с нуля)."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


def mask_phone(line):
    """Шаг 1: Шифруем номера телефонов в формат +*-***-**-**.
    Ищем любые последовательности цифр длиной 11 (8XXX...) или 12 (+7XXX...),
    затем маскируем все цифры, кроме первых двух и последних двух."""
    # Паттерн ловит телефоны в разных форматах:
    # +7 (999) 123-45-67, 89123456789, +79001112233 и т.д.
    phone_pattern = re.compile(
        r'(?:\+?7|8)\s*[(\s]*\d{3}[)\s\-]*\d{3}[-\s]*\d{2}[-\s]*\d{2}'
    )

    def replacer(match):
        # Извлекаем только цифры из найденного телефона
        digits = re.sub(r'\D', '', match.group())
        # Если начинается с 8 — заменяем на +7 (унификация)
        if digits.startswith('8') and len(digits) == 11:
            digits = '7' + digits[1:]
        # Форматируем в +*-***-**-** (7 цифр маскируются, 2 первые и 2 последние видны)
        # +7-***-**-** — код страны, 3 цифры маска, 2+2 видны
        return f"+{digits[0]}-***-***-**-{digits[-2:]}"

    return phone_pattern.sub(replacer, line)


def mask_email(line):
    """Шаг 2: Скрываем email адреса — заменяем на ***@домен.
    Домен оставляем видимым, имя пользователя маскируем."""
    email_pattern = re.compile(r'[\w.-]+@[\w.-]+\.\w+')

    def replacer(match):
        local, domain = match.group().split('@', 1)
        return f"***@{domain}"

    return email_pattern.sub(replacer, line)


def unify_date(line):
    """Шаг 3: Унифицируем даты к формату DD.MM.YYYY HH:MM.
    Исходные форматы в файле:
      - DD/MM/YYYY HH:MM  (05/12/2025 14:32)
      - DD.MM.YYYY HH:MM  (24.01.2026 09:15)
      - YYYY-MM-DD HH:MM  (2026-02-18 18:00)
    Все приводятся к единому: DD.MM.YYYY HH:MM"""

    # Формат DD/MM/YYYY HH:MM → DD.MM.YYYY HH:MM
    line = re.sub(
        r'\[(\d{2})/(\d{2})/(\d{4})\s+(\d{2}:\d{2})]',
        r'[\1.\2.\3 \4]',
        line
    )

    # Формат YYYY-MM-DD HH:MM → DD.MM.YYYY HH:MM
    line = re.sub(
        r'\[(\d{4})-(\d{2})-(\d{2})\s+(\d{2}:\d{2})]',
        r'[\3.\2.\1 \4]',
        line
    )

    return line


def process_line(line):
    """Обрабатываем одну строку: маскируем телефон, email, унифицируем дату."""
    line = mask_phone(line)
    line = mask_email(line)
    line = unify_date(line)
    return line


def main():
    lines = load_lines()

    print("Исходные данные:")
    for line in lines:
        print(f"  {line.rstrip()}")

    # Обрабатываем каждую строку
    result_lines = [process_line(line) for line in lines]

    save_lines(result_lines)

    print("\nРезультат:")
    for line in result_lines:
        print(f"  {line.rstrip()}")

    print(f"\nРезультат записан в файл: {OUTPUT_FILE}")



if __name__ == "__main__":
    main()
