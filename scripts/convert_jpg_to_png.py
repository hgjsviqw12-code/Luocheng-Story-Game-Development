from PIL import Image
import os

base_dir = os.path.dirname(__file__)

folders = ["assets/backgrounds", "assets/characters"]

for folder in folders:
    full_dir = os.path.join(base_dir, folder)
    if not os.path.exists(full_dir):
        continue
    for filename in os.listdir(full_dir):
        if filename.endswith(".jpg"):
            jpg_path = os.path.join(full_dir, filename)
            png_path = os.path.join(full_dir, filename[:-4] + ".png")
            try:
                img = Image.open(jpg_path)
                # 如果图片不是RGB模式则转换
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode != 'RGB' else None)
                    img = background
                img.save(png_path, "PNG")
                print(f"OK: {folder}/{filename} -> {filename[:-4]}.png")
            except Exception as e:
                print(f"FAIL: {folder}/{filename} - {e}")

print("转换完成")
