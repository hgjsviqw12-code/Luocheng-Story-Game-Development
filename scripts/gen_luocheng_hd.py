from PIL import Image, ImageDraw
import os
import math
import random

random.seed(888)

OUT = os.path.join(os.path.dirname(__file__), "character_previews")
os.makedirs(OUT, exist_ok=True)
CH_DIR = os.path.join(os.path.dirname(__file__), "assets", "characters")
os.makedirs(CH_DIR, exist_ok=True)

# 用更高分辨率的像素画布 (400x400 base, upscaled 2x = 800x800)
PW, PH = 200, 200
SCALE = 3
FW, FH = PW * SCALE, PH * SCALE


def upscale(img):
    return img.resize((FW, FH), Image.NEAREST)


def save(img, name, game_asset=False):
    out_dir = CH_DIR if game_asset else OUT
    path = os.path.join(out_dir, name + ".png")
    img.save(path, "PNG")
    print(f"  Saved: {name}.png ({img.size})")


def put(d, x, y, c):
    if 0 <= x < PW and 0 <= y < PH:
        d.point((x, y), fill=c)


def rect(d, x, y, w, h, c):
    for dy in range(h):
        for dx in range(w):
            put(d, x+dx, y+dy, c)


def ellip(d, cx, cy, rx, ry, c):
    for dy in range(-ry, ry+1):
        for dx in range(-rx, rx+1):
            if dx*dx*ry*ry + dy*dy*rx*rx <= rx*rx*ry*ry:
                put(d, cx+dx, cy+dy, c)


def line(d, x1, y1, x2, y2, c, w=1):
    d.line([(x1, y1), (x2, y2)], fill=c, width=w)


# ========== 高还原度颜色 (罗永浩特征色) ==========
SKIN = (232, 198, 172)
SKIN_S1 = (218, 178, 150)
SKIN_S2 = (200, 158, 130)
SKIN_HL = (245, 218, 198)
CHEEK = (235, 165, 150)
HAIR = (22, 18, 16)
HAIR_HL = (45, 38, 32)
HAIR_SIDE = (30, 25, 20)
BEARD = (48, 38, 30)
BEARD_LIGHT = (70, 55, 42)
EYE_W = (248, 245, 240)
EYE_PUPIL = (25, 20, 28)
EYE_IRIS = (55, 38, 28)
EYE_BROW = (28, 22, 18)
EYE_LASH = (30, 25, 22)
LIP = (185, 95, 95)
LIP_S = (155, 70, 72)
LIP_HL = (200, 120, 115)
NOSE_C = (212, 170, 142)
NOSE_S = (195, 150, 125)
SHADOW = (180, 145, 120, 128)
WHITE = (245, 245, 250)
BLACK = (15, 12, 18)

# 衣服颜色
SHIRT_BLACK = (28, 26, 32)
SHIRT_BLUE = (42, 58, 95)
SHIRT_GRAY = (75, 72, 82)
SWEATER_PURPLE = (85, 55, 100)
SWEATER_GREEN = (50, 80, 60)
SUIT = (22, 25, 35)
TIE_RED = (155, 30, 35)
COLLAR = (240, 238, 242)


