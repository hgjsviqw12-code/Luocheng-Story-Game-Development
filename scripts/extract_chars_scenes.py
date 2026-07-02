import json

with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)

# 收集所有人物
characters = {}  # character_id -> {'name': 中文名, 'desc': 描述}
speakers = {}    # speaker -> desc

for sid, scene in story['scenes'].items():
    for line in scene.get('lines', []):
        ch = line.get('character', '')
        if ch and ch != 'none':
            txt = line.get('text', '')
            if ch not in characters and txt:
                characters[ch] = txt[:80]

# 收集所有场景
scenes = {}
for sid, scene in story['scenes'].items():
    bg = scene.get('background', '')
    title = scene.get('title', '')
    if bg and bg not in scenes:
        scenes[bg] = {'title': title, 'count': 1}
    elif bg:
        scenes[bg]['count'] += 1

print("=== 人物 ===")
for k in sorted(characters.keys()):
    print(f"  {k}: {characters[k][:50]}")

print("\n=== 场景背景 ===")
for k in sorted(scenes.keys()):
    print(f"  {k}: {scenes[k]}")
