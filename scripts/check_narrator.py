import json
from collections import Counter

with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)

# 统计所有说话者
speakers = Counter()
scenes_with_speaker = {}

for sid, scene in story['scenes'].items():
    scene_chars = Counter()
    for line in scene.get('lines', []):
        ch = line.get('character', '')
        txt = line.get('text', '')
        if txt and ch:
            speakers[ch] += 1
            scene_chars[ch] += 1
    if scene_chars:
        scenes_with_speaker[sid] = dict(scene_chars)

print("=== 所有说话者统计 ===")
for ch, cnt in speakers.most_common():
    print(f"  {ch}: {cnt}条")

print("\n=== 前20个场景的说话者分布 ===")
for sid, chars in list(scenes_with_speaker.items())[:20]:
    title = story['scenes'][sid].get('title', sid)
    print(f"\n【{title}】{sid}:")
    for ch, cnt in sorted(chars.items(), key=lambda x: -x[1]):
        print(f"    {ch}: {cnt}条")

# 检查没有角色名字的旁白场景
print("\n=== 只有旁白或无说话者的场景 ===")
no_char_scenes = []
for sid, scene in story['scenes'].items():
    has_named_speaker = False
    for line in scene.get('lines', []):
        ch = line.get('character', '')
        txt = line.get('text', '')
        if txt and ch and ch not in ['none', '旁白', '系统']:
            has_named_speaker = True
            break
    if not has_named_speaker:
        title = scene.get('title', sid)
        bg = scene.get('background', '')
        line_count = len([l for l in scene.get('lines', []) if l.get('text')])
        no_char_scenes.append((sid, title, bg, line_count))

for sid, title, bg, cnt in no_char_scenes[:15]:
    print(f"  {title}: {cnt}条 (bg={bg})")
print(f"  共 {len(no_char_scenes)} 个场景没有具体角色说话")
