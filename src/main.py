# -*- coding: utf-8 -*-
"""
《罗诚的故事》 - 多分支剧情选择游戏
Python + Pygame 实现
v2.0 - 添加数值系统、成就系统
"""
import pygame
import json
import os
import sys
import math
import time

# 游戏配置
GAME_TITLE = "罗诚的故事"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# 颜色
COLOR_BG_DARK = (20, 20, 36)
COLOR_BG_LIGHT = (30, 30, 50)
COLOR_DIALOG_BG = (45, 45, 68)
COLOR_DIALOG_BORDER = (100, 100, 130)
COLOR_TEXT_MAIN = (240, 240, 250)
COLOR_TEXT_SOFT = (180, 180, 200)
COLOR_ACCENT_RED = (233, 69, 96)
COLOR_ACCENT_GOLD = (246, 224, 94)
COLOR_ACCENT_PURPLE = (159, 122, 234)
COLOR_ACCENT_GREEN = (72, 187, 120)
COLOR_ACCENT_BLUE = (66, 150, 250)
COLOR_ACCENT_ORANGE = (255, 165, 0)

# 属性颜色
COLOR_IDEAL = (255, 100, 100)      # 理想值 - 红色
COLOR_REALITY = (100, 150, 255)    # 现实值 - 蓝色
COLOR_WARMTH = (255, 180, 100)     # 温情值 - 橙色

# 游戏状态
STATE_TITLE = "title"
STATE_DISCLAIMER = "disclaimer"
STATE_DIALOG = "dialog"
STATE_CHOICE = "choice"
STATE_ENDING = "ending"
STATE_GALLERY = "gallery"
STATE_SAVE = "save"
STATE_SETTINGS = "settings"


class MusicManager:
    """音乐管理器 - 负责背景音乐播放和切换"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.audio_dir = os.path.join(base_dir, "assets", "audio")
        self.enabled = True
        self.volume = 0.5
        self.current_track = None
        self.fade_time = 800  # 淡入淡出时间(ms)

        # 音乐配置：场景/状态 -> 文件名映射
        self.tracks = {
            "menu": "menu.mp3",        # 主菜单
            "story": "story.mp3",      # 主剧情BGM
            "warm": "warm.mp3",        # 温情/回忆场景
            "tense": "tense.mp3",      # 紧张/危机场景
            "ending": "ending.mp3",    # 结局画面
            "celebration": "celebration.mp3",  # 庆功宴/庆祝
        }

        # 场景ID -> 音乐类型的映射
        self.scene_music_map = {
            # 温情/回忆场景
            "intro": "warm",
            "prologue_1_1": "warm",
            "prologue_1_2": "warm",
            "prologue_1_3": "warm",
            "prologue_4_2": "warm",
            "prologue_4_3a": "warm",
            "prologue_4_3b": "warm",
            "prologue_4_3c": "warm",
            "prologue_4_4": "warm",
            "prologue_5_1": "warm",
            "prologue_5_2": "warm",
            "prologue_7_1": "warm",
            "prologue_7_2": "celebration",
            "branch_e_1": "warm",
            "branch_e_2_2": "warm",
            "branch_e_3": "warm",

            # 紧张/危机场景
            "prologue_8": "tense",
            "branch_a_1": "tense",
            "branch_a_2": "tense",
            "branch_a_3": "tense",
            "branch_a_4": "tense",
            "branch_a_5": "tense",
            "branch_a_6": "tense",
            "branch_a_7": "tense",
            "branch_b_4": "tense",
            "branch_b_5": "tense",
            "branch_c_1": "tense",
            "branch_c_2": "tense",
            "branch_c_3": "tense",
            "branch_c_4": "tense",
        }

    def _get_path(self, track_name):
        """获取音乐文件完整路径"""
        filename = self.tracks.get(track_name)
        if not filename:
            return None
        path = os.path.join(self.audio_dir, filename)
        if os.path.exists(path):
            return path
        return None

    def play(self, track_name, loop=-1, fade_ms=None):
        """播放指定音乐
        track_name: 音乐类型名 (menu/story/warm/tense/ending/celebration)
        loop: -1表示无限循环
        fade_ms: 淡入时间(ms)，None表示使用默认值
        """
        if not self.enabled:
            return

        # 如果已经在播放同一首，不重复切换
        if self.current_track == track_name:
            return

        path = self._get_path(track_name)
        if not path:
            return

        fade = fade_ms if fade_ms is not None else self.fade_time

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loop, fade_ms=fade)
            self.current_track = track_name
        except (pygame.error, IOError) as e:
            print(f"[MusicManager] 播放音乐失败: {track_name} - {e}")

    def stop(self, fade_ms=None):
        """停止播放（带淡出）"""
        fade = fade_ms if fade_ms is not None else self.fade_time
        try:
            pygame.mixer.music.fadeout(fade)
        except pygame.error:
            pass
        self.current_track = None

    def set_volume(self, volume):
        """设置音量 0.0-1.0"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def get_volume(self):
        return self.volume

    def toggle(self):
        """切换音乐开关"""
        self.enabled = not self.enabled
        if not self.enabled:
            pygame.mixer.music.stop()
            self.current_track = None
        return self.enabled

    def play_for_scene(self, scene_id):
        """根据场景ID播放对应的音乐"""
        track = self.scene_music_map.get(scene_id)
        if track:
            self.play(track)
        else:
            # 默认播放 story BGM
            self.play("story")


