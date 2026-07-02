from PIL import Image, ImageDraw, ImageFilter
import os
import math
import random

random.seed(777)

OUT = os.path.join(os.path.dirname(__file__), "character_previews")
os.makedirs(OUT, exist_ok=True)

# 高分辨率基础 (256x256 pixel art, upscaled to 512x512)
PW, PH = 256, 256
SCALE = 2
FW, FH = PW * SCALE, PH * SCALE


def upscale(img):
    return img.resize((FW, FH), Image.NEAREST)


def save(img, name):
    path = os.path.join(OUT, name + ".png")
    img.save(path, "PNG")
    print(f"  Saved: {name}.png ({img.size})")


def fill(draw, x, y, w, h, c):
    draw.rectangle([x, y, x+w-1, y+h-1], fill=c)


def ellipse(draw, cx, cy, rx, ry, c):
    draw.ellipse([cx-rx, cy-ry, cx+rx-1, cy+ry-1], fill=c)


def line(draw, x1, y1, x2, y2, c, w=1):
    draw.line([(x1, y1), (x2, y2)], fill=c, width=w)


# ========== 颜色定义 ==========
SKIN = (230, 195, 170)
SKIN_SHADOW = (210, 170, 145)
SKIN_HIGHLIGHT = (245, 215, 190)
HAIR_BLACK = (25, 20, 18)
HAIR_DARK = (40, 32, 28)
EYE_DARK = (20, 18, 25)
EYE_BROWN = (60, 40, 30)
EYE_WHITE = (250, 248, 245)
EYE_HL = (255, 255, 255)
BROW = (35, 28, 22)
LIP = (185, 100, 100)
LIP_SHADOW = (150, 75, 80)
NOSE = (215, 175, 150)
SHIRT_BLACK = (30, 28, 35)
SHIRT_DARK = (40, 38, 50)
SHIRT_BLUE = (45, 60, 90)
SHIRT_GRAY = (80, 75, 85)
SUIT_DARK = (25, 28, 38)
TIE_RED = (160, 35, 35)
TIE_BLUE = (40, 60, 110)
COLLAR_WHITE = (235, 235, 240)
BG_WARM = (245, 230, 210)
BG_BLUE = (50, 70, 120)
BG_PURPLE = (60, 40, 90)
BG_NEUTRAL = (200, 190, 180)
BEARD = (50, 40, 35)


def draw_head_base(draw, cx, cy, face_w=50, face_h=58, skin=SKIN):
    """绘制基础头部（圆脸，符合人物特征）"""
    # 脖子阴影
    ellipse(draw, cx, cy+face_h-2, 18, 12, SKIN_SHADOW)
    # 脖子
    fill(draw, cx-10, cy+face_h-8, 20, 20, skin)
    # 脸部（圆脸）
    ellipse(draw, cx, cy, face_w, face_h, skin)
    # 下巴阴影
    for i in range(8):
        alpha = max(0, 15 - i*2)
        draw.point((cx-20+i, cy+face_h-8), fill=SKIN_SHADOW)
        draw.point((cx+19-i, cy+face_h-8), fill=SKIN_SHADOW)
    # 腮红
    for i in range(6):
        draw.point((cx-28+i, cy+8), fill=(235, 170, 155))
        draw.point((cx+22+i, cy+8), fill=(235, 170, 155))