def draw_face(d, cx, cy, face_rx=42, face_ry=48, age="mid"):
    """绘制圆脸（罗永浩标志性圆脸）"""
    # 脖子
    rect(d, cx-14, cy+face_ry-8, 28, 25, SKIN_S1)
    rect(d, cx-12, cy+face_ry-5, 24, 15, SKIN)

    # 脸部主色（圆脸，下半部分更宽）
    for dy in range(-face_ry, face_ry+1):
        for dx in range(-face_rx-2, face_rx+3):
            # 圆脸公式：下方比标准椭圆宽
            t = dy / face_ry
            w_factor = 1.0
            if t > 0.3:
                w_factor = 1.0 + (t - 0.3) * 0.25
            rx_eff = int(face_rx * w_factor)
            if dx*dx*(face_ry*face_ry) + dy*dy*(face_rx*face_rx) <= (face_rx*face_rx)*(face_ry*face_ry):
                put(d, cx+dx, cy+dy, SKIN)

    # 下颌阴影（中年微胖双下巴效果）
    for dx in range(-face_rx+5, face_rx-4):
        for dy_off in range(6):
            t = abs(dx) / face_rx
            if t < 0.7:
                y = cy + face_ry - 2 + dy_off
                darkness = max(0, (6 - dy_off) * 3 - int(t*15))
                put(d, cx+dx, y, (max(0, SKIN_S1[0]-darkness), max(0, SKIN_S1[1]-darkness), max(0, SKIN_S1[2]-darkness)))

    # 额头高光
    for dy in range(-face_ry+5, -face_ry+20):
        for dx in range(-20, 21):
            t = abs(dx) / 20
            if t < 0.8 and random.random() < 0.5:
                put(d, cx+dx, cy+dy, SKIN_HL)

    # 腮红
    for cheek_x in [cx-28, cx+28]:
        for dy in range(10, 25):
            for dx in range(-8, 9):
                dist = abs(math.sqrt(dx*dx + (dy-17)*(dy-17)*0.5))
                if dist < 7 and random.random() < 0.4:
                    put(d, cheek_x+dx, cy+dy, CHEEK)


def draw_eyes(d, cx, cy, ey_off=0, expr="normal", glasses=False):
    """绘制眼睛（标志性小眼睛，单眼皮）"""
    ey = cy + ey_off
    eye_dist = 22

    for side, ex in enumerate([cx - eye_dist, cx + eye_dist]):
        if expr == "smile" or expr == "happy":
            # 笑眼（弯成缝）
            for dx in range(-10, 11):
                t = dx / 10
                curve = int((1 - t*t) * 3)
                put(d, ex+dx, ey-curve, EYE_LASH)
                put(d, ex+dx, ey-curve+1, EYE_BROW)
                for w in range(-1, 2):
                    if abs(dx) < 7 - abs(w):
                        put(d, ex+dx+w, ey-curve+1, EYE_LASH)
        elif expr == "angry" or expr == "determined":
            # 眯眼/坚毅眼神
            rect(d, ex-8, ey-2, 16, 4, EYE_W)
            rect(d, ex-4, ey-1, 7, 3, EYE_IRIS)
            rect(d, ex-2, ey, 4, 2, EYE_PUPIL)
            put(d, ex+1, ey-1, (255, 255, 255))
            # 上眼线加粗
            for dx in range(-10, 11):
                put(d, ex+dx, ey-3, EYE_LASH)
                put(d, ex+dx, ey-4, EYE_BROW)
        elif expr == "tired":
            # 疲惫眼（黑眼圈）
            rect(d, ex-8, ey-1, 16, 5, EYE_W)
            rect(d, ex-4, ey, 6, 3, EYE_IRIS)
            rect(d, ex-2, ey+1, 3, 2, EYE_PUPIL)
            # 眼袋
            for dx in range(-9, 10):
                put(d, ex+dx, ey+5, SKIN_S2)
                put(d, ex+dx, ey+6, SKIN_S1)
        else:
            # 正常眼睛（小眼睛，单眼皮特征）
            rect(d, ex-8, ey-3, 16, 6, EYE_W)
            rect(d, ex-5, ey-2, 9, 5, EYE_IRIS)
            rect(d, ex-3, ey-1, 5, 3, EYE_PUPIL)
            # 高光
            put(d, ex, ey-2, (255, 255, 255))
            put(d, ex-3, ey-3, (255, 255, 255))
            # 上眼线（单眼皮）
            for dx in range(-10, 11):
                put(d, ex+dx, ey-4, EYE_LASH)
            # 下眼睑
            for dx in range(-7, 8):
                put(d, ex+dx, ey+4, SKIN_S1)

    if glasses:
        # 黑框眼镜
        for gx in [cx - eye_dist, cx + eye_dist]:
            for dx in range(-13, 14):
                for dy in range(-8, 9):
                    if abs(dx) == 13 or abs(dy) == 8:
                        if abs(dx)*8*8 + abs(dy)*13*13 <= 13*13*8*8:
                            put(d, gx+dx, ey+dy, (30, 30, 35))
            # 镜片反光
            for dx in range(-8, -3):
                put(d, gx+dx, ey-4, (200, 220, 240, 80))
        # 鼻梁架
        for dx in range(-3, 4):
            put(d, cx+dx, ey+1, (30, 30, 35))
        # 镜腿
        for dx in range(8, 15):
            put(d, cx-eye_dist-13-dx, ey-2, (30, 30, 35))
            put(d, cx+eye_dist+12+dx, ey-2, (30, 30, 35))


