import os
import requests
from django.shortcuts import render

# Отключаем прокси (как в restful_api_demo.py)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)

PROXIES = {"http": None, "https": None}
API_URL = "https://api.restful-api.dev/objects"


def objects_list(request):
    """Представление: запрашивает список предметов у API
    и передаёт его в шаблон для отображения в таблице."""
    try:
        response = requests.get(API_URL, proxies=PROXIES, timeout=10)
        if response.status_code == 200:
            objects = response.json()
        else:
            objects = []
    except requests.RequestException:
        objects = []

    return render(request, 'objects_app/objects_list.html', {
        'objects': objects,
    })
