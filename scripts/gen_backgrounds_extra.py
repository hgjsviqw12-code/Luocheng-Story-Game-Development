from PIL import Image, ImageDraw
import os
import math
import random

random.seed(666)

BG_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
PW, PH = 160, 90
SCALE = 6
FW, FH = PW * SCALE, PH * SCALE

def upscale(img):
    return img.resize((FW, FH), Image.NEAREST)

def save(img, name):
    path = os.path.join(BG_DIR, name + ".png")
    img.save(path, "PNG")
    print(f"  Saved: {name}.png")

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

def vgrad(d, colors, y0=0, y1=None):
    if y1 is None: y1 = PH
    h = y1 - y0
    n = len(colors) - 1
    for y in range(y0, y1):
        t = (y - y0) / max(1, h - 1) * n
        idx = min(int(t), n - 1)
        f = t - idx
        c0, c1 = colors[idx], colors[idx + 1]
        r = int(c0[0] + (c1[0] - c0[0]) * f)
        g = int(c0[1] + (c1[1] - c0[1]) * f)
        b = int(c0[2] + (c1[2] - c0[2]) * f)
        for x in range(PW):
            put(d, x, y, (r, g, b))


# 1. classroom - 高中教室
def bg_classroom():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(180, 200, 230), (200, 220, 245)], 0, 40)
    rect(d, 0, 40, PW, PH-40, (230, 225, 210))
    rect(d, 0, 72, PW, PH-72, (160, 130, 90))
    # 黑板
    rect(d, 35, 8, 90, 28, (30, 60, 40))
    rect(d, 37, 10, 86, 24, (25, 50, 35))
    # 黑板字
    rect(d, 45, 14, 20, 2, (220, 220, 200))
    rect(d, 45, 18, 35, 2, (220, 220, 200))
    rect(d, 45, 22, 30, 2, (220, 220, 200))
    # 黑板边框
    rect(d, 35, 8, 90, 2, (100, 80, 60))
    rect(d, 35, 34, 90, 2, (100, 80, 60))
    rect(d, 35, 8, 2, 28, (100, 80, 60))
    rect(d, 123, 8, 2, 28, (100, 80, 60))
    # 讲台
    rect(d, 60, 38, 40, 5, (120, 90, 60))
    rect(d, 78, 38, 4, 8, (80, 60, 40))
    rect(d, 118, 38, 4, 8, (80, 60, 40))
    # 课桌椅
    for rx in [15, 45, 75, 105, 135]:
        rect(d, rx-6, 55, 12, 3, (100, 80, 60))  # 桌
        rect(d, rx+4, 58, 3, 10, (80, 60, 40))   # 桌腿
        rect(d, rx+4, 68, 3, 10, (80, 60, 40))   # 桌腿
        rect(d, rx+12, 55, 5, 3, (80, 60, 50))   # 椅背
        rect(d, rx+13, 58, 4, 8, (60, 45, 35))   # 椅座
    # 窗户
    for wx in [0, 40, 80, 120]:
        rect(d, wx, 2, 35, 20, (180, 210, 230))
        rect(d, wx, 2, 35, 1, (220, 230, 240))
        rect(d, wx+17, 2, 1, 20, (220, 230, 240))
        rect(d, wx, 11, 35, 1, (220, 230, 240))
    # 天花板荧光灯
    for lx in [20, 70, 120]:
        rect(d, lx, 1, 20, 2, (220, 220, 210))
    # 墙上挂钟
    ellip(d, 140, 15, 5, 5, (200, 200, 200))
    ellip(d, 140, 15, 3, 3, (240, 240, 240))
    put(d, 140, 14, (50, 50, 60))
    for a in range(0, 360, 90):
        rx = int(140 + 2 * math.cos(math.radians(a)))
        ry = int(15 + 2 * math.sin(math.radians(a)))
        put(d, rx, ry, (80, 80, 100))
    return upscale(img)


