import urllib.request
import os
import urllib.parse

base = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?"

# 场景图配置
backgrounds = [
    ("bg_home_old", "Pixel art scene, anime narrative style, old Chinese factory workers apartment complex, red brick buildings, warm sunset light, smoke from kitchens, nostalgic mood, soft lighting, no text"),
    ("bg_room_rent", "Pixel art scene, anime narrative style, small dimly lit rental room, single bed, desk with lamp, English word notes pasted all over wall, lonely study atmosphere, blue-gray tones, no text"),
    ("bg_classroom", "Pixel art scene, anime narrative style, Chinese training school classroom, blackboard, rows of desks, young students, bright fluorescent lights, warm learning atmosphere, no text"),
    ("bg_office_startup", "Pixel art scene, anime narrative style, small crowded Chinese tech startup office, whiteboard with Chinese characters 'craftsman', people working at desks in narrow hallway, passionate startup mood, no text"),
    ("bg_factory", "Pixel art scene, anime narrative style, smartphone factory production line, workers assembling phones, industrial atmosphere, blue-white fluorescent lights, no text"),
    ("bg_venue", "Pixel art scene, anime narrative style, large product launch event venue, stage with spotlight, audience silhouettes, big screen, excited tech atmosphere, no text"),
    ("bg_office_night", "Pixel art scene, anime narrative style, late night CEO office interior, desk with computer glowing, stack of documents, city night view through window, deep blue and purple tones, moody atmosphere, no text"),
    ("bg_livestudio", "Pixel art scene, anime narrative style, live streaming studio, professional camera, ring lights, neon pink and purple glow, phone products on table, modern energetic atmosphere, no text"),
    ("bg_xiaomi", "Pixel art scene, anime narrative style, modern Chinese tech company campus, orange and white buildings, glass offices, energetic campus mood, no text"),
    ("bg_apple", "Pixel art scene, anime narrative style, futuristic circular tech campus building, glass and steel, clean modern design, blue sky, no text"),
    ("bg_kitchen", "Pixel art scene, anime narrative style, cozy home kitchen at dusk, warm yellow light, cooking steam, family dining table, warm and peaceful atmosphere, no text"),
    ("bg_trainstation", "Pixel art scene, anime narrative style, empty train station platform at night, lonely man sitting on bench, distant city lights, cold blue tones, melancholic atmosphere, no text"),
]

characters = [
    ("luocheng_young", "Pixel art character portrait, anime style, young Chinese man with long hair to shoulders, stubborn determined eyes, wearing black shirt, thin build, game avatar, simple background, expressive face, no text"),
    ("luocheng_mid", "Pixel art character portrait, anime style, middle-aged Chinese man with gray-white short hair, stubborn determined eyes, slight eye bags, wearing dark shirt, game avatar, simple background, expressive face, no text"),
    ("wife", "Pixel art character portrait, anime style, Chinese woman with short black hair, gentle warm smile, simple modest clothes, game avatar, simple background, expressive face, no text"),
    ("laowang", "Pixel art character portrait, anime style, middle-aged chubby Chinese man with glasses, holding vacuum flask, friendly tech engineer look, game avatar, simple background, expressive face, no text"),
    ("laozhou", "Pixel art character portrait, anime style, tall thin Chinese man in suit, serious expression, lawyer or executive look, game avatar, simple background, expressive face, no text"),
    ("xiaozhang", "Pixel art character portrait, anime style, young Chinese woman with ponytail, smart sharp eyes, holding calculator, finance manager look, game avatar, simple background, expressive face, no text"),
    ("chengzong", "Pixel art character portrait, anime style, middle-aged Chinese man with warm smile, wearing dark t-shirt, friendly tech CEO look, game avatar, simple background, expressive face, no text"),
    ("tim", "Pixel art character portrait, anime style, Western man with short hair, wearing casual suit, gentle expression, tech executive look, game avatar, simple background, expressive face, no text"),
]

def download(name, prompt, folder, size):
    url = base + "prompt=" + urllib.parse.quote(prompt) + "&image_size=" + size
    full_dir = os.path.join(os.path.dirname(__file__), "assets", folder)
    os.makedirs(full_dir, exist_ok=True)
    path = os.path.join(full_dir, name + ".jpg")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as response:
            data = response.read()
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK: {folder}/{name}.jpg")
    except Exception as e:
        print(f"FAIL: {folder}/{name}.jpg - {e}")

for name, prompt in backgrounds:
    download(name, prompt, "backgrounds", "landscape_16_9")

for name, prompt in characters:
    download(name, prompt, "characters", "square")

print("全部完成")
