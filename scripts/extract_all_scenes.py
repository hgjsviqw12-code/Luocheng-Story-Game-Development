import json

with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)

scenes = story['scenes']

# 收集每个场景的人物和背景
scene_list = []
for sid in sorted(scenes.keys()):
    scene = scenes[sid]
    title = scene.get('title', sid)
    bg = scene.get('background', '')
    sp = scene.get('speaker', '')
    
    chars = []
    for line in scene.get('lines', []):
        ch = line.get('character', '')
        if ch and ch != 'none' and ch not in chars:
            chars.append(ch)
    
    # 收集对话内容片段
    dialogues = []
    for line in scene.get('lines', []):
        txt = line.get('text', '')
        if txt and len(txt) > 5:
            dialogues.append(txt[:60])
        if len(dialogues) >= 3:
            break
    
    scene_list.append({
        'id': sid,
        'title': title,
        'bg': bg,
        'chars': chars,
        'dialogues': dialogues
    })

print(f"共 {len(scene_list)} 个场景")
for s in scene_list:
    chars_str = ', '.join(s['chars']) if s['chars'] else '无'
    print(f"\n【{s['title']}】")
    print(f"  场景ID: {s['id']}  背景: {s['bg']}")
    print(f"  出现人物: {chars_str}")
    if s['dialogues']:
        print(f"  内容摘要:")
        for d in s['dialogues']:
            print(f"    - {d}...")
