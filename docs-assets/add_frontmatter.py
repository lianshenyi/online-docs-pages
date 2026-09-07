#!/usr/bin/env python3
"""
为所有 md 文件添加 front-matter
- tags: 根据文件夹路径生成，用 - 连接
- title: 文件名（不含扩展名）
- 如果已有 front-matter 则跳过
"""

import os
import re

def get_tags_and_title(filepath):
    # 去掉开头的 ./
    path = filepath.lstrip('./')
    parts = path.split('/')
    # title 是文件名去掉 .md
    filename = parts[-1]
    title = filename[:-3] if filename.endswith('.md') else filename
    # tags 是所有文件夹部分，用 - 连接
    folders = parts[:-1]
    tag = '-'.join(folders) if folders else ''
    return tag, title

def has_frontmatter(content):
    return content.startswith('---')

def add_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_frontmatter(content):
        return False  # 已有 front-matter，跳过

    tag, title = get_tags_and_title(filepath)

    # 构建 front-matter
    fm_lines = ['---']
    fm_lines.append(f'title: "{title}"')
    if tag:
        fm_lines.append(f'tags: [{tag}]')
    fm_lines.append('---')
    fm_lines.append('')

    frontmatter = '\n'.join(fm_lines)
    new_content = frontmatter + content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    added = 0
    skipped = 0
    for root, dirs, files in os.walk('.'):
        # 跳过 .obsidian 目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.endswith('.md'):
                continue
            filepath = os.path.join(root, file)
            result = add_frontmatter(filepath)
            if result:
                print(f'[added]   {filepath}')
                added += 1
            else:
                print(f'[skipped] {filepath}')
                skipped += 1

    print(f'\n完成: 新增 {added} 个，跳过 {skipped} 个')

if __name__ == '__main__':
    main()
