import urllib.request
import os
import time
from PIL import Image
import hashlib

base = "https://aka.doubaocdn.com/s/"

assets = {
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
    "assets/characters/luocheng_young.png": "buLX1wfbrj",
    "assets/characters/laozhou.png": "FPyS1wfbsT",
    "assets/characters/xiaozhang.png": "xEtw1wfbsU",
    "assets/characters/chengzong.png": "sQW51wfbsV",
    "assets/characters/tim.png": "X68N1wfbsX",
    "assets/characters/wu_laoban.png": "XQbX1wfbsY",
    "assets/characters/luocheng_kid.png": "OBy81wfbsa",
}

PLACEHOLDER_HASH = "19a0b822"  # known placeholder hash

def is_real_image(path):
    """Check if the downloaded image is real (not placeholder)"""
    if not os.path.exists(path):
        return False
    if os.path.getsize(path) < 10000:
        return False
    try:
        img = Image.open(path)
        w, h = img.size
        # Placeholder is 1832x1832
        if w == 1832 and h == 1832:
            h_md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()[:8]
            if h_md5 == PLACEHOLDER_HASH:
                return False
        return True
    except:
        return False

def download_one(path, code, max_retries=10):
    full_path = os.path.join(os.path.dirname(__file__), path)
    if is_real_image(full_path):
        print(f"  Already OK: {path}")
        return True
    
    url = base + code
    for attempt in range(max_retries):
        try:
            # Delete old placeholder
            if os.path.exists(full_path):
                os.remove(full_path)
            
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read()
            
            # Save to temp first
            tmp_path = full_path + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(data)
            
            # Check if it's real
            try:
                img = Image.open(tmp_path)
                w, h = img.size
                if w == 1832 and h == 1832:
                    h_md5 = hashlib.md5(data).hexdigest()[:8]
                    if h_md5 == PLACEHOLDER_HASH:
                        os.remove(tmp_path)
                        wait = 10 * (attempt + 1)
                        print(f"  Still generating ({path}), waiting {wait}s... (attempt {attempt+1}/{max_retries})")
                        time.sleep(wait)
                        continue
                
                # Real image!
                img.save(full_path, "PNG")
                os.remove(tmp_path)
                size_kb = len(data) // 1024
                print(f"  OK: {path} ({w}x{h}, {size_kb}KB)")
                return True
            except Exception as e:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                print(f"  Error checking {path}: {e}, retry...")
                time.sleep(5)
        except Exception as e:
            print(f"  Download error {path}: {e}, retry...")
            time.sleep(5)
    
    print(f"  FAILED after {max_retries} retries: {path}")
    return False

print("Waiting 30 seconds for images to generate...")
time.sleep(30)

ok = 0
fail = 0
skip = 0
total = len(assets)

for i, (path, code) in enumerate(assets.items()):
    print(f"[{i+1}/{total}] Downloading {path}...")
    if is_real_image(os.path.join(os.path.dirname(__file__), path)):
        print(f"  Already OK (cached)")
        skip += 1
        continue
    if download_one(path, code):
        ok += 1
    else:
        fail += 1

print(f"\n=== Download complete ===")
print(f"OK: {ok}, Failed: {fail}, Skipped: {skip}")

# Final verification
print("\n=== Final verification ===")
for folder in ["assets/backgrounds", "assets/characters"]:
    full_dir = os.path.join(os.path.dirname(__file__), folder)
    for f in sorted(os.listdir(full_dir)):
        if f.endswith('.png'):
            path = os.path.join(full_dir, f)
            try:
                img = Image.open(path)
                h = hashlib.md5(open(path,'rb').read()).hexdigest()[:8]
                status = "GOOD" if h != PLACEHOLDER_HASH and img.size != (1832, 1832) else "BAD"
                print(f"  [{status}] {f}: {img.size}")
            except Exception as e:
                print(f"  [ERROR] {f}: {e}")
