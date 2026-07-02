from PIL import Image, ImageDraw, ImageFilter
import math
import random
import os

random.seed(42)

W, H = 1280, 720
SCALE = 4
PW, PH = W // SCALE, H // SCALE  # 320x180 pixel art resolution

OUT_BG = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
OUT_CH = os.path.join(os.path.dirname(__file__), "assets", "characters")
os.makedirs(OUT_BG, exist_ok=True)
os.makedirs(OUT_CH, exist_ok=True)


def make_image(draw_func):
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw, img)
    return img.resize((W, H), Image.NEAREST)


def save(img, filename):
    path = os.path.join(OUT_BG, filename)
    img.save(path, "PNG")
    print(f"  Saved: {filename} ({img.size})")


def save_char(img, filename):
    path = os.path.join(OUT_CH, filename)
    img.save(path, "PNG")
    print(f"  Saved: {filename} ({img.size})")


def gradient(draw, w, h, c1, c2, vertical=True):
    for i in range(h if vertical else w):
        r = i / (h if vertical else w)
        c = tuple(int(c1[j] * (1 - r) + c2[j] * r) for j in range(3))
        if vertical:
            draw.line([(0, i), (w, i)], fill=c)
        else:
            draw.line([(i, 0), (i, h)], fill=c)


def stars(draw, w, h, count=30, color=(255, 255, 200)):
    for _ in range(count):
        x, y = random.randint(0, w - 1), random.randint(0, h // 2)
        draw.point((x, y), fill=color)
        if random.random() < 0.3:
            draw.point((x + 1, y), fill=color)
            draw.point((x, y + 1), fill=color)


def windows_night(draw, x_start, y_start, cols, rows, w_size, h_size, gap, lit_color=(255, 220, 150), dark_color=(30, 40, 60)):
    for r in range(rows):
        for c in range(cols):
            x = x_start + c * (w_size + gap)
            y = y_start + r * (h_size + gap)
            is_lit = random.random() < 0.6
            color = lit_color if is_lit else dark_color
            draw.rectangle([x, y, x + w_size, y + h_size], fill=color)


def pixels_rect(draw, x, y, w, h, color):
    draw.rectangle([x, y, x + w, y + h], fill=color)


# ========== 背景图生成 ==========

def bg_classroom(draw, img):
    gradient(draw, PW, PH, (180, 160, 120), (140, 120, 90))
    # 黑板
    pixels_rect(draw, 30, 15, 260, 50, (40, 60, 40))
    pixels_rect(draw, 28, 13, 264, 54, (80, 60, 40))
    # 黑板上的粉笔字
    for i in range(5):
        for j in range(random.randint(3, 8)):
            px = 40 + j * 8
            py = 22 + i * 8
            if random.random() < 0.7:
                draw.point((px, py), fill=(200, 220, 200))
    # 课桌
    for row in range(4):
        for col in range(6):
            bx = 20 + col * 48
            by = 90 + row * 22
            pixels_rect(draw, bx, by, 35, 3, (100, 70, 40))
            pixels_rect(draw, bx + 2, by + 3, 3, 15, (80, 55, 30))
    # 荧光灯
    pixels_rect(draw, 80, 5, 160, 4, (255, 255, 240))
    pixels_rect(draw, 20, 5, 30, 4, (255, 255, 240))
    pixels_rect(draw, 260, 5, 40, 4, (255, 255, 240))


def bg_office_day(draw, img):
    gradient(draw, PW, PH, (180, 200, 220), (200, 215, 230))
    # 大窗户
    for i in range(4):
        wx = 20 + i * 75
        pixels_rect(draw, wx, 10, 60, 80, (180, 210, 240))
        pixels_rect(draw, wx + 28, 10, 2, 80, (150, 170, 190))
        pixels_rect(draw, wx, 48, 60, 2, (150, 170, 190))
    # 窗外建筑剪影
    for i in range(8):
        bx = 15 + i * 38
        bh = random.randint(20, 50)
        pixels_rect(draw, bx, 80 - bh, 30, bh, (150, 170, 190))
    # 办公桌
    for i in range(3):
        dx = 30 + i * 100
        pixels_rect(draw, dx, 110, 70, 30, (180, 150, 120))
        pixels_rect(draw, dx + 5, 100, 30, 12, (60, 60, 80))  # 显示器
        pixels_rect(draw, dx + 40, 115, 15, 8, (200, 200, 180))  # 文件
    # 地板
    pixels_rect(draw, 0, 140, PW, 40, (160, 140, 110))


def bg_office_night(draw, img):
    """这个已有好图，跳过生成，保留现有PNG"""
    gradient(draw, PW, PH, (15, 20, 40), (25, 30, 55))
    stars(draw, PW, PH, 20)
    # 城市夜景窗户
    for bx in range(0, PW, 15):
        bh = random.randint(30, 80)
        pixels_rect(draw, bx, PH - bh - 40, 12, bh, (30, 35, 50))
        for wy in range(0, bh, 8):
            for wx in range(2, 10, 5):
                if random.random() < 0.5:
                    draw.point((bx + wx, PH - bh - 40 + wy), fill=(255, 220, 120))
    # 办公桌台灯
    pixels_rect(draw, 200, 120, 60, 35, (40, 35, 50))
    pixels_rect(draw, 210, 100, 40, 22, (50, 45, 65))  # 电脑屏幕
    # 台灯光圈
    for r in range(30):
        alpha = max(0, 80 - r * 3)
        c = (255, 230, 150)
        for dx in range(-r, r + 1):
            if 0 <= 220 + dx < PW and 0 <= 115 - r // 2 < PH:
                draw.point((220 + dx, 115 - r // 2), fill=c)


def bg_office_dark(draw, img):
    gradient(draw, PW, PH, (8, 5, 15), (15, 10, 25))
    # 只有一盏灯亮
    pixels_rect(draw, 140, 100, 50, 4, (80, 60, 30))
    # 光圈
    for r in range(40):
        for a in range(0, 360, 10):
            rx = int(165 + r * math.cos(math.radians(a)))
            ry = int(130 + r * 0.6 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                brightness = max(0, 40 - r)
                draw.point((rx, ry), fill=(brightness + 10, brightness + 5, brightness // 2))
    # 剪影家具
    pixels_rect(draw, 50, 120, 80, 40, (15, 12, 25))
    pixels_rect(draw, 200, 130, 70, 30, (15, 12, 25))
    pixels_rect(draw, 0, 160, PW, 20, (10, 8, 18))


def bg_office_modern(draw, img):
    gradient(draw, PW, PH, (200, 210, 220), (180, 195, 210))
    # 玻璃墙
    for i in range(5):
        gx = 20 + i * 60
        pixels_rect(draw, gx, 10, 55, 100, (160, 200, 220, 80))
        pixels_rect(draw, gx, 10, 2, 100, (120, 150, 170))
    # 极简办公桌
    pixels_rect(draw, 60, 120, 200, 35, (220, 220, 225))
    pixels_rect(draw, 80, 100, 50, 22, (40, 40, 50))
    pixels_rect(draw, 180, 105, 40, 18, (40, 40, 50))
    # 绿植
    pixels_rect(draw, 240, 110, 15, 25, (60, 50, 30))
    pixels_rect(draw, 236, 95, 23, 20, (40, 120, 50))
    # 地板
    pixels_rect(draw, 0, 155, PW, 25, (190, 190, 200))


def bg_startup(draw, img):
    gradient(draw, PW, PH, (50, 55, 75), (70, 75, 95))
    # 白板
    pixels_rect(draw, 10, 8, 120, 50, (240, 240, 230))
    pixels_rect(draw, 8, 6, 124, 54, (180, 180, 170))
    # 白板上写"工匠"
    draw.text((25, 18), "craft", fill=(200, 50, 50))
    # 杂乱的桌子
    for i in range(5):
        dx = 140 + i * 35
        pixels_rect(draw, dx, 80 + random.randint(-5, 10), 28, 30, (90, 75, 60))
        pixels_rect(draw, dx + 3, 70 + random.randint(-3, 5), 18, 12, (50, 50, 70))
    # 披萨盒
    pixels_rect(draw, 150, 130, 25, 12, (200, 150, 50))
    pixels_rect(draw, 220, 125, 20, 15, (200, 150, 50))
    # 暖色灯光
    for r in range(50):
        for a in range(0, 360, 15):
            rx = int(160 + r * math.cos(math.radians(a)))
            ry = int(60 + r * 0.5 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 25 - r // 2)
                draw.point((rx, ry), fill=(40 + b, 35 + b, 50))
    # 地板
    pixels_rect(draw, 0, 150, PW, 30, (60, 55, 70))


def bg_factory(draw, img):
    gradient(draw, PW, PH, (80, 65, 50), (100, 80, 60))
    # 传送带
    for i in range(3):
        cy = 60 + i * 35
        pixels_rect(draw, 0, cy, PW, 12, (80, 80, 85))
        for j in range(0, PW, 20):
            pixels_rect(draw, j, cy + 4, 12, 4, (100, 100, 105))
        # 手机产品
        for j in range(0, PW, 50):
            pixels_rect(draw, j + 10, cy - 10, 12, 20, (50, 50, 60))
    # 荧光灯
    for i in range(6):
        lx = 20 + i * 52
        pixels_rect(draw, lx, 5, 35, 4, (255, 255, 230))
    # 地面
    pixels_rect(draw, 0, 155, PW, 25, (70, 58, 45))


def bg_venue(draw, img):
    gradient(draw, PW, PH, (20, 10, 30), (40, 20, 50))
    # 舞台聚光灯
    for angle in [-30, 0, 30]:
        cx, cy = PW // 2, 0
        for r in range(120):
            spread = int(r * 0.4)
            for dx in range(-spread, spread + 1, 2):
                rx = cx + dx + int(r * math.tan(math.radians(angle)))
                ry = r
                if 0 <= rx < PW and 0 <= ry < PH:
                    b = max(0, 60 - r // 2)
                    draw.point((rx, ry), fill=(b + 30, b + 20, b))
    # 舞台
    pixels_rect(draw, 100, 100, 120, 50, (30, 20, 40))
    # 大屏幕
    pixels_rect(draw, 110, 40, 100, 55, (20, 30, 60))
    # 观众剪影
    for i in range(40):
        ax = random.randint(0, PW - 1)
        ah = random.randint(15, 30)
        pixels_rect(draw, ax, PH - ah, 6, ah, (10, 5, 15))


def bg_livestudio(draw, img):
    """这个已有好图，保留现有PNG"""
    gradient(draw, PW, PH, (60, 20, 80), (40, 15, 60))
    # 补光灯
    for r in range(60):
        for angle in range(0, 360, 30):
            rx = int(60 + r * math.cos(math.radians(angle)))
            ry = int(40 + r * math.sin(math.radians(angle)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 80 - r)
                draw.point((rx, ry), fill=(b + 100, b // 2, b + 80))
    for r in range(60):
        for angle in range(0, 360, 30):
            rx = int(260 + r * math.cos(math.radians(angle)))
            ry = int(40 + r * math.sin(math.radians(angle)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 80 - r)
                draw.point((rx, ry), fill=(b + 100, b // 2, b + 80))
    # 桌子和手机
    pixels_rect(draw, 80, 110, 160, 30, (80, 50, 100))
    for i in range(5):
        px = 100 + i * 30
        pixels_rect(draw, px, 95, 15, 20, (40, 40, 60))
    # 摄像机轮廓
    pixels_rect(draw, 140, 60, 25, 20, (30, 30, 40))
    pixels_rect(draw, 148, 50, 10, 12, (50, 50, 60))


def bg_kitchen(draw, img):
    """这个已有好图，保留现有PNG"""
    gradient(draw, PW, PH, (200, 160, 100), (230, 190, 130))
    # 窗户暖光
    for r in range(50):
        for a in range(0, 360, 20):
            rx = int(80 + r * 0.5 * math.cos(math.radians(a)))
            ry = int(40 + r * 0.3 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 50 - r)
                draw.point((rx, ry), fill=(255, 220 + b, 150 + b))
    # 橱柜
    pixels_rect(draw, 0, 80, PW, 40, (150, 110, 70))
    pixels_rect(draw, 0, 130, PW, 50, (120, 90, 55))
    # 餐桌
    pixels_rect(draw, 80, 110, 160, 25, (140, 100, 60))
    # 碗的蒸汽
    for i in range(5):
        sx = 140 + random.randint(-10, 10)
        for sy in range(20):
            draw.point((sx + sy // 3, 85 - sy), fill=(220, 220, 230))


def bg_home_old(draw, img):
    """这个已有好图，保留现有PNG"""
    gradient(draw, PW, PH, (200, 140, 80), (230, 170, 100))
    # 红砖楼
    for bx in [20, 100, 200]:
        bh = random.randint(80, 110)
        pixels_rect(draw, bx, PH - bh - 20, 70, bh, (160, 70, 50))
        # 窗户
        for wy in range(10, bh - 10, 15):
            for wx in range(5, 60, 15):
                lit = random.random() < 0.5
                c = (255, 220, 120) if lit else (80, 50, 40)
                pixels_rect(draw, bx + wx, PH - bh - 20 + wy, 8, 8, c)
    # 炊烟
    for _ in range(3):
        cx = random.randint(30, PW - 30)
        for i in range(15):
            draw.point((cx + i, PH - 140 - i * 3), fill=(200, 200, 200))
    # 地面
    pixels_rect(draw, 0, PH - 20, PW, 20, (150, 110, 60))
    # 夕阳
    for r in range(25):
        for a in range(0, 360, 10):
            rx = int(260 + r * math.cos(math.radians(a)))
            ry = int(40 + r * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                draw.point((rx, ry), fill=(255, 200 - r * 3, 100 - r * 3))


def bg_room_rent(draw, img):
    """这个已有好图，保留现有PNG"""
    gradient(draw, PW, PH, (50, 55, 70), (35, 40, 55))
    # 单词墙
    for i in range(30):
        wx = random.randint(5, PW - 30)
        wy = random.randint(5, 80)
        for j in range(random.randint(2, 6)):
            draw.point((wx + j, wy), fill=(200, 200, 180))
            draw.point((wx + j, wy + 1), fill=(200, 200, 180))
    # 小床
    pixels_rect(draw, 10, 110, 80, 35, (80, 60, 50))
    pixels_rect(draw, 10, 105, 80, 8, (200, 200, 210))
    # 书桌
    pixels_rect(draw, 200, 100, 90, 35, (100, 75, 50))
    # 台灯
    for r in range(25):
        for a in range(0, 360, 20):
            rx = int(230 + r * 0.8 * math.cos(math.radians(a)))
            ry = int(95 + r * 0.5 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 50 - r * 2)
                draw.point((rx, ry), fill=(255, 230 + b, 150 + b))
    # 地板
    pixels_rect(draw, 0, 145, PW, 35, (55, 45, 35))


def bg_xiaomi(draw, img):
    gradient(draw, PW, PH, (200, 130, 50), (230, 160, 80))
    # 现代建筑
    pixels_rect(draw, 50, 40, 100, 100, (240, 240, 245))
    pixels_rect(draw, 170, 50, 80, 90, (240, 240, 245))
    pixels_rect(draw, 40, 30, 120, 12, (255, 160, 50))  # 橙色招牌
    # 玻璃窗
    for wy in range(50, 130, 12):
        for wx in range(55, 145, 12):
            pixels_rect(draw, wx, wy, 8, 8, (180, 210, 240))
    # 绿化
    for i in range(8):
        pixels_rect(draw, 20 + i * 38, 135, 20, 15, (50, 120, 50))
    # 天空
    # 地面
    pixels_rect(draw, 0, 150, PW, 30, (180, 180, 190))


def bg_apple(draw, img):
    gradient(draw, PW, PH, (130, 180, 230), (180, 210, 240))
    # 环形建筑
    cx, cy = PW // 2, 100
    for r in range(60, 80):
        for a in range(0, 360, 3):
            rx = int(cx + r * math.cos(math.radians(a)))
            ry = int(cy + r * 0.4 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                draw.point((rx, ry), fill=(200, 210, 220))
    # 玻璃反光
    for r in range(62, 78):
        for a in range(20, 160, 5):
            rx = int(cx + r * math.cos(math.radians(a)))
            ry = int(cy + r * 0.4 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                draw.point((rx, ry), fill=(170, 200, 230))
    # 草地
    pixels_rect(draw, 0, 135, PW, 45, (80, 140, 70))
    # 树
    for i in range(6):
        tx = 30 + i * 50
        pixels_rect(draw, tx, 115, 5, 22, (90, 60, 30))
        pixels_rect(draw, tx - 10, 95, 25, 25, (50, 120, 50))


def bg_noodle_shop(draw, img):
    gradient(draw, PW, PH, (80, 50, 30), (120, 70, 40))
    # 暖光
    for r in range(80):
        for a in range(0, 360, 15):
            rx = int(PW // 2 + r * math.cos(math.radians(a)))
            ry = int(80 + r * 0.7 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 35 - r // 3)
                draw.point((rx, ry), fill=(180 + b, 120 + b, 50 + b))
    # 木桌
    pixels_rect(draw, 60, 110, 200, 25, (100, 60, 30))
    # 碗
    pixels_rect(draw, 130, 95, 30, 18, (220, 220, 230))
    # 蒸汽
    for i in range(10):
        sx = 135 + i * 2
        for sy in range(25):
            draw.point((sx + sy // 4, 90 - sy), fill=(200, 200, 210))
    # 吧台
    pixels_rect(draw, 0, 135, PW, 45, (70, 45, 25))


def bg_bar(draw, img):
    gradient(draw, PW, PH, (20, 10, 40), (40, 15, 60))
    # 霓虹灯
    for r in range(40):
        for a in range(0, 360, 20):
            rx = int(50 + r * math.cos(math.radians(a)))
            ry = int(30 + r * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 60 - r * 2)
                draw.point((rx, ry), fill=(b + 80, b // 3, b + 100))
    for r in range(40):
        for a in range(0, 360, 20):
            rx = int(270 + r * math.cos(math.radians(a)))
            ry = int(30 + r * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 60 - r * 2)
                draw.point((rx, ry), fill=(b + 20, b + 80, b + 100))
    # 吧台
    pixels_rect(draw, 0, 110, PW, 35, (50, 35, 50))
    # 酒杯
    pixels_rect(draw, 100, 95, 12, 18, (150, 180, 200))
    pixels_rect(draw, 200, 95, 12, 18, (150, 180, 200))
    # 地板
    pixels_rect(draw, 0, 145, PW, 35, (25, 15, 35))


def bg_street_food(draw, img):
    gradient(draw, PW, PH, (40, 40, 60), (60, 50, 50))
    # 黎明天空渐变
    for y in range(60):
        r = int(255 * (1 - y / 60))
        g = int(180 * (1 - y / 60))
        b = int(100 * (1 - y / 60))
        draw.line([(0, y), (PW, y)], fill=(r + 30, g + 30, b + 20))
    # 推车
    pixels_rect(draw, 110, 100, 100, 40, (180, 100, 30))
    pixels_rect(draw, 100, 95, 120, 8, (200, 120, 40))
    # 暖灯
    for r in range(35):
        for a in range(0, 360, 20):
            rx = int(160 + r * math.cos(math.radians(a)))
            ry = int(90 + r * 0.6 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 50 - r * 2)
                draw.point((rx, ry), fill=(255, 220 - b, 100 + b))
    # 街道
    pixels_rect(draw, 0, 140, PW, 40, (50, 45, 40))


def bg_celebration(draw, img):
    gradient(draw, PW, PH, (150, 40, 40), (180, 80, 30))
    # 圆桌
    pixels_rect(draw, 80, 100, 160, 35, (120, 70, 30))
    # 盘子
    for i in range(6):
        dx = 90 + i * 25
        pixels_rect(draw, dx, 105, 18, 8, (240, 240, 230))
    # 红色装饰
    pixels_rect(draw, 140, 20, 40, 25, (200, 30, 30))
    # 金色灯光
    for r in range(70):
        for a in range(0, 360, 15):
            rx = int(PW // 2 + r * 1.2 * math.cos(math.radians(a)))
            ry = int(70 + r * 0.6 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 25 - r // 4)
                draw.point((rx, ry), fill=(200 + b, 150 + b, 50))
    # 地板
    pixels_rect(draw, 0, 135, PW, 45, (100, 60, 30))


def bg_bookstore(draw, img):
    gradient(draw, PW, PH, (80, 60, 40), (100, 75, 50))
    # 书架
    for sx in range(0, PW, 50):
        pixels_rect(draw, sx, 10, 45, 130, (80, 50, 25))
        for sh in range(6):
            sy = 15 + sh * 20
            for bx in range(sx + 3, sx + 43, 6):
                bh = random.randint(12, 17)
                bc = random.choice([(150, 40, 40), (40, 80, 150), (40, 120, 60), (150, 120, 40), (100, 50, 120)])
                pixels_rect(draw, bx, sy, 4, bh, bc)
    # 阅读灯
    for r in range(30):
        for a in range(0, 360, 20):
            rx = int(260 + r * math.cos(math.radians(a)))
            ry = int(120 + r * 0.5 * math.sin(math.radians(a)))
            if 0 <= rx < PW and 0 <= ry < PH:
                b = max(0, 40 - r * 2)
                draw.point((rx, ry), fill=(255, 230 + b, 150 + b))
    # 柜台
    pixels_rect(draw, 230, 135, 80, 45, (70, 45, 25))
    # 地板
    pixels_rect(draw, 0, 155, PW, 25, (60, 45, 30))


def bg_corridor(draw, img):
    gradient(draw, PW, PH, (20, 25, 40), (30, 35, 50))
    # 走廊透视
    for i in range(20):
        t = i / 20
        lw = int(30 + t * (PW - 60))
        lx = (PW - lw) // 2
        ly = int(20 + t * 120)
        c = int(20 + t * 25)
        draw.line([(lx, ly), (lx + lw, ly)], fill=(c + 20, c + 25, c + 40))
    # 门
    for side in [0, 1]:
        for i in range(4):
            t = 0.2 + i * 0.2
            dw = int(15 + t * 20)
            dh = int(25 + t * 40)
            if side == 0:
                dx = int(20 + t * 60)
            else:
                dx = int(PW - 20 - dw - t * 60)
            dy = int(30 + t * 100)
            pixels_rect(draw, dx, dy, dw, dh, (25, 22, 35))
    # 闪烁荧光灯
    flicker = random.random() < 0.7
    pixels_rect(draw, PW // 2 - 40, 10, 80, 4, (200, 220, 255) if flicker else (100, 110, 130))
    # 烟头红光
    for r in range(8):
        draw.point((PW - 60 + r % 3, 140 + r // 3), fill=(255, 50, 20))
    # 地板
    pixels_rect(draw, 0, 155, PW, 25, (25, 28, 42))


def bg_hospital(draw, img):
    gradient(draw, PW, PH, (200, 210, 220), (220, 225, 235))
    # 白墙
    pixels_rect(draw, 0, 0, PW, 130, (230, 235, 240))
    # 走廊
    for i in range(15):
        t = i / 15
        lw = int(40 + t * (PW - 80))
        lx = (PW - lw) // 2
        ly = int(30 + t * 80)
        c = int(220 - t * 30)
        draw.line([(lx, ly), (lx + lw, ly)], fill=(c, c + 5, c + 10))
    # 椅子
    for i in range(4):
        pixels_rect(draw, 40 + i * 60, 120, 35, 25, (180, 185, 200))
    # 灯光
    pixels_rect(draw, 50, 8, 40, 4, (255, 255, 240))
    pixels_rect(draw, 230, 8, 40, 4, (255, 255, 240))
    # 地板
    pixels_rect(draw, 0, 145, PW, 35, (200, 205, 215))


def bg_press(draw, img):
    gradient(draw, PW, PH, (200, 210, 230), (180, 190, 210))
    # 讲台
    pixels_rect(draw, 130, 80, 60, 50, (80, 80, 90))
    # 麦克风
    pixels_rect(draw, 150, 65, 4, 20, (40, 40, 50))
    pixels_rect(draw, 147, 60, 10, 8, (50, 50, 60))
    # 相机闪光
    for _ in range(5):
        fx = random.randint(20, PW - 20)
        fy = random.randint(40, 90)
        pixels_rect(draw, fx, fy, 8, 6, (30, 30, 40))
        if random.random() < 0.3:
            for r in range(10):
                draw.point((fx + 4 + r, fy + 3), fill=(255, 255, 255))
    # 记者剪影
    for i in range(8):
        ax = random.randint(10, PW - 10)
        pixels_rect(draw, ax, 110, 8, 20, (60, 60, 70))
        pixels_rect(draw, ax - 2, 130, 12, 25, (50, 50, 60))
    # 背景板
    pixels_rect(draw, 80, 20, 160, 55, (180, 185, 200))
    # 地板
    pixels_rect(draw, 0, 155, PW, 25, (150, 155, 170))


def bg_airport(draw, img):
    gradient(draw, PW, PH, (150, 180, 210), (180, 200, 220))
    # 大窗户
    for i in range(5):
        wx = 15 + i * 60
        pixels_rect(draw, wx, 10, 50, 70, (180, 210, 230))
        # 飞机
        if i == 2:
            pixels_rect(draw, wx + 10, 25, 25, 8, (200, 200, 210))
            pixels_rect(draw, wx + 5, 28, 12, 3, (180, 180, 190))
            pixels_rect(draw, wx + 28, 28, 12, 3, (180, 180, 190))
    # 登机口指示
    pixels_rect(draw, 200, 30, 60, 20, (30, 80, 150))
    # 座椅
    for i in range(6):
        pixels_rect(draw, 20 + i * 48, 110, 30, 25, (80, 100, 130))
        pixels_rect(draw, 20 + i * 48, 105, 30, 8, (90, 110, 140))
    # 地板
    pixels_rect(draw, 0, 135, PW, 45, (170, 180, 200))


def bg_conference(draw, img):
    gradient(draw, PW, PH, (10, 20, 50), (20, 40, 80))
    # 舞台
    pixels_rect(draw, 50, 60, 220, 70, (15, 25, 50))
    # 大屏幕
    pixels_rect(draw, 70, 20, 180, 50, (30, 60, 120))
    # 聚光灯
    for angle in [-20, 0, 20]:
        cx, cy = PW // 2, 0
        for r in range(100):
            spread = int(r * 0.35)
            for dx in range(-spread, spread + 1, 3):
                rx = cx + dx + int(r * math.tan(math.radians(angle)))
                ry = r
                if 0 <= rx < PW and 0 <= ry < PH:
                    b = max(0, 40 - r // 3)
                    draw.point((rx, ry), fill=(b + 20, b + 40, b + 80))
    # 观众
    for i in range(60):
        ax = random.randint(0, PW - 1)
        ah = random.randint(10, 22)
        pixels_rect(draw, ax, PH - ah, 5, ah, (8, 15, 35))


def bg_small_office(draw, img):
    gradient(draw, PW, PH, (60, 55, 75), (80, 70, 90))
    # 杂乱桌子
    for i in range(6):
        dx = 10 + i * 50
        pixels_rect(draw, dx, 90 + random.randint(-10, 10), 40, 35, (80, 60, 45))
        pixels_rect(draw, dx + 5, 75 + random.randint(-5, 8), 25, 18, (40, 45, 60))
    # 披萨盒
    pixels_rect(draw, 30, 130, 25, 12, (200, 150, 50))
    pixels_rect(draw, 200, 125, 25, 12, (200, 150, 50))
    pixels_rect(draw, 250, 135, 20, 10, (50, 100, 50))
    # 白板
    pixels_rect(draw, 5, 5, 100, 40, (230, 230, 220))
    # 暖光
    for r in range(50):
        b = max(0, 30 - r // 2)
        draw.ellipse([160 - r, 50 - r // 2, 160 + r, 50 + r // 2], fill=(40 + b, 35 + b, 45))
    # 地板
    pixels_rect(draw, 0, 150, PW, 30, (50, 45, 60))


def bg_balcony(draw, img):
    gradient(draw, PW, PH, (10, 10, 35), (20, 15, 45))
    stars(draw, PW, PH, 50, (255, 255, 220))
    # 城市天际线
    for i in range(20):
        bx = i * 17 - 5
        bh = random.randint(20, 70)
        pixels_rect(draw, bx, PH - bh - 30, 14, bh, (15, 20, 40))
        for wy in range(0, bh - 5, 8):
            for wx in range(2, 12, 5):
                if random.random() < 0.4:
                    draw.point((bx + wx, PH - bh - 30 + wy), fill=(255, 220, 120))
    # 栏杆
    pixels_rect(draw, 0, 125, PW, 4, (60, 65, 80))
    for i in range(20):
        pixels_rect(draw, i * 17, 125, 3, 30, (50, 55, 70))
    # 烟头
    for r in range(5):
        draw.point((50 + r, 120 - r), fill=(255, 60, 20))
    # 阳台地面
    pixels_rect(draw, 0, 155, PW, 25, (25, 25, 40))


def bg_train_platform(draw, img):
    gradient(draw, PW, PH, (15, 20, 40), (30, 35, 50))
    # 昏黄路灯
    for lx in [50, 160, 270]:
        for r in range(35):
            for a in range(0, 360, 20):
                rx = int(lx + r * math.cos(math.radians(a)))
                ry = int(90 + r * 0.8 * math.sin(math.radians(a)))
                if 0 <= rx < PW and 0 <= ry < PH:
                    b = max(0, 30 - r)
                    draw.point((rx, ry), fill=(200 + b, 170 + b, 80 + b))
        pixels_rect(draw, lx - 2, 60, 4, 60, (40, 40, 50))
    # 长椅上的人
    pixels_rect(draw, 130, 115, 20, 25, (30, 30, 50))
    pixels_rect(draw, 135, 105, 12, 12, (25, 25, 40))
    # 站台
    pixels_rect(draw, 0, 140, PW, 40, (50, 48, 55))
    pixels_rect(draw, 0, 138, PW, 3, (255, 220, 100))
    # 铁轨
    pixels_rect(draw, 0, 165, PW, 3, (60, 60, 70))


# ========== 生成所有背景图 ==========
print("=== Generating pixel art backgrounds ===")

# 已有好图的标记为 None 以跳过（使用现有PNG）
existing_good = {"bg_home_old", "bg_livestudio", "bg_office_night", "bg_room_rent", "bg_kitchen"}

bg_funcs = {
    "bg_classroom": bg_classroom,
    "bg_office_day": bg_office_day,
    "bg_office_dark": bg_office_dark,
    "bg_office_modern": bg_office_modern,
    "bg_office_startup": bg_startup,
    "bg_factory": bg_factory,
    "bg_venue": bg_venue,
    "bg_xiaomi": bg_xiaomi,
    "bg_apple": bg_apple,
    "bg_noodle_shop": bg_noodle_shop,
    "bg_bar": bg_bar,
    "bg_street_food": bg_street_food,
    "bg_celebration": bg_celebration,
    "bg_bookstore": bg_bookstore,
    "bg_corridor": bg_corridor,
    "bg_hospital": bg_hospital,
    "bg_press": bg_press,
    "bg_airport": bg_airport,
    "bg_conference": bg_conference,
    "bg_small_office": bg_small_office,
    "bg_balcony": bg_balcony,
    "bg_train_platform": bg_train_platform,
}

for name, func in bg_funcs.items():
    if name in existing_good:
        print(f"  Skip (existing good): {name}.png")
        continue
    img = make_image(func)
    save(img, name + ".png")

# ========== 生成角色头像 ==========
print("\n=== Generating pixel art character avatars ===")

CW, CH = 128, 128


def draw_avatar(base_color, hair_color, skin=(220, 185, 160), shirt_color=None, accent=None, has_glasses=False, has_beard=False):
    img = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = CW // 2, CH // 2

    if shirt_color is None:
        shirt_color = base_color

    # 身体
    d.rectangle([cx - 28, cy + 10, cx + 28, cy + 50], fill=shirt_color)
    # 脖子
    d.rectangle([cx - 8, cy + 2, cx + 8, cy + 14], fill=skin)
    # 头
    d.ellipse([cx - 24, cy - 32, cx + 24, cy + 8], fill=skin)
    # 头发
    if hair_color:
        d.ellipse([cx - 26, cy - 38, cx + 26, cy - 8], fill=hair_color)
        d.rectangle([cx - 26, cy - 20, cx + 26, cy - 14], fill=hair_color)
    # 眼睛
    eye_y = cy - 10
    d.rectangle([cx - 12, eye_y, cx - 6, eye_y + 4], fill=(30, 30, 30))
    d.rectangle([cx + 6, eye_y, cx + 12, eye_y + 4], fill=(30, 30, 30))
    d.rectangle([cx - 10, eye_y + 1, cx - 8, eye_y + 3], fill=(255, 255, 255))
    d.rectangle([cx + 8, eye_y + 1, cx + 10, eye_y + 3], fill=(255, 255, 255))
    # 眉毛
    d.rectangle([cx - 14, eye_y - 5, cx - 4, eye_y - 3], fill=hair_color or (40, 40, 40))
    d.rectangle([cx + 4, eye_y - 5, cx + 14, eye_y - 3], fill=hair_color or (40, 40, 40))
    # 嘴
    if accent == "smile":
        d.arc([cx - 8, cy - 2, cx + 8, cy + 10], 0, 180, fill=(180, 80, 80), width=2)
    elif accent == "serious":
        d.rectangle([cx - 6, cy + 2, cx + 6, cy + 4], fill=(150, 70, 70))
    else:
        d.arc([cx - 6, cy, cx + 6, cy + 8], 0, 180, fill=(160, 70, 70), width=2)
    # 眼镜
    if has_glasses:
        d.ellipse([cx - 16, eye_y - 4, cx - 2, eye_y + 8], outline=(60, 60, 80), width=2)
        d.ellipse([cx + 2, eye_y - 4, cx + 16, eye_y + 8], outline=(60, 60, 80), width=2)
        d.line([cx - 2, eye_y + 2, cx + 2, eye_y + 2], fill=(60, 60, 80), width=2)
    # 胡子
    if has_beard:
        for bx in range(cx - 12, cx + 13, 2):
            for by in range(cy - 2, cy + 6):
                if random.random() < 0.5:
                    d.point((bx, by), fill=hair_color or (60, 50, 40))
    return img


avatars = {
    "luocheng_young": lambda: draw_avatar((40, 40, 50), (30, 25, 25), accent="serious"),
    "luocheng_kid": lambda: draw_avatar((80, 80, 120), (30, 25, 25), skin=(230, 195, 170)),
    "laozhou": lambda: draw_avatar((50, 50, 70), (50, 45, 40), has_glasses=True, accent="serious"),
    "xiaozhang": lambda: draw_avatar((60, 50, 80), (20, 15, 15), skin=(235, 200, 180), shirt_color=(100, 80, 120), accent="smile"),
    "chengzong": lambda: draw_avatar((40, 40, 45), (30, 25, 20), skin=(225, 190, 165), has_glasses=False, accent="smile"),
    "tim": lambda: draw_avatar((50, 60, 80), (180, 170, 160), skin=(220, 195, 180), shirt_color=(60, 70, 90), accent="smile"),
    "wu_laoban": lambda: draw_avatar((100, 70, 40), (150, 130, 110), skin=(210, 180, 150), has_glasses=True, accent="smile"),
}

existing_chars = {"laowang", "luocheng_mid", "wife"}

for name, gen in avatars.items():
    if name in existing_chars:
        print(f"  Skip (existing): {name}.png")
        continue
    img = gen()
    save_char(img, name + ".png")

print("\n=== All pixel art assets generated! ===")
