from PIL import Image, ImageDraw
import os, math, random

random.seed(777)
BG_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
PW, PH = 160, 90
SCALE = 6
FW, FH = PW * SCALE, PH * SCALE

def upscale(img): return img.resize((FW, FH), Image.NEAREST)
def save(img, name):
    img.save(os.path.join(BG_DIR, name + ".png"), "PNG")
    print(f"  {name}.png")

def put(d, x, y, c):
    if 0 <= x < PW and 0 <= y < PH: d.point((x, y), fill=c)

def rect(d, x, y, w, h, c):
    for dy in range(h):
        for dx in range(w): put(d, x+dx, y+dy, c)

def ellip(d, cx, cy, rx, ry, c):
    for dy in range(-ry, ry+1):
        for dx in range(-rx, rx+1):
            if dx*dx*ry*ry + dy*dy*rx*rx <= rx*rx*ry*ry: put(d, cx+dx, cy+dy, c)

def vg(d, colors, y0=0, y1=None):
    if y1 is None: y1 = PH
    h = y1-y0; n=len(colors)-1
    for y in range(y0, y1):
        t=(y-y0)/max(1,h-1)*n; i=min(int(t),n-1); f=t-i
        c0,c1=colors[i],colors[i+1]
        put(d,0,y,(int(c0[0]+(c1[0]-c0[0])*f),int(c0[1]+(c1[1]-c0[1])*f),int(c0[2]+(c1[2]-c0[2])*f)))
    for y in range(y0, y1):
        for x in range(1,PW): put(d,x,y,put(d,x-1,y) or 0)


# ---------- FIXED vg (proper full-column gradient) ----------
def vg_full(d, colors, y0=0, y1=None):
    if y1 is None: y1 = PH
    h = y1 - y0; n = len(colors) - 1
    for y in range(y0, y1):
        t = (y - y0) / max(1, h - 1) * n
        idx = min(int(t), n - 1)
        f = t - idx
        c0, c1 = colors[idx], colors[idx + 1]
        r = int(c0[0] + (c1[0] - c0[0]) * f)
        g = int(c0[1] + (c1[1] - c0[1]) * f)
        b = int(c0[2] + (c1[2] - c0[2]) * f)
        for x in range(PW):
            d.point((x, y), fill=(r, g, b))


def vg_horiz(d, colors, x0=0, x1=None):
    if x1 is None: x1 = PW
    w = x1 - x0; n = len(colors) - 1
    for x in range(x0, x1):
        t = (x - x0) / max(1, w - 1) * n
        idx = min(int(t), n - 1)
        f = t - idx
        c0, c1 = colors[idx], colors[idx + 1]
        r = int(c0[0] + (c1[0] - c0[0]) * f)
        g = int(c0[1] + (c1[1] - c0[1]) * f)
        b = int(c0[2] + (c1[2] - c0[2]) * f)
        for y in range(PH): d.point((x, y), fill=(r, g, b))


# ========== 缺失的12张 ==========

# 1. bg_office_modern - 现代科技公司
def bg_office_modern():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(200, 215, 230), (220, 230, 245)], 0, 50)
    rect(d, 0, 50, PW, PH-50, (240, 242, 245))
    rect(d, 0, 50, PW, 3, (220, 225, 230))
    # 玻璃幕墙
    rect(d, 0, 0, PW, 50, (195, 215, 230))
    for wx in range(0, PW, 30):
        rect(d, wx, 0, 2, 50, (215, 225, 235))
    rect(d, 0, 48, PW, 2, (210, 218, 225))
    # 窗外城市
    for bx in range(5, PW, 10):
        h = random.randint(8, 25); w = random.randint(5, 9)
        rect(d, bx, 48-h, w, h, (170, 185, 205))
        for wy in range(48-h, 48, 4):
            for wx2 in range(bx+1, bx+w-1, 3):
                if random.random() < 0.5: put(d, wx2, wy, (215, 205, 175))
    # 玻璃隔断
    for gx in [30, 90]:
        rect(d, gx, 0, 2, 60, (200, 210, 220))
        rect(d, gx-1, 0, 1, 60, (220, 228, 235))
    # 会议桌
    rect(d, 50, 62, 60, 5, (195, 170, 140))
    rect(d, 50, 62, 60, 1, (215, 190, 160))
    rect(d, 52, 67, 3, 8, (175, 150, 120))
    rect(d, 105, 67, 3, 8, (175, 150, 120))
    # 会议椅
    for cx in [55, 75, 95]:
        rect(d, cx, 68, 8, 2, (115, 105, 125))
        rect(d, cx+2, 70, 4, 5, (95, 85, 105))
        rect(d, cx, 65, 8, 3, (115, 105, 125))
    for cx in [60, 80, 100]:
        rect(d, cx, 55, 8, 2, (115, 105, 125))
        rect(d, cx, 50, 8, 5, (95, 85, 105))
    # 地面
    rect(d, 0, 70, PW, PH-70, (205, 210, 215))
    for y in range(70, PH, 3):
        for x in range(0, PW, 8):
            if random.random() < 0.15: put(d, x, y, (190, 195, 200))
    # 前台
    rect(d, 130, 55, 25, 10, (225, 225, 235))
    rect(d, 130, 55, 25, 1, (245, 245, 250))
    return upscale(img)


