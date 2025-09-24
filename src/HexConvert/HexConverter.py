"""

created by: zzh 2025-09-23

二进制 <-> 十六进制文本 转换

功能:
  - bin_to_hex(src, dst) : 二进制文件 -> 十六进制文本文件
  - hex_to_bin(src, dst) : 十六进制文本文件 -> 二进制文件

规范:
  - 输出文本: 每行16字节，字节用空格分隔，大写 (如: "00 1A FF ...")
  - 输入十六进制文本可包含任意非十六进制字符(空白/逗号/冒号等)——会被忽略
  - 过滤后若总长度为奇数 -> 抛出 ValueError
"""
from __future__ import annotations
import os
import re


def bin_to_hex(src: str, dst: str) -> None:
    """二进制文件 -> 十六进制文本文件"""
    if not os.path.isfile(src):
        raise FileNotFoundError(f"输入文件不存在: {src}")
    with open(src, "rb") as fin, open(dst, "w", encoding="ascii") as fout:
        buffer = bytearray()
        while True:
            chunk = fin.read(1024 * 1024)
            if not chunk:
                break
            buffer.extend(chunk)
            while len(buffer) >= 16:
                line_bytes = buffer[:16]
                del buffer[:16]
                fout.write(" ".join(f"{b:02X}" for b in line_bytes) + "\n")
        # 余数
        if buffer:
            fout.write(" ".join(f"{b:02X}" for b in buffer) + "\n")


def hex_to_bin(src: str, dst: str) -> None:
    """十六进制文本文件 -> 二进制文件"""
    if not os.path.isfile(src):
        raise FileNotFoundError(f"输入文件不存在: {src}")
    with open(src, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    hexchars = re.sub(r"[^0-9A-Fa-f]", "", raw)
    if len(hexchars) % 2 == 1:
        raise ValueError("十六进制文本长度为奇数，存在残缺字节。")
    data = bytes.fromhex(hexchars)
    with open(dst, "wb") as fout:
        fout.write(data)

