from PIL import Image, ImageDraw
import os
import random

random.seed(123)
OUT_CH = os.path.join(os.path.dirname(__file__), "assets", "characters")
os.makedirs(OUT_CH, exist_ok=True)

CW, CH = 128, 128


def draw_avatar(skin=(220, 185, 160), hair_color=(30, 25, 25), shirt=(50, 50, 70),
                expression="neutral", has_glasses=False, has_beard=False, tie=None):
    img = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = CW // 2, CH // 2

    d.rounded_rectangle([cx - 35, cy + 8, cx + 35, cy + 52], radius=5, fill=shirt)
    d.rectangle([cx - 9, cy + 2, cx + 9, cy + 16], fill=skin)
    d.ellipse([cx - 26, cy - 34, cx + 26, cy + 10], fill=skin)
    if hair_color:
        d.ellipse([cx - 28, cy - 40, cx + 28, cy - 6], fill=hair_color)
        d.rectangle([cx - 28, cy - 22, cx + 28, cy - 14], fill=hair_color)
        if has_beard:
            d.pieslice([cx - 22, cy - 10, cx + 22, cy + 14], 0, 180, fill=hair_color)
    eye_y = cy - 10
    d.rectangle([cx - 13, eye_y, cx - 5, eye_y + 5], fill=(25, 25, 30))
    d.rectangle([cx + 5, eye_y, cx + 13, eye_y + 5], fill=(25, 25, 30))
    d.rectangle([cx - 10, eye_y + 1, cx - 8, eye_y + 3], fill=(255, 255, 255))
    d.rectangle([cx + 8, eye_y + 1, cx + 10, eye_y + 3], fill=(255, 255, 255))
    brow_c = hair_color or (40, 35, 30)
    d.rectangle([cx - 15, eye_y - 6, cx - 3, eye_y - 4], fill=brow_c)
    d.rectangle([cx + 3, eye_y - 6, cx + 15, eye_y - 4], fill=brow_c)
    if expression == "smile":
        d.arc([cx - 9, cy - 2, cx + 9, cy + 12], 0, 180, fill=(180, 70, 70), width=2)
    elif expression == "serious":
        d.rectangle([cx - 7, cy + 3, cx + 7, cy + 5], fill=(140, 60, 60))
    elif expression == "determined":
        d.arc([cx - 8, cy - 1, cx + 8, cy + 10], 0, 180, fill=(160, 65, 65), width=2)
        d.rectangle([cx - 7, cy + 5, cx + 7, cy + 6], fill=(160, 65, 65))
    else:
        d.arc([cx - 6, cy, cx + 6, cy + 8], 0, 180, fill=(150, 65, 65), width=2)
    if has_glasses:
        d.ellipse([cx - 17, eye_y - 5, cx - 3, eye_y + 9], outline=(50, 50, 70), width=2)
        d.ellipse([cx + 3, eye_y - 5, cx + 17, eye_y + 9], outline=(50, 50, 70), width=2)
        d.line([cx - 3, eye_y + 2, cx + 3, eye_y + 2], fill=(50, 50, 70), width=2)
    if tie:
        d.polygon([(cx - 4, cy + 10), (cx + 4, cy + 10), (cx + 6, cy + 30), (cx, cy + 36), (cx - 6, cy + 30)], fill=tie)
    return img


def make_bg_black():
    img = Image.new("RGB", (320, 180), (5, 5, 10))
    for y in range(180):
        r = int(5 + y * 0.05)
        g = int(5 + y * 0.03)
        b = int(10 + y * 0.08)
        for x in range(320):
            img.putpixel((x, y), (r, g, b))
    return img.resize((1280, 720), Image.NEAREST)


def make_bg_title():
    img = Image.new("RGB", (320, 180), (10, 5, 20))
    d = ImageDraw.Draw(img)
    for _ in range(40):
        import random as r
        sx, sy = r.randint(0, 319), r.randint(0, 100)
        d.point((sx, sy), fill=(255, 255, 200))
    for i in range(8):
        bx = i * 42 - 5
        bh = r.randint(25, 55)
        d.rectangle([bx, 180 - bh - 15, bx + 35, 180 - 15], fill=(15, 10, 30))
        for wy in range(0, bh - 5, 6):
            for wx in range(3, 32, 8):
                if r.random() < 0.4:
                    d.point((bx + wx, 180 - bh - 15 + wy), fill=(255, 200, 80))
    d.rectangle([0, 165, 320, 180], fill=(20, 15, 30))
    return img.resize((1280, 720), Image.NEAREST)


print("Generating backgrounds...")
bg_path = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
bg_black = make_bg_black()
bg_black.save(os.path.join(bg_path, "bg_black.png"), "PNG")
print("  Saved bg_black.png")

print("\nGenerating character avatars...")