def draw_eyes(draw, cx, cy, eye_y_offset=0, expression="normal", look="center"):
    """绘制眼睛"""
    ey = cy + eye_y_offset
    eye_w, eye_h = 10, 7
    eye_dist = 22
    # 眼白
    if expression in ["smile", "happy"]:
        # 笑眼（弯月形）
        for ex in [cx - eye_dist, cx + eye_dist]:
            for dx in range(-eye_w//2, eye_w//2+1):
                for dy in range(-1, 3):
                    t = abs(dx) / (eye_w//2)
                    curve = int((1 - t*t) * 2)
                    if dy == curve:
                        draw.point((ex+dx, ey+dy), fill=EYE_DARK)
    else:
        for ex in [cx - eye_dist, cx + eye_dist]:
            fill(draw, ex-eye_w//2, ey-eye_h//2, eye_w, eye_h, EYE_WHITE)
            # 瞳孔
            pupil_off = 0
            if look == "left":
                pupil_off = -2
            elif look == "right":
                pupil_off = 2
            elif look == "up":
                pupil_off = 0
            # 虹膜
            iris_c = EYE_BROWN
            fill(draw, ex+pupil_off-3, ey-2, 6, 5, iris_c)
            fill(draw, ex+pupil_off-2, ey-3, 4, 3, EYE_DARK)
            # 高光
            draw.point((ex+pupil_off, ey-1), fill=EYE_HL)
            draw.point((ex+pupil_off-2, ey-2), fill=EYE_HL)
            # 上眼线
            for dx in range(-eye_w//2-1, eye_w//2+2):
                draw.point((ex+dx, ey-eye_h//2-1), fill=EYE_DARK)
            # 下眼线
            for dx in range(-eye_w//2, eye_w//2+1):
                draw.point((ex+dx, ey+eye_h//2), fill=(100, 80, 70))


def draw_eyebrows(draw, cx, cy, brow_y=-5, style="normal"):
    """绘制眉毛"""
    ey = cy + brow_y
    bw, bh = 16, 3
    bd = 20
    for bx in [cx - bd, cx + bd]:
        if style == "angry":
            for dx in range(bw):
                offset = -int(2 * abs(dx - bw//2) / bw)
                if dx < 4:
                    offset -= 1
                draw.point((bx-bw//2+dx, ey+offset), fill=BROW)
                if dx > 0 and dx < bw-1:
                    draw.point((bx-bw//2+dx, ey+offset+1), fill=BROW)
        elif style == "sad":
            for dx in range(bw):
                offset = int(2 * abs(dx - bw//2) / bw)
                draw.point((bx-bw//2+dx, ey+offset), fill=BROW)
        else:
            for dx in range(bw):
                draw.point((bx-bw//2+dx, ey), fill=BROW)
                draw.point((bx-bw//2+dx, ey+1), fill=(60, 48, 38))

def draw_nose(draw, cx, cy):
    """绘制鼻子"""
    ny = cy + 6
    # 鼻梁
    for dy in range(-8, 0):
        draw.point((cx, ny+dy), fill=NOSE)
    # 鼻头
    draw.point((cx-2, ny+1), fill=NOSE)
    draw.point((cx, ny+2), fill=NOSE)
    draw.point((cx+2, ny+1), fill=NOSE)
    # 鼻翼
    draw.point((cx-4, ny), fill=SKIN_SHADOW)
    draw.point((cx+3, ny), fill=SKIN_SHADOW)


def draw_mouth(draw, cx, cy, style="smile"):
    """绘制嘴巴"""
    my = cy + 18
    if style == "smile":
        for dx in range(-10, 11):
            t = dx / 10
            curve = int(t * t * 4)
            draw.point((cx+dx, my-curve), fill=LIP)
        # 下唇
        for dx in range(-6, 7):
            t = abs(dx) / 6
            curve = int((1-t) * 3)
            draw.point((cx+dx, my+1-curve), fill=LIP_SHADOW)
    elif style == "determined":
        fill(draw, cx-8, my, 16, 2, LIP)
        fill(draw, cx-6, my+1, 12, 1, LIP_SHADOW)
    elif style == "open":
        fill(draw, cx-6, my-1, 12, 5, (80, 40, 50))
        for dx in range(-5, 6):
            draw.point((cx+dx, my-1), fill=(220, 140, 140))
    elif style == "serious":
        fill(draw, cx-7, my, 14, 2, LIP_SHADOW)


def draw_hair_short(draw, cx, cy, hw=52, hh=40, style="normal"):
    """绘制短发（中年男性发型）"""
    top_y = cy - hh + 5
    # 头顶
    for dy in range(hh):
        t = dy / hh
        w = int(hw * math.sin(t * math.pi * 0.7))
        if style == "balding":
            if dy < 15:
                w = max(0, w - 15 + dy)
        for dx in range(-w, w+1):
            y = top_y + dy
            if 0 <= cx+dx < PW and 0 <= y < PH:
                draw.point((cx+dx, y), fill=HAIR_BLACK)
    # 两侧头发
    for side in [-1, 1]:
        sx = cx + side * (hw - 8)
        for dy in range(0, 30):
            w = max(2, 8 - dy//4)
            for dx in range(w):
                y = cy - 5 + dy
                draw.point((sx + side*dx, y), fill=HAIR_BLACK)
    # 发际线（前额）
    for dx in range(-25, 26):
        if abs(dx) > 8 or style == "receding":
            draw.point((cx+dx, cy-35+abs(dx)//8), fill=SKIN)
    # 头发高光
    for dy in range(5):
        for dx in range(-20, 21):
            t = abs(dx) / 20
            if random.random() < 0.3 and t < 0.7:
                draw.point((cx+dx, top_y+dy+3), fill=HAIR_DARK)


def draw_shirt(draw, cx, cy_top, color=SHIRT_BLACK, tie=None, collar=True):
    """绘制上衣"""
    # 肩膀
    shoulder_y = cy_top
    fill(draw, cx-45, shoulder_y, 90, 80, color)
    # 领口
    if collar:
        fill(draw, cx-12, shoulder_y-3, 24, 15, COLLAR_WHITE)
        fill(draw, cx-8, shoulder_y, 16, 10, SKIN_SHADOW)
    if tie:
        fill(draw, cx-4, shoulder_y+2, 8, 35, tie)
        # 领带结
        fill(draw, cx-6, shoulder_y, 12, 8, tie)
        # 领结V形
        for dx in range(-3, 4):
            draw.point((cx+dx, shoulder_y+12+abs(dx)), fill=tie)
    # 衣服阴影
    for dy in range(60):
        darkness = min(40, dy // 2)
        for dx in range(-45+dy//3, 46-dy//3):
            pass


def draw_background(draw, style="warm"):
    """绘制背景"""
    if style == "warm":
        for y in range(PH):
            t = y / PH
            r = int(245 - t * 30)
            g = int(225 - t * 40)
            b = int(200 - t * 50)
            for x in range(PW):
                draw.point((x, y), fill=(r, g, b))
        # 光晕
        for r in range(80):
            for a in range(0, 360, 8):
                rx = int(60 + r * math.cos(math.radians(a)))
                ry = int(50 + r * math.sin(math.radians(a)))
                if 0 <= rx < PW and 0 <= ry < PH:
                    alpha = max(0, 30 - r//3)
                    base = draw.im.getpixel((rx, ry)) if rx < PW and ry < PH else BG_WARM
                    draw.point((rx, ry), fill=(min(255, base[0]+alpha), min(255, base[1]+alpha//2), base[2]))
    elif style == "blue":
        for y in range(PH):
            t = y / PH
            r = int(30 + t * 40)
            g = int(50 + t * 30)
            b = int(100 + t * 40)
            for x in range(PW):
                draw.point((x, y), fill=(r, g, b))
    elif style == "stage":
        for y in range(PH):
            for x in range(PW):
                t = ((x - PW//2)**2 + (y - PH//3)**2) ** 0.5
                v = max(0, min(255, int(180 - t * 0.8)))
                draw.point((x, y), fill=(v//4, v//6, v//3))
        # 聚光
        for r in range(100):
            for a in range(0, 360, 5):
                rx = int(PW//2 + r * 0.8 * math.cos(math.radians(a)))
                ry = int(60 + r * 1.2 * math.sin(math.radians(a)))
                if 0 <= rx < PW and 0 <= ry < PH:
                    b = max(0, 50 - r//3)
                    draw.point((rx, ry), fill=(b+20, b+10, b+40))
    elif style == "neutral":
        for y in range(PH):
            t = y / PH
            v = int(210 - t * 40)
            for x in range(PW):
                draw.point((x, y), fill=(v, v-5, v-10))


# ========== 版本1：经典动漫风 - 坚定微笑 ==========
def v1_classic():
    img = Image.new("RGB", (PW, PH), BG_WARM)
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_background(d, "warm")
    draw_shirt(d, cx, cy+55, SHIRT_BLACK, None, collar=True)
    draw_head_base(d, cx, cy, 50, 58)
    draw_hair_short(d, cx, cy-5, 52, 38)
    draw_eyebrows(d, cx, cy, brow_y=-15, style="normal")
    draw_eyes(d, cx, cy-2, "normal", "center")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "smile")
    return upscale(img)


# ========== 版本2：西装革履发布会版 ==========
def v2_suit():
    img = Image.new("RGB", (PW, PH), (20, 25, 50))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 15
    draw_background(d, "stage")
    draw_shirt(d, cx, cy+55, SUIT_DARK, TIE_RED, collar=True)
    draw_head_base(d, cx, cy, 48, 55)
    draw_hair_short(d, cx, cy-8, 50, 36, "receding")
    draw_eyebrows(d, cx, cy, brow_y=-18, style="normal")
    draw_eyes(d, cx, cy-5, "determined", "center")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "determined")
    return upscale(img)


# ========== 版本3：年轻版（20多岁北漂时期） ==========
def v3_young():
    img = Image.new("RGB", (PW, PH), (60, 50, 80))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_background(d, "blue")
    # 格子衬衫
    draw_shirt(d, cx, cy+55, (60, 70, 100), None, collar=False)
    draw_head_base(d, cx, cy, 45, 52, SKIN)
    draw_hair_short(d, cx, cy-5, 48, 42)
    draw_eyebrows(d, cx, cy, brow_y=-14, style="normal")
    draw_eyes(d, cx, cy-3, "normal", "up")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "smile")
    return upscale(img)


# ========== 版本4：直播带货版 ==========
def v4_livestream():
    img = Image.new("RGB", (PW, PH), (80, 30, 80))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    # 紫色补光背景
    for y in range(PH):
        for x in range(PW):
            d1 = ((x-80)**2 + (y-60)**2) ** 0.5
            d2 = ((x-176)**2 + (y-60)**2) ** 0.5
            p = max(0, 60 - d1//3) + max(0, 60 - d2//3)
            d.point((x, y), fill=(50+p//3, 20+p//4, 70+p//2))
    draw_shirt(d, cx, cy+55, SHIRT_BLACK, None, collar=False)
    draw_head_base(d, cx, cy, 52, 60)
    draw_hair_short(d, cx, cy-5, 54, 38)
    draw_eyebrows(d, cx, cy, brow_y=-14, style="normal")
    draw_eyes(d, cx, cy-2, "normal", "center")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "open")
    return upscale(img)


# ========== 版本5：Q版/可爱风 ==========
def v5_chibi():
    img = Image.new("RGB", (PW, PH), (240, 230, 200))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2
    # 可爱渐变背景
    for y in range(PH):
        t = y / PH
        r = int(255 - t*15)
        g = int(235 - t*25)
        b = int(210 - t*30)
        for x in range(PW):
            d.point((x, y), fill=(r, g, b))
    # Q版大头
    head_s = 70
    draw_shirt(d, cx, cy+40, SHIRT_DARK, None, collar=False)
    # 大圆头
    ellipse(d, cx, cy-10, head_s, head_s-5, SKIN)
    # 腮红
    for i in range(10):
        d.point((cx-45+i, cy+10), fill=(240, 165, 150))
        d.point((cx+35+i, cy+10), fill=(240, 165, 150))
    # 短发
    ellipse(d, cx, cy-25, head_s-5, 40, HAIR_BLACK)
    fill(d, cx-head_s+5, cy-20, head_s*2-10, 20, HAIR_BLACK)
    # 大眼睛
    for ex in [cx-22, cx+22]:
        fill(d, ex-10, cy-10, 18, 16, EYE_WHITE)
        fill(d, ex-6, cy-8, 12, 12, EYE_BROWN)
        fill(d, ex-4, cy-7, 8, 10, EYE_DARK)
        d.point((ex-2, cy-6), fill=EYE_HL)
        d.point((ex-5, cy-9), fill=EYE_HL)
    # 眉毛
    fill(d, cx-32, cy-24, 18, 3, BROW)
    fill(d, cx+14, cy-24, 18, 3, BROW)
    # 小嘴
    fill(d, cx-5, cy+15, 10, 3, LIP)
    for dx in range(-3, 4):
        d.point((cx+dx, cy+18-abs(dx)), fill=LIP_SHADOW)
    return upscale(img)


# ========== 版本6：严肃思考版（深夜办公室） ==========
def v6_thinking():
    img = Image.new("RGB", (PW, PH), (10, 8, 20))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    # 暗色背景，台灯光
    for y in range(PH):
        for x in range(PW):
            d.point((x, y), fill=(12+y//8, 10+y//8, 25+y//6))
    # 台灯暖光
    for r in range(90):
        for a in range(0, 360, 5):
            rx = int(cx + r * math.cos(math.radians(a)))
            ry = int(cy+20 + r * 0.8 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 35 - r//3)
                cur = d.im.getpixel((rx, ry))
                d.point((rx, ry), fill=(min(255, cur[0]+b), min(255, cur[1]+b*2//3), cur[2]))
    draw_shirt(d, cx, cy+55, SHIRT_GRAY, None, collar=False)
    draw_head_base(d, cx, cy, 48, 56)
    draw_hair_short(d, cx, cy-5, 50, 36, "receding")
    draw_eyebrows(d, cx, cy, brow_y=-15, style="angry")
    draw_eyes(d, cx, cy-3, "serious", "down")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "serious")
    return upscale(img)


# ========== 版本7：胡茬沧桑版 ==========
def v7_bearded():
    img = Image.new("RGB", (PW, PH), (180, 160, 140))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_background(d, "neutral")
    draw_shirt(d, cx, cy+55, SHIRT_BLUE, None, collar=True)
    draw_head_base(d, cx, cy, 50, 58)
    # 胡茬
    for dy in range(20):
        for dx in range(-28, 29):
            if dx*dx/900 + (dy-10)*(dy-10)/100 < 1:
                if random.random() < 0.4:
                    d.point((cx+dx, cy+dy), fill=BEARD)
    draw_hair_short(d, cx, cy-5, 52, 36, "balding")
    draw_eyebrows(d, cx, cy, brow_y=-15, style="normal")
    draw_eyes(d, cx, cy-2, "determined", "center")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "determined")
    return upscale(img)


# ========== 版本8：温馨笑容版（家中） ==========
def v8_warm():
    img = Image.new("RGB", (PW, PH), (240, 200, 150))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    # 暖橙背景
    for y in range(PH):
        t = y / PH
        r = int(255 - t*20)
        g = int(210 - t*40)
        b = int(160 - t*50)
        for x in range(PW):
            d.point((x, y), fill=(r, g, b))
    # 居家毛衣
    draw_shirt(d, cx, cy+55, (80, 60, 90), None, collar=False)
    draw_head_base(d, cx, cy, 52, 60)
    draw_hair_short(d, cx, cy-5, 54, 38)
    draw_eyebrows(d, cx, cy, brow_y=-14, style="normal")
    draw_eyes(d, cx, cy-2, "smile", "center")
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, "smile")
    # 眼镜
    for ex in [cx-22, cx+22]:
        d.ellipse([ex-12, cy-8, ex+12, cy+6], outline=(60, 60, 75), width=2)
    line(d, cx-10, cy-1, cx+10, cy-1, (60, 60, 75))
    return upscale(img)


print("=== Generating Luocheng character portraits (8 versions) ===")
versions = [
    ("luocheng_01_classic_anime", v1_classic),
    ("luocheng_02_suit_stage", v2_suit),
    ("luocheng_03_young_dreams", v3_young),
    ("luocheng_04_livestream", v4_livestream),
    ("luocheng_05_chibi_cute", v5_chibi),
    ("luocheng_06_thinking_night", v6_thinking),
    ("luocheng_07_bearded_haggard", v7_bearded),
    ("luocheng_08_warm_home", v8_warm),
]
for name, func in versions:
    img = func()
    save(img, name)

# Also generate the game avatar version (128x128 for in-game use)
def game_avatar():
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 64, 55
    # 衬衫
    d.rounded_rectangle([cx-30, cy+20, cx+30, cy+60], radius=4, fill=SHIRT_BLACK)
    # 领口
    fill(d, cx-9, cy+18, 18, 10, COLLAR_WHITE)
    fill(d, cx-6, cy+22, 12, 8, SKIN_SHADOW)
    # 脖子
    fill(d, cx-7, cy+14, 14, 10, SKIN)
    # 脸
    ellipse(d, cx, cy, 28, 32, SKIN)
    # 头发
    ellipse(d, cx, cy-8, 30, 22, HAIR_BLACK)
    fill(d, cx-30, cy-14, 60, 15, HAIR_BLACK)
    for side in [-1, 1]:
        for dy in range(18):
            w = max(1, 5 - dy//3)
            for ddx in range(w):
                d.point((cx + side*(27+ddx), cy-2+dy), fill=HAIR_BLACK)
    # 眼睛
    for ex in [cx-13, cx+13]:
        fill(d, ex-4, cy-4, 8, 5, EYE_WHITE)
        fill(d, ex-2, cy-3, 4, 4, EYE_BROWN)
        fill(d, ex-1, cy-2, 2, 2, EYE_DARK)
        d.point((ex, cy-3), fill=EYE_HL)
    # 眉毛
    fill(d, cx-18, cy-9, 10, 2, BROW)
    fill(d, cx+8, cy-9, 10, 2, BROW)
    # 嘴
    for dx in range(-6, 7):
        t = dx/6
        curve = int(t*t*2)
        d.point((cx+dx, cy+12-curve), fill=LIP)
    return img

avatar = game_avatar()
avatar.save(os.path.join(os.path.dirname(__file__), "assets", "characters", "luocheng.png"), "PNG")
avatar.save(os.path.join(OUT, "luocheng_00_game_avatar.png"), "PNG")
print(f"  Saved: luocheng_00_game_avatar.png ((128, 128))")

print("\n=== All portraits generated! ===")
print(f"Directory: {OUT}")