# 2. bg_black - 黑屏
def bg_black():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(0, 0, 2), (5, 5, 12), (2, 2, 8)], 0, PH)
    return upscale(img)


# 3. bg_celebration - 庆功宴
def bg_celebration():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(35, 18, 55), (75, 28, 48), (55, 18, 38), (35, 18, 28)], 0, PH)
    rect(d, 0, 0, PW, 55, (75, 28, 28))
    rect(d, 0, 0, PW, 3, (195, 145, 45))
    # 横幅
    rect(d, 20, 8, 120, 12, (175, 48, 48))
    rect(d, 22, 10, 116, 8, (195, 78, 78))
    for dx in [30, 50, 70, 90, 110, 130]:
        put(d, dx, 13, (250, 215, 95))
    # 圆桌
    ellip(d, 80, 60, 40, 20, (115, 78, 48))
    ellip(d, 80, 60, 38, 18, (155, 108, 68))
    # 菜
    for px, py, c in [(60, 55, (195, 148, 78)), (80, 53, (175, 118, 58)), (100, 56, (215, 168, 98))]:
        ellip(d, px, py, 6, 4, c)
    # 酒杯
    for wx in [50, 70, 90, 110]:
        ellip(d, wx, 57, 3, 2, (235, 228, 178))
        rect(d, wx-1, 53, 2, 5, (195, 178, 138))
    # 椅子
    for a in range(0, 360, 45):
        sx = int(80 + 45*math.cos(math.radians(a)))
        sy = int(60 + 22*math.sin(math.radians(a)))
        ellip(d, sx, sy, 6, 5, (98, 68, 58))
    # 灯笼
    for lx in [15, 40, 65, 90, 115, 145]:
        ellip(d, lx, 5, 5, 6, (250, 98, 48))
        for r in range(8):
            for a in range(0, 360, 20):
                rx2=int(lx+r*0.5*math.cos(math.radians(a)))
                ry2=int(5+r*0.5*math.sin(math.radians(a)))
                if random.random() < 0.3: put(d, rx2, ry2, (250, 78, 28))
    rect(d, 0, 72, PW, PH-72, (55, 38, 32))
    for y in range(72, PH, 4):
        for x in range(0, PW, 15):
            put(d, x, y, (42, 28, 22))
    return upscale(img)


