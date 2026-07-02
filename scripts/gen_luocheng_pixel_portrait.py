from PIL import Image, ImageDraw
import os
import math
import random

random.seed(999)

OUT = os.path.join(os.path.dirname(__file__), "character_previews")
os.makedirs(OUT, exist_ok=True)
CH_DIR = os.path.join(os.path.dirname(__file__), "assets", "characters")

# 高分辨率像素画布 - 96x96基础，放大6倍=576x576
PW, PH = 96, 96
SCALE = 6
FW, FH = PW * SCALE, PH * SCALE

BG_COLOR = (225, 225, 228)
BORDER_COLOR = (10, 8, 12)

# ========== 肤色层次（暖色调，仿乔布斯像素肖像风格） ==========
SKIN_L0 = (255, 235, 210)   # 最亮高光
SKIN_L1 = (250, 215, 185)   # 高光
SKIN_L2 = (240, 195, 160)   # 主肤色亮
SKIN_L3 = (225, 175, 138)   # 主肤色
SKIN_L4 = (205, 150, 115)   # 肤色阴影1
SKIN_L5 = (180, 120, 88)    # 肤色阴影2
SKIN_L6 = (150, 90, 62)     # 深色阴影
SKIN_L7 = (120, 65, 45)     # 最深阴影
CHEEK = (220, 130, 110)     # 腮红

# 头发颜色（黑发）
HAIR_L0 = (70, 55, 45)
HAIR_L1 = (50, 38, 30)
HAIR_L2 = (32, 24, 20)
HAIR_L3 = (18, 13, 10)

# 胡须（灰黑胡茬）
BEARD_L0 = (100, 80, 65)
BEARD_L1 = (75, 58, 45)
BEARD_L2 = (50, 38, 30)
BEARD_L3 = (30, 22, 18)
BEARD_GRAY = (160, 145, 130)  # 灰白胡须

# 衣服颜色
SHIRT_BLACK_L0 = (50, 48, 55)
SHIRT_BLACK_L1 = (32, 30, 38)
SHIRT_BLACK_L2 = (18, 16, 22)
SHIRT_BLACK_L3 = (8, 6, 12)

COLLAR_SHADOW = (160, 120, 90)

# 眼睛
EYE_WHITE = (250, 245, 238)
EYE_IRIS = (50, 35, 25)
EYE_PUPIL = (20, 15, 12)
EYE_HL = (255, 255, 255)
EYE_BROW = (28, 20, 15)

# 嘴唇
LIP_L0 = (195, 115, 105)
LIP_L1 = (170, 85, 78)
LIP_L2 = (140, 60, 55)

# 眼镜
GLASS_FRAME = (180, 175, 175)
GLASS_LENS = (200, 210, 220, 40)

# 鼻子高光
NOSE_HL = (255, 240, 220)


def upscale(img):
    return img.resize((FW, FH), Image.NEAREST)


def save(img, name, game_dir=False):
    target = CH_DIR if game_dir else OUT
    path = os.path.join(target, name + ".png")
    img.save(path, "PNG")
    print(f"  Saved: {name}.png ({img.size})")


def put(d, x, y, c):
    if 0 <= x < PW and 0 <= y < PH:
        d.point((x, y), fill=c)


def rect(d, x, y, w, h, c):
    for dy in range(h):
        for dx in range(w):
            put(d, x+dx, y+dy, c)


def fill_ellip(d, cx, cy, rx, ry, c):
    for dy in range(-ry, ry+1):
        for dx in range(-rx, rx+1):
            if dx*dx*ry*ry + dy*dy*rx*rx <= rx*rx*ry*ry+ry*ry:
                put(d, cx+dx, cy+dy, c)


def draw_border(d):
    for i in range(3):
        rect(d, i, i, PW-2*i, PH-2*i, BORDER_COLOR)
    # 内部留1像素黑边
    rect(d, 3, 3, PW-6, PH-6, BG_COLOR)


