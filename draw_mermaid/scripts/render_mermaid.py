#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 Mermaid 代码渲染为 PNG 图片。

用法:
  # 从 .mmd 文件渲染
  python render_mermaid.py -i diagram.mmd -o output.png

  # 从 stdin 读取 mermaid 代码
  echo "graph TD; A-->B" | python render_mermaid.py -o output.png

  # 直接传入 mermaid 代码字符串
  python render_mermaid.py --code "graph TD; A-->B" -o output.png

  # 指定主题和背景色
  python render_mermaid.py -i diagram.mmd -o output.png --theme forest --bg transparent
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def find_mmdc() -> str:
    """查找 mmdc 可执行文件路径。"""
    # 优先使用全局安装的 mmdc
    mmdc = shutil.which("mmdc")
    if mmdc:
        return mmdc

    # 尝试 npx 方式
    npx = shutil.which("npx")
    if npx:
        return f"{npx} -y @mermaid-js/mermaid-cli"

    return ""


def render(
    mermaid_code: str,
    output_path: str,
    theme: str = "default",
    bg_color: str = "white",
    width: int = 1200,
    scale: int = 2,
) -> str:
    """将 mermaid 代码渲染为 PNG 并返回输出路径。"""
    mmdc = find_mmdc()
    if not mmdc:
        print(
            "错误: 未找到 mmdc。请先安装: npm install -g @mermaid-js/mermaid-cli",
            file=sys.stderr,
        )
        sys.exit(1)

    # 确保输出目录存在
    out_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(out_dir, exist_ok=True)

    # 写入临时 .mmd 文件
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(mermaid_code)
        tmp_path = tmp.name

    try:
        cmd = (
            f"{mmdc} -i {tmp_path} -o {os.path.abspath(output_path)} "
            f"-t {theme} -b {bg_color} -w {width} -s {scale}"
        )
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60
        )

        if result.returncode != 0:
            print(f"mmdc 执行失败:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        abs_output = os.path.abspath(output_path)
        if not os.path.exists(abs_output):
            print("错误: PNG 文件未生成，请检查 mermaid 语法是否正确。", file=sys.stderr)
            sys.exit(1)

        print(f"已生成: {abs_output}")
        return abs_output
    finally:
        os.unlink(tmp_path)


def main():
    parser = argparse.ArgumentParser(description="Mermaid 代码转 PNG 图片")
    parser.add_argument("-i", "--input", help="输入 .mmd 文件路径")
    parser.add_argument(
        "-o", "--output", required=True, help="输出 PNG 文件路径"
    )
    parser.add_argument("--code", help="直接传入 mermaid 代码字符串")
    parser.add_argument(
        "--theme",
        default="default",
        choices=["default", "forest", "dark", "neutral"],
        help="渲染主题 (默认: default)",
    )
    parser.add_argument("--bg", default="white", help="背景色 (默认: white)")
    parser.add_argument("--width", type=int, default=1200, help="图片宽度 (默认: 1200)")
    parser.add_argument("--scale", type=int, default=2, help="缩放倍数 (默认: 2)")

    args = parser.parse_args()

    # 读取 mermaid 代码: --code > -i > stdin
    if args.code:
        mermaid_code = args.code
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            mermaid_code = f.read()
    elif not sys.stdin.isatty():
        mermaid_code = sys.stdin.read()
    else:
        print("错误: 请通过 --code、-i 或 stdin 提供 mermaid 代码。", file=sys.stderr)
        sys.exit(1)

    if not mermaid_code.strip():
        print("错误: mermaid 代码为空。", file=sys.stderr)
        sys.exit(1)

    render(
        mermaid_code=mermaid_code,
        output_path=args.output,
        theme=args.theme,
        bg_color=args.bg,
        width=args.width,
        scale=args.scale,
    )


if __name__ == "__main__":
    main()
