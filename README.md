# 罗诚的故事

一款基于 Python + Pygame 的视觉小说/文字冒险游戏，讲述罗诚从负债数亿到涅槃重生的创业故事。

## 项目结构

```
Story game/
├── src/                  # 核心源代码
│   ├── main.py          # 游戏主程序
│   ├── story.json       # 剧情数据
│   ├── main.spec        # PyInstaller打包配置
│   ├── settings.json    # 用户设置
│   └── requirements.txt # 依赖列表
│
├── web-game/            # 网页版（HTML5 Canvas）
│   ├── index.html       # 网页版主文件
│   ├── data/            # 网页版剧情数据
│   └── assets/          # 网页版资源
│
├── assets/              # 桌面版资源文件
│   ├── audio/           # 背景音乐
│   ├── backgrounds/     # 场景背景图
│   ├── characters/      # 角色头像
│   ├── logo.jpg         # 游戏LOGO原图
│   └── logo.ico         # 游戏LOGO图标
│
├── dist/                # 打包输出
│   └── 罗诚的故事.exe   # Windows可执行文件
│
├── docs/                # 项目文档
│   ├── 剧本-*.md        # 剧本文档（多个版本）
│   ├── 美术规范-v1.md   # 美术规范
│   ├── 人物场景对照表.md
│   ├── 快速参考表.md
│   ├── AI图片生成提示词手册.md
│   ├── *剧情树状图.md
│   └── 选题策划案.md
│
├── scripts/             # 工具脚本
│   ├── gen_*.py         # 资源生成脚本
│   ├── check_*.py       # 资源检查脚本
│   ├── download_*.py    # 资源下载脚本
│   ├── extract_*.py     # 剧情提取脚本
│   ├── cleanup*.py      # 清理脚本
│   ├── test_game.py     # 游戏测试
│   └── 打包游戏.bat     # 打包批处理
│
├── showcase/            # 创意展示
│   ├── *.html           # 各类展示页面
│   └── 游戏UI界面.png
│
├── saves/               # 存档目录（运行时生成）
│
└── build/               # PyInstaller构建临时文件
```

## 快速开始

### 桌面版运行
```bash
cd src
python main.py
```

### 桌面版打包
```bash
cd scripts
打包游戏.bat
# 或
pyinstaller --onefile --windowed --icon=../assets/logo.ico --add-data "../assets;assets" --add-data "../src/story.json;." --name "罗诚的故事" ../src/main.py
```

### 网页版运行
```bash
cd web-game
python -m http.server 8080
# 浏览器访问 http://localhost:8080
```

## 游戏特色

- 多分支剧情系统
- 三维属性系统（理想 / 现实 / 温情）
- 13种不同结局
- 17个可解锁成就
- 完整存档/读档功能
- 背景音乐系统
- 设置系统（音量调节、剧情重置）
- D支线（二周目解锁）

## 技术栈

- Python 3.13 + Pygame 2.6
- HTML5 Canvas + JavaScript（网页版）
- JSON 数据驱动
- PyInstaller 打包

## 许可

本作品全部人物、企业、经历均为架空虚构。