class Game:
    def __init__(self, base_dir=None):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        try:
            icon_path = os.path.join(self.base_dir, "assets", "logo.ico")
            if os.path.exists(icon_path):
                pygame.display.set_icon(pygame.image.load(icon_path))
        except:
            pass
        self.clock = pygame.time.Clock()
        self.font_path = None
        if base_dir:
            self.base_dir = base_dir
        elif '__file__' in globals():
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.base_dir = os.getcwd()
        self.init_fonts()

        # 初始化音乐管理器
        self.music = MusicManager(self.base_dir)

        # 加载剧情数据
        self.story_data = self.load_story()
        self.current_scene_id = "disclaimer"
        self.current_line_index = 0
        self.state = STATE_DISCLAIMER

        # 数值系统
        initial_stats = self.story_data.get("initial_stats", {"ideal": 20, "reality": 20, "warmth": 20})
        self.ideal = initial_stats.get("ideal", 20)      # 理想值
        self.reality = initial_stats.get("reality", 20)  # 现实值
        self.warmth = initial_stats.get("warmth", 20)    # 温情值

        # 游戏进度
        self.story_choices = []
        self.play_count = self.load_play_count()  # 游戏次数

        # 已解锁结局和成就
        self.unlocked_endings = self.load_endings()
        self.unlocked_achievements = self.load_achievements()

        # 文本动画
        self.text_display = ""
        self.text_target = ""
        self.text_timer = 0
        self.text_speed = 25
        self.text_complete = False

        # 存档
        self.save_slots = [None] * 6
        self.load_save_list()

        # UI动画
        self.anim_frame = 0
        self.hover_choice = -1
        self.current_choices = []

        # 当前说话者
        self.current_speaker = "none"
        self.current_character = "none"

        # 加载图片资源
        self.backgrounds = {}
        self.characters = {}
        self.ui_images = {}
        self.load_assets()

        # 当前结局
        self.current_ending = None

        # 当前成就提示
        self.achievement_popup = None
        self.achievement_timer = 0

        # 设置界面状态
        self.settings_reset_hover = False
        self.settings_save_hover = False
        self.show_reset_confirm = False
        self.reset_confirm_yes_rect = None
        self.reset_confirm_no_rect = None
        self.dragging_volume = False

        # 加载音量设置
        self.load_volume_setting()

    def init_fonts(self):
        font_paths = [
            r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\msyh.ttf",
            r"C:\Windows\Fonts\simhei.ttf",
        ]
        for path in font_paths:
            if os.path.exists(path):
                self.font_path = path
                break
        if self.font_path:
            self.font_large = pygame.font.Font(self.font_path, 36)
            self.font_title = pygame.font.Font(self.font_path, 28)
            self.font_name = pygame.font.Font(self.font_path, 22)
            self.font_text = pygame.font.Font(self.font_path, 20)
            self.font_small = pygame.font.Font(self.font_path, 16)
            self.font_tiny = pygame.font.Font(self.font_path, 14)
        else:
            self.font_large = pygame.font.SysFont("arial", 36)
            self.font_title = pygame.font.SysFont("arial", 28)
            self.font_name = pygame.font.SysFont("arial", 22)
            self.font_text = pygame.font.SysFont("arial", 20)
            self.font_small = pygame.font.SysFont("arial", 16)
            self.font_tiny = pygame.font.SysFont("arial", 14)

    def get_file_path(self, filename):
        return os.path.join(self.base_dir, filename)

    def load_assets(self):
        """加载美术资源"""
        # 加载背景图
        bg_dir = self.get_file_path("assets/backgrounds")
        if os.path.exists(bg_dir):
            for filename in os.listdir(bg_dir):
                if filename.endswith(".png"):
                    key = filename[:-4]
                    try:
                        img = pygame.image.load(os.path.join(bg_dir, filename)).convert()
                        self.backgrounds[key] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    except (pygame.error, FileNotFoundError) as e:
                        print(f"加载背景失败 {filename}: {e}")

        # 加载角色头像
        char_dir = self.get_file_path("assets/characters")
        if os.path.exists(char_dir):
            for filename in os.listdir(char_dir):
                if filename.endswith(".png"):
                    key = filename[:-4]
                    try:
                        img = pygame.image.load(os.path.join(char_dir, filename)).convert_alpha()
                        # 头像统一 120x120
                        self.characters[key] = pygame.transform.scale(img, (120, 120))
                    except (pygame.error, FileNotFoundError) as e:
                        print(f"加载头像失败 {filename}: {e}")

    def load_story(self):
        filepath = self.get_file_path("story.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"scenes": {}}

    def load_endings(self):
        filepath = self.get_file_path("endings.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("unlocked", [])
        return []

    def save_endings(self):
        filepath = self.get_file_path("endings.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"unlocked": self.unlocked_endings}, f, ensure_ascii=False)

    def load_achievements(self):
        filepath = self.get_file_path("achievements.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("unlocked", [])
        return []

    def save_achievements(self):
        filepath = self.get_file_path("achievements.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"unlocked": self.unlocked_achievements}, f, ensure_ascii=False)

    def load_play_count(self):
        filepath = self.get_file_path("play_count.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("count", 0)
        return 0

    def save_play_count(self):
        filepath = self.get_file_path("play_count.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"count": self.play_count}, f)

    def load_volume_setting(self):
        filepath = self.get_file_path("settings.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    vol = data.get("volume", 0.5)
                    self.music.set_volume(vol)
            except (json.JSONDecodeError, KeyError, IOError):
                pass

    def save_volume_setting(self):
        filepath = self.get_file_path("settings.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"volume": self.music.get_volume()}, f)
        except (IOError, TypeError):
            pass

    def reset_all_progress(self):
        for i in range(6):
            path = os.path.join(self.base_dir, f"save_{i}.json")
            if os.path.exists(path):
                os.remove(path)
        for fname in ["play_count.json", "endings.json", "achievements.json"]:
            path = self.get_file_path(fname)
            if os.path.exists(path):
                os.remove(path)
        self.play_count = 0
        self.unlocked_endings = []
        self.unlocked_achievements = []
        self.save_slots = [None] * 6
        self.load_save_list()

    def load_save_list(self):
        for i in range(6):
            path = os.path.join(self.base_dir, f"save_{i}.json")
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.save_slots[i] = data
                except (json.JSONDecodeError, IOError):
                    self.save_slots[i] = None

    def draw_gradient_background(self, colors):
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_background(self, bg_type):
        # 优先显示图片背景
        bg_map = {
            "home": "bg_home_old",
            "office_night": "bg_office_night",
            "office_day": "bg_office_day",
            "office_dark": "bg_office_dark",
            "livestudio": "bg_livestudio",
            "startup": "bg_small_office",
            "office_modern": "bg_office_modern",
            "factory": "bg_factory",
            "xiaomi_office": "bg_xiaomi",
            "apple_office": "bg_apple",
            "classroom": "bg_classroom",
            "noodle_shop": "bg_noodle_shop",
            "bar": "bg_bar",
            "street_food": "bg_street_food",
            "venue": "bg_venue",
            "celebration": "bg_celebration",
            "bookstore": "bg_bookstore",
            "corridor": "bg_corridor",
            "hospital": "bg_hospital",
            "press": "bg_press",
            "airport": "bg_airport",
            "conference": "bg_conference",
            "balcony": "bg_balcony",
            "train_platform": "bg_train_platform",
            "room_rent": "bg_room_rent",
            "black": "bg_black",
            "inn": "bg_inn",
            "farmyard": "bg_farmyard",
            "restaurant": "bg_restaurant",
            "teacher_office": "bg_teacher_office"
        }
        img_key = bg_map.get(bg_type)
        if img_key and img_key in self.backgrounds:
            self.screen.blit(self.backgrounds[img_key], (0, 0))
            # 叠加暗色让文字更清晰
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            self.screen.blit(overlay, (0, 0))
            return

        # 没有图片时回退到渐变
        colors = {
            "black": [(0, 0, 0), (10, 10, 20)],
            "office_night": [(20, 30, 50), (30, 40, 70)],
            "office_day": [(70, 90, 110), (100, 120, 140)],
            "office_dark": [(15, 10, 15), (30, 25, 35)],
            "livestudio": [(60, 30, 80), (100, 50, 120)],
            "xiaomi_office": [(30, 50, 80), (70, 100, 140)],
            "apple_office": [(200, 200, 210), (230, 230, 240)],
            "factory": [(80, 50, 30), (120, 80, 50)],
            "startup": [(40, 50, 70), (80, 100, 130)],
            "home": [(70, 60, 50), (120, 100, 90)],
            "office_modern": [(50, 70, 90), (90, 110, 130)]
        }
        c = colors.get(bg_type, colors["office_night"])
        self.draw_gradient_background(c)

    def draw_fire_icon(self, x, y, color):
        pygame.draw.polygon(self.screen, color, [
            (x + 8, y),
            (x + 2, y + 10),
            (x + 5, y + 7),
            (x + 3, y + 14),
            (x + 13, y + 14),
            (x + 11, y + 7),
            (x + 14, y + 10),
        ])
        pygame.draw.polygon(self.screen, (255, 220, 100), [
            (x + 8, y + 4),
            (x + 5, y + 10),
            (x + 7, y + 8),
            (x + 6, y + 13),
            (x + 10, y + 13),
            (x + 9, y + 8),
            (x + 11, y + 10),
        ])

    def draw_briefcase_icon(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x + 2, y + 5, 12, 9), border_radius=1)
        pygame.draw.rect(self.screen, color, (x + 5, y + 2, 6, 4), border_radius=1)
        pygame.draw.rect(self.screen, (25, 25, 45), (x + 7, y + 8, 2, 3))
        pygame.draw.line(self.screen, (20, 20, 40), (x + 2, y + 8), (x + 14, y + 8), 1)

    def draw_heart_icon(self, x, y, color):
        pygame.draw.polygon(self.screen, color, [
            (x + 8, y + 13),
            (x + 1, y + 6),
            (x + 1, y + 3),
            (x + 4, y + 1),
            (x + 8, y + 4),
            (x + 12, y + 1),
            (x + 15, y + 3),
            (x + 15, y + 6),
        ])
        pygame.draw.circle(self.screen, color, (x + 4, y + 4), 3)
        pygame.draw.circle(self.screen, color, (x + 12, y + 4), 3)

    def draw_status_bar(self):
        bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 55)
        pygame.draw.rect(self.screen, (25, 25, 45), bar_rect)
        pygame.draw.line(self.screen, (50, 50, 80), (0, 54), (SCREEN_WIDTH, 54))

        stats = [
            ("理想", self.ideal, COLOR_IDEAL, 100, "fire"),
            ("现实", self.reality, COLOR_REALITY, 100, "briefcase"),
            ("温情", self.warmth, COLOR_WARMTH, 100, "heart"),
        ]
        
        x = 20
        for name, value, color, max_val, icon_type in stats:
            icon_y = 10
            if icon_type == "fire":
                self.draw_fire_icon(x, icon_y, color)
            elif icon_type == "briefcase":
                self.draw_briefcase_icon(x, icon_y, color)
            elif icon_type == "heart":
                self.draw_heart_icon(x, icon_y, color)
            
            name_text = self.font_small.render(name, True, color)
            self.screen.blit(name_text, (x + 20, 8))
            
            bar_x = x + 60
            bar_w = 100
            pygame.draw.rect(self.screen, (40, 40, 60), (bar_x, 10, bar_w, 12), border_radius=6)
            
            fill_w = int(bar_w * min(value, max_val) / max_val)
            if fill_w > 0:
                pygame.draw.rect(self.screen, color, (bar_x, 10, fill_w, 12), border_radius=6)
            
            val_text = self.font_tiny.render(str(value), True, COLOR_TEXT_MAIN)
            self.screen.blit(val_text, (bar_x + bar_w + 5, 9))
            
            x += 200

        # 章节名
        scene = self.story_data.get("scenes", {}).get(self.current_scene_id, {})
        title = scene.get("title", "")
        if title:
            text3 = self.font_small.render(f"【{title}】", True, COLOR_ACCENT_RED)
            self.screen.blit(text3, (SCREEN_WIDTH - text3.get_width() - 20, 18))

    def draw_dialog_box(self):
        dlg_rect = pygame.Rect(40, SCREEN_HEIGHT - 250, SCREEN_WIDTH - 80, 220)
        pygame.draw.rect(self.screen, COLOR_DIALOG_BG, dlg_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_DIALOG_BORDER, dlg_rect, width=2, border_radius=12)

        pygame.draw.line(self.screen, COLOR_ACCENT_RED,
                         (dlg_rect.x + 20, dlg_rect.y + 2),
                         (dlg_rect.x + dlg_rect.width - 20, dlg_rect.y + 2), 2)

        char_key = None
        is_narrator = False
        if self.current_character and self.current_character != "none":
            char_key = self.current_character
        elif self.current_speaker and self.current_speaker != "none" and self.current_speaker != "旁白":
            speaker_map = {
                "罗诚": "luocheng_mid",
                "妻子": "wife",
                "老王": "laowang",
                "老周": "laozhou",
                "程总": "cheng",
                "小张": "xiaozhang",
                "Coco": "coco",
                "吴老板": "wu_laoban"
            }
            char_key = speaker_map.get(self.current_speaker)
        elif self.current_speaker == "旁白" or (not self.current_speaker):
            is_narrator = True

        has_avatar = char_key and char_key in self.characters

        # 头像：对话框左侧内部
        if has_avatar:
            avatar = self.characters[char_key]
            avatar_x = dlg_rect.x + 25
            avatar_y = dlg_rect.y + 60
            pygame.draw.rect(self.screen, (30, 25, 35), (avatar_x - 5, avatar_y - 5, 130, 130), border_radius=10)
            pygame.draw.rect(self.screen, COLOR_DIALOG_BORDER, (avatar_x - 5, avatar_y - 5, 130, 130), width=2, border_radius=10)
            self.screen.blit(avatar, (avatar_x, avatar_y))

        # 说话者名字标签（放在对话框顶部，左对齐）
        label_x = dlg_rect.x + 25
        if has_avatar:
            label_x = dlg_rect.x + 170

        if self.current_speaker and self.current_speaker != "none":
            name_w = max(100, self.font_name.size(self.current_speaker)[0] + 24)
            name_bg = pygame.Rect(label_x, dlg_rect.y - 1, name_w, 30)
            pygame.draw.rect(self.screen, COLOR_ACCENT_RED, name_bg, border_bottom_left_radius=6, border_bottom_right_radius=6)
            name_text = self.font_name.render(self.current_speaker, True, (255, 255, 255))
            self.screen.blit(name_text, (name_bg.x + 12, name_bg.y + 4))
        elif is_narrator:
            name_w = 80
            name_bg = pygame.Rect(label_x, dlg_rect.y - 1, name_w, 30)
            pygame.draw.rect(self.screen, (90, 90, 120), name_bg, border_bottom_left_radius=6, border_bottom_right_radius=6)
            name_text = self.font_name.render("旁白", True, (210, 210, 230))
            self.screen.blit(name_text, (name_bg.x + 16, name_bg.y + 4))

        # 对话文本
        if has_avatar:
            text_x = dlg_rect.x + 170
        else:
            text_x = dlg_rect.x + 40
        text_max_w = dlg_rect.width - (text_x - dlg_rect.x) - 40

        lines = self.wrap_text(self.text_display, text_max_w)
        y = dlg_rect.y + 50
        for line in lines[:6]:
            text_surface = self.font_text.render(line, True, COLOR_TEXT_MAIN)
            self.screen.blit(text_surface, (text_x, y))
            y += 30

        # 点击继续提示
        if self.text_complete:
            alpha = 128 + int(127 * math.sin(self.anim_frame * 0.05))
            prompt = self.font_small.render("▼ 点击 / 按空格 继续", True, (150, 150, 170))
            prompt.set_alpha(alpha)
            self.screen.blit(prompt, (dlg_rect.x + dlg_rect.width - prompt.get_width() - 25,
                                        dlg_rect.y + dlg_rect.height - 30))

    def wrap_text(self, text, max_width):
        words = []
        current = ""
        for char in text:
            current += char
            if self.font_text.size(current)[0] >= max_width:
                words.append(current[:-1])
                current = char
        if current:
            words.append(current)
        return words

    def draw_pixel_lock(self, x, y, size=28):
        pixel = size // 16
        c_lock = (200, 180, 120)
        c_dark = (120, 100, 60)
        c_highlight = (230, 210, 150)

        # 锁身
        body_x = x + pixel * 3
        body_y = y + pixel * 7
        body_w = pixel * 10
        body_h = pixel * 8
        pygame.draw.rect(self.screen, c_lock, (body_x, body_y, body_w, body_h), border_radius=pixel)
        pygame.draw.rect(self.screen, c_dark, (body_x, body_y, body_w, body_h), width=pixel, border_radius=pixel)

        # 锁芯
        keyhole_cx = body_x + body_w // 2
        keyhole_cy = body_y + body_h // 2
        pygame.draw.circle(self.screen, c_dark, (keyhole_cx, keyhole_cy - pixel), pixel)
        pygame.draw.rect(self.screen, c_dark, (keyhole_cx - pixel, keyhole_cy - pixel, pixel * 2, pixel * 4))

        # 锁梁（U形）
        shackle_x = x + pixel * 5
        shackle_y = y + pixel * 2
        shackle_w = pixel * 6
        shackle_h = pixel * 7
        pygame.draw.rect(self.screen, c_lock, (shackle_x, shackle_y, shackle_w, pixel * 2), border_radius=pixel)
        pygame.draw.rect(self.screen, c_lock, (shackle_x, shackle_y, pixel * 2, shackle_h), border_radius=pixel)
        pygame.draw.rect(self.screen, c_lock, (shackle_x + shackle_w - pixel * 2, shackle_y, pixel * 2, shackle_h), border_radius=pixel)
        pygame.draw.rect(self.screen, c_dark, (shackle_x, shackle_y, shackle_w, pixel * 2), width=pixel, border_radius=pixel)
        pygame.draw.rect(self.screen, c_dark, (shackle_x, shackle_y, pixel * 2, shackle_h), width=pixel, border_radius=pixel)
        pygame.draw.rect(self.screen, c_dark, (shackle_x + shackle_w - pixel * 2, shackle_y, pixel * 2, shackle_h), width=pixel, border_radius=pixel)

        # 高光
        pygame.draw.rect(self.screen, c_highlight, (body_x + pixel, body_y + pixel, pixel * 2, pixel * 2))

    def draw_choice_panel(self, choices):
        # 半透明遮罩
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, 0))

        panel_w, panel_h = 780, 480
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2

        pygame.draw.rect(self.screen, (30, 30, 50), (panel_x, panel_y, panel_w, panel_h), border_radius=16)
        pygame.draw.rect(self.screen, COLOR_ACCENT_RED, (panel_x, panel_y, panel_w, panel_h), width=2, border_radius=16)

        # 标题
        title = self.font_title.render("【关键抉择】", True, COLOR_ACCENT_RED)
        self.screen.blit(title, (panel_x + panel_w // 2 - title.get_width() // 2, panel_y + 15))

        pygame.draw.line(self.screen, (80, 80, 110),
                         (panel_x + 40, panel_y + 55), (panel_x + panel_w - 40, panel_y + 55), 2)

        # 选项
        for i, choice in enumerate(choices):
            cx = panel_x + 30
            cy = panel_y + 70 + i * 75
            is_hover = (i == self.hover_choice)
            
            # 检查是否锁定
            option_locked = self.is_choice_locked(choice)

            if option_locked:
                color = (35, 35, 50)
                border = (70, 70, 90)
            elif is_hover:
                color = (COLOR_ACCENT_RED[0], COLOR_ACCENT_RED[1], COLOR_ACCENT_RED[2])
                border = COLOR_ACCENT_RED
            else:
                color = (50, 50, 70)
                border = (80, 80, 110)

            pygame.draw.rect(self.screen, color, (cx, cy, panel_w - 60, 65), border_radius=8)
            pygame.draw.rect(self.screen, border, (cx, cy, panel_w - 60, 65), width=2, border_radius=8)

            # 选择字母
            letter = self.font_name.render(f"{chr(65 + i)}.", True, COLOR_ACCENT_RED)
            self.screen.blit(letter, (cx + 15, cy + 10))

            # 选择文本
            text = self.font_text.render(choice["text"], True, COLOR_TEXT_MAIN)
            self.screen.blit(text, (cx + 50, cy + 10))

            # 属性变化提示
            hint = choice.get("hint", "")
            if hint:
                hint_text = self.font_tiny.render(hint, True, COLOR_TEXT_SOFT)
                self.screen.blit(hint_text, (cx + 50, cy + 38))

            # 锁定图标和提示
            if option_locked:
                lock_size = 32
                self.draw_pixel_lock(cx + panel_w - 60 - lock_size - 15, cy + (65 - lock_size) // 2, lock_size)
                if choice.get("locked", False):
                    lock_label = self.font_tiny.render("需二周目解锁", True, COLOR_ACCENT_PURPLE)
                else:
                    lock_label = self.font_tiny.render("仅一周目可选", True, COLOR_ACCENT_PURPLE)
                self.screen.blit(lock_label, (cx + panel_w - 60 - lock_size - 25 - lock_label.get_width(), cy + 22))

    def draw_ending_screen(self, ending_data):
        type_colors = {
            "最佳": [(246, 224, 94), (200, 150, 50)],
            "好": [(72, 187, 120), (50, 150, 100)],
            "普通": [(150, 150, 170), (100, 100, 120)],
            "失败": [(233, 69, 96), (180, 40, 60)],
            "隐藏": [(159, 122, 234), (120, 80, 180)]
        }
        c = type_colors.get(ending_data.get("type_cn", "普通"), type_colors["普通"])
        self.draw_gradient_background([c[0], c[1]])

        # 标题
        title = self.font_large.render(f"【{ending_data.get('title', '')}】", True, COLOR_TEXT_MAIN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # 星级
        stars = "★" * ending_data.get("stars", 3)
        star_text = self.font_title.render(stars, True, COLOR_ACCENT_GOLD)
        self.screen.blit(star_text, (SCREEN_WIDTH // 2 - star_text.get_width() // 2, 120))

        # 类型
        type_text = self.font_name.render(f"【{ending_data.get('type_cn', '普通')}结局】", True, COLOR_ACCENT_GOLD)
        self.screen.blit(type_text, (SCREEN_WIDTH // 2 - type_text.get_width() // 2, 170))

        # 最终属性
        stats_y = 220
        stats_text = self.font_text.render(
            f"最终属性 — 🔥理想:{self.ideal}  💼现实:{self.reality}  ❤️温情:{self.warmth}", 
            True, COLOR_TEXT_MAIN
        )
        self.screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, stats_y))

        # 描述
        desc = ending_data.get("description", "")
        desc_lines = self.wrap_text(desc, SCREEN_WIDTH - 300)
        for i, line in enumerate(desc_lines):
            desc_text = self.font_text.render(line, True, COLOR_TEXT_MAIN)
            self.screen.blit(desc_text, (SCREEN_WIDTH // 2 - desc_text.get_width() // 2, 270 + i * 30))

        # 成就
        ach = ending_data.get("achievement", "")
        if ach:
            ach_text = self.font_title.render(f"🏆 成就解锁：{ach}", True, COLOR_ACCENT_GOLD)
            self.screen.blit(ach_text, (SCREEN_WIDTH // 2 - ach_text.get_width() // 2, SCREEN_HEIGHT - 300))

        # 操作提示
        hint_text = self.font_small.render("点击返回主菜单 | 按1重新开始 | 按2主菜单 | 按3图鉴", True, COLOR_TEXT_SOFT)
        self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 200))

    def draw_achievement_popup(self):
        if self.achievement_popup and self.achievement_timer > 0:
            alpha = min(255, self.achievement_timer * 3)
            popup_h = 60
            popup_y = 60
            
            s = pygame.Surface((SCREEN_WIDTH, popup_h), pygame.SRCALPHA)
            s.fill((50, 50, 80, min(200, alpha)))
            self.screen.blit(s, (0, popup_y))
            
            text = self.font_title.render(f"🏆 成就解锁：{self.achievement_popup}", True, COLOR_ACCENT_GOLD)
            text.set_alpha(alpha)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, popup_y + 15))

    def draw_title_screen(self):
        # 播放主菜单音乐
        self.music.play("menu")

        colors = [
            (20 + int(10 * math.sin(self.anim_frame * 0.01)),
             20 + int(10 * math.cos(self.anim_frame * 0.015)),
             40 + int(15 * math.sin(self.anim_frame * 0.008))),
            (50, 50, 90)
        ]
        self.draw_gradient_background(colors)

        # 装饰星星
        for i in range(20):
            x = (i * 67 + self.anim_frame) % SCREEN_WIDTH
            y = (i * 113) % (SCREEN_HEIGHT // 2)
            pygame.draw.circle(self.screen, COLOR_ACCENT_GOLD, (x, y), 2)

        # 标题
        title_y = 150
        title_main = self.font_large.render("罗诚的故事", True, COLOR_ACCENT_RED)
        title_shadow = self.font_large.render("罗诚的故事", True, (0, 0, 0))
        self.screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_main.get_width() // 2 + 4, title_y + 4))
        self.screen.blit(title_main, (SCREEN_WIDTH // 2 - title_main.get_width() // 2, title_y))

        subtitle = self.font_title.render("从负债数亿到涅槃重生", True, COLOR_ACCENT_GOLD)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, title_y + 60))

        # 游戏次数提示
        if self.play_count >= 1:
            week_text = self.font_small.render(f"已通关 {self.play_count} 次 | 二周目已解锁D支线", True, COLOR_ACCENT_PURPLE)
            self.screen.blit(week_text, (SCREEN_WIDTH // 2 - week_text.get_width() // 2, title_y + 100))

        # 菜单按钮
        has_save = self.save_slots[0] is not None
        menu_items = [
            ("1. 开始游戏", COLOR_ACCENT_GREEN, True),
            ("2. 继续游戏", COLOR_ACCENT_BLUE if has_save else (80, 80, 100), has_save),
            ("3. 结局图鉴", COLOR_ACCENT_PURPLE, True),
            ("4. 设置", COLOR_ACCENT_ORANGE, True),
            ("5. 退出游戏", COLOR_ACCENT_RED, True)
        ]
        y = 330
        for text, color, enabled in menu_items:
            text_surf = self.font_title.render(text, True, color)
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y, 300, 50)
            bg_color = (40, 40, 60) if enabled else (30, 30, 45)
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
            border_color = color if enabled else (50, 50, 70)
            pygame.draw.rect(self.screen, border_color, rect, width=2, border_radius=8)
            self.screen.blit(text_surf, (rect.x + 60, rect.y + 13))
            y += 65

        hint = self.font_small.render("按数字键 1-5 选择 | 点击菜单也可", True, COLOR_TEXT_SOFT)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))

        version = self.font_small.render("v2.0  |  Python + Pygame", True, (80, 80, 110))
        self.screen.blit(version, (SCREEN_WIDTH - version.get_width() - 20, SCREEN_HEIGHT - 30))

    def draw_gallery(self):
        self.draw_gradient_background([(30, 30, 50), (50, 50, 80)])

        title = self.font_large.render("结局图鉴", True, COLOR_ACCENT_RED)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))

        subtitle = self.font_small.render("已解锁 {}/{} 个结局 | 已获得 {}/{} 个成就".format(
            len(self.unlocked_endings), len(self.get_all_endings()),
            len(self.unlocked_achievements), len(self.get_all_achievements())
        ), True, COLOR_ACCENT_GOLD)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 55))

        all_endings = self.get_all_endings()
        cols = 3
        card_w, card_h = 310, 92
        start_x = (SCREEN_WIDTH - card_w * cols - 25 * (cols - 1)) // 2
        start_y = 85

        type_colors = {
            "最佳": COLOR_ACCENT_GOLD,
            "好": COLOR_ACCENT_GREEN,
            "普通": (150, 150, 170),
            "失败": COLOR_ACCENT_RED,
            "隐藏": COLOR_ACCENT_PURPLE
        }

        for idx, ending in enumerate(all_endings):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (card_w + 25)
            y = start_y + row * (card_h + 12)
            is_unlocked = ending["id"] in self.unlocked_endings

            if is_unlocked:
                border_color = type_colors.get(ending.get("type_cn", "普通"), (100, 100, 120))
                pygame.draw.rect(self.screen, (45, 45, 65), (x, y, card_w, card_h), border_radius=10)
                pygame.draw.rect(self.screen, border_color, (x, y, card_w, card_h), width=2, border_radius=10)

                t = self.font_name.render(ending.get("title", ""), True, COLOR_TEXT_MAIN)
                self.screen.blit(t, (x + 12, y + 10))

                stars = "★" * ending.get("stars", 3)
                s = self.font_small.render(stars, True, COLOR_ACCENT_GOLD)
                self.screen.blit(s, (x + card_w - 80, y + 12))

                t_type = self.font_tiny.render(f"【{ending.get('type_cn', '普通')}】", True, border_color)
                self.screen.blit(t_type, (x + 12, y + 38))

                desc = ending.get("description", "")
                lines = self.wrap_text(desc, card_w - 24)
                for i, line in enumerate(lines[:2]):
                    d = self.font_tiny.render(line, True, COLOR_TEXT_SOFT)
                    self.screen.blit(d, (x + 12, y + 58 + i * 16))
            else:
                pygame.draw.rect(self.screen, (30, 30, 45), (x, y, card_w, card_h), border_radius=10)
                pygame.draw.rect(self.screen, (60, 60, 80), (x, y, card_w, card_h), width=2, border_radius=10)
                question = self.font_title.render("?", True, (80, 80, 110))
                self.screen.blit(question, (x + card_w // 2 - question.get_width() // 2,
                                              y + card_h // 2 - question.get_height() // 2))

        hint = self.font_small.render("点击返回 | 按 2 或 ESC 返回主菜单", True, COLOR_TEXT_SOFT)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 30))

    def draw_settings(self):
        self.draw_gradient_background([(30, 30, 50), (50, 50, 80)])

        title = self.font_large.render("设置", True, COLOR_ACCENT_ORANGE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        panel_w, panel_h = 600, 380
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = 130

        pygame.draw.rect(self.screen, (30, 30, 50), (panel_x, panel_y, panel_w, panel_h), border_radius=16)
        pygame.draw.rect(self.screen, (80, 80, 110), (panel_x, panel_y, panel_w, panel_h), width=2, border_radius=16)

        # 音量设置
        label_vol = self.font_title.render("游戏音量", True, COLOR_TEXT_MAIN)
        self.screen.blit(label_vol, (panel_x + 40, panel_y + 40))

        # 滑条轨道
        slider_x = panel_x + 40
        slider_y = panel_y + 100
        slider_w = panel_w - 80
        slider_h = 8

        pygame.draw.rect(self.screen, (60, 60, 80), (slider_x, slider_y, slider_w, slider_h), border_radius=4)

        # 当前音量填充
        fill_w = int(slider_w * self.music.get_volume())
        pygame.draw.rect(self.screen, COLOR_ACCENT_ORANGE, (slider_x, slider_y, fill_w, slider_h), border_radius=4)

        # 滑块
        handle_r = 14
        handle_x = slider_x + fill_w
        handle_y = slider_y + slider_h // 2
        pygame.draw.circle(self.screen, (255, 200, 100), (handle_x, handle_y), handle_r)
        pygame.draw.circle(self.screen, COLOR_ACCENT_ORANGE, (handle_x, handle_y), handle_r, 3)

        # 音量百分比
        vol_pct = int(self.music.get_volume() * 100)
        pct_text = self.font_text.render(f"{vol_pct}%", True, COLOR_ACCENT_GOLD)
        self.screen.blit(pct_text, (slider_x + slider_w - pct_text.get_width(), slider_y - 32))

        # 分割线
        pygame.draw.line(self.screen, (70, 70, 100),
                         (panel_x + 40, panel_y + 160), (panel_x + panel_w - 40, panel_y + 160), 2)

        # 重置游戏数据
        label_reset = self.font_title.render("重置游戏数据", True, COLOR_TEXT_MAIN)
        self.screen.blit(label_reset, (panel_x + 40, panel_y + 190))

        desc_reset = self.font_small.render("删除所有存档、通关记录和成就，重新开始", True, COLOR_TEXT_SOFT)
        self.screen.blit(desc_reset, (panel_x + 40, panel_y + 230))

        # 重置按钮
        reset_btn_w, reset_btn_h = 200, 50
        reset_btn_x = panel_x + (panel_w - reset_btn_w) // 2
        reset_btn_y = panel_y + 280
        reset_hover = self.settings_reset_hover
        reset_bg = (80, 30, 40) if reset_hover else (60, 30, 35)
        reset_border = COLOR_ACCENT_RED if reset_hover else (120, 60, 70)
        pygame.draw.rect(self.screen, reset_bg, (reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h), border_radius=8)
        pygame.draw.rect(self.screen, reset_border, (reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h), width=2, border_radius=8)
        reset_text = self.font_text.render("重置游戏", True, COLOR_ACCENT_RED)
        self.screen.blit(reset_text, (reset_btn_x + reset_btn_w // 2 - reset_text.get_width() // 2, reset_btn_y + 12))

        # 保存按钮
        save_btn_w, save_btn_h = 200, 50
        save_btn_x = panel_x + (panel_w - save_btn_w) // 2
        save_btn_y = panel_y + 340
        save_hover = self.settings_save_hover
        save_bg = (40, 70, 50) if save_hover else (35, 55, 40)
        save_border = COLOR_ACCENT_GREEN if save_hover else (70, 120, 80)
        pygame.draw.rect(self.screen, save_bg, (save_btn_x, save_btn_y, save_btn_w, save_btn_h), border_radius=8)
        pygame.draw.rect(self.screen, save_border, (save_btn_x, save_btn_y, save_btn_w, save_btn_h), width=2, border_radius=8)
        save_text = self.font_text.render("返回主菜单", True, COLOR_ACCENT_GREEN)
        self.screen.blit(save_text, (save_btn_x + save_btn_w // 2 - save_text.get_width() // 2, save_btn_y + 12))

        # 确认重置对话框
        if self.show_reset_confirm:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, 0))

            conf_w, conf_h = 500, 220
            conf_x = (SCREEN_WIDTH - conf_w) // 2
            conf_y = (SCREEN_HEIGHT - conf_h) // 2
            pygame.draw.rect(self.screen, (30, 30, 50), (conf_x, conf_y, conf_w, conf_h), border_radius=12)
            pygame.draw.rect(self.screen, COLOR_ACCENT_RED, (conf_x, conf_y, conf_w, conf_h), width=2, border_radius=12)

            conf_title = self.font_title.render("确认重置？", True, COLOR_ACCENT_RED)
            self.screen.blit(conf_title, (conf_x + conf_w // 2 - conf_title.get_width() // 2, conf_y + 30))

            conf_line1 = self.font_text.render("将删除所有存档、通关记录和成就", True, COLOR_TEXT_MAIN)
            conf_line2 = self.font_text.render("此操作不可撤销！", True, COLOR_ACCENT_RED)
            self.screen.blit(conf_line1, (conf_x + conf_w // 2 - conf_line1.get_width() // 2, conf_y + 85))
            self.screen.blit(conf_line2, (conf_x + conf_w // 2 - conf_line2.get_width() // 2, conf_y + 120))

            # 确认按钮
            btn_w, btn_h = 120, 45
            btn_y = conf_y + 160
            yes_x = conf_x + conf_w // 2 - btn_w - 20
            no_x = conf_x + conf_w // 2 + 20

            pygame.draw.rect(self.screen, (80, 30, 40), (yes_x, btn_y, btn_w, btn_h), border_radius=8)
            pygame.draw.rect(self.screen, COLOR_ACCENT_RED, (yes_x, btn_y, btn_w, btn_h), width=2, border_radius=8)
            yes_text = self.font_text.render("确认重置", True, COLOR_ACCENT_RED)
            self.screen.blit(yes_text, (yes_x + btn_w // 2 - yes_text.get_width() // 2, btn_y + 10))

            pygame.draw.rect(self.screen, (50, 50, 70), (no_x, btn_y, btn_w, btn_h), border_radius=8)
            pygame.draw.rect(self.screen, COLOR_TEXT_SOFT, (no_x, btn_y, btn_w, btn_h), width=2, border_radius=8)
            no_text = self.font_text.render("取消", True, COLOR_TEXT_SOFT)
            self.screen.blit(no_text, (no_x + btn_w // 2 - no_text.get_width() // 2, btn_y + 10))

            self.reset_confirm_yes_rect = pygame.Rect(yes_x, btn_y, btn_w, btn_h)
            self.reset_confirm_no_rect = pygame.Rect(no_x, btn_y, btn_w, btn_h)

    def get_all_endings(self):
        endings = []
        for scene_id, scene in self.story_data.get("scenes", {}).items():
            if "ending" in scene:
                endings.append(scene["ending"])
        return endings

    def get_all_achievements(self):
        return list(self.story_data.get("achievements", {}).keys())

    def get_current_scene(self):
        return self.story_data.get("scenes", {}).get(self.current_scene_id, {})

    def start_story(self):
        # 播放剧情背景音乐
        self.music.play("story")

        # 重置属性
        initial_stats = self.story_data.get("initial_stats", {"ideal": 20, "reality": 20, "warmth": 20})
        self.ideal = initial_stats.get("ideal", 20)
        self.reality = initial_stats.get("reality", 20)
        self.warmth = initial_stats.get("warmth", 20)
        
        self.story_choices = []
        self.current_scene_id = "intro"  # 从人物简介开始
        self.current_line_index = 0
        self.state = STATE_DIALOG
        self.load_current_scene()
        self.auto_save()

    def load_current_scene(self):
        scene = self.get_current_scene()

        # 根据场景切换背景音乐
        if self.state in [STATE_DIALOG, STATE_CHOICE]:
            self.music.play_for_scene(self.current_scene_id)

        lines = scene.get("lines", [])
        # 自动跳过空行，找到下一句有内容的台词
        while self.current_line_index < len(lines):
            line = lines[self.current_line_index]
            text = line.get("text", "")
            if text.strip() != "":
                break
            self.current_line_index += 1

        if self.current_line_index < len(lines):
            line = lines[self.current_line_index]
            self.current_speaker = line.get("speaker", "")
            if self.current_speaker == "":
                self.current_speaker = "旁白"
            self.text_target = line.get("text", "")
            self.text_display = ""
            self.text_timer = 0
            self.text_complete = False
            self.current_character = line.get("character", "none")

    def advance_dialog(self):
        scene = self.get_current_scene()
        lines = scene.get("lines", [])

        if not self.text_complete:
            self.text_display = self.text_target
            self.text_complete = True
            return

        self.current_line_index += 1
        if self.current_line_index < len(lines):
            self.load_current_scene()
            self.auto_save()
        else:
            # 检查场景成就
            if "achievement" in scene:
                self.unlock_achievement(scene["achievement"]["id"], scene["achievement"]["name"])
            
            choices = scene.get("choices")
            if choices and len(choices) > 0:
                # 检查是否所有选项都被锁定
                all_locked = all(self.is_choice_locked(c) for c in choices)
                if all_locked:
                    # 所有选项都锁定，跳到下一场景
                    next_scene = scene.get("next_scene")
                    if next_scene:
                        self.current_scene_id = next_scene
                        self.current_line_index = 0
                        self.load_current_scene()
                        self.auto_save()
                    return
                self.state = STATE_CHOICE
                self.current_choices = choices
                # 默认选中第一个未锁定的选项
                first_unlocked = 0
                for i, c in enumerate(choices):
                    if not self.is_choice_locked(c):
                        first_unlocked = i
                        break
                self.hover_choice = first_unlocked
                self.auto_save()
            else:
                next_scene = scene.get("next_scene")
                if next_scene:
                    self.current_scene_id = next_scene
                    self.current_line_index = 0
                    self.load_current_scene()
                    self.auto_save()
                else:
                    if "ending" in scene:
                        ending_data = scene["ending"]
                        if ending_data["id"] not in self.unlocked_endings:
                            self.unlocked_endings.append(ending_data["id"])
                            self.save_endings()
                        self.play_count += 1
                        self.save_play_count()
                        # 播放结局音乐
                        self.music.play("ending")
                        self.current_ending = ending_data
                        self.state = STATE_ENDING

    def unlock_achievement(self, ach_id, ach_name):
        if ach_id not in self.unlocked_achievements:
            self.unlocked_achievements.append(ach_id)
            self.save_achievements()
            self.achievement_popup = ach_name
            self.achievement_timer = 180  # 3秒显示

    def is_choice_locked(self, choice):
        """检查选项是否锁定"""
        is_locked = choice.get("locked", False)
        is_first_only = choice.get("first_play_only", False)
        return (is_locked and self.play_count < 1) or (is_first_only and self.play_count >= 1)

    def choose_option(self, index):
        if index >= len(self.current_choices):
            return
        
        choice = self.current_choices[index]
        if self.is_choice_locked(choice):
            return
        self.story_choices.append({"scene": self.current_scene_id, "choice": index})
        
        # 更新属性
        stat_changes = choice.get("stat_changes", {})
        if stat_changes:
            self.ideal += stat_changes.get("ideal", 0)
            self.reality += stat_changes.get("reality", 0)
            self.warmth += stat_changes.get("warmth", 0)
            # 限制范围
            self.ideal = max(0, min(100, self.ideal))
            self.reality = max(0, min(100, self.reality))
            self.warmth = max(0, min(100, self.warmth))
        
        self.current_scene_id = choice["next_scene"]
        self.current_line_index = 0
        self.state = STATE_DIALOG
        self.load_current_scene()
        self.auto_save()

    def update_text(self, dt):
        if self.state == STATE_DIALOG and not self.text_complete:
            self.text_timer += dt
            if self.text_timer >= self.text_speed:
                self.text_timer = 0
                if len(self.text_display) < len(self.text_target):
                    self.text_display += self.text_target[len(self.text_display)]
                else:
                    self.text_complete = True
        
        # 成就提示计时
        if self.achievement_timer > 0:
            self.achievement_timer -= 1
            if self.achievement_timer <= 0:
                self.achievement_popup = None

    def run(self):
        running = True
        last_time = pygame.time.get_ticks()
        while running:
            current_time = pygame.time.get_ticks()
            dt = current_time - last_time
            last_time = current_time

            self.anim_frame += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_key(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_click(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.dragging_volume:
                            self.save_volume_setting()
                        self.dragging_volume = False
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

            self.update_text(dt)
            self.render()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit(0)

    def handle_key(self, key):
        if self.state == STATE_DISCLAIMER:
            if key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                self.state = STATE_TITLE
        elif self.state == STATE_TITLE:
            if key == pygame.K_1 or key == pygame.K_KP1:
                self.start_story()
            elif key == pygame.K_2 or key == pygame.K_KP2:
                if self.save_slots[0]:
                    self.load_game(0)
            elif key == pygame.K_3 or key == pygame.K_KP3:
                self.state = STATE_GALLERY
            elif key == pygame.K_4 or key == pygame.K_KP4:
                self.state = STATE_SETTINGS
                self.settings_reset_hover = False
                self.settings_save_hover = False
                self.show_reset_confirm = False
            elif key == pygame.K_5 or key == pygame.K_KP5:
                return False
        elif self.state == STATE_SETTINGS:
            if key in [pygame.K_ESCAPE, pygame.K_2, pygame.K_KP2]:
                if self.show_reset_confirm:
                    self.show_reset_confirm = False
                else:
                    self.state = STATE_TITLE
                    self.save_volume_setting()
        elif self.state == STATE_DIALOG:
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self.advance_dialog()
            elif key == pygame.K_ESCAPE:
                self.state = STATE_TITLE
                self.music.play("menu")
        elif self.state == STATE_CHOICE:
            if key >= pygame.K_1 and key <= pygame.K_9:
                idx = key - pygame.K_1
                if idx < len(self.current_choices):
                    self.choose_option(idx)
            elif key >= pygame.K_KP1 and key <= pygame.K_KP9:
                idx = key - pygame.K_KP1
                if idx < len(self.current_choices):
                    self.choose_option(idx)
            elif key == pygame.K_UP:
                # 向上找第一个未锁定的选项
                new_idx = self.hover_choice - 1
                while new_idx >= 0:
                    if not self.is_choice_locked(self.current_choices[new_idx]):
                        self.hover_choice = new_idx
                        break
                    new_idx -= 1
            elif key == pygame.K_DOWN:
                # 向下找第一个未锁定的选项
                new_idx = self.hover_choice + 1
                while new_idx < len(self.current_choices):
                    if not self.is_choice_locked(self.current_choices[new_idx]):
                        self.hover_choice = new_idx
                        break
                    new_idx += 1
            elif key == pygame.K_RETURN and self.hover_choice >= 0:
                self.choose_option(self.hover_choice)
        elif self.state == STATE_ENDING:
            if key == pygame.K_1 or key == pygame.K_KP1:
                self.start_story()
            elif key == pygame.K_2 or key == pygame.K_KP2:
                self.state = STATE_TITLE
                self.music.play("menu")
            elif key == pygame.K_3 or key == pygame.K_KP3:
                self.state = STATE_GALLERY
        elif self.state == STATE_GALLERY:
            if key == pygame.K_2 or key == pygame.K_KP2 or key == pygame.K_ESCAPE:
                self.state = STATE_TITLE
                self.music.play("menu")
        return True

    def handle_mouse_click(self, pos):
        if self.state == STATE_DISCLAIMER:
            self.state = STATE_TITLE
            self.music.play("menu")
        elif self.state == STATE_TITLE:
            menu_y = 330
            for i in range(5):
                rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, menu_y + i * 65, 300, 50)
                if rect.collidepoint(pos):
                    if i == 0:
                        self.start_story()
                    elif i == 1:
                        if self.save_slots[0]:
                            self.load_game(0)
                    elif i == 2:
                        self.state = STATE_GALLERY
                    elif i == 3:
                        self.state = STATE_SETTINGS
                        self.settings_reset_hover = False
                        self.settings_save_hover = False
                        self.show_reset_confirm = False
                    elif i == 4:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    break
        elif self.state == STATE_DIALOG:
            self.advance_dialog()
        elif self.state == STATE_CHOICE:
            panel_w, panel_h = 780, 480
            panel_x = (SCREEN_WIDTH - panel_w) // 2
            panel_y = (SCREEN_HEIGHT - panel_h) // 2
            for i in range(len(self.current_choices)):
                cx = panel_x + 30
                cy = panel_y + 70 + i * 75
                if cx <= pos[0] <= cx + panel_w - 60 and cy <= pos[1] <= cy + 65:
                    self.choose_option(i)
                    break
        elif self.state == STATE_ENDING:
            self.state = STATE_TITLE
            self.music.play("menu")
        elif self.state == STATE_GALLERY:
            self.state = STATE_TITLE
            self.music.play("menu")
        elif self.state == STATE_SETTINGS:
            if self.show_reset_confirm:
                if self.reset_confirm_yes_rect and self.reset_confirm_yes_rect.collidepoint(pos):
                    self.reset_all_progress()
                    self.show_reset_confirm = False
                elif self.reset_confirm_no_rect and self.reset_confirm_no_rect.collidepoint(pos):
                    self.show_reset_confirm = False
            else:
                panel_w, panel_h = 600, 380
                panel_x = (SCREEN_WIDTH - panel_w) // 2
                panel_y = 130
                slider_x = panel_x + 40
                slider_y = panel_y + 100
                slider_w = panel_w - 80
                slider_h = 8
                handle_r = 14
                handle_y = slider_y + slider_h // 2
                if slider_x - handle_r <= pos[0] <= slider_x + slider_w + handle_r and handle_y - handle_r <= pos[1] <= handle_y + handle_r:
                    self.dragging_volume = True
                    ratio = max(0.0, min(1.0, (pos[0] - slider_x) / slider_w))
                    self.music.set_volume(ratio)
                else:
                    reset_btn_w, reset_btn_h = 200, 50
                    reset_btn_x = panel_x + (panel_w - reset_btn_w) // 2
                    reset_btn_y = panel_y + 280
                    if reset_btn_x <= pos[0] <= reset_btn_x + reset_btn_w and reset_btn_y <= pos[1] <= reset_btn_y + reset_btn_h:
                        self.show_reset_confirm = True
                    else:
                        save_btn_w, save_btn_h = 200, 50
                        save_btn_x = panel_x + (panel_w - save_btn_w) // 2
                        save_btn_y = panel_y + 340
                        if save_btn_x <= pos[0] <= save_btn_x + save_btn_w and save_btn_y <= pos[1] <= save_btn_y + save_btn_h:
                            self.state = STATE_TITLE
                            self.save_volume_setting()

    def handle_mouse_motion(self, pos):
        if self.state == STATE_CHOICE:
            panel_w, panel_h = 780, 480
            panel_x = (SCREEN_WIDTH - panel_w) // 2
            panel_y = (SCREEN_HEIGHT - panel_h) // 2
            for i in range(len(self.current_choices)):
                cx = panel_x + 30
                cy = panel_y + 70 + i * 75
                if cx <= pos[0] <= cx + panel_w - 60 and cy <= pos[1] <= cy + 65:
                    self.hover_choice = i
                    break
        elif self.state == STATE_SETTINGS:
            if self.dragging_volume:
                panel_w, panel_h = 600, 380
                panel_x = (SCREEN_WIDTH - panel_w) // 2
                slider_x = panel_x + 40
                slider_w = panel_w - 80
                ratio = max(0.0, min(1.0, (pos[0] - slider_x) / slider_w))
                self.music.set_volume(ratio)
            elif not self.show_reset_confirm:
                panel_w, panel_h = 600, 380
                panel_x = (SCREEN_WIDTH - panel_w) // 2
                panel_y = 130
                reset_btn_w, reset_btn_h = 200, 50
                reset_btn_x = panel_x + (panel_w - reset_btn_w) // 2
                reset_btn_y = panel_y + 280
                self.settings_reset_hover = (
                    reset_btn_x <= pos[0] <= reset_btn_x + reset_btn_w
                    and reset_btn_y <= pos[1] <= reset_btn_y + reset_btn_h
                )
                save_btn_w, save_btn_h = 200, 50
                save_btn_x = panel_x + (panel_w - save_btn_w) // 2
                save_btn_y = panel_y + 340
                self.settings_save_hover = (
                    save_btn_x <= pos[0] <= save_btn_x + save_btn_w
                    and save_btn_y <= pos[1] <= save_btn_y + save_btn_h
                )

    def render(self):
        if self.state == STATE_DISCLAIMER:
            self.draw_background("black")
            scene = self.get_current_scene()
            lines = scene.get("lines", [])
            if self.current_line_index < len(lines):
                self.text_target = lines[self.current_line_index].get("text", "")
            
            # 显示免责声明
            y = 150
            for line in lines:
                if line.get("text"):
                    text = self.font_text.render(line["text"], True, COLOR_TEXT_MAIN)
                    self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
                    y += 35
            
            hint = self.font_small.render("点击或按空格继续", True, COLOR_TEXT_SOFT)
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 100))
            
        elif self.state == STATE_TITLE:
            self.draw_title_screen()
        elif self.state in [STATE_DIALOG, STATE_CHOICE]:
            scene = self.get_current_scene()
            self.draw_background(scene.get("background", "office_night"))
            self.draw_status_bar()
            self.draw_dialog_box()
            if self.state == STATE_CHOICE:
                self.draw_choice_panel(self.current_choices)
            self.draw_achievement_popup()
        elif self.state == STATE_ENDING:
            self.draw_ending_screen(self.current_ending)
        elif self.state == STATE_GALLERY:
            self.draw_gallery()
        elif self.state == STATE_SETTINGS:
            self.draw_settings()

    def save_game(self, slot):
        data = {
            "scene_id": self.current_scene_id,
            "line_index": self.current_line_index,
            "ideal": self.ideal,
            "reality": self.reality,
            "warmth": self.warmth,
            "choices": self.story_choices,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "scene_name": self.get_current_scene().get("name", "")
        }
        path = os.path.join(self.base_dir, f"save_{slot}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.save_slots[slot] = data
        except (IOError, TypeError):
            pass

    def auto_save(self):
        self.save_game(0)

    def load_game(self, slot):
        if self.save_slots[slot]:
            data = self.save_slots[slot]
            scene_id = data.get("scene_id", "intro")
            # 校验场景是否存在，不存在则从开头开始
            if scene_id not in self.story_data.get("scenes", {}):
                self.start_story()
                return
            self.current_scene_id = scene_id
            self.current_line_index = max(0, data.get("line_index", 0))
            self.ideal = max(0, min(100, data.get("ideal", 20)))
            self.reality = max(0, min(100, data.get("reality", 20)))
            self.warmth = max(0, min(100, data.get("warmth", 20)))
            self.story_choices = data.get("choices", [])
            self.state = STATE_DIALOG
            self.load_current_scene()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()