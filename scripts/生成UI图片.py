"""
生成《老罗的故事》游戏UI界面图片
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 窗口尺寸
WIDTH = 960
HEIGHT = 600

# 颜色
BG_COLOR = (26, 26, 46)  # 深蓝黑色
STATUS_BAR_BG = (45, 45, 68)
DIALOG_BG = (30, 30, 50)
DIALOG_BORDER = (61, 61, 92)
ACCENT_RED = (233, 69, 96)
ACCENT_GOLD = (246, 224, 94)
TEXT_WHITE = (224, 224, 224)
TEXT_GRAY = (160, 160, 160)
HIDDEN_PURPLE = (159, 122, 234)

def create_game_ui():
    # 创建空白图片
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 尝试加载字体
    try:
        font_title = ImageFont.truetype("msyh.ttc", 16)  # 微软雅黑
        font_large = ImageFont.truetype("msyh.ttc", 24)
        font_small = ImageFont.truetype("msyh.ttc", 14)
        font_text = ImageFont.truetype("msyh.ttc", 13)
    except:
        font_title = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # ============ 顶部状态栏 ============
    draw.rectangle([0, 0, WIDTH, 40], fill=STATUS_BAR_BG)
    draw.line([(0, 39), (WIDTH, 39)], fill=(61, 61, 92))

    # 资金状态
    draw.text((20, 12), "💰 资金: 负债6亿", font=font_small, fill=(245, 101, 101))

    # 口碑状态
    draw.text((180, 12), "⭐ 口碑: ★★☆☆☆", font=font_small, fill=(246, 224, 94))

    # 当前幕数
    title_text = "【第一幕：至暗时刻】"
    title_width = draw.textlength(title_text, font=font_small) if hasattr(draw, 'textlength') else 120
    draw.text((WIDTH - title_width - 20, 12), title_text, font=font_small, fill=ACCENT_RED)

    # ============ 场景区域 ============
    # 背景渐变效果（用几个矩形模拟）
    for y in range(40, 400):
        ratio = (y - 40) / 360
        r = int(13 + ratio * 20)
        g = int(27 + ratio * 15)
        b = int(46 + ratio * 20)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # 窗户灯光效果
    draw.rectangle([780, 50, 860, 170], fill=(50, 45, 40))
    draw.rectangle([783, 53, 857, 167], fill=(60, 55, 50))
    # 窗户格子
    draw.line([(820, 53), (820, 167)], fill=(40, 35, 30), width=2)
    draw.line([(783, 110), (857, 110)], fill=(40, 35, 30), width=2)
    # 窗户光晕
    for i in range(5):
        alpha = 30 - i * 5
        draw.rectangle([775 - i*3, 45 - i*2, 865 + i*3, 175 + i*2],
                       outline=(255, 220, 150, alpha) if hasattr(draw, 'rectangle') else (255, 220, 150))

    # 桌上文件（债务账单）
    # 文件1
    draw.polygon([(400, 320), (470, 310), (480, 390), (410, 400)], fill=(255, 220, 220))
    draw.polygon([(400, 320), (470, 310), (465, 320), (395, 330)], fill=(255, 180, 180))
    # 文件2
    draw.polygon([(430, 325), (500, 315), (510, 395), (440, 405)], fill=(255, 255, 255))
    # 文件3
    draw.polygon([(460, 318), (530, 308), (540, 388), (470, 398)], fill=(255, 230, 200))

    # ============ 角色立绘区域 ============
    # 立绘背景框
    draw.rectangle([60, 100, 240, 380], fill=(61, 55, 80), outline=(74, 74, 106), width=2)

    # 角色头部（圆形）
    draw.ellipse([110, 130, 190, 210], fill=(245, 222, 179))
    # 头发
    draw.polygon([(105, 150), (195, 150), (195, 130), (150, 110), (105, 130)], fill=(44, 44, 44))
    # 眼睛
    draw.ellipse([125, 165, 135, 175], fill=(44, 44, 44))
    draw.ellipse([165, 165, 175, 175], fill=(44, 44, 44))
    # 身体（西装）
    draw.polygon([(80, 210), (220, 210), (230, 380), (70, 380)], fill=(30, 30, 50))
    # 西装领子
    draw.polygon([(130, 210), (150, 260), (170, 210)], fill=(200, 50, 50))

    # 角色名字标签
    name_text = "老罗"
    draw.rounded_rectangle([90, 385, 160, 410], radius=10, fill=ACCENT_RED)
    draw.text((100, 390), name_text, font=font_small, fill=(255, 255, 255))

    # ============ 对话框 ============
    dlg_x, dlg_y = 280, 390
    dlg_w, dlg_h = 640, 150

    # 对话框背景
    draw.rounded_rectangle([dlg_x, dlg_y, dlg_x + dlg_w, dlg_y + dlg_h],
                           radius=12, fill=DIALOG_BG, outline=DIALOG_BORDER, width=2)

    # 对话框顶部装饰线
    draw.line([(dlg_x + 20, dlg_y + 2), (dlg_x + dlg_w - 20, dlg_y + 2)],
              fill=ACCENT_RED, width=2)

    # 说话者名字
    draw.text((dlg_x + 15, dlg_y + 15), "老罗", font=font_small, fill=ACCENT_RED)

    # 对话文本（分两行）
    text1 = "银行又打电话来了...说我的贷款已经"
    text2 = "逾期"
    text3 = "了。锤子科技的资金链...真的撑不住了。"

    y_pos = dlg_y + 45
    draw.text((dlg_x + 15, y_pos), text1, font=font_text, fill=TEXT_WHITE)

    # 高亮"逾期"
    if hasattr(draw, 'textlength'):
        x_逾期 = dlg_x + 15 + draw.textlength(text1, font=font_text)
        draw.text((x_逾期, y_pos), text2, font=font_text, fill=ACCENT_GOLD)
        x_cont = x_逾期 + draw.textlength(text2, font=font_text)
    else:
        draw.text((dlg_x + 15 + len(text1) * 7, y_pos), text2, font=font_text, fill=ACCENT_GOLD)
        x_cont = dlg_x + 15 + (len(text1) + len(text2)) * 7

    draw.text((x_cont, y_pos), text3, font=font_text, fill=TEXT_WHITE)

    # 第二行文本
    draw.text((dlg_x + 15, y_pos + 30), "桌上堆满了债务账单和供应商的催款函...", font=font_text, fill=TEXT_WHITE)

    # 点击提示
    click_hint = "▼ 点击继续"
    hint_width = draw.textlength(click_hint, font=font_small) if hasattr(draw, 'textlength') else 60
    draw.text((dlg_x + dlg_w - hint_width - 15, dlg_y + dlg_h - 30),
              click_hint, font=font_small, fill=(100, 100, 100))

    # ============ 底部工具栏 ============
    draw.rectangle([0, HEIGHT - 50, WIDTH, HEIGHT], fill=(21, 21, 42))
    draw.line([(0, HEIGHT - 51), (WIDTH, HEIGHT - 51)], fill=(61, 61, 92))

    # 工具栏按钮
    tools = [("💾", "存档"), ("📂", "读档"), ("⚙", "设置"), ("📖", "图鉴"), ("✕", "退出")]
    spacing = WIDTH // 6

    for i, (icon, label) in enumerate(tools):
        x = spacing * (i + 1) - 30
        y = HEIGHT - 40
        # 按钮区域
        draw.rounded_rectangle([x - 10, y - 5, x + 50, y + 30], radius=6, fill=(61, 61, 92))
        draw.text((x, y - 3), icon, font=font_small, fill=TEXT_GRAY)
        draw.text((x + 20, y - 3), label, font=font_small, fill=TEXT_GRAY)

    # ============ 选择面板（右侧半透明显示）============
    # 为了展示效果，在右侧显示选择面板的示意
    choice_x, choice_y = 300, 395
    choice_w, choice_h = 600, 145

    # 选择面板边框
    draw.rounded_rectangle([choice_x, choice_y, choice_x + choice_w, choice_y + choice_h],
                           radius=12, fill=(30, 30, 50, 240), outline=ACCENT_RED, width=2)

    # 选择标题
    choice_title = "【关键抉择】你站在人生的十字路口，你会怎么做？"
    title_w = draw.textlength(choice_title, font=font_small) if hasattr(draw, 'textlength') else 200
    draw.text((choice_x + choice_w//2 - title_w//2, choice_y + 10), choice_title,
              font=font_small, fill=ACCENT_RED)

    # 分隔线
    draw.line([(choice_x + 20, choice_y + 35), (choice_x + choice_w - 20, choice_y + 35)],
              fill=DIALOG_BORDER)

    # 选项
    choices = [
        ("A", "继续死磕手机行业", "风险高，但如果成功回报巨大", False),
        ("B", "转型直播带货", "全新赛道，但你并不懂...", False),
        ("C", "加入小米（雷军邀请）", "稳定，但会失去主导权", False),
        ("D", "加入苹果（库克邀请）", "(隐藏选项) ⭐特殊条件解锁", True),
        ("E", "卖掉公司，彻底退出", "激流勇退，回归平凡人生", False),
    ]

    option_y = choice_y + 45
    for key, text, desc, is_hidden in choices:
        # 选项背景
        opt_color = HIDDEN_PURPLE if is_hidden else (60, 60, 90)
        draw.rounded_rectangle([choice_x + 15, option_y, choice_x + choice_w - 15, option_y + 20],
                               radius=4, fill=(*opt_color, 100) if len(opt_color) == 3 else opt_color)

        # 选项字母
        key_color = HIDDEN_PURPLE if is_hidden else ACCENT_RED
        draw.text((choice_x + 20, option_y + 2), key, font=font_small, fill=key_color)
        draw.text((choice_x + 40, option_y + 2), text, font=font_text, fill=TEXT_WHITE)

        # 选项描述
        draw.text((choice_x + 250, option_y + 2), desc, font=font_small, fill=(136, 136, 136))

        option_y += 22

    return img

if __name__ == "__main__":
    img = create_game_ui()

    # 保存图片
    output_path = r"d:\Story game\游戏UI界面.png"
    img.save(output_path, "PNG")
    print(f"图片已保存到: {output_path}")

    # 同时显示
    img.show()
