from PIL import Image, ImageDraw
import os
import math
import random

random.seed(555)

BG_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
os.makedirs(BG_DIR, exist_ok=True)

# 像素画布：160x90 (16:9) 放大6倍 = 960x540 (游戏会缩放到1280x720)
PW, PH = 160, 90
SCALE = 6
FW, FH = PW * SCALE, PH * SCALE


def upscale(img):
    return img.resize((FW, FH), Image.NEAREST)


def save(img, name):
    path = os.path.join(BG_DIR, name + ".png")
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


def vertical_gradient(d, colors, y_range=None):
    """垂直渐变"""
    y0, y1 = y_range if y_range else (0, PH)
    h = y1 - y0
    n = len(colors) - 1
    for y in range(y0, y1):
        t = (y - y0) / max(1, h - 1) * n
        idx = min(int(t), n - 1)
        f = t - idx
        c0 = colors[idx]
        c1 = colors[idx + 1]
        r = int(c0[0] + (c1[0] - c0[0]) * f)
        g = int(c0[1] + (c1[1] - c0[1]) * f)
        b = int(c0[2] + (c1[2] - c0[2]) * f)
        for x in range(PW):
            put(d, x, y, (r, g, b))


# ============================================================
# 1. home - 北方老式居民楼傍晚
# ============================================================
def bg_home():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # 天空渐变（傍晚橙粉色）
    sky_colors = [
        (30, 20, 50),    # 最上：深紫蓝
        (80, 50, 90),    # 紫
        (180, 90, 80),   # 橙红
        (240, 150, 90),  # 橙黄
        (255, 200, 130), # 近地平线：暖黄
    ]
    vertical_gradient(d, sky_colors, (0, 45))

    # 地平线/远处屋顶轮廓
    for y in range(40, 48):
        for x in range(PW):
            t = x / PW
            h = 5 + int(3 * math.sin(x * 0.15) * math.sin(x * 0.07 + 1))
            if y > 40 + h:
                put(d, x, y, (40, 35, 45))

    # 近处红砖楼
    building_y = 20
    building_h = 70
    # 楼体
    rect(d, 0, building_y, PW, building_h, (90, 45, 35))
    # 砖墙纹理
    for y in range(building_y, building_y + building_h, 3):
        for x in range(0, PW, 8):
            offset = (y // 3) % 2 * 4
            put(d, x + offset, y, (75, 35, 28))
            put(d, x + offset + 1, y, (70, 32, 25))

    # 窗户（暖黄色灯光）
    windows = [
        (8, 28, 12, 10, True),
        (30, 28, 12, 10, True),
        (52, 30, 12, 10, False),
        (74, 25, 12, 10, True),
        (96, 32, 12, 10, True),
        (118, 28, 12, 10, False),
        (140, 30, 16, 10, True),
        (8, 50, 12, 10, True),
        (30, 52, 12, 10, True),
        (52, 50, 12, 10, True),
        (74, 50, 12, 10, False),
        (96, 48, 12, 10, True),
        (118, 52, 12, 10, True),
        (140, 50, 16, 10, False),
        (8, 72, 12, 10, False),
        (30, 72, 12, 10, True),
        (52, 74, 12, 10, True),
        (74, 72, 12, 10, True),
        (96, 70, 12, 10, False),
        (118, 72, 12, 10, True),
        (140, 74, 16, 10, True),
    ]
    for wx, wy, ww, wh, lit in windows:
        if lit:
            # 亮窗：暖黄色
            rect(d, wx, wy, ww, wh, (255, 220, 120))
            # 光晕
            for dy in range(-2, wh+2):
                for dx in range(-2, ww+2):
                    if 0 <= wx+dx < PW and 0 <= wy+dy < PH:
                        if dx < 0 or dx >= ww or dy < 0 or dy >= wh:
                            if random.random() < 0.4:
                                put(d, wx+dx, wy+dy, (255, 180, 80))
        else:
            # 暗窗：深蓝色
            rect(d, wx, wy, ww, wh, (30, 40, 65))
            rect(d, wx+1, wy+1, ww-2, wh-2, (20, 30, 55))
        # 窗框
        rect(d, wx, wy, ww, 1, (60, 30, 20))
        rect(d, wx, wy+wh-1, ww, 1, (60, 30, 20))
        rect(d, wx + ww//2, wy, 1, wh, (60, 30, 20))

    # 楼道
    rect(d, 65, 75, 10, 15, (50, 25, 20))
    rect(d, 66, 76, 8, 13, (30, 15, 12))
    # 楼道灯
    put(d, 70, 77, (255, 200, 80))

    # 阳台
    for wx in [8, 30, 96, 118]:
        rect(d, wx, wy if 'wy' in dir() else 45, 12, 3, (60, 30, 22))
        for dx in range(1, 12, 2):
            put(d, wx+dx, 44, (60, 30, 22))

    # 空调外机
    rect(d, 25, 38, 8, 5, (200, 200, 205))
    rect(d, 26, 39, 6, 3, (150, 150, 160))
    rect(d, 115, 58, 8, 5, (200, 200, 205))
    rect(d, 116, 59, 6, 3, (150, 150, 160))

    # 晾衣绳和衣服
    for i in range(3):
        x0 = 20 + i * 40
        for x in range(x0, x0 + 25):
            put(d, x, 42, (80, 60, 40))
        # 衣服
        rect(d, x0+5, 42, 6, 8, (180, 60, 60))
        rect(d, x0+13, 42, 5, 7, (60, 80, 140))

    # 地面
    rect(d, 0, building_y + building_h, PW, PH - building_y - building_h, (50, 40, 35))
    # 地面纹理
    for y in range(building_y + building_h, PH):
        for x in range(0, PW, 10):
            if random.random() < 0.3:
                put(d, x + random.randint(0, 9), y, (35, 28, 25))

    # 远处树剪影
    for tx in [5, 155]:
        for r in range(8):
            for a in range(0, 360, 10):
                rx = int(tx + r * math.cos(math.radians(a)))
                ry = int(building_y + building_h - 8 + r * 0.7 * math.sin(math.radians(a)))
                if 0 <= rx < PW and 0 <= ry < PH:
                    put(d, rx, ry, (25, 40, 25))

    return upscale(img)


# ============================================================
# 2. office_night - 现代办公室夜景
# ============================================================
def bg_office_night():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # 窗外夜景（蓝色调）
    night_colors = [
        (10, 12, 30),
        (15, 20, 50),
        (25, 35, 70),
        (30, 40, 75),
    ]
    vertical_gradient(d, night_colors, (0, 50))

    # 远处城市灯光
    random.seed(42)
    for _ in range(80):
        x = random.randint(0, PW-1)
        y = random.randint(10, 45)
        if random.random() < 0.6:
            c = (255, 230, 150)
        elif random.random() < 0.5:
            c = (200, 150, 255)
        else:
            c = (150, 200, 255)
        put(d, x, y, c)
        if random.random() < 0.3:
            put(d, x, y+1, c)
    random.seed(555)

    # 大窗户玻璃
    rect(d, 0, 0, PW, 52, (50, 60, 80))
    # 窗框
    for wx in range(0, PW, 40):
        rect(d, wx, 0, 2, 52, (70, 75, 85))
    rect(d, 0, 50, PW, 2, (70, 75, 85))
    rect(d, 0, 25, PW, 2, (70, 75, 85))

    # 室内
    rect(d, 0, 52, PW, PH-52, (40, 38, 45))

    # 办公桌（多排）
    desks_colors = [(50, 45, 55), (45, 42, 50), (55, 50, 60)]
    # 第一排桌子（近）
    for dx in range(0, PW, 28):
        rect(d, dx, 65, 26, 4, (65, 55, 45))
        # 电脑显示器
        rect(d, dx+8, 58, 10, 7, (20, 25, 35))
        # 屏幕光
        rect(d, dx+9, 59, 8, 5, (60, 130, 200))
        # 显示器底座
        rect(d, dx+11, 65, 4, 2, (30, 30, 35))
        # 桌腿
        rect(d, dx+1, 69, 2, 15, (40, 35, 30))
        rect(d, dx+22, 69, 2, 15, (40, 35, 30))

    # 第二排桌子（远，小）
    for dx in range(5, PW, 24):
        rect(d, dx, 56, 20, 3, (55, 48, 40))
        rect(d, dx+6, 52, 7, 4, (20, 25, 35))
        rect(d, dx+7, 53, 5, 2, (70, 140, 200))

    # 台灯光（暖黄色）
    lamp_x = [20, 60, 100, 140]
    for lx in lamp_x:
        # 灯罩
        rect(d, lx-3, 57, 6, 2, (80, 60, 30))
        # 光柱
        for r in range(10):
            for dx in range(-r, r+1):
                if random.random() < 0.5:
                    put(d, lx+dx, 60+r, (120, 90, 40))

    # 天花板灯
    for cx in range(20, PW, 35):
        rect(d, cx-4, 0, 8, 2, (180, 170, 140))
        # 灯光扩散
        for dy in range(2, 6):
            put(d, cx, dy, (100, 90, 70))

    # 植物（角落）
    for px in [5, 152]:
        rect(d, px, 72, 6, 8, (30, 60, 35))
        for r in range(6):
            for a in range(0, 360, 15):
                rx = int(px+3 + r * math.cos(math.radians(a)))
                ry = int(70 + r * 0.6 * math.sin(math.radians(a)))
                put(d, rx, ry, (40, 70, 40))

    # 椅子
    for cx in [14, 52, 92, 132]:
        rect(d, cx, 70, 8, 3, (35, 30, 40))
        rect(d, cx+1, 72, 6, 10, (30, 25, 35))
        # 椅背
        rect(d, cx, 67, 8, 4, (35, 30, 40))

    return upscale(img)


# ============================================================
# 3. office_day - 白天办公室
# ============================================================
def bg_office_day():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # 明亮天空
    sky_colors = [
        (130, 180, 230),
        (160, 200, 240),
        (200, 220, 245),
    ]
    vertical_gradient(d, sky_colors, (0, 48))

    # 云朵
    for cx, cy, r in [(25, 15, 5), (80, 10, 6), (130, 18, 4)]:
        for dx in range(-r*2, r*2+1):
            for dy in range(-r, r+1):
                dist = math.sqrt(dx*dx + dy*dy * 2)
                if dist < r:
                    put(d, cx+dx, cy+dy, (250, 250, 255))

    # 大窗户
    rect(d, 0, 0, PW, 50, (180, 210, 235))
    for wx in range(0, PW, 40):
        rect(d, wx, 0, 2, 50, (220, 225, 230))
    rect(d, 0, 48, PW, 2, (220, 225, 230))
    rect(d, 0, 24, PW, 2, (220, 225, 230))

    # 室内墙壁（白色）
    rect(d, 0, 50, PW, PH-50, (235, 232, 225))

    # 地板（木色）
    rect(d, 0, 78, PW, PH-78, (160, 125, 85))
    for y in range(78, PH, 3):
        for x in range(0, PW, 15):
            put(d, x, y, (145, 110, 75))

    # 办公桌
    for dx in range(0, PW, 30):
        rect(d, dx, 68, 28, 3, (180, 145, 95))
        # 电脑
        rect(d, dx+10, 60, 9, 8, (30, 30, 35))
        rect(d, dx+11, 61, 7, 6, (100, 180, 220))
        rect(d, dx+13, 68, 3, 2, (40, 40, 45))
        # 文件/本子
        rect(d, dx+2, 65, 6, 4, (240, 240, 245))
        put(d, dx+3, 66, (180, 180, 190))
        put(d, dx+4, 67, (180, 180, 190))

    # 椅子
    for cx in [15, 45, 75, 105, 135]:
        rect(d, cx, 72, 8, 3, (80, 80, 90))
        rect(d, cx+1, 75, 6, 8, (70, 70, 80))
        rect(d, cx, 70, 8, 3, (80, 80, 90))

    # 植物
    for px in [3, 150]:
        rect(d, px, 68, 7, 10, (50, 80, 45))
        for r in range(8):
            for a in range(0, 360, 12):
                rx = int(px+4 + r * 1.2 * math.cos(math.radians(a)))
                ry = int(66 + r * 0.7 * math.sin(math.radians(a)))
                put(d, rx, ry, (60, 100, 50))

    # 挂画
    rect(d, 10, 54, 12, 8, (180, 140, 100))
    rect(d, 11, 55, 10, 6, (200, 170, 130))
    # 画里的山
    put(d, 13, 59, (100, 120, 100))
    put(d, 14, 58, (100, 120, 100))
    put(d, 15, 59, (120, 140, 120))
    put(d, 16, 57, (100, 120, 100))
    put(d, 17, 59, (100, 120, 100))
    put(d, 18, 58, (120, 140, 120))
    put(d, 19, 59, (100, 120, 100))

    # 远处远处的楼（窗外）
    for bx in range(0, PW, 15):
        h = random.randint(15, 35)
        rect(d, bx, 48-h, 12, h, (150, 160, 180))

    return upscale(img)


# ============================================================
# 4. office_dark - 深夜独灯
# ============================================================
def bg_office_dark():
    img = Image.new("RGB", (PW, PH), (5, 3, 10))
    d = ImageDraw.Draw(img)

    # 整体深色背景
    rect(d, 0, 0, PW, PH, (8, 6, 15))

    # 远处一点点城市光（窗户）
    for wy in [20, 30, 40]:
        for wx in range(10, PW-10, 18):
            if random.random() < 0.4:
                c = (100, 90, 70) if random.random() < 0.5 else (60, 70, 100)
                rect(d, wx, wy, 4, 3, c)

    # 大窗户轮廓
    rect(d, 0, 0, PW, 50, (15, 18, 30))
    for wx in range(0, PW, 40):
        rect(d, wx, 0, 2, 50, (25, 28, 40))
    rect(d, 0, 48, PW, 2, (25, 28, 40))

    # 办公桌（只有近处一张）
    desk_x = 50
    rect(d, desk_x, 65, 60, 5, (40, 35, 30))
    rect(d, desk_x+2, 70, 4, 15, (30, 25, 20))
    rect(d, desk_x+54, 70, 4, 15, (30, 25, 20))

    # 台灯（唯一光源）
    lamp_x = 80
    # 灯座
    rect(d, lamp_x-4, 62, 8, 3, (70, 50, 25))
    rect(d, lamp_x-1, 58, 2, 6, (60, 45, 20))
    # 灯罩
    rect(d, lamp_x-6, 54, 12, 4, (90, 65, 30))

    # 台灯光晕（暖黄，照亮桌面）
    for r in range(20):
        for dx in range(-r*2, r*2+1):
            dist = math.sqrt(dx*dx + (r-5)*(r-5))
            if dist < r:
                if dist < r * 0.5:
                    c = (255, 210, 130)
                elif dist < r * 0.8:
                    c = (200, 150, 80)
                else:
                    c = (100, 70, 40)
                alpha = 1 - dist / r
                if random.random() < alpha * 0.6:
                    put(d, lamp_x+dx, 60+r, c)

    # 桌面上的物品（被光照亮）
    # 电脑（暗）
    rect(d, desk_x+35, 58, 12, 7, (20, 18, 28))
    rect(d, desk_x+36, 59, 10, 5, (30, 40, 60))
    # 屏幕微光
    rect(d, desk_x+37, 60, 8, 3, (40, 70, 100))
    # 显示器底座
    rect(d, desk_x+39, 65, 4, 2, (25, 22, 32))

    # 文件堆
    rect(d, desk_x+5, 60, 10, 5, (80, 70, 60))
    rect(d, desk_x+6, 61, 8, 1, (100, 90, 80))
    rect(d, desk_x+7, 62, 7, 1, (90, 80, 70))

    # 咖啡杯
    rect(d, desk_x+20, 62, 5, 4, (60, 50, 45))
    put(d, desk_x+25, 63, (60, 50, 45))
    # 热气
    for i in range(3):
        put(d, desk_x+21+i, 59-i, (120, 110, 100))
        if random.random() < 0.5:
            put(d, desk_x+22+i, 58-i, (130, 120, 110))

    # 椅子
    chair_x = 70
    rect(d, chair_x, 70, 10, 3, (25, 22, 30))
    rect(d, chair_x+1, 73, 8, 10, (20, 18, 25))
    rect(d, chair_x, 66, 10, 5, (25, 22, 30))

    # 其他桌子（黑暗中看不见）

    # 地板
    rect(d, 0, 80, PW, PH-80, (15, 12, 20))

    # 墙上的时钟（一点点光）
    rect(d, 130, 55, 10, 10, (30, 25, 35))
    ellip(d, 135, 60, 4, 4, (40, 35, 45))
    put(d, 135, 58, (200, 180, 150))

    return upscale(img)


# ============================================================
# 5. livestudio - 直播间
# ============================================================
def bg_livestudio():
    img = Image.new("RGB", (PW, PH), (10, 5, 20))
    d = ImageDraw.Draw(img)

    # 紫粉渐变背景
    bg_colors = [
        (30, 10, 60),
        (80, 20, 100),
        (120, 30, 110),
    ]
    vertical_gradient(d, bg_colors, (0, 40))

    # 左右环形补光灯（紫色+粉色）
    for lx, color in [(20, (200, 50, 150)), (140, (100, 50, 200))]:
        # 灯环
        for r in range(10, 16):
            for a in range(0, 360, 8):
                rx = int(lx + r * math.cos(math.radians(a)))
                ry = int(35 + r * 0.8 * math.sin(math.radians(a)))
                if abs(r - 13) < 2:
                    put(d, rx, ry, color)
        # 光晕
        for r in range(25):
            for a in range(0, 360, 10):
                rx = int(lx + r * math.cos(math.radians(a)))
                ry = int(35 + r * 0.8 * math.sin(math.radians(a)))
                if random.random() < 0.3:
                    dim = max(0, 255 - r * 10)
                    put(d, rx, ry, (dim//6, dim//15, dim//4))

    # 地面（深色）
    rect(d, 0, 70, PW, PH-70, (20, 10, 35))

    # 主播台
    rect(d, 50, 62, 60, 8, (40, 30, 55))
    rect(d, 52, 70, 5, 12, (30, 20, 40))
    rect(d, 105, 70, 5, 12, (30, 20, 40))
    # 台面高光
    rect(d, 50, 62, 60, 1, (60, 50, 75))

    # 桌上的产品展示
    # 手机
    rect(d, 60, 57, 6, 10, (20, 25, 35))
    rect(d, 61, 58, 4, 7, (100, 150, 200))
    rect(d, 62, 59, 2, 5, (200, 220, 240))
    # 手机2
    rect(d, 72, 56, 6, 11, (30, 30, 40))
    rect(d, 73, 57, 4, 8, (150, 100, 200))
    # 笔
    rect(d, 85, 58, 8, 2, (180, 140, 80))
    put(d, 93, 58, (200, 160, 100))
    # 小音箱
    rect(d, 98, 57, 5, 7, (50, 50, 60))
    for dy in range(57, 64, 2):
        put(d, 99, dy, (70, 70, 80))
        put(d, 100, dy, (70, 70, 80))
        put(d, 101, dy, (70, 70, 80))

    # 麦克风
    rect(d, 77, 48, 6, 10, (60, 50, 70))
    rect(d, 78, 46, 4, 3, (80, 70, 90))
    # 支架
    rect(d, 79, 58, 2, 5, (40, 35, 45))

    # 背景显示屏（直播数据）
    rect(d, 55, 15, 50, 25, (15, 15, 30))
    rect(d, 56, 16, 48, 23, (25, 20, 45))
    # 数字（观看人数）
    put(d, 60, 20, (255, 200, 50))
    put(d, 64, 20, (255, 200, 50))
    put(d, 68, 20, (255, 200, 50))
    put(d, 72, 20, (255, 200, 50))
    # 弹幕条
    rect(d, 58, 28, 44, 2, (40, 35, 60))
    rect(d, 58, 32, 40, 2, (35, 30, 55))
    rect(d, 58, 36, 35, 2, (30, 25, 50))

    # 摄像头
    rect(d, 75, 3, 10, 8, (30, 30, 40))
    rect(d, 77, 5, 6, 4, (80, 120, 160))
    put(d, 80, 6, (255, 255, 255))
    # 红灯
    put(d, 86, 5, (255, 40, 40))

    # 地面反光
    for x in range(0, PW, 3):
        if random.random() < 0.4:
            put(d, x, 75, (60, 20, 80))

    return upscale(img)


# ============================================================
# 6. startup - 初创公司
# ============================================================
def bg_startup():
    img = Image.new("RGB", (PW, PH), (30, 40, 60))
    d = ImageDraw.Draw(img)

    # 墙壁（灰蓝）
    rect(d, 0, 0, PW, 65, (60, 70, 85))

    # 窗户（远处）
    rect(d, 110, 10, 40, 30, (150, 180, 200))
    for wx in [130]:
        rect(d, wx, 10, 1, 30, (180, 200, 210))
    rect(d, 110, 25, 40, 1, (180, 200, 210))

    # 白板（墙上）
    rect(d, 10, 15, 35, 25, (230, 230, 220))
    rect(d, 10, 15, 35, 1, (180, 180, 170))
    rect(d, 10, 39, 35, 1, (180, 180, 170))
    # 白板上的字（简单线条）
    rect(d, 13, 18, 8, 2, (60, 60, 70))
    rect(d, 13, 22, 15, 1, (60, 60, 70))
    rect(d, 13, 25, 12, 2, (60, 60, 70))
    rect(d, 13, 30, 10, 1, (60, 60, 70))
    rect(d, 13, 33, 18, 2, (60, 60, 70))
    # 图表
    rect(d, 28, 28, 1, 10, (80, 100, 120))
    for i in range(5):
        h = 2 + i * 2
        rect(d, 30+i*3, 38-h, 2, h, (100, 140, 180))

    # 地上散落的纸箱
    rect(d, 5, 70, 12, 8, (180, 140, 90))
    rect(d, 6, 71, 10, 1, (200, 160, 110))
    rect(d, 140, 72, 15, 10, (170, 130, 80))
    rect(d, 141, 73, 13, 1, (190, 150, 100))

    # 拥挤的办公桌（多台电脑）
    desks = [
        (40, 55, 30, 3),
        (80, 55, 30, 3),
    ]
    for dx, dy, dw, dh in desks:
        rect(d, dx, dy, dw, dh, (120, 90, 60))
        # 显示器
        rect(d, dx+5, dy-10, 8, 10, (30, 30, 40))
        rect(d, dx+6, dy-9, 6, 7, (80, 160, 200))
        rect(d, dx+7, dy-3, 4, 2, (40, 40, 50))
        # 键盘
        rect(d, dx+2, dy-2, 10, 2, (60, 60, 70))

    # 第二排桌子
    rect(d, 25, 48, 25, 2, (100, 75, 50))
    rect(d, 100, 48, 25, 2, (100, 75, 50))

    # 椅子（乱）
    chair_pos = [35, 75, 115]
    for cx in chair_pos:
        rect(d, cx, 58, 6, 2, (50, 45, 55))
        rect(d, cx+1, 60, 4, 8, (40, 35, 45))

    # 披萨盒
    rect(d, 65, 66, 10, 5, (220, 200, 150))
    rect(d, 66, 67, 8, 1, (240, 220, 170))
    put(d, 68, 68, (200, 150, 80))
    put(d, 71, 68, (200, 150, 80))

    # 咖啡杯（多）
    cups = [(50, 55), (90, 55), (130, 48)]
    for cx, cy in cups:
        rect(d, cx, cy, 3, 3, (50, 40, 30))
        put(d, cx+3, cy+1, (50, 40, 30))

    # 地板
    rect(d, 0, 75, PW, PH-75, (80, 60, 45))
    for y in range(75, PH, 2):
        for x in range(0, PW, 12):
            put(d, x, y, (65, 48, 35))

    # 垃圾桶
    rect(d, 3, 68, 8, 10, (60, 60, 65))
    rect(d, 3, 68, 8, 1, (80, 80, 85))

    # 海报/贴纸（墙上）
    rect(d, 55, 10, 15, 10, (180, 80, 80))
    rect(d, 56, 11, 13, 8, (200, 100, 100))

    return upscale(img)


# ============================================================
# 7. factory - 手机工厂
# ============================================================
def bg_factory():
    img = Image.new("RGB", (PW, PH), (60, 60, 70))
    d = ImageDraw.Draw(img)

    # 天花板（灰色+灯）
    rect(d, 0, 0, PW, 15, (80, 80, 90))
    for cx in range(15, PW, 25):
        rect(d, cx-4, 1, 8, 2, (200, 200, 210))
        # 灯光
        for dy in range(2, 8):
            put(d, cx, dy, (120, 120, 130))

    # 墙壁（浅灰）
    rect(d, 0, 15, PW, 50, (130, 130, 140))

    # 窗户（高）
    for wx in range(10, PW, 35):
        rect(d, wx, 20, 15, 15, (180, 200, 220))
        rect(d, wx, 20, 15, 1, (160, 160, 170))
        rect(d, wx, 34, 15, 1, (160, 160, 170))
        rect(d, wx+7, 20, 1, 15, (160, 160, 170))

    # 大型机器
    for mx in [15, 55, 95, 135]:
        # 机器主体
        rect(d, mx, 40, 18, 25, (90, 100, 110))
        rect(d, mx, 40, 18, 2, (110, 120, 130))
        # 控制面板
        rect(d, mx+3, 45, 12, 8, (40, 40, 50))
        # 按钮灯
        put(d, mx+5, 47, (255, 80, 80))
        put(d, mx+9, 47, (80, 255, 80))
        put(d, mx+13, 47, (255, 255, 80))
        # 显示屏
        rect(d, mx+4, 50, 10, 2, (50, 100, 150))
        # 传送带接口
        rect(d, mx+7, 63, 4, 3, (60, 60, 70))

    # 传送带
    belt_y = 65
    rect(d, 0, belt_y, PW, 5, (50, 45, 40))
    rect(d, 0, belt_y, PW, 1, (70, 65, 60))
    # 传送带上的手机
    for px in range(10, PW, 25):
        rect(d, px, belt_y-5, 6, 4, (25, 30, 40))
        rect(d, px+1, belt_y-4, 4, 2, (100, 150, 200))
        put(d, px+3, belt_y-4, (200, 220, 240))

    # 地面（工业地坪）
    rect(d, 0, 70, PW, PH-70, (90, 85, 80))
    for y in range(70, PH, 4):
        for x in range(0, PW, 8):
            if random.random() < 0.2:
                put(d, x, y, (75, 70, 65))

    # 安全黄线
    rect(d, 0, 70, PW, 1, (255, 220, 50))

    # 管道（天花板上）
    rect(d, 0, 10, PW, 3, (60, 55, 50))
    rect(d, 0, 7, PW, 2, (70, 65, 60))

    # 堆放的箱子
    for bx in [3, 150]:
        rect(d, bx, 60, 10, 10, (180, 150, 100))
        rect(d, bx+1, 61, 8, 1, (200, 170, 120))
        rect(d, bx, 50, 10, 10, (170, 140, 90))
        rect(d, bx+1, 51, 8, 1, (190, 160, 110))

    return upscale(img)


# ============================================================
# 8. xiaomi_office - 谷米办公室
# ============================================================
def bg_xiaomi():
    img = Image.new("RGB", (PW, PH), (200, 220, 240))
    d = ImageDraw.Draw(img)

    # 明亮现代（橙白主色调）
    rect(d, 0, 0, PW, 55, (245, 245, 248))

    # 大玻璃窗
    rect(d, 0, 5, PW, 40, (210, 230, 245))
    for wx in range(0, PW, 32):
        rect(d, wx, 5, 2, 40, (230, 235, 240))
    rect(d, 0, 44, PW, 2, (230, 235, 240))

    # 橙色主题墙
    rect(d, 0, 45, PW, 8, (255, 110, 30))
    # Logo位置（圆形橙白）
    for r in range(5):
        for a in range(0, 360, 5):
            rx = int(20 + r * math.cos(math.radians(a)))
            ry = int(49 + r * 0.7 * math.sin(math.radians(a)))
            put(d, rx, ry, (255, 130, 40))
    # MI字母感
    rect(d, 18, 47, 2, 4, (255, 255, 255))
    rect(d, 20, 47, 2, 4, (255, 255, 255))

    # 办公桌（现代简约）
    rect(d, 0, 53, PW, 3, (255, 255, 255))
    for dx in range(0, PW, 28):
        # 桌子
        rect(d, dx, 60, 26, 3, (240, 240, 245))
        # 显示器（极简）
        rect(d, dx+10, 52, 8, 8, (245, 245, 250))
        rect(d, dx+11, 53, 6, 5, (80, 160, 220))
        rect(d, dx+13, 60, 2, 3, (200, 200, 210))
        # 桌腿
        rect(d, dx+2, 63, 2, 12, (220, 220, 225))
        rect(d, dx+22, 63, 2, 12, (220, 220, 225))

    # 椅子（现代办公椅）
    for cx in [14, 42, 70, 98, 126, 154]:
        rect(d, cx, 65, 7, 3, (120, 100, 140))
        rect(d, cx+1, 68, 5, 7, (100, 80, 120))
        rect(d, cx, 62, 7, 4, (120, 100, 140))

    # 地面（浅灰）
    rect(d, 0, 75, PW, PH-75, (220, 220, 225))
    for y in range(75, PH, 5):
        for x in range(0, PW, 10):
            if random.random() < 0.2:
                put(d, x, y, (200, 200, 210))

    # 盆栽（简约）
    for px in [2, 152]:
        rect(d, px, 62, 6, 10, (60, 120, 60))
        for r in range(6):
            for a in range(0, 360, 10):
                rx = int(px+3 + r * math.cos(math.radians(a)))
                ry = int(60 + r * 0.5 * math.sin(math.radians(a)))
                put(d, rx, ry, (80, 140, 80))

    # 远处产品展示架
    rect(d, 50, 10, 60, 25, (250, 250, 252))
    # 架子上的产品
    products = [55, 70, 85, 100]
    for px in products:
        rect(d, px, 20, 5, 12, (230, 230, 235))
        rect(d, px+1, 21, 3, 8, (200, 220, 240))

    return upscale(img)


# ============================================================
# 9. apple_office - 红果公司
# ============================================================
def bg_apple():
    img = Image.new("RGB", (PW, PH), (240, 245, 250))
    d = ImageDraw.Draw(img)

    # 极简白色
    rect(d, 0, 0, PW, 60, (250, 250, 252))

    # 大落地窗
    rect(d, 0, 5, PW, 40, (225, 235, 245))
    # 极简窗框
    for wx in range(0, PW, 40):
        rect(d, wx, 5, 1, 40, (240, 242, 245))
    rect(d, 0, 44, PW, 1, (240, 242, 245))

    # 窗外：环形建筑剪影（Apple Park风格）
    rect(d, 20, 25, 120, 15, (200, 210, 220))
    for dx in range(20, 140):
        dist = abs(dx - 80)
        if dist < 60:
            h = int(8 * (1 - dist/60) + 5)
            for dy in range(h):
                put(d, dx, 28-dy, (210, 220, 230))
    # 中间空地（绿）
    rect(d, 45, 32, 70, 8, (150, 200, 130))

    # 地面（浅灰木纹）
    rect(d, 0, 60, PW, PH-60, (230, 225, 220))
    for y in range(60, PH, 4):
        for x in range(0, PW, 20):
            put(d, x, y, (215, 210, 205))

    # 长木桌
    rect(d, 20, 62, 120, 4, (210, 185, 155))
    rect(d, 20, 62, 120, 1, (230, 205, 175))
    # 桌腿
    rect(d, 22, 66, 3, 10, (190, 165, 135))
    rect(d, 135, 66, 3, 10, (190, 165, 135))

    # 桌上的产品
    # 笔记本
    rect(d, 40, 57, 12, 6, (180, 180, 185))
    rect(d, 41, 58, 10, 4, (240, 240, 245))
    rect(d, 42, 59, 8, 2, (100, 150, 200))
    # 手机
    rect(d, 70, 58, 5, 8, (200, 200, 205))
    rect(d, 71, 59, 3, 5, (100, 180, 220))
    # 平板
    rect(d, 95, 56, 10, 10, (210, 210, 215))
    rect(d, 96, 57, 8, 7, (80, 130, 180))
    # 笔
    rect(d, 115, 60, 8, 1, (150, 150, 155))

    # 简约椅子
    for cx in [30, 70, 110]:
        rect(d, cx, 66, 6, 2, (200, 200, 210))
        rect(d, cx+1, 68, 4, 6, (190, 190, 200))
        rect(d, cx, 62, 6, 3, (200, 200, 210))

    # 绿植
    for px in [5, 150]:
        rect(d, px, 55, 5, 8, (70, 110, 70))
        for r in range(5):
            for a in range(0, 360, 12):
                rx = int(px+3 + r * 0.9 * math.cos(math.radians(a)))
                ry = int(53 + r * 0.6 * math.sin(math.radians(a)))
                put(d, rx, ry, (90, 130, 90))

    # 墙面装饰（极简线条）
    rect(d, 10, 10, 1, 30, (220, 220, 225))
    rect(d, 149, 10, 1, 30, (220, 220, 225))

    return upscale(img)


# ============================================================
# 10. office_modern - 现代科技公司
# ============================================================
def bg_office_modern():
    img = Image.new("RGB", (PW, PH), (230, 235, 240))
    d = ImageDraw.Draw(img)

    # 玻璃幕墙
    rect(d, 0, 0, PW, 50, (200, 220, 235))
    for wx in range(0, PW, 30):
        rect(d, wx, 0, 2, 50, (220, 228, 235))
    rect(d, 0, 48, PW, 2, (210, 218, 225))

    # 窗外城市天际线
    for bx in range(5, PW, 10):
        h = random.randint(10, 30)
        w = random.randint(6, 10)
        rect(d, bx, 45-h, w, h, (180, 190, 205))
        for wy in range(45-h, 45, 4):
            for wx in range(bx+1, bx+w-1, 3):
                if random.random() < 0.5:
                    put(d, wx, wy, (220, 210, 180))

    # 室内（现代简约）
    rect(d, 0, 50, PW, 10, (245, 245, 250))

    # 玻璃隔断墙
    for gx in [30, 90]:
        rect(d, gx, 0, 2, 60, (200, 210, 220))
        rect(d, gx-1, 0, 1, 60, (220, 228, 235))

    # 会议桌
    rect(d, 50, 62, 60, 5, (200, 175, 145))
    rect(d, 50, 62, 60, 1, (220, 195, 165))
    rect(d, 52, 67, 3, 8, (180, 155, 125))
    rect(d, 105, 67, 3, 8, (180, 155, 125))

    # 椅子（会议椅）
    for cx in [55, 75, 95]:
        rect(d, cx, 68, 8, 2, (120, 110, 130))
        rect(d, cx+2, 70, 4, 5, (100, 90, 110))
        rect(d, cx, 65, 8, 3, (120, 110, 130))
    for cx in [60, 80, 100]:
        rect(d, cx, 55, 8, 2, (120, 110, 130))
        rect(d, cx, 50, 8, 5, (100, 90, 110))

    # 地面
    rect(d, 0, 70, PW, PH-70, (210, 215, 220))
    for y in range(70, PH, 3):
        for x in range(0, PW, 8):
            if random.random() < 0.15:
                put(d, x, y, (195, 200, 205))

    # 前台/接待
    rect(d, 130, 55, 25, 10, (230, 230, 240))
    rect(d, 130, 55, 25, 1, (250, 250, 255))

    return upscale(img)


# ============================================================
# 11. black - 黑屏
# ============================================================
def bg_black():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (0, 0, 0))
    # 极细微渐变（避免完全死黑）
    for y in range(PH):
        t = y / PH
        v = int(3 + t * 5)
        for x in range(PW):
            put(d, x, y, (v, v, v+2))
    return upscale(img)


# ========== 生成所有核心背景图 ==========
print("=== 生成高细节像素动漫风格背景图 ===")
print()

backgrounds = [
    ("bg_home_old", bg_home, "老式居民楼傍晚"),
    ("bg_office_night", bg_office_night, "办公室夜景"),
    ("bg_office_day", bg_office_day, "白天办公室"),
    ("bg_office_dark", bg_office_dark, "深夜独灯办公室"),
    ("bg_livestudio", bg_livestudio, "直播间"),
    ("bg_small_office", bg_startup, "初创公司"),
    ("bg_factory", bg_factory, "手机工厂"),
    ("bg_xiaomi", bg_xiaomi, "谷米办公室"),
    ("bg_apple", bg_apple, "红果公司"),
    ("bg_office_modern", bg_office_modern, "现代科技公司"),
    ("bg_black", bg_black, "黑屏"),
]

for name, func, desc in backgrounds:
    print(f"生成 {name} ({desc})...")
    img = func()
    save(img, name)
    print()

print(f"=== 全部 {len(backgrounds)} 张核心背景图生成完成 ===")
print(f"目录: {BG_DIR}")
