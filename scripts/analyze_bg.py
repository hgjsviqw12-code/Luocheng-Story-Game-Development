# -*- coding: utf-8 -*-
import json

with open("story.json", "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data.get("scenes", {})

# 背景图定义
backgrounds = {
    "home": "老家/旧房子（北方小城，家属院，旧家具）",
    "office_night": "夜晚办公室（加班，昏暗，城市夜景窗外）",
    "office_day": "白天办公室（明亮，正常上班）",
    "office_dark": "昏暗小办公室/破旧办公室（创业初期，压抑）",
    "livestudio": "直播间（补光灯，手机支架，背景墙）",
    "startup": "小创业办公室（居民楼/老写字楼，拥挤，有烟火气）",
    "office_modern": "现代科技公司办公室（大公司，落地窗，明亮）",
    "factory": "工厂/车间（流水线，机器，工人）",
    "xiaomi_office": "谷米科技办公室（橙色/科技感，年轻员工）",
    "apple_office": "红果科技办公室（白色简约，海外风格）",
    "classroom": "教室（小学/中学，课桌，黑板）",
    "noodle_shop": "面馆/小餐馆（简陋，温馨，市井）",
    "bar": "酒吧（昏暗，吧台，酒杯）",
    "street_food": "街头/夜市（地摊，小吃，霓虹灯）",
    "venue": "活动会场/演讲台（大型活动）",
    "celebration": "庆功宴/宴会（酒席，庆祝氛围）",
    "bookstore": "书店（书架，旧书，安静）",
    "corridor": "走廊（公司走廊，长长的，有墙上照片）",
    "hospital": "医院走廊/病房（白色，消毒水感）",
    "press": "记者会（媒体，话筒，闪光灯）",
    "airport": "机场（候机厅，航班显示屏）",
    "conference": "大型发布会（舞台，聚光灯，观众）",
    "balcony": "阳台夜景（城市灯光，栏杆）",
    "train_platform": "火车站台（火车，站台，候车人群）",
    "room_rent": "出租屋（简陋，狭窄，年轻人租房）",
    "black": "黑屏/纯黑（标题/免责/转场）",
}

results = []

for sid, scene_data in scenes.items():
    title = scene_data.get("title", sid)
    current_bg = scene_data.get("background", "none")
    lines = scene_data.get("lines", [])
    text = "".join([line.get("text", "") for line in lines])

    # 基于关键词匹配建议背景
    scores = {}
    for bg_key, desc in backgrounds.items():
        scores[bg_key] = 0

    # 关键词映射
    keywords = {
        "classroom": ["教室", "课堂", "小学", "老师", "同学", "作文", "班主任", "语文课", "教鞭", "讲台下", "三年级"],
        "bookstore": ["书店", "书屋", "二手书", "书架", "旧书", "武侠小说", "吴老板", "《硅谷之火》"],
        "street_food": ["地摊", "夜市", "小吃", "路边", "烤串", "烤红薯", "城管", "袜子", "编织袋", "摆摊"],
        "train_platform": ["火车站", "站台", "火车", "候车室", "长椅睡", "列车", "广播里播报"],
        "home": ["家", "家里", "老家", "旧房子", "家属院", "父亲", "母亲", "爸妈", "妻子", "客厅", "厨房", "卧室", "阳台", "回家", "沙发", "家人"],
        "room_rent": ["出租屋", "租房", "出租房", "一间小房子", "一张床一张桌子", "隔壁是麻将馆", "居民楼"],
        "office_day": ["办公室", "公司", "白天", "上班", "会议室", "全员大会", "HR", "面试", "员工", "同事", "入职", "工位", "开会"],
        "office_night": ["加班", "夜晚", "深夜", "晚上", "凌晨", "通宵", "灯还亮着", "三个通宵", "夜景", "窗外是"],
        "office_dark": ["昏暗", "破旧", "小公司", "创业初期", "拮据", "逼仄", "压抑", "不到一百平米", "居民楼"],
        "startup": ["创业初期", "坚石科技刚成立", "小办公室", "三十个人挤", "老写字楼", "创业", "开博客平台", "居民楼里"],
        "office_modern": ["现代", "大公司", "大厦", "摩天楼", "星河跳动", "收购", "谈判", "MCN", "签约"],
        "factory": ["工厂", "车间", "代工厂", "产线", "流水线", "物料", "样机", "原型机", "良品率", "硬件", "电路板"],
        "xiaomi_office": ["谷米", "程总", "科技园", "性价比", "红米风格"],
        "apple_office": ["红果", "Coco", "海外", "硅谷", "英文", "美国", "苹果风"],
        "livestudio": ["直播", "主播", "直播间", "带货", "短视频", "镜头", "弹幕", "补光灯"],
        "conference": ["发布会", "演讲", "舞台", "聚光灯", "台下掌声", "发布会上", "PPT", "场馆"],
        "celebration": ["庆功宴", "庆祝", "婚礼", "宴席", "喝醉", "庆功"],
        "corridor": ["走廊", "楼道", "走廊里", "沿着走廊", "安全门", "楼梯间"],
        "airport": ["机场", "飞机", "航班", "登机", "航站楼"],
        "hospital": ["医院", "病房", "住院", "生病", "手术"],
        "bar": ["酒吧", "喝酒", "吧台", "酒保"],
        "noodle_shop": ["面馆", "小餐馆", "茶餐厅", "吃饭", "点菜", "菜单"],
        "venue": ["会场", "活动", "大型活动", "论坛"],
        "press": ["记者", "媒体", "发布会", "采访", "话筒"],
        "balcony": ["阳台", "天台"],
        "black": ["免责声明", "黑屏", "标题画面"],
    }

    for bg_key, kws in keywords.items():
        for kw in kws:
            if kw in text or kw in title:
                scores[bg_key] = scores.get(bg_key, 0) + 1

    # 排序
    sorted_bgs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top3 = [(bg, s) for bg, s in sorted_bgs[:3] if s > 0]

    results.append({
        "id": sid,
        "title": title,
        "current": current_bg,
        "top3": top3,
        "needs_change": len(top3) > 0 and top3[0][0] != current_bg and top3[0][1] >= 2
    })

# 输出
print("=" * 100)
print("场景背景匹配分析报告")
print("=" * 100)

print(f"\n总场景数: {len(results)}")
print(f"当前使用的背景类型: {len(set(r['current'] for r in results))}")
print(f"建议修改的场景: {sum(1 for r in results if r['needs_change'])}")

print("\n" + "=" * 100)
print("建议修改背景的场景（按场景顺序）")
print("=" * 100)

for r in results:
    if r["needs_change"]:
        best_bg = r["top3"][0][0]
        best_score = r["top3"][0][1]
        top3_str = ", ".join([f"{bg}({s})" for bg, s in r["top3"]])
        print(f"\n  【{r['title']}】({r['id']})")
        print(f"    当前背景: {r['current']} ({backgrounds.get(r['current'], '?')})")
        print(f"    建议改为: {best_bg} ({backgrounds.get(best_bg, '?')})  匹配度: {best_score}")
        print(f"    Top3候选: {top3_str}")

print("\n" + "=" * 100)
print("所有场景一览（含当前背景）")
print("=" * 100)

for r in results:
    mark = " ⚠️" if r["needs_change"] else ""
    print(f"  [{r['current']:20s}] {r['title']:30s} ({r['id']}){mark}")

print("\n" + "=" * 100)
print("背景使用统计")
print("=" * 100)

from collections import Counter
bg_counts = Counter(r["current"] for r in results)
for bg, count in bg_counts.most_common():
    print(f"  {bg:20s}  {count:2d} 个场景  - {backgrounds.get(bg, '?')}")
