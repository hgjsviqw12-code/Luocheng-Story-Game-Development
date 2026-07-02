import urllib.request
import os
import urllib.parse
import time

base = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?"

def download(name, prompt, folder, size):
    url = base + "prompt=" + urllib.parse.quote(prompt) + "&image_size=" + size
    full_dir = os.path.join(os.path.dirname(__file__), "assets", folder)
    os.makedirs(full_dir, exist_ok=True)
    path = os.path.join(full_dir, name + ".jpg")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"SKIP (exists): {folder}/{name}.jpg")
        return
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK: {folder}/{name}.jpg ({len(data)} bytes)")
        time.sleep(1)
    except Exception as e:
        print(f"FAIL: {folder}/{name}.jpg - {e}")

# ============ 场景背景图 (landscape_16_9) ============
backgrounds = [
    # 已有12张，补充缺失的
    ("bg_office_day", "Pixel art scene, anime narrative style, bright modern office interior during daytime, large windows with sunlight, desks with computers, clean white and blue tones, professional working atmosphere, no text, no people"),
    ("bg_office_dark", "Pixel art scene, anime narrative style, extremely dark and depressing office at midnight, only one desk lamp glowing, shadows everywhere, deep blue purple tones, lonely hopeless mood, no text, no people"),
    ("bg_office_modern", "Pixel art scene, anime narrative style, ultra modern corporate office interior, glass walls, minimalist design, silver and blue colors, executives meeting room, high end tech company, no text, no people"),
    ("bg_noodle_shop", "Pixel art scene, anime narrative style, small cozy Chinese noodle shop at night, warm orange light from lamps, steam rising from bowls, wooden tables, two businessmen chatting over noodles, intimate warm atmosphere, no text"),
    ("bg_bar", "Pixel art scene, anime narrative style, quiet bar at night, neon signs reflecting on counter, whiskey glasses, moody purple blue lighting, lonely person drinking alone, melancholic atmosphere, no text, no people"),
    ("bg_stage", "Pixel art scene, anime narrative style, grand product launch stage, bright spotlight on center, large LED screen behind, dark audience silhouettes, red and gold lighting, epic presentation moment, no text, no people"),
    ("bg_street_food", "Pixel art scene, anime narrative style, Chinese street food stall at dawn, jianbing pancake cart, warm yellow lamp, elderly vendor cooking, quiet street, peaceful morning atmosphere, no text"),
    ("bg_celebration", "Pixel art scene, anime narrative style, company celebration dinner in restaurant, round table with food, people toasting, warm red and gold lighting, happy successful mood, Chinese banquet style, no text"),
    ("bg_bookstore", "Pixel art scene, anime narrative style, old dusty secondhand bookstore, shelves packed with books, warm reading lamp, old man behind counter, wooden interior, nostalgic cozy atmosphere, no text, no people"),
    ("bg_corridor", "Pixel art scene, anime narrative style, narrow office corridor at night, flickering fluorescent lights, doors on both sides, smoke in the air from a cigarette, lonely figure standing at end, dark blue tones, no text"),
    ("bg_hospital", "Pixel art scene, anime narrative style, hospital corridor at night, white sterile walls, fluorescent lights, waiting chairs, quiet tense atmosphere, blue white tones, no text, no people"),
    ("bg_press", "Pixel art scene, anime narrative style, press conference room, microphones on table, reporters with cameras, flash photography, bright white lights, tense media atmosphere, no text, no people"),
    ("bg_airport", "Pixel art scene, anime narrative style, international airport departure hall, large windows showing airplanes, modern glass architecture, person looking at boarding pass, blue grey tones, bittersweet farewell mood, no text"),
    ("bg_conference", "Pixel art scene, anime narrative style, large tech conference keynote stage, huge screen, audience of thousands, spotlights, blue and white lighting, exciting product reveal moment, no text, no people"),
    ("bg_small_office", "Pixel art scene, anime narrative style, tiny crowded startup office in early days, people working at cheap desks, computers everywhere, pizza boxes on table, passionate chaotic energy, warm lighting, no text"),
    ("bg_balcony", "Pixel art scene, anime narrative style, apartment balcony at night overlooking city lights, a man standing alone with cigarette, city skyline in distance, contemplative mood, dark blue tones, stars visible, no text"),
    ("bg_classroom_old", "Pixel art scene, anime narrative style, old Chinese English training classroom from 2000s, blackboard with English words, wooden desks, white fluorescent lights, students studying hard, warm learning atmosphere, no text"),
    ("bg_train_platform", "Pixel art scene, anime narrative style, old Chinese train station platform at night in 1990s, dim yellow lights, steam from train, young man with backpack sitting on bench alone, cold blue tones, melancholic departure mood, no text"),
]

# ============ 人物头像 (square) ============
characters = [
    ("wu_laoban", "Pixel art character portrait, anime style, elderly Chinese man in his 60s, kind wise eyes, wearing old sweater, secondhand bookstore owner, gentle smile, game avatar, simple warm background, expressive face, no text"),
    ("luocheng_kid", "Pixel art character portrait, anime style, young Chinese boy age 10, determined stubborn eyes, short hair, simple old clothes, childhood look, game avatar, simple warm background, expressive face, no text"),
    ("fan_young", "Pixel art character portrait, anime style, young Chinese man in early 20s, glasses, adoring enthusiastic eyes, wearing company lanyard, young tech fan look, game avatar, simple background, expressive face, no text"),
    ("narrator", "Pixel art character portrait, anime style, silhouette of storyteller figure, mysterious warm glowing outline, holding a book, narrative game narrator avatar, dark background with gold accents, no facial features visible, no text"),
]

print("=== 开始生成场景背景图 ===")
for name, prompt in backgrounds:
    download(name, prompt, "backgrounds", "landscape_16_9")

print("\n=== 开始生成人物头像 ===")
for name, prompt in characters:
    download(name, prompt, "characters", "square")

print("\n=== 全部完成 ===")
