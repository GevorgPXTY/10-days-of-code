import json

# Исходный файл — только читаем, не меняем
INPUT_FILE = "test_json.txt"
# Файл с результатом — создаётся с нуля при каждом запуске
OUTPUT_FILE = "test_json_V2.txt"


def load_data():
    """Загружаем JSON из исходного файла (только чтение)."""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """Сохраняем результат в отдельный файл.
    Если файл существует — перезаписывается с нуля."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def step1_create_document4(data):
    """ШАГ 1: Создаём document4 (версия 1), дочерний для document3 (версия 3).
    В parents записываем, что родитель — document3 версии 3."""
    print("=" * 60)
    print("ШАГ 1: Создание document4 (версия 1)")
    print("=" * 60)

    # Создаём новую версию 1 документа document4
    # parents указывает, от кого произошла эта версия: от document3 версии 3
    data["document4"] = {
        "1": {
            "parents": {
                "document3": ["3"]
            }
        }
    }

    print("document4 версия 1 создана.")
    print(f"Содержимое: {json.dumps(data['document4'], indent=4)}")
    return True


def step2_delete_version(data):
    """ШАГ 2: Удаляем версию 1 из document1.
    Правило: при удалении родительского документа нужно удалить
    его упоминание в дочерних документах (в их parents)."""
    print("\n" + "=" * 60)
    print("ШАГ 2: Удаление версии 1 из document1")
    print("=" * 60)

    doc_name = "document1"
    ver_name = "1"

    # Собираем все ссылки на document1 версию 1 в дочерних документах
    # Проходим по всем документам и их версиям, ищем упоминания в parents
    references_found = []
    for d_name, versions in data.items():
        if d_name == doc_name:
            continue
        for v_name, v_data in versions.items():
            parents = v_data.get("parents", {})
            if doc_name in parents:
                # Проверяем, есть ли версия 1 в списке родителей
                if ver_name in parents[doc_name]:
                    references_found.append((d_name, v_name))

    # Удаляем упоминания document1 версии 1 из дочерних документов
    for d_name, v_name in references_found:
        parents = data[d_name][v_name]["parents"]
        # Удаляем конкретную версию из списка
        parents[doc_name].remove(ver_name)
        # Если после удаления список версий пуст — удаляем весь ключ документа
        if not parents[doc_name]:
            del parents[doc_name]
        # Если parents стал пустым — оставляем пустой словарь
        print(f"Удалена ссылка на {doc_name} вер.{ver_name} из {d_name} вер.{v_name}")

    # Теперь удаляем саму версию 1 из document1
    if doc_name in data and ver_name in data[doc_name]:
        del data[doc_name][ver_name]
        print(f"Версия {ver_name} удалена из {doc_name}.")
    else:
        print(f"Версия {ver_name} не найдена в {doc_name}.")
        return False

    # Если у документа больше нет версий — удаляем весь документ
    if not data[doc_name]:
        del data[doc_name]
        print(f"{doc_name} полностью удалён (нет оставшихся версий).")

    return True


def main():
    # Загружаем исходные данные
    data = load_data()
    print("Исходные данные загружены:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # Шаг 1: создаём document4 версия 1 (дочерний для document3 версия 3)
    step1_ok = step1_create_document4(data)

    # Шаг 2: удаляем версию 1 из document1 + чистим ссылки в дочерних
    step2_ok = step2_delete_version(data)

    # Сохраняем итоговый результат
    save_data(data)

    # Выводим итог
    print("\n" + "=" * 60)
    print("ИТОГИ")
    print("=" * 60)
    print(f"Шаг 1 (Создание document4):  {'ОК' if step1_ok else 'ОШИБКА'}")
    print(f"Шаг 2 (Удаление version 1):  {'ОК' if step2_ok else 'ОШИБКА'}")
    print(f"\nИтоговое содержимое записано в файл: {OUTPUT_FILE}")
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