# 4. bg_bookstore - 书店
def bg_bookstore():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(38, 28, 18), (78, 53, 33), (58, 38, 23)], 0, PH)
    # 左书架
    rect(d, 0, 0, 45, PH, (98, 63, 33))
    rect(d, 0, 0, 45, 3, (118, 78, 43))
    for y in range(8, PH, 12):
        rect(d, 0, y, 45, 2, (78, 48, 23))
        x = 2
        while x < 43:
            w = random.randint(2, 5); h = 8
            c = random.choice([(175, 58, 58),(58, 78, 138),(195, 158, 58),(98, 98, 78),(158, 78, 118),(78, 58, 148)])
            rect(d, x, y+2, w, h, c); x += w+1
    # 右书架
    rect(d, 115, 0, 45, PH, (98, 63, 33))
    rect(d, 115, 0, 45, 3, (118, 78, 43))
    for y in range(8, PH, 12):
        rect(d, 115, y, 45, 2, (78, 48, 23))
        x = 117
        while x < 158:
            w = random.randint(2, 5); h = 8
            c = random.choice([(175, 58, 58),(58, 78, 138),(195, 158, 58),(98, 98, 78),(158, 78, 118),(78, 58, 148)])
            rect(d, x, y+2, w, h, c); x += w+1
    # 中间过道
    rect(d, 45, 55, 70, PH-55, (128, 88, 53))
    for y in range(55, PH, 5):
        for x in range(45, 115, 18):
            put(d, x, y, (108, 73, 43))
    # 阅读灯
    for lx in [55, 80, 105]:
        ellip(d, lx, 45, 8, 5, (250, 218, 148))
        rect(d, lx-2, 35, 4, 12, (78, 58, 38))
        for r in range(20):
            for a in range(0, 360, 15):
                rx2=int(lx+r*0.4*math.cos(math.radians(a)))
                ry2=int(45+r*0.3*math.sin(math.radians(a)))
                if random.random() < 0.25: put(d, rx2, ry2, (195, 168, 98))
    # 傍晚光线
    rect(d, 50, 2, 60, 25, (195, 178, 118))
    rect(d, 50, 2, 60, 2, (235, 218, 158))
    # 旧书桌
    rect(d, 60, 62, 40, 5, (98, 63, 33))
    rect(d, 62, 67, 3, 15, (78, 48, 28))
    rect(d, 97, 67, 3, 15, (78, 48, 28))
    rect(d, 65, 58, 15, 5, (178, 128, 78))
    rect(d, 75, 59, 12, 4, (158, 108, 68))
    return upscale(img)


# 5. bg_corridor - 深夜走廊
def bg_corridor():
    img = Image.new("RGB", (PW, PH), (5, 5, 10))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (12, 10, 18))
    rect(d, 0, 0, PW, 15, (38, 33, 43))
    rect(d, 0, 15, 20, 50, (53, 46, 53))
    rect(d, 140, 15, 20, 50, (53, 46, 53))
    rect(d, 0, 65, PW, PH-65, (28, 26, 33))
    for y in range(65, PH, 3):
        for x in range(0, PW, 10):
            put(d, x, y, (23, 20, 28))
    # 荧光灯
    for lx in [40, 80, 120]:
        rect(d, lx, 1, 30, 3, (195, 195, 208))
        for dy in range(3, 8):
            for dx in range(-2, 32):
                if random.random() < 0.3: put(d, lx+dx, dy, (78, 78, 88))
    # 尽头窗户
    rect(d, 55, 18, 50, 30, (18, 28, 48))
    for _ in range(30):
        x=random.randint(57,103); y=random.randint(20,46)
        c=(250,218,148) if random.random()<0.5 else (148,178,250)
        put(d, x, y, c)
    for wx in [55, 103, 79]:
        rect(d, wx, 18, 2, 30, (78, 73, 83))
    rect(d, 55, 18, 50, 2, (78, 73, 83))
    rect(d, 55, 46, 50, 2, (78, 73, 83))
    # 窗户光
    for y in range(65, 75):
        for x in range(55, 105):
            if random.random() < 0.3: put(d, x, y, (28, 33, 48))
    # 消防栓
    rect(d, 5, 30, 8, 12, (158, 38, 38))
    rect(d, 6, 31, 6, 10, (178, 48, 48))
    rect(d, 7, 32, 4, 8, (198, 58, 58))
    # 地上烟头
    for tx, ty in [(35,70),(50,73),(110,71)]:
        ellip(d, tx, ty, 2, 1, (250, 148, 48))
        put(d, tx, ty-2, (198, 198, 198))
    return upscale(img)