def draw_skin_base(d, cx, cy, rx=28, ry=33):
    """绘制脸部底色 - 圆脸，暖色调"""
    # 主肤色填充
    for dy in range(-ry-2, ry+3):
        for dx in range(-rx-3, rx+4):
            t_y = dy / ry
            # 圆脸：下半部加宽
            w_factor = 1.0
            if t_y > 0.2:
                w_factor = 1.0 + (t_y - 0.2) * 0.22
            rx_eff = rx * w_factor
            if dx*dx/(rx_eff*rx_eff) + dy*dy/(ry*ry) <= 1.0:
                # 基础肤色：顶部亮，底部/侧面深
                if t_y < -0.5:
                    c = SKIN_L1
                elif t_y < -0.2:
                    c = SKIN_L2
                elif t_y < 0.2:
                    c = SKIN_L3
                elif t_y < 0.5:
                    c = SKIN_L4
                else:
                    c = SKIN_L5
                # 左侧（光源侧）更亮
                if dx < -rx_eff*0.3:
                    c = SKIN_L3 if c == SKIN_L4 else c
                    if t_y < 0:
                        c = SKIN_L2 if c == SKIN_L3 else c
                # 右侧阴影
                if dx > rx_eff*0.5:
                    c = SKIN_L5 if c == SKIN_L4 else c
                    c = SKIN_L6 if c == SKIN_L5 else c
                put(d, cx+dx, cy+dy, c)


