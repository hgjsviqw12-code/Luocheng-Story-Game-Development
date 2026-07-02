# -*- coding: utf-8 -*-
import json

with open("story.json", "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", {})

# 背景修改映射表
bg_changes = {
    # 序章
    "intro": "black",                           # 人物简介 → 黑屏更有仪式感
    "prologue_1_3": "classroom",                # 童年·我的理想 → 教室
    "prologue_2": "teacher_office",             # 辍学 → 教师办公室
    "prologue_2_2": "train_platform",           # 辍学·火车站之夜 → 火车站台
    "prologue_2_3": "bookstore",                # 辍学·二手书店 → 书店
    "prologue_2_4": "street_food",              # 辍学·摆地摊 → 街头夜市
    "prologue_4_2": "inn",                      # 遇见 → 大理客栈
    "prologue_5_2": "restaurant",               # 第一桶金 → 高级餐厅
    "prologue_6_5": "conference",               # S1发布会 → 大型发布会
    "prologue_7_2": "farmyard",                 # 最后一次团建 → 农家院

    # 第一幕
    "scene_1_1c": "corridor",                   # 走廊回忆 → 走廊

    # A线
    "branch_a_4": "conference",                 # 发布会前夕 → 大型发布会
    "ending_a_fail": "conference",              # 悲情英雄 → 发布会
    "ending_a_sell": "conference",              # 体面退场 → 发布会

    # B线
    "branch_b_2": "livestudio",                 # 学习直播 → 直播间
    "branch_b_5": "livestudio",                 # 网络暴力 → 直播间
    "branch_b_5_2": "livestudio",               # MCN签约 → 直播间

    # C线
    "branch_c_4": "xiaomi_office",              # 程总开导 → 谷米办公室
    "branch_c_4_2": "celebration",              # 庆功宴喝醉 → 庆功宴
    "ending_c_conflict": "xiaomi_office",       # 悲情离开 → 谷米办公室

    # D线
    "branch_d_1": "airport",                    # 飞往海外 → 机场
    "branch_d_4": "office_night",               # 家的召唤 → 夜晚办公室
    "ending_d_return": "conference",            # 海归归来 → 发布会

    # E线
    "branch_e_2_2": "corridor",                 # 回机械厂家属院 → 走廊
    "branch_e_3": "office_day",                 # 最后的告别 → 白天办公室
    "ending_e_comeback": "conference",          # 细红线归来 → 发布会
}

count = 0
for scene_id, new_bg in bg_changes.items():
    if scene_id in scenes:
        old_bg = scenes[scene_id].get("background", "")
        if old_bg != new_bg:
            scenes[scene_id]["background"] = new_bg
            count += 1
            print(f"  ✓ {scene_id}: {old_bg} → {new_bg}")
        else:
            print(f"  = {scene_id}: 已经是 {new_bg}")
    else:
        print(f"  ✗ {scene_id}: 场景不存在")

with open("story.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"\n共修改了 {count} 个场景的背景")