# 6. bg_hospital - 医院走廊
def bg_hospital():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (228, 233, 238))
    rect(d, 0, 0, PW, 15, (243, 246, 250))
    rect(d, 0, 15, PW, 55, (233, 238, 243))
    rect(d, 0, 40, PW, 12, (198, 218, 208))
    rect(d, 0, 40, PW, 2, (168, 193, 178))
    rect(d, 0, 52, PW, PH-52, (218, 218, 223))
    for y in range(52, PH, 4):
        for x in range(0, PW, 12):
            put(d, x, y, (198, 198, 206))
    # 荧光灯
    for lx in [20, 70, 120]:
        rect(d, lx, 1, 40, 4, (253, 253, 253))
        for dy in range(4, 10):
            for dx in range(0, 40, 2):
                if random.random() < 0.2: put(d, lx+dx, dy, (218, 218, 223))
    # 门
    for dx in [10, 60, 110]:
        rect(d, dx, 20, 25, 35, (198, 208, 213))
        rect(d, dx+1, 21, 23, 33, (218, 228, 233))
        rect(d, dx+10, 30, 5, 15, (178, 198, 198))
        rect(d, dx+22, 30, 3, 15, (178, 198, 198))
        rect(d, dx+3, 22, 19, 10, (178, 198, 198))
    # 候诊椅
    for sx in [5, 45, 85, 125]:
        rect(d, sx, 52, 25, 4, (118, 138, 148))
        for dx in range(0, 25, 4):
            rect(d, sx+dx, 56, 2, 8, (98, 118, 128))
    # 指示牌
    rect(d, 130, 3, 25, 10, (58, 138, 118))
    rect(d, 131, 4, 23, 8, (78, 158, 138))
    for dx in [-3, 3]: rect(d, 140+dx, 5, 2, 6, (218, 48, 48))
    rect(d, 137, 6, 6, 2, (218, 48, 48))
    return upscale(img)


# 7. bg_press - 记者会
def bg_press():
    img = Image.new("RGB", (PW, PH), (5, 5, 15))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (10, 8, 25))
    rect(d, 0, 20, PW, 50, (25, 28, 40))
    rect(d, 0, 20, PW, 3, (48, 53, 68))
    rect(d, 50, 30, 60, 20, (38, 43, 58))
    rect(d, 52, 32, 56, 16, (58, 63, 78))
    rect(d, 78, 15, 4, 18, (28, 28, 38))
    ellip(d, 80, 15, 4, 4, (48, 48, 58))
    # 屏幕
    rect(d, 10, 22, 130, 25, (15, 20, 40))
    rect(d, 12, 24, 126, 21, (20, 25, 50))
    for bx in [25, 55, 85, 115]:
        rect(d, bx, 28, 20, 12, (35, 45, 70))
        rect(d, bx+2, 30, 16, 6, (68, 88, 128))
    rect(d, 55, 35, 50, 2, (178, 198, 218))
    # 聚光灯
    for sx in [20, 80, 140]:
        for r in range(40):
            spread=int(r*0.8); b=max(0,50-r)
            for dx in range(-spread, spread+1, 3):
                rx2=sx+dx; ry2=20+r
                if rx2<PW and ry2<PH: put(d, rx2, ry2, (b//3, b//4, b))
    # 闪光灯
    for _ in range(15):
        x=random.randint(5,PW-5); y=random.randint(65,85)
        if random.random() < 0.3:
            c=(253,253,238) if random.random()<0.7 else (250,218,148)
            put(d, x, y, c)
    # 记者席
    for y in range(68, 88, 4):
        for x in range(0, PW, 6):
            if random.random() < 0.5:
                c=(20,18,30) if random.random()<0.6 else (35,32,50)
                ellip(d, x+3, y, 3, 4, c)
    return upscale(img)


# 8. bg_airport - 机场
def bg_airport():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(148, 178, 218), (198, 218, 238), (218, 233, 248)], 0, 35)
    rect(d, 0, 15, PW, 55, (218, 228, 238))
    rect(d, 0, 18, PW, 35, (198, 218, 233))
    for wx in range(0, PW, 25):
        rect(d, wx, 18, 2, 35, (218, 233, 243))
    rect(d, 0, 52, PW, 1, (218, 233, 243))
    # 窗外飞机
    rect(d, 20, 30, 100, 15, (218, 223, 228))
    for wx in [30, 50, 70, 90, 110]:
        rect(d, wx, 25, 30, 8, (238, 240, 243))
        rect(d, wx+5, 22, 20, 4, (198, 208, 218))
    rect(d, 0, 53, PW, PH-53, (228, 230, 236))
    for y in range(53, PH, 4):
        for x in range(0, PW, 10):
            put(d, x, y, (213, 216, 223))
    # 座位
    for sx in [10, 40, 70, 100, 130]:
        rect(d, sx, 62, 20, 5, (138, 148, 163))
        for dx in range(0, 20, 4):
            rect(d, sx+dx, 67, 2, 10, (108, 118, 133))
    # 航班屏
    rect(d, 30, 5, 100, 12, (28, 33, 43))
    rect(d, 32, 7, 96, 8, (20, 25, 35))
    for dx in [40, 60, 80, 100, 115]:
        put(d, dx, 10, (250, 198, 48))
    # 柱子
    for px in [15, 75, 145]:
        rect(d, px, 18, 6, 60, (198, 203, 213))
        rect(d, px, 18, 6, 2, (178, 183, 193))
    return upscale(img)