# 2. noodle_shop - 面馆
def bg_noodle_shop():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(60, 40, 30), (120, 80, 50), (80, 50, 35)], 0, PH)
    # 墙壁（暖黄色）
    rect(d, 0, 0, PW, 55, (140, 100, 65))
    # 地面（木地板）
    rect(d, 0, 55, PW, PH-55, (100, 70, 40))
    for y in range(55, PH, 3):
        for x in range(0, PW, 15):
            put(d, x, y, (85, 58, 32))
    # 吧台
    rect(d, 0, 45, PW, 15, (160, 120, 70))
    rect(d, 0, 45, PW, 2, (200, 160, 100))
    rect(d, 0, 60, 3, 30, (120, 90, 50))
    rect(d, PW-3, 60, 3, 30, (120, 90, 50))
    # 木凳
    for bx in [15, 55, 95, 135]:
        rect(d, bx, 65, 12, 4, (130, 95, 55))
        rect(d, bx+2, 69, 2, 15, (100, 70, 40))
        rect(d, bx+8, 69, 2, 15, (100, 70, 40))
    # 碗（吧台上）
    for wx in [25, 60, 95, 130]:
        ellip(d, wx, 41, 6, 3, (240, 230, 210))
        ellip(d, wx, 40, 5, 2, (200, 160, 100))
        put(d, wx, 39, (255, 220, 150))
        for dx in range(-3, 4):
            put(d, wx+dx, 38, (255, 220, 150))
    # 蒸汽
    for wx in [25, 60, 95, 130]:
        for i in range(6):
            if random.random() < 0.5:
                put(d, wx + random.randint(-2, 2), 35 - i*2, (200, 180, 160))
    # 挂着的筷子/勺子
    rect(d, 80, 20, 2, 15, (180, 150, 100))
    rect(d, 78, 20, 8, 2, (180, 150, 100))
    for dx in range(0, 8, 2):
        rect(d, 78+dx, 22, 1, 8, (200, 170, 120))
    # 窗户（暖光透进来）
    for wx in [0, 80]:
        rect(d, wx, 8, 35, 20, (255, 220, 150))
        rect(d, wx, 8, 35, 2, (200, 180, 140))
    # 招牌
    rect(d, 55, 2, 50, 10, (180, 80, 40))
    rect(d, 57, 4, 46, 6, (220, 120, 60))
    # 灯泡
    for lx in [40, 100, 145]:
        rect(d, lx-2, 3, 4, 5, (80, 60, 40))
        ellip(d, lx, 10, 6, 6, (255, 220, 150))
        for r in range(12):
            for a in range(0, 360, 15):
                rx2 = int(lx + r * 0.7 * math.cos(math.radians(a)))
                ry2 = int(10 + r * 0.7 * math.sin(math.radians(a)))
                if random.random() < 0.25:
                    put(d, rx2, ry2, (255, 220, 120))
    return upscale(img)


