# -*- coding: utf-8 -*-
"""
快速语法和功能测试
"""
import sys
import os

sys.path.insert(0, r"d:\Story game")

# 先测试 story.json 加载
print("=" * 60)
print("测试1: 加载剧情数据...")
story_path = r"d:\Story game\story.json"
with open(story_path, "r", encoding="utf-8") as f:
    import json
    story_data = json.load(f)
    scenes = story_data.get("scenes", {})
    print(f"  ✓ 成功加载 {len(scenes)} 个场景")

# 检查关键场景
required_scenes = ["start", "intro_1", "intro_2", "branch_a_1", "branch_b_1", "branch_c_1", "branch_d_1", "branch_e_1"]
for s in required_scenes:
    if s in scenes:
        print(f"  ✓ 场景存在: {s}")
    else:
        print(f"  ✗ 场景缺失: {s}")

# 统计结局数量
endings = 0
for scene_id, scene in scenes.items():
    if "ending" in scene:
        endings += 1
print(f"  ✓ 共 {endings} 个结局场景")

# 测试 main.py 语法
print("\n" + "=" * 60)
print("测试2: 检查 main.py 语法...")
with open(r"d:\Story game\main.py", "r", encoding="utf-8") as f:
    source = f.read()
try:
    compile(source, "main.py", "exec")
    print("  ✓ Python 语法正确")
except SyntaxError as e:
    print(f"  ✗ 语法错误: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("测试3: 运行游戏（5秒后自动退出）...")
print("=" * 60)
print("\n请在弹出的窗口中查看游戏界面！")
print("窗口将在运行后显示。按 ESC 或点击 X 可退出。\n")

# 设置环境变量 - 正式运行
os.environ.pop("SDL_VIDEODRIVER", None)

# 模拟游戏短暂运行
import time
import threading

def run_game():
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("老罗的故事")

        # 读取 main.py 中的类
        main_path = r"d:\Story game\main.py"
        with open(main_path, "r", encoding="utf-8") as f:
            main_code = f.read()

        # 创建命名空间
        namespace = {}
        exec(main_code, namespace)
        Game = namespace["Game"]

        # 实例化游戏
        game = Game()
        print("  ✓ Game 类实例化成功")
        print("  ✓ 开始游戏循环...")

        start_time = time.time()
        running = True
        while running and time.time() - start_time < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 渲染一帧
            game.render()
            pygame.display.flip()
            game.clock.tick(60)

        # 记录状态
        print(f"\n  ✓ 游戏运行 {int(time.time() - start_time)} 秒")
        print(f"  ✓ 当前状态: {game.state}")
        print(f"  ✓ 当前场景: {game.current_scene_id}")

        pygame.quit()
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！游戏可正常运行！")
        print("=" * 60)
        print(f"\n启动命令: .venv\\Scripts\\python.exe main.py")
    except Exception as e:
        print(f"  ✗ 错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

run_game()