# 9. bg_conference - 大型发布会
def bg_conference():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    rect(d, 0, 0, PW, PH, (8, 6, 18))
    rect(d, 0, 15, PW, 55, (20, 22, 35))
    rect(d, 15, 18, 130, 40, (15, 20, 40))
    rect(d, 17, 20, 126, 36, (20, 25, 50))
    ellip(d, 80, 38, 20, 12, (48, 58, 98))
    rect(d, 60, 35, 40, 6, (78, 98, 148))
    for dx in range(5): put(d, 65+dx*5, 36, (148, 178, 218))
    # 聚光灯
    for sx in [30, 80, 130]:
        for r in range(50):
            spread=int(r*1.2); b=max(0,60-r)
            for dx in range(-spread, spread+1, 3):
                rx2=sx+dx; ry2=15+r
                if rx2<PW and ry2<PH: put(d, rx2, ry2, (b//4, b//5, b//2))
    rect(d, 55, 50, 50, 12, (38, 48, 68))
    rect(d, 58, 52, 44, 8, (58, 73, 98))
    rect(d, 78, 35, 4, 18, (28, 33, 43))
    ellip(d, 80, 35, 4, 4, (48, 58, 73))
    # 观众
    for y in range(67, 85, 4):
        for x in range(0, PW, 7):
            if random.random() < 0.55:
                c=(25,22,35) if random.random()<0.7 else (40,35,55)
                ellip(d, x+3, y, 3, 4, c)
    rect(d, 0, 85, PW, PH-85, (15, 12, 25))
    return upscale(img)


# 10. bg_balcony - 阳台夜景
def bg_balcony():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(5, 5, 20), (10, 10, 35), (20, 20, 50)], 0, 50)
    # 城市天际线
    for bx in range(0, PW, 12):
        h=random.randint(10,30); w=random.randint(8,11)
        rect(d, bx, 50-h, w, h, (15, 18, 30))
        for wy in range(50-h+3, 50, 4):
            for wx2 in range(bx+1, bx+w-1, 3):
                if random.random() < 0.4:
                    c=(250,218,148) if random.random()<0.6 else (148,178,250)
                    put(d, wx2, wy, c)
    rect(d, 0, 50, PW, PH-50, (43, 40, 38))
    for y in range(50, PH, 3):
        for x in range(0, PW, 8):
            put(d, x, y, (33, 30, 28))
    # 栏杆
    rect(d, 0, 50, PW, 3, (78, 73, 68))
    for rx in range(3, PW, 10):
        rect(d, rx, 45, 2, 8, (68, 63, 58))
    # 城市灯光
    for _ in range(60):
        x=random.randint(0,PW-1); y=random.randint(5,45)
        c=(250,228,148) if random.random()<0.5 else (148,178,250)
        put(d, x, y, c)
    # 月亮
    ellip(d, 135, 15, 8, 8, (238, 228, 198))
    for r in range(15):
        for a in range(0, 360, 15):
            rx2=int(135+r*0.5*math.cos(math.radians(a)))
            ry2=int(15+r*0.5*math.sin(math.radians(a)))
            if random.random() < 0.2: put(d, rx2, ry2, (198, 188, 158))
    # 烟头
    for tx, ty in [(30,72),(80,75),(120,70)]:
        ellip(d, tx, ty, 2, 1, (250, 98, 28))
    # 啤酒瓶
    ellip(d, 60, 70, 3, 4, (58, 98, 48))
    rect(d, 58, 66, 4, 5, (38, 78, 33))
    return upscale(img)


