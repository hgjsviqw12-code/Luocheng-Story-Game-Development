import json
import os

with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)

scenes = story['scenes']

# 收集所有角色
characters = set()
character_names = set()
# 收集所有场景背景
backgrounds = set()
# 收集所有说话者
speakers = set()
# 场景列表
scene_list = []

for scene_id, scene in scenes.items():
    title = scene.get('title', '')
    bg = scene.get('background', '')
    sp = scene.get('speaker', '')
    if bg:
        backgrounds.add(bg)
    if sp:
        speakers.add(sp)
    scene_list.append((scene_id, title, bg))
    
    for line in scene.get('lines', []):
        ch = line.get('character', 'none')
        if ch and ch != 'none':
            characters.add(ch)
        txt = line.get('text', '')
        # 尝试从文本中提取人名（用一些常见的名字模式）

print("=" * 60)
print("【剧本中出现的人物】")
print("=" * 60)
print(f"\n角色标识（character字段）：{len(characters)}个")
for c in sorted(characters):
    print(f"  - {c}")

print(f"\n场景说话者（speaker字段）：{len(speakers)}个")
for s in sorted(speakers):
    print(f"  - {s}")

# 从文本中推测更多角色名
print(f"\n主要角色（按剧情重要性）：")
main_chars = [
    ("罗诚", "主角，从负债到逆袭的创业者"),
    ("妻子", "罗诚的妻子，支持他的家人"),
    ("老王", "罗诚的好友和合伙人"),
    ("老周", "投资人"),
    ("程总", "科技公司CEO"),
    ("小张", "年轻同事/员工"),
    ("吴老板", "面馆老板"),
    ("Tim", "红果公司高管"),
]
for name, desc in main_chars:
    print(f"  - {name}：{desc}")

print("\n" + "=" * 60)
print("【剧本中出现的场景背景】")
print("=" * 60)
print(f"\n共 {len(backgrounds)} 种背景类型：")
bg_desc = {
    "black": "黑屏/标题画面",
    "home": "罗诚的家（老式居民楼）",
    "office_night": "办公室夜景",
    "office_day": "白天办公室",
    "office_dark": "深夜黑暗办公室",
    "office_modern": "现代科技公司办公室",
    "startup": "初创公司办公区",
    "factory": "手机工厂",
    "livestudio": "直播间",
    "xiaomi_office": "谷米公司办公室",
    "apple_office": "红果公司办公室",
}
for bg in sorted(backgrounds):
    desc = bg_desc.get(bg, bg)
    print(f"  - {bg}：{desc}")

print("\n" + "=" * 60)
print(f"【全部场景列表】（共 {len(scene_list)} 个场景）")
print("=" * 60)
for i, (sid, title, bg) in enumerate(scene_list, 1):
    print(f"  {i:2d}. [{sid}] {title}  (背景: {bg})")
