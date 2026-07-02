import os
import hashlib
from PIL import Image

PLACEHOLDER_HASH = "19a0b822"
good_bg = {"bg_home_old.png", "bg_livestudio.png", "bg_office_night.png", "bg_room_rent.png"}
good_char = {"laowang.png", "luocheng_mid.png", "wife.png"}

for folder in ["assets/backgrounds", "assets/characters"]:
    full_dir = os.path.join(os.path.dirname(__file__), folder)
    for f in os.listdir(full_dir):
        if not f.endswith('.png'):
            continue
        path = os.path.join(full_dir, f)
        is_good = False
        if folder.endswith('backgrounds') and f in good_bg:
            is_good = True
        elif folder.endswith('characters') and f in good_char:
            is_good = True
        else:
            try:
                img = Image.open(path)
                if img.size == (1832, 1832):
                    h = hashlib.md5(open(path, 'rb').read()).hexdigest()[:8]
                    if h == PLACEHOLDER_HASH:
                        os.remove(path)
                        print(f"Deleted placeholder: {folder}/{f}")
                        continue
            except:
                pass
        if is_good:
            print(f"Keep: {folder}/{f}")

print("\nCleanup done.")
