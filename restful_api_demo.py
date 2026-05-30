import os
import requests

# Отключаем системный прокси, чтобы избежать ошибки
# "Missing dependencies for SOCKS support" при запуске в PyCharm venv
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)

# Явно указываем requests не использовать прокси для каждого запроса
PROXIES = {"http": None, "https": None}

# Базовый URL API для работы с объектами
BASE_URL = "https://api.restful-api.dev/objects"


def create_object():
    """ШАГ 1: Создаём новый предмет через POST-запрос.
    Отправляем на сервер название и характеристики предмета.
    Сервер возвращает созданный объект с присвоенным ID."""
    print("=" * 60)
    print("ШАГ 1: Создание предмета")
    print("=" * 60)
    # Тело запроса — структура взята с сайта restful-api.dev:
    # поле "name" — название предмета, поле "data" — произвольный JSON с характеристиками
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    try:
        # POST-запрос создаёт новый объект на сервере
        response = requests.post(BASE_URL, json=payload, proxies=PROXIES)
        # Успешное создание — статус 200 или 201
        if response.status_code in (200, 201):
            data = response.json()
            # ID нужен для всех последующих шагов (получение, обновление, удаление)
            obj_id = data.get("id")
            print(f"Предмет создан успешно!")
            print(f"ID: {obj_id}")
            print(f"Ответ сервера: {data}")
            return obj_id, True
        else:
            print(f"Ошибка при создании! Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None, False
    except requests.RequestException as e:
        print(f"Исключение при создании: {e}")
        return None, False


def get_object(obj_id):
    """ШАГ 2: Получаем данные созданного предмета через GET-запрос.
    Используем ID, полученный на шаге 1.
    Если шаг 1 не удался (obj_id is None), выводим предупреждение и возвращаем False."""
    print("\n" + "=" * 60)
    print("ШАГ 2: Получение данных предмета")
    print("=" * 60)
    # Проверяем, что ID существует (шаг 1 мог завершиться с ошибкой)
    if not obj_id:
        print("Нет ID предмета — запрос невозможен.")
        return False
    try:
        # GET-запрос по адресу /objects/{id} возвращает данные конкретного предмета
        response = requests.get(f"{BASE_URL}/{obj_id}", proxies=PROXIES)
        if response.status_code == 200:
            data = response.json()
            print(f"Данные предмета получены успешно!")
            print(f"Ответ сервера: {data}")
            return True
        else:
            print(f"Ошибка при получении! Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Исключение при получении: {e}")
        return False


def update_object(obj_id):
    """ШАГ 3: Перезаписываем данные предмета через PUT-запрос.
    PUT полностью заменяет объект на сервере новыми данными.
    Используем тот же ID, но меняем содержимое на новое."""
    print("\n" + "=" * 60)
    print("ШАГ 3: Обновление данных предмета")
    print("=" * 60)
    if not obj_id:
        print("Нет ID предмета — обновление невозможно.")
        return False
    # Новые данные для полной замены объекта (год, цена, CPU, диск, цвет — все новые)
    new_payload = {
        "name": "Apple MacBook Pro 16 (Updated)",
        "data": {
            "year": 2024,
            "price": 2499.99,
            "CPU model": "Apple M3 Max",
            "Hard disk size": "2 TB",
            "color": "Space Black"
        }
    }
    try:
        # PUT-запрос полностью заменяет объект по указанному ID
        response = requests.put(f"{BASE_URL}/{obj_id}", json=new_payload, proxies=PROXIES)
        if response.status_code == 200:
            data = response.json()
            print(f"Предмет обновлён успешно!")
            print(f"Ответ сервера: {data}")
            return True
        else:
            print(f"Ошибка при обновлении! Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Исключение при обновлении: {e}")
        return False


def delete_object(obj_id):
    """ШАГ 4: Удаляем предмет через DELETE-запрос.
    Сервер должен вернуть статус 200 и сообщение об удалении."""
    print("\n" + "=" * 60)
    print("ШАГ 4: Удаление предмета")
    print("=" * 60)
    if not obj_id:
        print("Нет ID предмета — удаление невозможно.")
        return False
    try:
        # DELETE-запрос удаляет объект по указанному ID
        response = requests.delete(f"{BASE_URL}/{obj_id}", proxies=PROXIES)
        if response.status_code == 200:
            data = response.json()
            print(f"Предмет удалён успешно!")
            print(f"Ответ сервера: {data}")
            return True
        else:
            print(f"Ошибка при удалении! Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Исключение при удалении: {e}")
        return False


def verify_deleted(obj_id):
    """Проверка, что предмет действительно удалён.
    Делаем GET-запрос — если сервер отвечает 404, значит объекта больше нет."""
    print("\n" + "=" * 60)
    print("Проверка: предмет действительно удалён?")
    print("=" * 60)
    if not obj_id:
        print("Нет ID предмета — проверка невозможна.")
        return
    try:
        # Если удаление прошло успешно, GET вернёт 404 (объект не найден)
        response = requests.get(f"{BASE_URL}/{obj_id}", proxies=PROXIES)
        if response.status_code == 404:
            print(f"Подтверждено: предмет с ID={obj_id} не найден (404). Удаление прошло успешно.")
        else:
            print(f"Предмет всё ещё существует! Статус: {response.status_code}")
            print(f"Ответ: {response.text}")
    except requests.RequestException as e:
        print(f"Исключение при проверке: {e}")


def main():
    """Основная логика программы.
    Порядок: создать → получить → обновить → удалить → проверить удаление.

    Важное условие: если шаг 2 (получение) не сработал,
    программа всё равно пытается выполнить шаги 3 (обновление) и 4 (удаление),
    поскольку у нас уже есть ID из шага 1."""
    # Шаг 1: создаём предмет и сохраняем его ID
    obj_id, step1_ok = create_object()

    # Шаг 2: получаем данные по ID
    # Даже если этот шаг упадёт, программа продолжит работу
    step2_ok = get_object(obj_id)
    if not step2_ok:
        print("\n[ВНИМАНИЕ] Шаг 2 не выполнен, но программа продолжит работу.")

    # Шаг 3: обновляем данные по тому же ID
    # Выполняется независимо от результата шага 2 (если есть obj_id)
    step3_ok = update_object(obj_id)
    if not step3_ok and step2_ok:
        print("\n[ВНИМАНИЕ] Шаг 3 не выполнен.")

    # Шаг 4: удаляем предмет по ID
    # Также выполняется независимо от результатов предыдущих шагов
    step4_ok = delete_object(obj_id)
    if step4_ok:
        # Если удаление прошло успешно — проверяем, что объект действительно исчез
        verify_deleted(obj_id)
    else:
        print("\n[ВНИМАНИЕ] Удаление не выполнено, проверка пропущена.")

    # Выводим итоговую сводку по всем шагам
    print("\n" + "=" * 60)
    print("ИТОГИ")
    print("=" * 60)
    print(f"Шаг 1 (Создание):    {'ОК' if step1_ok else 'ОШИБКА'}")
    print(f"Шаг 2 (Получение):   {'ОК' if step2_ok else 'ОШИБКА'}")
    print(f"Шаг 3 (Обновление):  {'ОК' if step3_ok else 'ОШИБКА'}")
    print(f"Шаг 4 (Удаление):    {'ОК' if step4_ok else 'ОШИБКА'}")


if __name__ == "__main__":
    main()