# luocheng - 主角罗诚，中年，深色短发，深色衬衫，坚毅表情
luocheng = draw_avatar(
    skin=(225, 190, 165),
    hair_color=(25, 20, 18),
    shirt=(35, 35, 45),
    expression="determined",
    has_glasses=False,
    has_beard=False
)
luocheng.save(os.path.join(OUT_CH, "luocheng.png"), "PNG")
print("  Saved luocheng.png")

# luocheng_mid - 中年版，映射到luocheng
luocheng_mid = draw_avatar(
    skin=(220, 185, 160),
    hair_color=(40, 30, 25),
    shirt=(45, 40, 55),
    expression="serious",
    has_glasses=False,
    has_beard=True
)
luocheng_mid.save(os.path.join(OUT_CH, "luocheng_mid.png"), "PNG")
print("  Saved luocheng_mid.png")

# laowang - 老王，好友，略胖，眼镜，温暖笑容
laowang = draw_avatar(
    skin=(215, 185, 160),
    hair_color=(60, 50, 40),
    shirt=(60, 80, 100),
    expression="smile",
    has_glasses=True,
    has_beard=False
)
laowang.save(os.path.join(OUT_CH, "laowang.png"), "PNG")
print("  Saved laowang.png")

# laozhou - 老周，投资人，西装革履，严肃，眼镜
laozhou = draw_avatar(
    skin=(220, 190, 165),
    hair_color=(50, 40, 35),
    shirt=(30, 30, 40),
    expression="serious",
    has_glasses=True,
    has_beard=False,
    tie=(150, 40, 40)
)
laozhou.save(os.path.join(OUT_CH, "laozhou.png"), "PNG")
print("  Saved laozhou.png")

# cheng - 程总，科技公司CEO，温和微笑，衬衫
cheng = draw_avatar(
    skin=(230, 200, 175),
    hair_color=(20, 18, 15),
    shirt=(50, 70, 100),
    expression="smile",
    has_glasses=False,
    has_beard=False,
    tie=None
)
cheng.save(os.path.join(OUT_CH, "cheng.png"), "PNG")
print("  Saved cheng.png")

# tim - Tim Cook原型，白发西裝，微笑
tim = draw_avatar(
    skin=(220, 195, 175),
    hair_color=(180, 175, 170),
    shirt=(40, 50, 70),
    expression="smile",
    has_glasses=False,
    has_beard=False,
    tie=(180, 180, 190)
)
tim.save(os.path.join(OUT_CH, "tim.png"), "PNG")
print("  Saved tim.png")

# wife - 妻子，长发，温柔微笑
def draw_wife():
    img = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = CW // 2, CH // 2
    d.rounded_rectangle([cx - 32, cy + 10, cx + 32, cy + 52], radius=5, fill=(120, 60, 80))
    d.rectangle([cx - 8, cy + 2, cx + 8, cy + 14], fill=(230, 195, 175))
    d.ellipse([cx - 24, cy - 32, cx + 24, cy + 8], fill=(230, 195, 175))
    d.ellipse([cx - 28, cy - 38, cx + 28, cy - 4], fill=(40, 25, 20))
    d.rectangle([cx - 32, cy - 20, cx + 32, cy + 5], fill=(40, 25, 20))
    eye_y = cy - 10
    d.rectangle([cx - 12, eye_y, cx - 5, eye_y + 4], fill=(30, 25, 30))
    d.rectangle([cx + 5, eye_y, cx + 12, eye_y + 4], fill=(30, 25, 30))
    d.rectangle([cx - 9, eye_y + 1, cx - 7, eye_y + 3], fill=(255, 255, 255))
    d.rectangle([cx + 7, eye_y + 1, cx + 9, eye_y + 3], fill=(255, 255, 255))
    d.arc([cx - 6, cy - 4, cx + 6, cy + 6], 0, 180, fill=(180, 80, 100), width=2)
    d.rectangle([cx - 14, eye_y - 4, cx - 4, eye_y - 2], fill=(40, 25, 20))
    d.rectangle([cx + 4, eye_y - 4, cx + 14, eye_y - 2], fill=(40, 25, 20))
    return img

wife = draw_wife()
wife.save(os.path.join(OUT_CH, "wife.png"), "PNG")
print("  Saved wife.png")

# xiaozhang - 小张，年轻同事
xiaozhang = draw_avatar(
    skin=(235, 205, 180),
    hair_color=(20, 15, 12),
    shirt=(70, 90, 120),
    expression="smile",
    has_glasses=False,
    has_beard=False
)
xiaozhang.save(os.path.join(OUT_CH, "xiaozhang.png"), "PNG")
print("  Saved xiaozhang.png")

# wu_laoban - 吴老板，面馆老板，围裙
wu_laoban = draw_avatar(
    skin=(210, 175, 145),
    hair_color=(50, 40, 30),
    shirt=(80, 50, 30),
    expression="smile",
    has_glasses=False,
    has_beard=True
)
wu_laoban.save(os.path.join(OUT_CH, "wu_laoban.png"), "PNG")
print("  Saved wu_laoban.png")

print("\n=== All character avatars generated! ===")