def draw_face_shading(d, cx, cy):
    """面部精细阴影"""
    # 额头高光
    for dy in range(-28, -15):
        for dx in range(-15, 16):
            dist = math.sqrt(dx*dx/225 + (dy+22)*(dy+22)/50)
            if dist < 1:
                put(d, cx+dx, cy+dy, SKIN_L0)
    # 左脸颊高光
    for dy in range(-5, 10):
        for dx in range(-20, -8):
            dist = math.sqrt((dx+14)*(dx+14)/40 + (dy-3)*(dy-3)/80)
            if dist < 1 and random.random() < 0.6:
                put(d, cx+dx, cy+dy, SKIN_L1)
    # 鼻梁高光
    for dy in range(-8, 8):
        w = max(1, 2 - abs(dy)//5)
        for dx in range(w):
            put(d, cx-1+dx, cy+dy, NOSE_HL if abs(dy) < 4 else SKIN_L1)
    # 鼻头
    fill_ellip(d, cx, cy+10, 5, 4, SKIN_L4)
    fill_ellip(d, cx-3, cy+10, 3, 3, SKIN_L3)
    fill_ellip(d, cx+3, cy+10, 3, 3, SKIN_L3)
    # 鼻翼阴影
    put(d, cx-5, cy+9, SKIN_L5)
    put(d, cx+5, cy+9, SKIN_L5)
    put(d, cx-5, cy+11, SKIN_L6)
    put(d, cx+5, cy+11, SKIN_L6)
    # 鼻孔
    put(d, cx-2, cy+12, SKIN_L7)
    put(d, cx+2, cy+12, SKIN_L7)
    # 鼻底阴影
    for dx in range(-4, 5):
        put(d, cx+dx, cy+13, SKIN_L6)
    # 颧骨阴影（右侧）
    for dy in range(0, 12):
        for dx in range(15, 26):
            dist = math.sqrt((dx-20)*(dx-20)/30 + (dy-5)*(dy-5)/50)
            if dist < 1:
                put(d, cx+dx, cy+dy, SKIN_L5)
    # 下颌阴影
    for dx in range(-24, 25):
        t = abs(dx)/24
        for dy in range(3):
            y = cy+28-dy+int(t*2)
            darkness = min(2, max(0, 2-dy))
            c = [SKIN_L5, SKIN_L6, SKIN_L7][darkness]
            put(d, cx+dx, y, c)
    # 左脸边缘
    for dy in range(-15, 25):
        t = abs(dy)/30
        x = cx-27+int(t*2)
        for dx2 in range(2):
            put(d, x-dx2, cy+dy, SKIN_L5 if abs(dy) < 15 else SKIN_L6)
    # 右脸阴影边缘
    for dy in range(-20, 28):
        t = abs(dy)/30
        x = cx+26-int(t*2)
        for dx2 in range(3):
            put(d, x+dx2, cy+dy, SKIN_L6 if dy > 5 else SKIN_L5)
    # 太阳穴阴影
    for dy in range(-22, -10):
        for dx in [-22, -21, 21, 22]:
            put(d, cx+dx, cy+dy, SKIN_L5)
    # 腮红
    for cx2 in [cx-16, cx+16]:
        for dy in range(2, 10):
            for dx in range(-6, 7):
                dist = math.sqrt(dx*dx/40 + (dy-6)*(dy-6)/25)
                if dist < 0.8 and random.random() < 0.4:
                    put(d, cx2+dx, cy+dy, CHEEK)


def draw_eyes(d, cx, cy, ey=0, glasses=False):
    """绘制眼睛 - 小眼睛，单眼皮"""
    eye_d = 13  # 两眼间距
    ey = cy + ey

    for side, ex in enumerate([cx - eye_d, cx + eye_d]):
        # 眼窝阴影
        for dy in range(-3, 5):
            for dx in range(-8, 9):
                dist = math.sqrt(dx*dx/70 + dy*dy/20)
                if dist < 1:
                    put(d, ex+dx, ey+dy, SKIN_L4 if dy < 2 else SKIN_L5)
        # 眼白
        rect(d, ex-5, ey-2, 10, 4, EYE_WHITE)
        # 上眼睑（单眼皮，较厚）
        for dx in range(-7, 8):
            put(d, ex+dx, ey-3, EYE_BROW)
            put(d, ex+dx, ey-4, EYE_BROW)
            if abs(dx) < 5:
                put(d, ex+dx, ey-5, (45, 35, 28))
        # 下眼睑
        for dx in range(-5, 6):
            put(d, ex+dx, ey+3, SKIN_L5)
        # 虹膜
        fill_ellip(d, ex+1 if side else ex-1, ey, 4, 3, EYE_IRIS)
        # 瞳孔
        fill_ellip(d, ex+1 if side else ex-1, ey, 2, 2, EYE_PUPIL)
        # 高光
        put(d, ex-1 if side else ex+1, ey-1, EYE_HL)
        put(d, ex+1, ey-2, EYE_HL)
        # 眼角阴影
        put(d, ex-6, ey+1, SKIN_L6)
        put(d, ex+6, ey+1, SKIN_L6)

    if glasses:
        draw_glasses(d, cx, ey-1)


def draw_glasses(d, cx, ey):
    """绘制圆框眼镜"""
    eye_d = 13
    for gx in [cx - eye_d, cx + eye_d]:
        # 圆框
        r = 9
        for a_step in range(0, 360, 3):
            a = math.radians(a_step)
            for w in range(2):
                rx = int(gx + (r+w-1) * math.cos(a))
                ry = int(ey + (r+w-1) * 0.85 * math.sin(a))
                put(d, rx, ry, GLASS_FRAME)
        # 镜片内阴影/反光
        for dy in range(-7, 8):
            for dx in range(-8, 9):
                if dx*dx/64 + dy*dy/50 < 0.7:
                    if dx < -3 and dy < -2 and random.random() < 0.3:
                        put(d, gx+dx, ey+dy, (230, 240, 250))
    # 鼻梁架
    for dx in range(-3, 4):
        put(d, cx+dx, ey+2, GLASS_FRAME)
    # 镜腿
    for dx in range(6, 15):
        put(d, cx-eye_d-9-dx//2, ey-3, GLASS_FRAME)
        put(d, cx+eye_d+8+dx//2, ey-3, GLASS_FRAME)


def draw_eyebrows(d, cx, cy, by=-10, style="normal"):
    """绘制浓眉"""
    bd = 13
    for bx in [cx - bd, cx + bd]:
        if style == "angry":
            for dx in range(-9, 10):
                t = dx/9
                h = -int(2*(1-abs(t)))
                if dx < 0:
                    h -= 2
                for w in range(3):
                    put(d, bx+dx, cy+by+h+w, EYE_BROW)
        else:
            for dx in range(-8, 9):
                for w in range(3):
                    put(d, bx+dx, cy+by+w, EYE_BROW)
                if abs(dx) < 5:
                    put(d, bx+dx, cy+by-1, (45, 32, 25))


def draw_mouth(d, cx, cy, my=24, style="neutral"):
    """绘制嘴巴"""
    my = cy + my
    if style == "smile":
        # 微笑
        for dx in range(-11, 12):
            t = dx/11
            curve = int(t*t*3)
            for w in range(3):
                put(d, cx+dx, my-curve+w, LIP_L1)
            put(d, cx+dx, my-curve-1, LIP_L2)
        # 人中
        for dy in range(-10, -2):
            put(d, cx-1, cy+dy, SKIN_L5)
            put(d, cx, cy+dy, SKIN_L4)
            put(d, cx+1, cy+dy, SKIN_L5)
        # 下唇
        for dx in range(-8, 9):
            t = abs(dx)/8
            curve = int((1-t)*3)
            put(d, cx+dx, my+1+curve, LIP_L2)
            put(d, cx+dx, my+2+curve, SKIN_L6)
        # 上唇M形
        for dx in range(-7, 8):
            t = dx/7
            cupid = int(2*(1-abs(t))*(t*t-0.2)*-2)
            put(d, cx+dx, my-4-cupid, LIP_L2)
        # 唇高光
        for dx in range(-4, 5):
            put(d, cx+dx, my-1, LIP_L0)
    else:
        # 平静/严肃
        rect(d, cx-9, my, 18, 2, LIP_L1)
        rect(d, cx-7, my-1, 14, 1, LIP_L0)
        rect(d, cx-8, my+2, 16, 2, LIP_L2)
        # 人中
        for dy in range(-10, -2):
            put(d, cx-1, cy+dy, SKIN_L5)
            put(d, cx, cy+dy, SKIN_L4)
        # 下唇阴影
        for dx in range(-7, 8):
            put(d, cx+dx, my+4, SKIN_L6)
        # 下巴高光
        fill_ellip(d, cx, my+8, 6, 3, SKIN_L3)


def draw_hair(d, cx, cy, balding=True, gray=False):
    """绘制短发 - M型发际线"""
    top_y = cy - 33
    # 头顶头发
    for dy in range(38):
        t = dy / 38
        base_w = int(32 * math.sin(t * math.pi * 0.65))
        if balding and dy < 20:
            w = max(0, base_w - 14 + dy//2)
        else:
            w = base_w
        for dx in range(-w, w+1):
            y = top_y + dy
            # 头发颜色层次：顶部高光，侧面深
            if dy < 8:
                c = HAIR_L1 if not gray else (120, 105, 90)
            elif dy < 20:
                c = HAIR_L2
            else:
                c = HAIR_L3
            # 鬓角灰白
            if gray and dy > 20 and abs(dx) > w-8:
                c = (130, 115, 100)
            put(d, cx+dx, y, c)
            # 发丝纹理
            if random.random() < 0.1 and dy > 5:
                put(d, cx+dx, y, HAIR_L0 if not gray else (150, 135, 120))
    # 两侧鬓角
    for side in [-1, 1]:
        for dy in range(0, 30):
            w = max(1, 8 - dy//4)
            for ddx in range(w):
                y = cy - 10 + dy
                sx = cx + side * 30
                c = HAIR_L3
                if gray and dy > 15:
                    c = (140, 125, 110)
                put(d, sx + side*ddx, y, c)
    # M型发际线
    hl_y = cy - 28
    if balding:
        hl_y = cy - 24
    for dx in range(-25, 26):
        recession = 0
        if abs(dx) < 10:
            recession = abs(dx)//2
        if balding:
            recession += 2
        for dy2 in range(recession+1):
            put(d, cx+dx, hl_y+dy2, SKIN_L1 if dy2 == 0 else SKIN_L2)
    # 头发边缘
    for dx in range(-32, 33):
        put(d, cx+dx, top_y+35, HAIR_L3)


def draw_ears(d, cx, cy):
    """绘制耳朵"""
    for side in [-1, 1]:
        ex = cx + side*28
        # 耳朵外轮廓
        fill_ellip(d, ex, cy+2, 5, 8, SKIN_L4)
        # 耳朵内轮廓
        fill_ellip(d, ex, cy+2, 3, 5, SKIN_L3)
        # 耳垂
        fill_ellip(d, ex, cy+8, 3, 3, SKIN_L5)
        # 耳轮阴影
        put(d, ex, cy, SKIN_L5)
        put(d, ex-side, cy+2, SKIN_L5)
        # 耳朵高光
        put(d, ex+side, cy-2, SKIN_L2)


def draw_neck(d, cx, cy, shirt_y):
    """绘制脖子和领口"""
    neck_top = cy + 25
    neck_bot = shirt_y
    # 脖子
    rect(d, cx-10, neck_top, 20, neck_bot-neck_top, SKIN_L4)
    # 脖子阴影（右侧）
    rect(d, cx+3, neck_top, 7, neck_bot-neck_top, SKIN_L5)
    rect(d, cx+7, neck_top, 3, neck_bot-neck_top, SKIN_L6)
    # 脖子左侧高光
    rect(d, cx-10, neck_top, 3, neck_bot-neck_top, SKIN_L3)
    # 喉结
    fill_ellip(d, cx, neck_top+10, 4, 3, SKIN_L3)
    for dy in range(4):
        put(d, cx-1, neck_top+10+dy, SKIN_L5)
    # 锁骨区域阴影
    for dx in range(-14, 15):
        t = abs(dx)/14
        put(d, cx+dx, neck_bot-1, SKIN_L6 if t < 0.5 else SKIN_L5)


def draw_shirt(d, cx, cy, shoulder_y, style="black_turtleneck"):
    """绘制衣服 - 黑色高领/黑T恤"""
    if style == "black_turtleneck":
        # 高领衫（像乔布斯风格）
        rect(d, 0, shoulder_y-4, PW, PH-shoulder_y+4, SHIRT_BLACK_L2)
        # 肩膀
        for dy in range(20):
            t = dy/20
            for dx in range(-45+int(t*10), 46-int(t*10)):
                put(d, cx+dx, shoulder_y+dy, SHIRT_BLACK_L1)
        # 高领
        rect(d, cx-12, shoulder_y-4, 24, 10, SHIRT_BLACK_L1)
        rect(d, cx-10, shoulder_y-6, 20, 4, SHIRT_BLACK_L2)
        # 领口阴影
        for dx in range(-8, 9):
            t = abs(dx)/8
            put(d, cx+dx, shoulder_y+5-int(t*2), SHIRT_BLACK_L3)
        # 衣服褶皱/阴影
        for dy in range(10, 40):
            for dx in range(-20, 21):
                if abs(dx) > 15 and random.random() < 0.05:
                    put(d, cx+dx, shoulder_y+dy, SHIRT_BLACK_L3)
        # 左肩高光
        for dy in range(15):
            put(d, cx-40+dy, shoulder_y+dy, SHIRT_BLACK_L0)
    elif style == "black_shirt":
        # 普通黑衬衫
        rect(d, 0, shoulder_y, PW, PH-shoulder_y, SHIRT_BLACK_L2)
        for dy in range(25):
            t = dy/25
            for dx in range(-48+int(t*12), 49-int(t*12)):
                put(d, cx+dx, shoulder_y+dy, SHIRT_BLACK_L1)
        # 圆领
        for r in range(10):
            for a_step in range(0, 360, 5):
                a = math.radians(a_step)
                if a_step > 180:
                    rx = int(cx + r * math.cos(a))
                    ry = int(shoulder_y + r * 0.6 * math.sin(a))
                    put(d, rx, ry, SKIN_L4)
        # 领口边
        for r in range(11, 13):
            for a_step in range(180, 360, 5):
                a = math.radians(a_step)
                rx = int(cx + r * math.cos(a))
                ry = int(shoulder_y-2 + r * 0.6 * math.sin(a))
                put(d, rx, ry, SHIRT_BLACK_L2)


def draw_beard_stubble(d, cx, cy, density=0.4, gray=False):
    """绘制胡茬"""
    for dy in range(8, 28):
        for dx in range(-24, 25):
            dist = math.sqrt(dx*dx/600 + (dy-17)*(dy-17)/150)
            if dist < 1 and random.random() < density:
                c = random.choice([BEARD_L2, BEARD_L3, BEARD_L1])
                if gray and random.random() < 0.3 and dy > 15:
                    c = BEARD_GRAY
                put(d, cx+dx, cy+dy, c)


# ========== 生成各个版本 ==========

def make_portrait(version_name, glasses=False, beard=True, balding=True, gray_hair=False,
                  shirt="black_shirt", expression="neutral"):
    img = Image.new("RGB", (PW, PH), BG_COLOR)
    d = ImageDraw.Draw(img)
    cx, cy = PW//2, PH//2 - 4

    draw_border(d)
    draw_shirt(d, cx, cy, cy+30, shirt)
    draw_neck(d, cx, cy, cy+30)
    draw_ears(d, cx, cy)
    draw_skin_base(d, cx, cy)
    draw_hair(d, cx, cy, balding=balding, gray=gray_hair)
    draw_face_shading(d, cx, cy)
    if beard:
        draw_beard_stubble(d, cx, cy, density=0.35, gray=gray_hair)
    draw_eyebrows(d, cx, cy, -13, "normal")
    draw_eyes(d, cx, cy, -5, glasses=glasses)
    draw_mouth(d, cx, cy, 22, expression)

    return upscale(img)


# 版本1：经典中年 - 黑衬衫，不戴眼镜，胡茬，微笑
print("=== 生成乔布斯像素风罗诚肖像 ===")
v1 = make_portrait("v1", glasses=False, beard=True, balding=True, shirt="black_shirt", expression="smile")
save(v1, "罗诚_像素风_v1_经典微笑")

# 版本2：戴眼镜，黑高领（致敬参考图风格），严肃
v2 = make_portrait("v2", glasses=True, beard=True, balding=True, shirt="black_turtleneck", expression="neutral")
save(v2, "罗诚_像素风_v2_眼镜高领")

# 版本3：戴眼镜，微笑，黑衬衫
v3 = make_portrait("v3", glasses=True, beard=True, balding=True, shirt="black_shirt", expression="smile")
save(v3, "罗诚_像素风_v3_眼镜微笑")

# 版本4：无胡茬，年轻感
v4 = make_portrait("v4", glasses=False, beard=False, balding=False, shirt="black_shirt", expression="smile")
save(v4, "罗诚_像素风_v4_青年版")

# 版本5：灰白胡子，戴眼镜，沧桑感
v5 = make_portrait("v5", glasses=True, beard=True, balding=True, gray_hair=True,
                   shirt="black_turtleneck", expression="neutral")
save(v5, "罗诚_像素风_v5_沧桑版")

# 版本6：无眼镜，无胡茬，平静表情
v6 = make_portrait("v6", glasses=False, beard=False, balding=True, shirt="black_shirt", expression="neutral")
save(v6, "罗诚_像素风_v6_平静中年")

# 同时生成一个游戏内使用的128x128头像版本
def make_game_avatar(glasses=False, beard=True):
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 简化版，直接缩放v1
    return v1.resize((128, 128), Image.NEAREST)

avatar = make_game_avatar()
avatar.save(os.path.join(CH_DIR, "luocheng.png"), "PNG")
save(avatar, "罗诚_像素风_游戏头像", game_dir=True)

print("\n=== 全部像素风头像生成完成！===")
print(f"目录: {OUT}")
