import os

CH_DIR = os.path.join(os.path.dirname(__file__), "assets", "characters")
BG_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")

print("=" * 60)
print("游戏资源检查报告")
print("=" * 60)

# speaker_map 从 main.py 提取
speaker_map = {
    "罗诚": "luocheng_mid",
    "妻子": "wife",
    "老王": "laowang",
    "老周": "laozhou",
    "程总": "cheng",
    "小张": "xiaozhang",
    "Coco": "coco",
    "吴老板": "wu_laoban",
}

bg_map = {
    "home": "bg_home_old",
    "office_night": "bg_office_night",
    "office_day": "bg_office_day",
    "office_dark": "bg_office_dark",
    "livestudio": "bg_livestudio",
    "startup": "bg_small_office",
    "office_modern": "bg_office_modern",
    "factory": "bg_factory",
    "xiaomi_office": "bg_xiaomi",
    "apple_office": "bg_apple",
    "classroom": "bg_classroom",
    "noodle_shop": "bg_noodle_shop",
    "bar": "bg_bar",
    "street_food": "bg_street_food",
    "venue": "bg_venue",
    "celebration": "bg_celebration",
    "bookstore": "bg_bookstore",
    "corridor": "bg_corridor",
    "hospital": "bg_hospital",
    "press": "bg_press",
    "airport": "bg_airport",
    "conference": "bg_conference",
    "balcony": "bg_balcony",
    "train_platform": "bg_train_platform",
    "room_rent": "bg_room_rent",
    "black": "bg_black",
}

print("\n【人物头像】(需8张)")
ok = 0
missing = []
for name, fname in speaker_map.items():
    fpath = os.path.join(CH_DIR, fname + ".png")
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        print(f"  ✅ {name} -> {fname}.png ({size//1024}KB)")
        ok += 1
    else:
        print(f"  ❌ {name} -> {fname}.png 【缺失】")
        missing.append(fname)
print(f"  结果: {ok}/{len(speaker_map)} 张头像")

print("\n【背景图片】(需27张)")
bg_ok = 0
bg_missing = []
for scn, fname in bg_map.items():
    fpath = os.path.join(BG_DIR, fname + ".png")
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        print(f"  ✅ {scn} -> {fname}.png ({size//1024}KB)")
        bg_ok += 1
    else:
        print(f"  ❌ {scn} -> {fname}.png 【缺失】")
        bg_missing.append(fname)
print(f"  结果: {bg_ok}/{len(bg_map)} 张背景")

print("\n" + "=" * 60)
if not missing and not bg_missing:
    print("✅ 全部资源就位，游戏可以正常运行！")
else:
    if missing:
        print(f"⚠️  缺失头像: {', '.join(missing)}")
    if bg_missing:
        print(f"⚠️  缺失背景: {', '.join(bg_missing)}")
print("=" * 60)