# 3. bar - 酒吧
def bg_bar():
    img = Image.new("RGB", (PW, PH), (10, 5, 20))
    d = ImageDraw.Draw(img)
    vgrad(d, [(15, 8, 30), (30, 15, 50), (20, 10, 35)], 0, PH)
    # 墙面（深色砖墙）
    rect(d, 0, 0, PW, 55, (35, 25, 35))
    for y in range(0, 55, 4):
        for x in range(0, PW, 12):
            put(d, x + (y//4 % 2)*6, y, (42, 30, 42))
            put(d, x + (y//4 % 2)*6 + 1, y, (30, 20, 30))
    # 地板
    rect(d, 0, 55, PW, PH-55, (30, 20, 25))
    for y in range(55, PH, 3):
        for x in range(0, PW, 20):
            put(d, x, y, (25, 15, 20))
    # 吧台
    rect(d, 0, 45, PW, 15, (60, 40, 50))
    rect(d, 0, 45, PW, 2, (80, 60, 70))
    rect(d, 0, 60, 3, 30, (45, 30, 40))
    rect(d, PW-3, 60, 3, 30, (45, 30, 40))
    # 酒瓶（吧台上）
    colors_bottle = [(150, 50, 50), (50, 100, 50), (200, 180, 50), (100, 80, 180), (180, 120, 50)]
    for bx in [15, 35, 55, 75, 95, 115, 135]:
        c = colors_bottle[(bx//20) % len(colors_bottle)]
        rect(d, bx, 38, 5, 8, c)
        rect(d, bx+1, 36, 3, 3, (80, 60, 50))
    # 霓虹灯招牌
    for nx, nc in [(20, (255, 50, 80)), (80, (50, 150, 255)), (130, (255, 200, 50))]:
        for r in range(6):
            for a in range(0, 360, 15):
                rx2 = int(nx + r * 0.5 * math.cos(math.radians(a)))
                ry2 = int(15 + r * 0.5 * math.sin(math.radians(a)))
                put(d, rx2, ry2, nc)
        rect(d, nx-4, 12, 8, 6, (20, 15, 25))
    # 霓虹灯光晕
    for nx in [20, 80, 130]:
        for r in range(20):
            for a in range(0, 360, 20):
                rx2 = int(nx + r * math.cos(math.radians(a)))
                ry2 = int(15 + r * 0.5 * math.sin(math.radians(a)))
                if random.random() < 0.2:
                    put(d, rx2, ry2, (40, 10, 40))
    # 凳子
    for sx in [20, 50, 80, 110, 140]:
        rect(d, sx-3, 62, 6, 3, (60, 45, 55))
        ellip(d, sx, 66, 5, 4, (50, 38, 48))
        rect(d, sx-1, 70, 2, 12, (40, 30, 40))
    # 镜子（吧台后）
    rect(d, 5, 10, 80, 25, (50, 55, 65))
    rect(d, 6, 11, 78, 23, (60, 65, 80))
    # 酒杯反光
    for gx in [30, 65, 100]:
        ellip(d, gx, 42, 3, 2, (200, 220, 240))
    return upscale(img)


# 4. street_food - 路边摊
def bg_street_food():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(10, 15, 40), (60, 40, 80), (100, 70, 50), (80, 50, 30)], 0, PH)
    # 地面（油污地砖）
    rect(d, 0, 60, PW, PH-60, (50, 40, 30))
    for y in range(60, PH, 4):
        for x in range(0, PW, 8):
            put(d, x, y, (40, 30, 20))
    # 小推车
    rect(d, 40, 35, 80, 20, (180, 140, 80))
    rect(d, 42, 37, 76, 16, (200, 160, 100))
    rect(d, 40, 55, 5, 12, (120, 90, 60))
    rect(d, 115, 55, 5, 12, (120, 90, 60))
    # 推车上的食材
    for fx in [50, 65, 80, 95, 110]:
        c = [(255, 200, 100), (200, 100, 60), (80, 160, 80), (255, 180, 80), (220, 180, 150)]
        ellip(d, fx, 34, 6, 4, c[(fx//15)%5])
    # 蒸汽
    for sx in [60, 85, 100]:
        for i in range(5):
            if random.random() < 0.4:
                put(d, sx + random.randint(-2, 2), 30 - i*3, (200, 180, 160))
    # 灯泡/灯笼
    for lx in [30, 80, 130]:
        ellip(d, lx, 18, 5, 6, (255, 200, 80))
        for r in range(15):
            for a in range(0, 360, 20):
                rx2 = int(lx + r * 0.6 * math.cos(math.radians(a)))
                ry2 = int(18 + r * 0.6 * math.sin(math.radians(a)))
                if random.random() < 0.3:
                    put(d, rx2, ry2, (255, 200, 100))
    # 远处的夜宵摊
    rect(d, 5, 45, 30, 12, (140, 100, 60))
    for fx in [10, 20, 28]:
        ellip(d, fx, 44, 4, 3, (200, 150, 80))
    # 远处骑楼下的人影
    for px in [10, 145]:
        rect(d, px, 55, 6, 15, (15, 12, 20))
        ellip(d, px+3, 53, 3, 3, (15, 12, 20))
    return upscale(img)


# 5. venue - 发布会场馆
def bg_venue():
    img = Image.new("RGB", (PW, PH), (5, 5, 15))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (8, 6, 20))
    # 舞台背景（大屏幕）
    rect(d, 10, 5, 140, 45, (20, 25, 50))
    rect(d, 12, 7, 136, 41, (15, 20, 45))
    # 屏幕内容（假想的产品图）
    for dx in range(30, 130, 20):
        rect(d, dx, 12, 15, 25, (40, 50, 80))
        rect(d, dx+2, 14, 11, 18, (80, 120, 180))
    rect(d, 60, 20, 40, 2, (200, 220, 240))
    rect(d, 70, 25, 20, 1, (200, 220, 240))
    # 聚光灯（舞台上方）
    for sx in [30, 80, 130]:
        for r in range(30):
            spread = int(r * 1.5)
            b = max(0, 40 - r)
            for dx in range(-spread, spread+1, 2):
                rx2 = sx + dx
                ry2 = 5 + r
                if rx2 < PW and ry2 < PH:
                    put(d, rx2, ry2, (b, b//2, b//3))
    # 讲台
    rect(d, 55, 50, 50, 8, (60, 50, 70))
    rect(d, 57, 52, 46, 4, (80, 70, 90))
    rect(d, 78, 58, 4, 20, (50, 40, 55))
    # 麦克风
    rect(d, 78, 40, 4, 12, (30, 30, 40))
    ellip(d, 80, 40, 3, 3, (40, 40, 50))
    # 观众席（远景，人影）
    for y in range(62, 75, 5):
        for x in range(0, PW, 8):
            if random.random() < 0.6:
                c = (30, 25, 40) if random.random() < 0.7 else (50, 45, 60)
                ellip(d, x+4, y, 4, 5, c)
                rect(d, x+2, y+5, 4, 8, c)
    # 场地地面
    rect(d, 0, 75, PW, PH-75, (20, 18, 30))
    for y in range(75, PH, 2):
        for x in range(0, PW, 10):
            if random.random() < 0.2:
                put(d, x, y, (15, 12, 25))
    return upscale(img)


# 6. celebration - 庆功宴
def bg_celebration():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(40, 20, 60), (80, 30, 50), (60, 20, 40), (40, 20, 30)], 0, PH)
    # 墙壁（暖红金色）
    rect(d, 0, 0, PW, 55, (80, 30, 30))
    rect(d, 0, 0, PW, 3, (200, 150, 50))
    # 横幅
    rect(d, 20, 8, 120, 12, (180, 50, 50))
    rect(d, 22, 10, 116, 8, (200, 80, 80))
    # 横幅字
    for dx in [30, 50, 70, 90, 110, 130]:
        put(d, dx, 13, (255, 220, 100))
    # 圆桌
    ellip(d, 80, 60, 40, 20, (120, 80, 50))
    ellip(d, 80, 60, 38, 18, (160, 110, 70))
    # 桌上的菜
    for px, py, c in [(60, 55, (200, 150, 80)), (80, 53, (180, 120, 60)), (100, 56, (220, 170, 100))]:
        ellip(d, px, py, 6, 4, c)
    # 酒杯
    for wx in [50, 70, 90, 110]:
        ellip(d, wx, 57, 3, 2, (240, 230, 180))
        rect(d, wx-1, 53, 2, 5, (200, 180, 140))
    # 椅子（围着桌子）
    for a in range(0, 360, 45):
        sx = int(80 + 45 * math.cos(math.radians(a)))
        sy = int(60 + 22 * math.sin(math.radians(a)))
        ellip(d, sx, sy, 6, 5, (100, 70, 60))
    # 灯笼/彩灯
    for lx in [15, 40, 65, 90, 115, 145]:
        ellip(d, lx, 5, 5, 6, (255, 100, 50))
        for r in range(8):
            for a in range(0, 360, 20):
                rx2 = int(lx + r * 0.5 * math.cos(math.radians(a)))
                ry2 = int(5 + r * 0.5 * math.sin(math.radians(a)))
                if random.random() < 0.3:
                    put(d, rx2, ry2, (255, 80, 30))
    # 地面
    rect(d, 0, 72, PW, PH-72, (60, 40, 35))
    for y in range(72, PH, 4):
        for x in range(0, PW, 15):
            put(d, x, y, (45, 30, 25))
    return upscale(img)


# 7. bookstore - 书店
def bg_bookstore():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(40, 30, 20), (80, 55, 35), (60, 40, 25)], 0, PH)
    # 书架
    rect(d, 0, 0, 45, PH, (100, 65, 35))
    rect(d, 0, 0, 45, 3, (120, 80, 45))
    for y in range(8, PH, 12):
        rect(d, 0, y, 45, 2, (80, 50, 25))
        # 书架上的书
        x = 2
        while x < 43:
            w = random.randint(2, 5)
            h = 8
            c = random.choice([(180, 60, 60), (60, 80, 140), (200, 160, 60), (100, 100, 80), (160, 80, 120), (80, 60, 150)])
            rect(d, x, y+2, w, h, c)
            x += w + 1
    # 右侧书架
    rect(d, 115, 0, 45, PH, (100, 65, 35))
    rect(d, 115, 0, 45, 3, (120, 80, 45))
    for y in range(8, PH, 12):
        rect(d, 115, y, 45, 2, (80, 50, 25))
        x = 117
        while x < 158:
            w = random.randint(2, 5)
            h = 8
            c = random.choice([(180, 60, 60), (60, 80, 140), (200, 160, 60), (100, 100, 80), (160, 80, 120), (80, 60, 150)])
            rect(d, x, y+2, w, h, c)
            x += w + 1
    # 中间过道（暖木地板）
    rect(d, 45, 55, 70, PH-55, (130, 90, 55))
    for y in range(55, PH, 5):
        for x in range(45, 115, 18):
            put(d, x, y, (110, 75, 45))
    # 阅读灯
    for lx in [55, 80, 105]:
        ellip(d, lx, 45, 8, 5, (255, 220, 150))
        rect(d, lx-2, 35, 4, 12, (80, 60, 40))
        for r in range(20):
            for a in range(0, 360, 15):
                rx2 = int(lx + r * 0.4 * math.cos(math.radians(a)))
                ry2 = int(45 + r * 0.3 * math.sin(math.radians(a)))
                if random.random() < 0.25:
                    put(d, rx2, ry2, (200, 170, 100))
    # 窗（傍晚光线）
    rect(d, 50, 2, 60, 25, (200, 180, 120))
    rect(d, 50, 2, 60, 2, (240, 220, 160))
    # 旧书桌
    rect(d, 60, 62, 40, 5, (100, 65, 35))
    rect(d, 62, 67, 3, 15, (80, 50, 30))
    rect(d, 97, 67, 3, 15, (80, 50, 30))
    # 桌上的旧书
    rect(d, 65, 58, 15, 5, (180, 130, 80))
    rect(d, 75, 59, 12, 4, (160, 110, 70))
    return upscale(img)


# 8. corridor - 走廊
def bg_corridor():
    img = Image.new("RGB", (PW, PH), (5, 5, 10))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (12, 10, 18))
    # 天花板
    rect(d, 0, 0, PW, 15, (40, 35, 45))
    # 墙面
    rect(d, 0, 15, 20, 50, (55, 48, 55))  # 左墙
    rect(d, 140, 15, 20, 50, (55, 48, 55))  # 右墙
    # 地板（油光地砖）
    rect(d, 0, 65, PW, PH-65, (30, 28, 35))
    for y in range(65, PH, 3):
        for x in range(0, PW, 10):
            put(d, x, y, (25, 22, 30))
    # 荧光灯（闪烁效果）
    for lx in [40, 80, 120]:
        rect(d, lx, 1, 30, 3, (200, 200, 210))
        for dy in range(3, 8):
            for dx in range(-2, 32):
                if random.random() < 0.3:
                    put(d, lx+dx, dy, (80, 80, 90))
    # 尽头窗户（深夜城市光）
    rect(d, 55, 18, 50, 30, (20, 30, 50))
    for _ in range(30):
        x = random.randint(57, 103)
        y = random.randint(20, 46)
        c = (255, 220, 150) if random.random() < 0.5 else (150, 180, 255)
        put(d, x, y, c)
    # 窗户框
    rect(d, 55, 18, 50, 2, (80, 75, 85))
    rect(d, 55, 46, 50, 2, (80, 75, 85))
    rect(d, 55, 18, 2, 30, (80, 75, 85))
    rect(d, 103, 18, 2, 30, (80, 75, 85))
    rect(d, 79, 18, 2, 30, (80, 75, 85))
    # 地面反光（窗户光）
    for y in range(65, 75):
        for x in range(55, 105):
            if random.random() < 0.3:
                put(d, x, y, (30, 35, 50))
    # 墙上的消防栓
    rect(d, 5, 30, 8, 12, (160, 40, 40))
    rect(d, 6, 31, 6, 10, (180, 50, 50))
    rect(d, 7, 32, 4, 8, (200, 60, 60))
    # 地上烟头（发光）
    for tx, ty in [(35, 70), (50, 73), (110, 71)]:
        ellip(d, tx, ty, 2, 1, (255, 150, 50))
        put(d, tx, ty-2, (200, 200, 200))
    return upscale(img)


# 9. hospital - 医院走廊
def bg_hospital():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (230, 235, 240))
    # 天花板
    rect(d, 0, 0, PW, 15, (245, 248, 252))
    # 墙面（浅绿/白）
    rect(d, 0, 15, PW, 55, (235, 240, 245))
    # 墙裙（淡绿色）
    rect(d, 0, 40, PW, 12, (200, 220, 210))
    rect(d, 0, 40, PW, 2, (170, 195, 180))
    # 地板（浅灰）
    rect(d, 0, 52, PW, PH-52, (220, 220, 225))
    for y in range(52, PH, 4):
        for x in range(0, PW, 12):
            put(d, x, y, (200, 200, 208))
    # 荧光灯管
    for lx in [20, 70, 120]:
        rect(d, lx, 1, 40, 4, (255, 255, 255))
        for dy in range(4, 10):
            for dx in range(0, 40, 2):
                if random.random() < 0.2:
                    put(d, lx+dx, dy, (220, 220, 225))
    # 医院门
    for dx in [10, 60, 110]:
        rect(d, dx, 20, 25, 35, (200, 210, 215))
        rect(d, dx+1, 21, 23, 33, (220, 230, 235))
        rect(d, dx+10, 30, 5, 15, (180, 200, 200))
        rect(d, dx+22, 30, 3, 15, (180, 200, 200))
        # 门上的窗户
        rect(d, dx+3, 22, 19, 10, (180, 200, 200))
    # 候诊椅
    for sx in [5, 45, 85, 125]:
        rect(d, sx, 52, 25, 4, (120, 140, 150))
        for dx in range(0, 25, 5):
            rect(d, sx+dx, 56, 2, 8, (100, 120, 130))
    # 指示牌
    rect(d, 130, 3, 25, 10, (60, 140, 120))
    rect(d, 131, 4, 23, 8, (80, 160, 140))
    # 红十字
    for dx in [-3, 3]:
        rect(d, 140+dx, 5, 2, 6, (220, 50, 50))
    rect(d, 137, 6, 6, 2, (220, 50, 50))
    return upscale(img)


# 10. press - 记者会
def bg_press():
    img = Image.new("RGB", (PW, PH), (5, 5, 15))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (10, 8, 25))
    # 舞台
    rect(d, 0, 20, PW, 50, (25, 28, 40))
    rect(d, 0, 20, PW, 3, (50, 55, 70))
    # 讲台
    rect(d, 50, 30, 60, 20, (40, 45, 60))
    rect(d, 52, 32, 56, 16, (60, 65, 80))
    # 麦克风
    rect(d, 78, 15, 4, 18, (30, 30, 40))
    ellip(d, 80, 15, 4, 4, (50, 50, 60))
    # 背景大屏幕
    rect(d, 10, 22, 130, 25, (15, 20, 40))
    rect(d, 12, 24, 126, 21, (20, 25, 50))
    # 屏幕上的PPT
    for bx in [25, 55, 85, 115]:
        rect(d, bx, 28, 20, 12, (35, 45, 70))
        rect(d, bx+2, 30, 16, 6, (70, 90, 130))
    rect(d, 55, 35, 50, 2, (180, 200, 220))
    # 聚光灯
    for sx in [20, 80, 140]:
        for r in range(40):
            spread = int(r * 0.8)
            b = max(0, 50 - r)
            for dx in range(-spread, spread+1, 3):
                rx2 = sx + dx
                ry2 = 20 + r
                if rx2 < PW and ry2 < PH:
                    put(d, rx2, ry2, (b//3, b//4, b))
    # 闪光灯效果（前景）
    for _ in range(15):
        x = random.randint(5, PW-5)
        y = random.randint(65, 85)
        if random.random() < 0.3:
            c = (255, 255, 240) if random.random() < 0.7 else (255, 220, 150)
            put(d, x, y, c)
    # 前景记者席
    for y in range(68, 88, 4):
        for x in range(0, PW, 6):
            if random.random() < 0.5:
                c = (20, 18, 30) if random.random() < 0.6 else (35, 32, 50)
                ellip(d, x+3, y, 3, 4, c)
    return upscale(img)


# 11. airport - 机场
def bg_airport():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(150, 180, 220), (200, 220, 240), (220, 235, 250)], 0, 35)
    # 候机楼（现代玻璃结构）
    rect(d, 0, 15, PW, 55, (220, 230, 240))
    # 大玻璃窗
    rect(d, 0, 18, PW, 35, (200, 220, 235))
    for wx in range(0, PW, 25):
        rect(d, wx, 18, 2, 35, (220, 235, 245))
    rect(d, 0, 52, PW, 1, (220, 235, 245))
    # 窗外飞机
    rect(d, 20, 30, 100, 15, (220, 225, 230))
    for wx in [30, 50, 70, 90, 110]:
        rect(d, wx, 25, 30, 8, (240, 242, 245))
        rect(d, wx+5, 22, 20, 4, (200, 210, 220))
    # 候机楼内部
    rect(d, 0, 53, PW, PH-53, (230, 232, 238))
    # 地面（光滑地砖）
    for y in range(53, PH, 4):
        for x in range(0, PW, 10):
            put(d, x, y, (215, 218, 225))
    # 座位区
    for sx in [10, 40, 70, 100, 130]:
        rect(d, sx, 62, 20, 5, (140, 150, 165))
        for dx in range(0, 20, 4):
            rect(d, sx+dx, 67, 2, 10, (110, 120, 135))
    # 电子屏幕（航班信息）
    rect(d, 30, 5, 100, 12, (30, 35, 45))
    rect(d, 32, 7, 96, 8, (20, 25, 35))
    for dx in [40, 60, 80, 100, 115]:
        put(d, dx, 10, (255, 200, 50))
    # 柱子
    for px in [15, 75, 145]:
        rect(d, px, 18, 6, 60, (200, 205, 215))
        rect(d, px, 18, 6, 2, (180, 185, 195))
    return upscale(img)


# 12. conference - 大型发布会
def bg_conference():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (8, 6, 18))
    # 舞台
    rect(d, 0, 15, PW, 55, (20, 22, 35))
    # 巨型屏幕
    rect(d, 15, 18, 130, 40, (15, 20, 40))
    rect(d, 17, 20, 126, 36, (20, 25, 50))
    # 屏幕内容（品牌LOGO感）
    ellip(d, 80, 38, 20, 12, (50, 60, 100))
    rect(d, 60, 35, 40, 6, (80, 100, 150))
    for dx in range(5):
        put(d, 65+dx*5, 36, (150, 180, 220))
    # 聚光灯从上方打下来
    for sx in [30, 80, 130]:
        for r in range(50):
            spread = int(r * 1.2)
            b = max(0, 60 - r)
            for dx in range(-spread, spread+1, 3):
                rx2 = sx + dx
                ry2 = 15 + r
                if rx2 < PW and ry2 < PH:
                    put(d, rx2, ry2, (b//4, b//5, b//2))
    # 讲台
    rect(d, 55, 50, 50, 12, (40, 50, 70))
    rect(d, 58, 52, 44, 8, (60, 75, 100))
    # 麦克风
    rect(d, 78, 35, 4, 18, (30, 35, 45))
    ellip(d, 80, 35, 4, 4, (50, 60, 75))
    # 观众席（远景）
    for y in range(67, 85, 4):
        for x in range(0, PW, 7):
            if random.random() < 0.55:
                c = (25, 22, 35) if random.random() < 0.7 else (40, 35, 55)
                ellip(d, x+3, y, 3, 4, c)
    # 地面反光
    rect(d, 0, 85, PW, PH-85, (15, 12, 25))
    return upscale(img)


# 13. balcony - 阳台夜景
def bg_balcony():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    # 夜空
    vgrad(d, [(5, 5, 20), (10, 10, 35), (20, 20, 50)], 0, 50)
    # 城市天际线
    for bx in range(0, PW, 12):
        h = random.randint(10, 30)
        w = random.randint(8, 11)
        rect(d, bx, 50-h, w, h, (15, 18, 30))
        # 窗户灯光
        for wy in range(50-h+3, 50, 4):
            for wx in range(bx+1, bx+w-1, 3):
                if random.random() < 0.4:
                    c = (255, 220, 150) if random.random() < 0.6 else (150, 180, 255)
                    put(d, wx, wy, c)
    # 阳台地面（水泥）
    rect(d, 0, 50, PW, PH-50, (45, 42, 40))
    for y in range(50, PH, 3):
        for x in range(0, PW, 8):
            put(d, x, y, (35, 32, 30))
    # 栏杆
    rect(d, 0, 50, PW, 3, (80, 75, 70))
    for rx in range(3, PW, 10):
        rect(d, rx, 45, 2, 8, (70, 65, 60))
    # 远处的城市灯光
    for _ in range(60):
        x = random.randint(0, PW-1)
        y = random.randint(5, 45)
        c = (255, 230, 150) if random.random() < 0.5 else (150, 180, 255)
        put(d, x, y, c)
    # 月亮
    ellip(d, 135, 15, 8, 8, (240, 230, 200))
    for r in range(15):
        for a in range(0, 360, 15):
            rx2 = int(135 + r * 0.5 * math.cos(math.radians(a)))
            ry2 = int(15 + r * 0.5 * math.sin(math.radians(a)))
            if random.random() < 0.2:
                put(d, rx2, ry2, (200, 190, 160))
    # 地上烟头
    for tx, ty in [(30, 72), (80, 75), (120, 70)]:
        ellip(d, tx, ty, 2, 1, (255, 100, 30))
    # 啤酒瓶
    ellip(d, 60, 70, 3, 4, (60, 100, 50))
    rect(d, 58, 66, 4, 5, (40, 80, 35))
    return upscale(img)


# 14. train_platform - 火车站台
def bg_train_platform():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(20, 25, 50), (40, 45, 70), (60, 55, 65)], 0, 40)
    # 站台地面
    rect(d, 0, 40, PW, PH-40, (80, 70, 60))
    for y in range(40, PH, 4):
        for x in range(0, PW, 12):
            put(d, x, y, (60, 50, 40))
    # 黄线
    rect(d, 0, 40, PW, 2, (220, 200, 50))
    # 站台柱
    for px in [15, 55, 95, 135]:
        rect(d, px, 0, 6, 45, (100, 90, 80))
        rect(d, px, 0, 6, 2, (130, 120, 100))
        rect(d, px, 0, 3, 45, (120, 110, 90))
        # 灯
        ellip(d, px+3, 5, 8, 5, (255, 220, 150))
        for r in range(15):
            for a in range(0, 360, 15):
                rx2 = int(px+3 + r * 0.5 * math.cos(math.radians(a)))
                ry2 = int(5 + r * 0.5 * math.sin(math.radians(a)))
                if random.random() < 0.25:
                    put(d, rx2, ry2, (200, 170, 100))
    # 长椅
    for bx in [25, 85]:
        rect(d, bx, 55, 30, 4, (80, 70, 60))
        rect(d, bx+2, 59, 3, 12, (60, 50, 45))
        rect(d, bx+25, 59, 3, 12, (60, 50, 45))
    # 远处火车
    rect(d, 0, 15, PW, 22, (60, 55, 60))
    for cx in range(0, PW, 15):
        rect(d, cx, 15, 12, 20, (70, 65, 70))
        rect(d, cx+2, 17, 8, 14, (50, 48, 52))
        put(d, cx+6, 19, (200, 200, 200))
    # 行李箱
    for lx, ly in [(40, 65), (95, 63), (130, 66)]:
        ellip(d, lx, ly, 6, 4, (60, 50, 70))
        rect(d, lx-1, ly-4, 2, 5, (50, 40, 60))
    return upscale(img)


