# -*- coding: utf-8 -*-
import json

with open("story.json", "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", {})

bg_usage = {}
scene_bg_list = []

for scene_id, scene_data in scenes.items():
    bg = scene_data.get("background", "unknown")
    title = scene_data.get("title", scene_id)
    scene_bg_list.append((scene_id, title, bg))
    if bg not in bg_usage:
        bg_usage[bg] = []
    bg_usage[bg].append(scene_id)

print("=" * 80)
print("所有场景及其背景一览")
print("=" * 80)
for sid, title, bg in scene_bg_list:
    print(f"  [{bg:20s}] {sid:30s} - {title}")

print()
print("=" * 80)
print("背景类型使用统计")
print("=" * 80)
for bg, sids in sorted(bg_usage.items()):
    print(f"  {bg:20s} 被 {len(sids):2d} 个场景使用")

print()
print("=" * 80)
print("已有的背景图片文件 vs 代码中引用的背景")
print("=" * 80)

import os
bg_dir = "assets/backgrounds"
existing_files = [f.replace(".png", "") for f in os.listdir(bg_dir) if f.endswith(".png")]

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
    "black": "bg_black"
}

referenced_bgs = set(bg_usage.keys())
mapped_files = set()
for bg_key in referenced_bgs:
    if bg_key in bg_map:
        mapped_files.add(bg_map[bg_key])

print(f"故事中引用的背景类型: {len(referenced_bgs)} 种")
print(f"  {sorted(referenced_bgs)}")
print()
print(f"对应的背景图片文件: {len(mapped_files)} 个")
missing = mapped_files - set(existing_files)
extra = set(existing_files) - mapped_files
print(f"缺失的图片: {len(missing)} 个")
for m in sorted(missing):
    print(f"  - {m}.png")
print(f"多余的图片: {len(extra)} 个")
for e in sorted(extra):
    print(f"  - {e}.png")

print()
print("=" * 80)
print("可能不匹配的场景（背景 vs 内容初步检查）")
print("=" * 80)

# 简单的语义匹配检查
checks = [
    ("home", ["家", "童年", "旧房子", "出租屋", "宿舍"]),
    ("classroom", ["教室", "课堂", "小学", "老师", "作文", "同学"]),
    ("office_day", ["办公室", "公司", "白天", "上班", "面试", "讲台", "培训"]),
    ("office_night", ["加班", "夜晚", "深夜", "晚上"]),
    ("office_dark", ["昏暗", "小公司", "创业初期", "破旧"]),
    ("bookstore", ["书店", "书屋", "书"]),
    ("street_food", ["地摊", "夜市", "小吃", "路边", "烤红薯", "烤串"]),
    ("noodle_shop", ["面馆", "餐馆", "茶餐厅"]),
    ("bar", ["酒吧", "喝酒"]),
    ("factory", ["工厂", "车间", "机械厂"]),
    ("hospital", ["医院", "病房"]),
    ("corridor", ["走廊", "楼道"]),
    ("airport", ["机场", "飞机"]),
    ("train_platform", ["火车站", "站台", "火车"]),
    ("conference", ["发布会", "演讲", "舞台"]),
    ("press", ["记者", "发布会", "媒体"]),
    ("celebration", ["庆功", "庆祝", "婚礼", "宴"]),
    ("balcony", ["阳台"]),
    ("room_rent", ["出租屋", "租房"]),
    ("livestudio", ["直播", "主播"]),
    ("xiaomi_office", ["小米"]),
    ("apple_office", ["苹果"]),
    ("office_modern", ["现代", "科技公司", "大厦"]),
    ("venue", ["会场", "活动"]),
    ("small_office", ["小办公室", "居民楼", "创业初期"]),
    ("black", ["黑屏", "标题", "免责"]),
]

mismatches = []
for sid, title, bg in scene_bg_list:
    scene_data = scenes[sid]
    lines = scene_data.get("lines", [])
    text = "".join([line.get("text", "") for line in lines])
    # 检查该背景的关键词是否出现在内容中
    bg_keywords = None
    for cb, kws in checks:
        if cb == bg:
            bg_keywords = kws
            break
    if bg_keywords:
        found = any(kw in text or kw in title for kw in bg_keywords)
        if not found:
            # 检查是否有其他背景的关键词更匹配
            better_match = None
            for other_bg, other_kws in checks:
                if other_bg == bg:
                    continue
                if any(kw in text or kw in title for kw in other_kws):
                    better_match = other_bg
                    break
            mismatches.append((sid, title, bg, better_match, text[:60]))

if mismatches:
    for sid, title, bg, better, sample in mismatches:
        better_str = f"  → 可能更匹配: {better}" if better else ""
        print(f"  [{bg:20s}] {title} ({sid}){better_str}")
        print(f"      内容片段: {sample}...")
else:
    print("  （初步检查未发现明显不匹配）")
