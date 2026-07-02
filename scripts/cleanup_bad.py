import urllib.request
import os
import urllib.parse
import time
import json

# 好的图片保留
good_bg = {"bg_home_old.png", "bg_livestudio.png", "bg_office_night.png", "bg_room_rent.png"}
good_char = {"laowang.png", "luocheng_mid.png", "wife.png"}

# 删除所有JPG和坏的PNG
for folder in ["assets/backgrounds", "assets/characters"]:
    full_dir = os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(full_dir):
        continue
    for f in os.listdir(full_dir):
        path = os.path.join(full_dir, f)
        if f.endswith('.jpg'):
            os.remove(path)
            print(f"Deleted JPG: {folder}/{f}")
        elif f.endswith('.png'):
            if folder.endswith('backgrounds') and f in good_bg:
                print(f"Keep good BG: {folder}/{f}")
            elif folder.endswith('characters') and f in good_char:
                print(f"Keep good char: {folder}/{f}")
            else:
                os.remove(path)
                print(f"Deleted bad PNG: {folder}/{f}")

print("\nCleanup done.")