# 15. room_rent - 出租屋
def bg_room_rent():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vgrad(d, [(50, 40, 35), (70, 55, 45), (55, 42, 35)], 0, PH)
    # 墙壁（泛黄的白墙）
    rect(d, 0, 0, PW, 60, (120, 105, 80))
    # 地面（木地板）
    rect(d, 0, 60, PW, PH-60, (90, 65, 40))
    for y in range(60, PH, 4):
        for x in range(0, PW, 15):
            put(d, x, y, (75, 52, 32))
    # 窗户（傍晚暖光）
    rect(d, 50, 10, 60, 30, (180, 150, 100))
    rect(d, 50, 10, 60, 2, (200, 170, 120))
    for wx in range(55, 105, 15):
        rect(d, wx, 10, 1, 30, (160, 130, 85))
    rect(d, 50, 24, 60, 1, (160, 130, 85))
    # 窗帘
    for cx in [50, 108]:
        for dy in range(5, 35, 3):
            w = 5 + int(3 * math.sin(dy * 0.3))
            rect(d, cx-w//2, 10+dy, w, 2, (180, 140, 110))
    # 床
    rect(d, 5, 45, 40, 20, (120, 100, 80))
    rect(d, 7, 47, 36, 16, (150, 130, 100))
    # 被子
    rect(d, 8, 48, 34, 10, (180, 160, 130))
    # 枕头
    ellip(d, 12, 48, 8, 4, (220, 200, 180))
    ellip(d, 30, 48, 8, 4, (220, 200, 180))
    # 床头柜
    rect(d, 5, 60, 10, 10, (100, 70, 45))
    # 台灯
    rect(d, 8, 35, 4, 12, (60, 45, 30))
    ellip(d, 10, 34, 8, 6, (255, 220, 150))
    for r in range(15):
        for a in range(0, 360, 15):
            rx2 = int(10 + r * 0.4 * math.cos(math.radians(a)))
            ry2 = int(34 + r * 0.3 * math.sin(math.radians(a)))
            if random.random() < 0.25:
                put(d, rx2, ry2, (200, 170, 100))
    # 墙上贴的纸
    rect(d, 125, 20, 15, 12, (230, 220, 200))
    rect(d, 126, 21, 13, 10, (245, 240, 225))
    # 书桌
    rect(d, 120, 55, 35, 4, (100, 70, 45))
    rect(d, 122, 59, 3, 12, (80, 55, 35))
    rect(d, 150, 59, 3, 12, (80, 55, 35))
    # 桌上电脑
    rect(d, 125, 48, 12, 8, (30, 30, 40))
    rect(d, 126, 49, 10, 5, (50, 100, 150))
    return upscale(img)


# 16. office_startup - 备用初创（与startup略有不同风格）
def bg_office_startup():
    img = Image.new("RGB", (PW, PH), (40, 50, 70))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, 60, (55, 65, 80))
    # 窗户
    rect(d, 100, 8, 50, 30, (160, 190, 220))
    for wx in [110, 130, 150]:
        rect(d, wx, 8, 1, 30, (180, 205, 230))
    rect(d, 100, 22, 50, 1, (180, 205, 230))
    # 白板
    rect(d, 8, 12, 35, 22, (230, 230, 220))
    rect(d, 8, 12, 35, 1, (180, 180, 170))
    rect(d, 8, 33, 35, 1, (180, 180, 170))
    for dx in [12, 18, 24, 30]:
        rect(d, dx, 15, 1, 17, (60, 60, 70))
    # 桌子和电脑（拥挤）
    for dx in [35, 65, 95]:
        rect(d, dx, 55, 28, 3, (110, 85, 55))
        rect(d, dx+6, 48, 8, 8, (30, 30, 40))
        rect(d, dx+7, 49, 6, 5, (80, 150, 200))
    # 地面
    rect(d, 0, 70, PW, PH-70, (70, 55, 40))
    # 披萨盒
    rect(d, 60, 65, 12, 5, (220, 195, 145))
    # 咖啡杯
    for cx in [45, 78, 112]:
        rect(d, cx, 52, 4, 4, (55, 45, 35))
    return upscale(img)


