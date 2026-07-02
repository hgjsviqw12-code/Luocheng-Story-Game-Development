import urllib.request
import os

base = "https://aka.doubaocdn.com/s/"

assets = {
    "assets/backgrounds/bg_home_old.png": "4Iz41wdKp6",
    "assets/backgrounds/bg_room_rent.png": "Hxz01wdKpI",
    "assets/backgrounds/bg_office_night.png": "2wZP1wdKpI",
    "assets/backgrounds/bg_livestudio.png": "XHPe1wdKpS",
    "assets/backgrounds/bg_office_startup.png": "c2Sa1wdKpU",
    "assets/backgrounds/bg_kitchen.png": "2rGW1wdKpX",
    "assets/characters/luocheng_mid.png": "vPVL1wdKph",
    "assets/characters/wife.png": "cnBV1wdKpj",
    "assets/characters/laowang.png": "ZZ1v1wdKpl",
}

for path, code in assets.items():
    full_path = os.path.join(os.path.dirname(__file__), path)
    url = base + code
    try:
        urllib.request.urlretrieve(url, full_path)
        print(f"OK: {path}")
    except Exception as e:
        print(f"FAIL: {path} - {e}")

print("done")
