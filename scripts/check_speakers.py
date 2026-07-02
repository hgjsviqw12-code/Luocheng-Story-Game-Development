import json
with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)

chars = set()
speakers = set()
for sid, scene in story['scenes'].items():
    sp = scene.get('speaker', '')
    if sp:
        speakers.add(sp)
    for line in scene.get('lines', []):
        ch = line.get('character', 'none')
        if ch and ch != 'none':
            chars.add(ch)

print("Scene-level speakers:", speakers)
print("\nLine-level characters:")
for c in sorted(chars):
    print(f"  {c}")