# ========== 生成所有补充背景图 ==========
print("=== 生成16张补充像素风背景图 ===")
backgrounds = [
    ("bg_classroom", bg_classroom, "高中教室"),
    ("bg_noodle_shop", bg_noodle_shop, "面馆"),
    ("bg_bar", bg_bar, "酒吧"),
    ("bg_street_food", bg_street_food, "路边摊"),
    ("bg_venue", bg_venue, "发布会场馆"),
    ("bg_celebration", bg_celebration, "庆功宴"),
    ("bg_bookstore", bg_bookstore, "书店"),
    ("bg_corridor", bg_corridor, "走廊"),
    ("bg_hospital", bg_hospital, "医院"),
    ("bg_press", bg_press, "记者会"),
    ("bg_airport", bg_airport, "机场"),
    ("bg_conference", bg_conference, "大型发布会"),
    ("bg_balcony", bg_balcony, "阳台夜景"),
    ("bg_train_platform", bg_train_platform, "火车站台"),
    ("bg_room_rent", bg_room_rent, "出租屋"),
    ("bg_office_startup", bg_office_startup, "备用初创办公室"),
]
for name, func, desc in backgrounds:
    print(f"生成 {name} ({desc})...")
    img = func()
    save(img, name)
print(f"\n=== 16张补充背景图全部完成 ===")
print(f"目录: {BG_DIR}")