# 11. bg_train_platform - 火车站台
def bg_train_platform():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(20, 25, 50), (40, 45, 70), (60, 55, 65)], 0, 40)
    rect(d, 0, 40, PW, PH-40, (78, 68, 58))
    for y in range(40, PH, 4):
        for x in range(0, PW, 12):
            put(d, x, y, (58, 48, 38))
    rect(d, 0, 40, PW, 2, (218, 198, 48))
    # 柱子
    for px in [15, 55, 95, 135]:
        rect(d, px, 0, 6, 45, (98, 88, 78))
        rect(d, px, 0, 6, 2, (128, 118, 98))
        rect(d, px, 0, 3, 45, (118, 108, 88))
        ellip(d, px+3, 5, 8, 5, (250, 218, 148))
        for r in range(15):
            for a in range(0, 360, 15):
                rx2=int(px+3+r*0.5*math.cos(math.radians(a)))
                ry2=int(5+r*0.5*math.sin(math.radians(a)))
                if random.random() < 0.25: put(d, rx2, ry2, (198, 168, 98))
    # 长椅
    for bx in [25, 85]:
        rect(d, bx, 55, 30, 4, (78, 68, 58))
        rect(d, bx+2, 59, 3, 12, (58, 48, 43))
        rect(d, bx+25, 59, 3, 12, (58, 48, 43))
    # 火车
    rect(d, 0, 15, PW, 22, (58, 53, 58))
    for cx in range(0, PW, 15):
        rect(d, cx, 15, 12, 20, (68, 63, 68))
        rect(d, cx+2, 17, 8, 14, (48, 46, 50))
        put(d, cx+6, 19, (198, 198, 198))
    # 行李箱
    for lx, ly in [(40,65),(95,63),(130,66)]:
        ellip(d, lx, ly, 6, 4, (58, 48, 68))
        rect(d, lx-1, ly-4, 2, 5, (48, 38, 58))
    return upscale(img)


# 12. bg_room_rent - 出租屋
def bg_room_rent():
    img = Image.new("RGB", (PW, PH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vg_full(d, [(48, 38, 33), (68, 53, 43), (53, 40, 33)], 0, PH)
    rect(d, 0, 0, PW, 60, (118, 103, 78))
    rect(d, 0, 60, PW, PH-60, (88, 63, 38))
    for y in range(60, PH, 4):
        for x in range(0, PW, 15):
            put(d, x, y, (73, 50, 30))
    # 窗户
    rect(d, 50, 10, 60, 30, (178, 148, 98))
    rect(d, 50, 10, 60, 2, (198, 168, 118))
    for wx in range(55, 105, 15):
        rect(d, wx, 10, 1, 30, (158, 128, 83))
    rect(d, 50, 24, 60, 1, (158, 128, 83))
    # 窗帘
    for cx in [50, 108]:
        for dy in range(5, 35, 3):
            w=5+int(3*math.sin(dy*0.3))
            rect(d, cx-w//2, 10+dy, w, 2, (178, 138, 108))
    # 床
    rect(d, 5, 45, 40, 20, (118, 98, 78))
    rect(d, 7, 47, 36, 16, (148, 128, 98))
    rect(d, 8, 48, 34, 10, (178, 158, 128))
    ellip(d, 12, 48, 8, 4, (218, 198, 178))
    ellip(d, 30, 48, 8, 4, (218, 198, 178))
    # 床头柜
    rect(d, 5, 60, 10, 10, (98, 68, 43))
    # 台灯
    rect(d, 8, 35, 4, 12, (58, 43, 28))
    ellip(d, 10, 34, 8, 6, (250, 218, 148))
    for r in range(15):
        for a in range(0, 360, 15):
            rx2=int(10+r*0.4*math.cos(math.radians(a)))
            ry2=int(34+r*0.3*math.sin(math.radians(a)))
            if random.random() < 0.25: put(d, rx2, ry2, (198, 168, 98))
    # 墙上的纸
    rect(d, 125, 20, 15, 12, (228, 218, 198))
    rect(d, 126, 21, 13, 10, (243, 238, 223))
    # 书桌
    rect(d, 120, 55, 35, 4, (98, 68, 43))
    rect(d, 122, 59, 3, 12, (78, 53, 33))
    rect(d, 150, 59, 3, 12, (78, 53, 33))
    rect(d, 125, 48, 12, 8, (28, 28, 38))
    rect(d, 126, 49, 10, 5, (48, 98, 148))
    return upscale(img)


# ========== 生成缺失的12张 ==========
print("=== 生成缺失的12张背景图 ===")
missing = [
    ("bg_office_modern", bg_office_modern, "现代科技公司"),
    ("bg_black", bg_black, "黑屏"),
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
]
for name, func, desc in missing:
    print(f"生成 {name} ({desc})...", end=" ")
    save(func(), name)
print(f"\n=== 12张全部完成！共 {14+12} 张背景图 ===")
