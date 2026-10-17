#!/usr/bin/env python3
"""
对所有 md 文件进行脱敏处理
- 跳过代码块内容（``` 和 ` 包裹的部分）
- 脱敏规则：
  - 身份证号   → <<身份证号>>
  - 手机号     → <<手机号>>
  - 邮箱       → <<邮箱>>
  - 密码字段   → <<密码>>
  - AWS AK     → <<AWS-AK>>
  - AWS SK     → <<AWS-SK>>
  - 公网 IP    → <<公网IP>>（私有/回环段不替换）
"""

import os
import re

# ─── 脱敏规则 ────────────────────────────────────────────────────────────────

RULES = [
    # 身份证号（18位，末位可为X）
    (re.compile(r'\b\d{17}[\dXx]\b'), '<<身份证号>>'),
    # 手机号（1开头，第二位3-9，共11位）
    (re.compile(r'\b1[3-9]\d{9}\b'), '<<手机号>>'),
    # 邮箱
    (re.compile(r'\b[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}\b'), '<<邮箱>>'),
    # 密码字段（password/passwd/pwd = 值）
    (re.compile(r'(password|passwd|pwd)\s*[:=]\s*\S+', re.IGNORECASE), r'\1=<<密码>>'),
    # AWS AccessKey
    (re.compile(r'\b(AKIA|ASIA|AROA|AIDA)[A-Z0-9]{16}\b'), '<<AWS-AK>>'),
    # AWS SecretKey（secret_key = 后面20位以上，用分组捕获前缀）
    (re.compile(r'([Ss]ecret[_\s\-]?[Kk]ey\s*[:=]\s*)[A-Za-z0-9/+=]{20,}'), r'\1<<AWS-SK>>'),
    # 公网 IP（排除 10.x、127.x、172.16-31.x、192.168.x）
    (re.compile(
        r'\b(?!(?:10|127)\.|172\.(?:1[6-9]|2\d|3[01])\.|192\.168\.)'
        r'(\d{1,3}\.){3}\d{1,3}\b'
    ), '<<公网IP>>'),
]

# ─── 核心函数 ────────────────────────────────────────────────────────────────

def desensitize_text(text: str) -> str:
    """提取代码块 → 脱敏普通文本 → 还原代码块"""
    blocks = []

    def save_block(m):
        blocks.append(m.group(0))
        return f'\x00BLOCK{len(blocks) - 1}\x00'

    # 先保护多行代码块，再保护行内代码
    result = re.sub(r'```[\s\S]*?```', save_block, text)
    result = re.sub(r'`[^`\n]+`', save_block, result)

    for pattern, replacement in RULES:
        result = pattern.sub(replacement, result)

    # 还原代码块
    result = re.sub(r'\x00BLOCK(\d+)\x00', lambda m: blocks[int(m.group(1))], result)
    return result


def process_file(filepath: str) -> bool:
    """对单个文件脱敏，返回是否有改动"""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    cleaned = desensitize_text(original)

    if cleaned == original:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    return True

# ─── 入口 ────────────────────────────────────────────────────────────────────

def main():
    changed = 0
    unchanged = 0

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.endswith('.md'):
                continue
            filepath = os.path.join(root, file)
            if process_file(filepath):
                print(f'[脱敏]   {filepath}')
                changed += 1
            else:
                print(f'[无变化] {filepath}')
                unchanged += 1

    print(f'\n完成: 脱敏 {changed} 个，无变化 {unchanged} 个')


if __name__ == '__main__':
    main()
