import urllib.request
import os
import hashlib
from PIL import Image
import time

OUT_DIR = os.path.join(os.path.dirname(__file__), "character_previews")
os.makedirs(OUT_DIR, exist_ok=True)

PLACEHOLDER_HASH = "19a0b822"
PLACEHOLDER_SIZE = (1832, 1832)

images = [
    ("luocheng_v1_anime_portrait", "https://aka.doubaocdn.com/s/3OiM1wfeGw"),
    ("luocheng_v2_chibi_pixel", "https://aka.doubaocdn.com/s/Iblb1wfeHq"),
    ("luocheng_v3_suit_stage", "https://aka.doubaocdn.com/s/t2T71wfeIp"),
    ("luocheng_v4_cute_casual", "https://aka.doubaocdn.com/s/7Eq01wfeJk"),
    ("luocheng_v5_young_hope", "https://aka.doubaocdn.com/s/d4Cf1wfeJt"),
    ("luocheng_v6_livestream", "https://aka.doubaocdn.com/s/2fdh1wfeKi"),
]

def download_with_retry(name, url, max_retries=3):
    """下载图片，重试3次，验证不是占位图"""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            data = urllib.request.urlopen(req, timeout=30).read()
            
            # 保存临时文件验证
            tmp_path = os.path.join(OUT_DIR, name + "_tmp.png")
            with open(tmp_path, 'wb') as f:
                f.write(data)
            
            # 验证图片
            try:
                img = Image.open(tmp_path)
                size = img.size
                file_hash = hashlib.md5(data).hexdigest()[:8]
                
                if size == PLACEHOLDER_SIZE:
                    print(f"  [{name}] Attempt {attempt+1}: Still placeholder (size=1832x1832, hash={file_hash}), waiting...")
                    os.remove(tmp_path)
                    time.sleep(30)
                    continue
                
                # 真实图片，正式保存
                final_path = os.path.join(OUT_DIR, name + ".png")
                os.rename(tmp_path, final_path)
                print(f"  [{name}] SUCCESS! Size={size}, File={len(data)} bytes, Hash={file_hash}")
                return True
            except Exception as e:
                print(f"  [{name}] Cannot open image: {e}")
                os.remove(tmp_path)
                time.sleep(15)
        except Exception as e:
            print(f"  [{name}] Download error (attempt {attempt+1}): {e}")
            time.sleep(15)
    print(f"  [{name}] FAILED after {max_retries} attempts")
    return False

print("=== Downloading Luocheng character previews ===")
success = 0
for name, url in images:
    print(f"\nDownloading {name}...")
    if download_with_retry(name, url):
        success += 1

print(f"\n=== Download complete: {success}/{len(images)} images saved ===")
print(f"Save directory: {OUT_DIR}")
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('.png'):
        path = os.path.join(OUT_DIR, f)
        img = Image.open(path)
        print(f"  {f}: {img.size}, {os.path.getsize(path)} bytes")