def draw_eyebrows(d, cx, cy, by_off=0, style="normal"):
    """绘制眉毛（浓眉特征）"""
    by = cy + by_off
    bd = 22

    for bx in [cx - bd, cx + bd]:
        if style == "angry":
            for dx in range(-10, 11):
                t = dx / 10
                h = -int(3 * (1 - abs(t)))
                if dx < 0:
                    h -= 2
                for w in range(2):
                    put(d, bx+dx, by+h+w, EYE_BROW)
        elif style == "sad":
            for dx in range(-10, 11):
                t = dx / 10
                h = int(3 * abs(t))
                for w in range(2):
                    put(d, bx+dx, by+h+w, EYE_BROW)
        elif style == "raised":
            for dx in range(-10, 11):
                t = dx / 10
                h = -int(2 * (1 - abs(t)))
                for w in range(2):
                    put(d, bx+dx, by+h+w, EYE_BROW)
        else:
            for dx in range(-10, 11):
                for w in range(3):
                    put(d, bx+dx, by+w, EYE_BROW)
                # 眉毛粗细变化（中间粗两头细）
                if abs(dx) < 6:
                    put(d, bx+dx, by-1, EYE_BROW)


def draw_nose(d, cx, cy):
    """绘制鼻子（蒜头鼻特征）"""
    ny = cy + 12
    # 鼻梁
    for dy in range(-12, 2):
        t = abs(dy) / 12
        w = max(1, int(1.5 + t))
        for dx in range(w):
            put(d, cx+dx-w//2, ny+dy, NOSE_C)
    # 鼻头（圆润蒜头鼻）
    ellip(d, cx, ny+3, 6, 5, SKIN)
    for dx in range(-5, 6):
        put(d, cx+dx, ny+6, NOSE_S)
    # 鼻翼
    put(d, cx-7, ny+2, NOSE_S)
    put(d, cx-6, ny+3, NOSE_S)
    put(d, cx+6, ny+2, NOSE_S)
    put(d, cx+5, ny+3, NOSE_S)
    # 鼻孔
    put(d, cx-3, ny+5, (120, 80, 70))
    put(d, cx+2, ny+5, (120, 80, 70))


def draw_mouth(d, cx, cy, my_off=0, style="smile"):
    """绘制嘴巴"""
    my = cy + my_off + 22
    if style == "smile":
        for dx in range(-14, 15):
            t = dx / 14
            curve = int(t*t * 5)
            for w in range(3):
                put(d, cx+dx, my-curve+w, LIP)
            put(d, cx+dx, my-curve-1, LIP_S)
        # 上唇M形
        for dx in range(-10, 11):
            t = dx / 10
            cupid = int(2 * (1 - abs(t)) * (t*t - 0.3) * -3)
            put(d, cx+dx, my-5-cupid, LIP_S)
        # 下唇
        for dx in range(-10, 11):
            t = abs(dx) / 10
            curve = int((1-t) * 4)
            put(d, cx+dx, my+1+curve, LIP_S)
        # 嘴唇高光
        for dx in range(-5, 6):
            put(d, cx+dx, my-2, LIP_HL)
    elif style == "open_speak":
        # 张嘴说话
        rect(d, cx-8, my-2, 16, 8, (80, 40, 50))
        rect(d, cx-6, my-1, 12, 3, (220, 140, 130))  # 舌头
        for dx in range(-10, 11):
            put(d, cx+dx, my-3, LIP)
            put(d, cx+dx, my+7, LIP_S)
    elif style == "determined":
        # 紧抿嘴唇
        rect(d, cx-10, my, 20, 3, LIP)
        rect(d, cx-8, my+3, 16, 2, LIP_S)
        for dx in range(-9, 10):
            put(d, cx+dx, my-1, LIP_S)
    elif style == "smirk":
        # 歪嘴笑（老罗经典表情）
        for dx in range(-10, 12):
            t = dx / 10
            curve = int(t*t * 3) + max(0, int(dx/4))
            for w in range(2):
                put(d, cx+dx, my-curve+w, LIP)
        for dx in range(-8, 5):
            put(d, cx+dx, my+2, LIP_S)
    else:
        # 平常嘴
        rect(d, cx-9, my, 18, 2, LIP)
        rect(d, cx-7, my+2, 14, 2, LIP_S)


def draw_hair(d, cx, cy, style="normal", balding=False):
    """绘制头发（短发，略高发际线）"""
    hrx = 45
    hry = 35
    top_y = cy - hry + 3

    # 头顶头发
    for dy in range(hry + 5):
        t = dy / hry
        if balding and dy < 18:
            w = max(0, int(hrx * math.sin(t * math.pi * 0.6)) - 12 + dy//2)
        else:
            w = int(hrx * math.sin(t * math.pi * 0.6))
        for dx in range(-w, w+1):
            y = top_y + dy
            put(d, cx+dx, y, HAIR)
            # 头发纹理
            if random.random() < 0.15 and dy > 5:
                put(d, cx+dx, y, HAIR_HL)

    # 两侧头发（鬓角）
    for side in [-1, 1]:
        for dy in range(0, 35):
            w = max(2, 10 - dy//3)
            for ddx in range(w):
                y = cy - 8 + dy
                sx = cx + side * (hrx - 5)
                put(d, sx + side*ddx, y, HAIR)

    # 前额发际线（M型发际线，中年特征）
    hairline_y = cy - 33
    if balding:
        hairline_y = cy - 28
    for dx in range(-28, 29):
        recession = 0
        if abs(dx) < 12:
            recession = abs(dx) // 3
        if balding:
            recession += 3
        put(d, cx+dx, hairline_y + recession, SKIN)
        for dy in range(recession):
            put(d, cx+dx, hairline_y + dy, SKIN)

    # 头发边缘阴影
    for dx in range(-42, 43):
        y = top_y + hry
        put(d, cx+dx, y, HAIR_SIDE)


def draw_beard_stubble(d, cx, cy, density=0.3):
    """绘制胡茬"""
    for dy in range(8, 25):
        for dx in range(-35, 36):
            dist = math.sqrt(dx*dx/1225 + (dy-15)*(dy-15)/100)
            if dist < 1 and random.random() < density:
                shade = random.choice([BEARD, BEARD_LIGHT, BEARD_LIGHT])
                put(d, cx+dx, cy+dy, shade)


def draw_clothes(d, cx, shoulder_y, style="shirt_black", tie=None):
    """绘制衣服"""
    if style == "shirt_black":
        # 黑色T恤/衬衫
        rect(d, cx-55, shoulder_y, 110, 90, SHIRT_BLACK)
        # 领口
        rect(d, cx-15, shoulder_y-5, 30, 18, SKIN)
        rect(d, cx-12, shoulder_y-8, 24, 8, SHIRT_BLACK)
        # 肩膀阴影
        for dy in range(5):
            for dx in range(-55+dy, -35):
                put(d, cx+dx, shoulder_y+dy, (20, 18, 24))
            for dx in range(35, 55-dy):
                put(d, cx+dx, shoulder_y+dy, (20, 18, 24))
    elif style == "suit_red_tie":
        # 深色西装+红领带（发布会造型）
        rect(d, cx-60, shoulder_y, 120, 90, SUIT)
        # 白衬衫
        rect(d, cx-18, shoulder_y-5, 36, 35, COLLAR)
        rect(d, cx-10, shoulder_y, 20, 20, SKIN)
        # 红领带
        rect(d, cx-5, shoulder_y+5, 10, 45, TIE_RED)
        rect(d, cx-7, shoulder_y+2, 14, 10, TIE_RED)
        for dx in range(-4, 5):
            put(d, cx+dx, shoulder_y+15+abs(dx), TIE_RED)
        # 西装翻领
        for dy in range(30):
            t = dy / 30
            lw = int(8 + t * 12)
            for dx in range(lw):
                put(d, cx-15-t*10-dx, shoulder_y+5+dy, (18, 20, 28))
                put(d, cx+15+t*10+dx, shoulder_y+5+dy, (18, 20, 28))
        # 领带夹
        rect(d, cx-6, shoulder_y+25, 12, 2, (180, 160, 100))
    elif style == "sweater_purple":
        # 紫色毛衣（居家）
        rect(d, cx-55, shoulder_y, 110, 90, SWEATER_PURPLE)
        # 圆领
        for r in range(12):
            for a in range(0, 360, 10):
                rx = int(cx + r * math.cos(math.radians(a)))
                ry = int(shoulder_y - 2 + r * 0.7 * math.sin(math.radians(a)))
                if a > 180:
                    put(d, rx, ry, SKIN)
        # 毛衣纹理
        for dy in range(0, 85, 4):
            for dx in range(-50, 50):
                if random.random() < 0.3:
                    put(d, cx+dx, shoulder_y+dy, (70, 45, 85))
    elif style == "tshirt_blue":
        # 蓝色T恤（北漂年轻时期）
        rect(d, cx-50, shoulder_y, 100, 85, SHIRT_BLUE)
        rect(d, cx-13, shoulder_y-5, 26, 15, SKIN)
        rect(d, cx-10, shoulder_y-8, 20, 6, SHIRT_BLUE)
    elif style == "tank_top":
        # 背心（直播/居家）
        rect(d, cx-50, shoulder_y, 100, 85, (40, 38, 45))
        rect(d, cx-15, shoulder_y-5, 30, 20, SKIN)
        rect(d, cx-35, shoulder_y, 20, 80, (35, 33, 40))
        rect(d, cx+15, shoulder_y, 20, 80, (35, 33, 40))


def draw_bg(d, style):
    """绘制背景"""
    if style == "warm_office":
        # 温暖办公室背景
        for y in range(PH):
            t = y / PH
            for x in range(PW):
                v = int(40 + (1-t)*20)
                d.point((x, y), fill=(v+20, v+15, v+5))
        # 台灯暖光
        for r in range(80):
            b = max(0, 40 - r//2)
            for a in range(0, 360, 8):
                rx = int(50 + r * math.cos(math.radians(a)))
                ry = int(80 + r * math.sin(math.radians(a)))
                put(d, rx, ry, (60+b, 50+b*3//4, 30+b//2))
    elif style == "stage_spotlight":
        # 发布会聚光灯
        for y in range(PH):
            for x in range(PW):
                d.point((x, y), fill=(10, 8, 20))
        cx_l, cy_l = PW//2, 0
        for r in range(130):
            spread = int(r * 0.5)
            b = max(0, int(60 - r//2))
            for dx in range(-spread, spread+1, 2):
                rx = cx_l + dx
                ry = r
                put(d, rx, ry, (b//3, b//4, b))
    elif style == "home_warm":
        # 温暖居家背景
        for y in range(PH):
            t = y / PH
            for x in range(PW):
                r = int(180 - t*40)
                g = int(140 - t*30)
                b = int(100 - t*20)
                d.point((x, y), fill=(r, g, b))
    elif style == "livestream":
        # 直播间紫粉背景
        for y in range(PH):
            for x in range(PW):
                d1 = math.sqrt((x-40)**2 + (y-50)**2)
                d2 = math.sqrt((x-160)**2 + (y-50)**2)
                p = int(max(0, 80 - d1) + max(0, 80 - d2))
                d.point((x, y), fill=(40+p//3, 15+p//4, 60+p//2))
    elif style == "night_office":
        # 深夜办公室蓝调
        for y in range(PH):
            t = y / PH
            for x in range(PW):
                d.point((x, y), fill=(int(10+t*15), int(12+t*15), int(30+t*20)))
        # 远处窗户光
        for wy in range(30, 100, 15):
            for wx in range(20, 180, 20):
                if random.random() < 0.5:
                    rect(d, wx, wy, 8, 10, (255, 220, 120))
    elif style == "neutral_gray":
        for y in range(PH):
            for x in range(PW):
                v = int(180 - y//3)
                d.point((x, y), fill=(v, v-5, v-10))
    elif style == "young_blue":
        for y in range(PH):
            t = y / PH
            for x in range(PW):
                d.point((x, y), fill=(int(30+t*20), int(50+t*20), int(90+t*30)))


# ========== 6个版本的罗诚 ==========

def portrait_v1_classic():
    """版本1：经典中年 - 黑色衬衫，温和微笑，无眼镜"""
    img = Image.new("RGB", (PW, PH), (180, 160, 140))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_bg(d, "warm_office")
    draw_clothes(d, cx, cy+52, "shirt_black")
    draw_face(d, cx, cy, 42, 48)
    draw_hair(d, cx, cy, "normal", balding=True)
    draw_beard_stubble(d, cx, cy, 0.25)
    draw_eyebrows(d, cx, cy, -20, "normal")
    draw_eyes(d, cx, cy, -5, "normal", glasses=False)
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, 0, "smile")
    return upscale(img)


def portrait_v2_speech():
    """版本2：发布会演讲 - 西装红领带，坚毅表情"""
    img = Image.new("RGB", (PW, PH), (10, 8, 20))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 15
    draw_bg(d, "stage_spotlight")
    draw_clothes(d, cx, cy+50, "suit_red_tie")
    draw_face(d, cx, cy, 40, 46)
    draw_hair(d, cx, cy-2, "normal", balding=True)
    draw_beard_stubble(d, cx, cy, 0.15)
    draw_eyebrows(d, cx, cy, -22, "angry")
    draw_eyes(d, cx, cy, -7, "determined", glasses=False)
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, -2, "determined")
    return upscale(img)


def portrait_v3_livestream():
    """版本3：直播带货 - 黑色T恤，张嘴说话，紫色补光"""
    img = Image.new("RGB", (PW, PH), (50, 20, 60))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_bg(d, "livestream")
    draw_clothes(d, cx, cy+52, "shirt_black")
    draw_face(d, cx, cy, 44, 50)
    draw_hair(d, cx, cy, "normal", balding=True)
    draw_beard_stubble(d, cx, cy, 0.35)
    draw_eyebrows(d, cx, cy, -19, "raised")
    draw_eyes(d, cx, cy, -4, "normal", glasses=False)
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, 0, "open_speak")
    return upscale(img)


def portrait_v4_home():
    """版本4：家中温馨 - 紫色毛衣，戴眼镜，温和笑容"""
    img = Image.new("RGB", (PW, PH), (160, 120, 80))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_bg(d, "home_warm")
    draw_clothes(d, cx, cy+52, "sweater_purple")
    draw_face(d, cx, cy, 43, 49)
    draw_hair(d, cx, cy, "normal", balding=True)
    draw_eyebrows(d, cx, cy, -20, "normal")
    draw_eyes(d, cx, cy, -5, "smile", glasses=True)
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, 0, "smile")
    return upscale(img)


def portrait_v5_young():
    """版本5：年轻北漂 - 蓝色T恤，精神饱满，头发浓密"""
    img = Image.new("RGB", (PW, PH), (30, 50, 90))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 8
    draw_bg(d, "young_blue")
    draw_clothes(d, cx, cy+50, "tshirt_blue")
    draw_face(d, cx, cy, 38, 44)
    draw_hair(d, cx, cy, "normal", balding=False)
    draw_eyebrows(d, cx, cy, -18, "normal")
    draw_eyes(d, cx, cy, -3, "normal", glasses=False)
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, 0, "smirk")
    return upscale(img)


def portrait_v6_night():
    """版本6：深夜加班 - 灰色衬衫，疲惫胡茬，黑眼圈"""
    img = Image.new("RGB", (PW, PH), (10, 12, 30))
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 10
    draw_bg(d, "night_office")
    draw_clothes(d, cx, cy+52, "tank_top")
    draw_face(d, cx, cy, 42, 48)
    draw_hair(d, cx, cy, "normal", balding=True)
    draw_beard_stubble(d, cx, cy, 0.5)
    draw_eyebrows(d, cx, cy, -20, "sad")
    draw_eyes(d, cx, cy, -5, "tired", glasses=False)
    draw_nose(d, cx, cy)
    draw_mouth(d, cx, cy, 0, "determined")
    return upscale(img)


def game_avatar_final():
    """游戏内使用的128x128头像"""
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 64, 52
    # 衬衫
    d.rounded_rectangle([cx-35, cy+25, cx+35, cy+65], radius=4, fill=SHIRT_BLACK)
    # 领口
    rect(d, cx-13, cy+20, 26, 12, SKIN)
    rect(d, cx-10, cy+18, 20, 6, SHIRT_BLACK)
    # 脖子
    rect(d, cx-10, cy+18, 20, 12, SKIN_S1)
    # 圆脸
    ellip(d, cx, cy, 30, 35, SKIN)
    # 短发
    ellip(d, cx, cy-8, 32, 22, HAIR)
    rect(d, cx-33, cy-14, 66, 18, HAIR)
    for side in [-1, 1]:
        for dy in range(20):
            w = max(1, 6 - dy//3)
            for ddx in range(w):
                put_pixel = True
                if 0 <= cx + side*(29+ddx) < 128 and 0 <= cy-3+dy < 128:
                    d.point((cx + side*(29+ddx), cy-3+dy), fill=HAIR)
    # M发际线
    for dx in range(-18, 19):
        recession = abs(dx)//3 if abs(dx) < 8 else 0
        if 0 <= cx+dx < 128:
            d.point((cx+dx, cy-25+recession), fill=SKIN)
    # 小眼睛
    for ex in [cx-15, cx+15]:
        rect(d, ex-6, cy-4, 12, 5, EYE_W)
        rect(d, ex-3, cy-3, 5, 4, EYE_IRIS)
        rect(d, ex-1, cy-2, 3, 2, EYE_PUPIL)
        d.point((ex+1, cy-3), fill=(255, 255, 255))
    # 浓眉
    for bx in [cx-15, cx+15]:
        for dx in range(-8, 9):
            d.point((bx+dx, cy-10), fill=EYE_BROW)
    # 嘴（微笑）
    for dx in range(-8, 9):
        t = dx/8
        curve = int(t*t*3)
        d.point((cx+dx, cy+14-curve), fill=LIP)
    return img


# ========== 生成所有版本 ==========
print("=== Generating high-detail pixel-anime Luocheng portraits ===")
versions = [
    ("罗诚_01_经典中年_黑衬衫微笑", portrait_v1_classic, False),
    ("罗诚_02_发布会演讲_西装领带", portrait_v2_speech, False),
    ("罗诚_03_直播带货_张嘴说话", portrait_v3_livestream, False),
    ("罗诚_04_家中温馨_紫毛衣眼镜", portrait_v4_home, False),
    ("罗诚_05_年轻北漂_蓝T恤精神", portrait_v5_young, False),
    ("罗诚_06_深夜加班_疲惫胡茬", portrait_v6_night, False),
]
for name, func, is_game in versions:
    img = func()
    save(img, name, is_game)

# 游戏头像
avatar = game_avatar_final()
avatar.save(os.path.join(CH_DIR, "luocheng.png"), "PNG")
avatar.save(os.path.join(OUT, "罗诚_00_游戏内头像.png"), "PNG")
print(f"  Saved: 罗诚_00_游戏内头像.png ((128, 128))")

# 额外生成几张特殊表情的游戏用头像
def make_avatar_variant(shirt_color, mouth_style, eyes_style, has_beard=False, bald=True):
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 64, 52
    d.rounded_rectangle([cx-35, cy+25, cx+35, cy+65], radius=4, fill=shirt_color)
    rect(d, cx-13, cy+20, 26, 12, SKIN)
    rect(d, cx-10, cy+18, 20, 6, shirt_color)
    rect(d, cx-10, cy+18, 20, 12, SKIN_S1)
    ellip(d, cx, cy, 30, 35, SKIN)
    ellip(d, cx, cy-8, 32, 22, HAIR)
    rect(d, cx-33, cy-14, 66, 18, HAIR)
    for dx in range(-18, 19):
        recession = abs(dx)//3 if abs(dx) < 8 else 0
        if bald:
            recession += 2
        d.point((cx+dx, cy-25+recession), fill=SKIN)
    for ex in [cx-15, cx+15]:
        rect(d, ex-6, cy-4, 12, 5, EYE_W)
        rect(d, ex-3, cy-3, 5, 4, EYE_IRIS)
        rect(d, ex-1, cy-2, 3, 2, EYE_PUPIL)
        d.point((ex+1, cy-3), fill=(255, 255, 255))
    for bx in [cx-15, cx+15]:
        for dx in range(-8, 9):
            d.point((bx+dx, cy-10), fill=EYE_BROW)
    if mouth_style == "smile":
        for dx in range(-8, 9):
            t = dx/8
            curve = int(t*t*3)
            d.point((cx+dx, cy+14-curve), fill=LIP)
    elif mouth_style == "serious":
        rect(d, cx-7, cy+13, 14, 2, LIP)
    elif mouth_style == "open":
        rect(d, cx-5, cy+11, 10, 6, (80, 40, 50))
    return img


# 年轻版
av_young = make_avatar_variant(SHIRT_BLUE, "smile", "normal", bald=False)
av_young.save(os.path.join(CH_DIR, "luocheng_young.png"), "PNG")
av_young.save(os.path.join(OUT, "罗诚_young_青年版.png"), "PNG")
print(f"  Saved: 罗诚_young_青年版.png ((128, 128))")

# 胡茬中年版
av_beard = make_avatar_variant(SHIRT_BLACK, "serious", "normal", has_beard=True)
av_beard.save(os.path.join(CH_DIR, "luocheng_mid.png"), "PNG")
av_beard.save(os.path.join(OUT, "罗诚_mid_沧桑中年版.png"), "PNG")
print(f"  Saved: 罗诚_mid_沧桑中年版.png ((128, 128))")

print(f"\n=== 全部{len(versions)+3}张图片生成完成！===")
print(f"预览目录: {OUT}")
print(f"游戏资源目录: {CH_DIR}")
