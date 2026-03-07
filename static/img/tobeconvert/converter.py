import os
import sys
import subprocess

def main():
    # 1. 检查参数是否正确
    if len(sys.argv) != 2:
        print("用法：python3 png2bgjpg.py 起始数字")
        print("例子：python3 png2bgjpg.py 3   → 生成 bg3.jpg, bg4.jpg...")
        sys.exit(1)

    # 2. 获取起始编号
    try:
        start_num = int(sys.argv[1])
    except ValueError:
        print("错误：参数必须是整数！")
        sys.exit(1)

    # 3. 获取当前目录所有 png 文件（按文件名排序）
    png_files = sorted([f for f in os.listdir('.') if f.lower().endswith('.png')])

    if not png_files:
        print("当前目录没有找到任何 .png 文件")
        sys.exit(0)

    print(f"找到 {len(png_files)} 张 PNG 图片")
    print(f"将从 bg{start_num}.jpg 开始命名...")
    print("-" * 50)

    # 4. 逐个转换
    current_num = start_num
    for png_file in png_files:
        # 输出文件名
        jpg_file = f"bg{current_num}.jpg"

        print(f"转换：{png_file} → {jpg_file}")

        # 调用 Linux convert 命令
        try:
            subprocess.run(
                ["convert", png_file, jpg_file],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            print(f"⚠️  转换失败：{png_file}（请确认安装了 imagemagick）")
        except FileNotFoundError:
            print("❌ 错误：未找到 convert 命令，请先安装：sudo apt install imagemagick")
            sys.exit(1)

        current_num += 1

    print("-" * 50)
    print(f"✅ 全部转换完成！共 {len(png_files)} 张")

if __name__ == "__main__":
    main()