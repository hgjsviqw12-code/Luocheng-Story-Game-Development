import urllib.request
import os

base = "https://aka.doubaocdn.com/s/"

assets = {
    # 背景图 (landscape_16_9)
    "assets/backgrounds/bg_classroom.png": "toGS1wfbom",
    "assets/backgrounds/bg_office_startup.png": "2Qnw1wfbon",
    "assets/backgrounds/bg_factory.png": "ZAya1wfboo",
    "assets/backgrounds/bg_venue.png": "49Cl1wfboq",
    "assets/backgrounds/bg_kitchen.png": "0WZU1wfbor",
    "assets/backgrounds/bg_xiaomi.png": "SqHH1wfbot",
    "assets/backgrounds/bg_apple.png": "bidx1wfbpf",
    "assets/backgrounds/bg_office_day.png": "VxYI1wfbpf",
    "assets/backgrounds/bg_office_dark.png": "sZDs1wfbpf",
    "assets/backgrounds/bg_office_modern.png": "g7tW1wfbpf",
    "assets/backgrounds/bg_noodle_shop.png": "UDut1wfbpg",
    "assets/backgrounds/bg_bar.png": "tUQE1wfbpi",
    "assets/backgrounds/bg_street_food.png": "CWD11wfbqb",
    "assets/backgrounds/bg_celebration.png": "Fkvi1wfbqd",
    "assets/backgrounds/bg_bookstore.png": "gTMb1wfbqe",
    "assets/backgrounds/bg_corridor.png": "LIE61wfbqf",
    "assets/backgrounds/bg_hospital.png": "pm3d1wfbqh",
    "assets/backgrounds/bg_press.png": "XoYw1wfbqi",
    "assets/backgrounds/bg_airport.png": "OK5X1wfbrc",
    "assets/backgrounds/bg_conference.png": "ZwJb1wfbrc",
    "assets/backgrounds/bg_small_office.png": "5GVz1wfbre",
    "assets/backgrounds/bg_balcony.png": "le711wfbrh",
    "assets/backgrounds/bg_train_platform.png": "fKFQ1wfbri",

    # 人物头像 (square)
    "assets/characters/luocheng_young.png": "buLX1wfbrj",
    "assets/characters/laozhou.png": "FPyS1wfbsT",
    "assets/characters/xiaozhang.png": "xEtw1wfbsU",
    "assets/characters/chengzong.png": "sQW51wfbsV",
    "assets/characters/tim.png": "X68N1wfbsX",
    "assets/characters/wu_laoban.png": "XQbX1wfbsY",
    "assets/characters/luocheng_kid.png": "OBy81wfbsa",
}

# 检查已有的好图片
existing_good = {
    "assets/backgrounds/bg_home_old.png",
    "assets/backgrounds/bg_livestudio.png",
    "assets/backgrounds/bg_office_night.png",
    "assets/backgrounds/bg_room_rent.png",
    "assets/characters/laowang.png",
    "assets/characters/luocheng_mid.png",
    "assets/characters/wife.png",
}

ok = 0
fail = 0
skip = 0

for path, code in assets.items():
    full_path = os.path.join(os.path.dirname(__file__), path)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 10000:
        print(f"SKIP (exists): {path}")
        skip += 1
        continue
    url = base + code
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
        with open(full_path, "wb") as f:
            f.write(data)
        size_kb = len(data) // 1024
        print(f"OK: {path} ({size_kb}KB)")
        ok += 1
    except Exception as e:
        print(f"FAIL: {path} - {e}")
        fail += 1

print(f"\nDone! OK={ok} FAIL={fail} SKIP={skip}")

# 验证所有图片
print("\n=== 验证所有图片 ===")
from PIL import Image
import hashlib

for folder in ["assets/backgrounds", "assets/characters"]:
    full_dir = os.path.join(os.path.dirname(__file__), folder)
    for f in sorted(os.listdir(full_dir)):
        if f.endswith('.png'):
            path = os.path.join(full_dir, f)
            try:
                img = Image.open(path)
                h = hashlib.md5(open(path,'rb').read()).hexdigest()[:8]
                print(f"  {f}: {img.size} {img.mode} hash={h}")
            except Exception as e:
                print(f"  {f}: ERROR - {e}")
