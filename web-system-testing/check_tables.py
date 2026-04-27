#!/usr/bin/env python3
"""检查SKILL.md中的表格格式"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

content = open('C:/Users/z1292/.claude/skills/web-system-testing/SKILL.md', 'r', encoding='utf-8').read()

lines = content.split('\n')
tables = []
current_table = []
in_code_block = False

for i, line in enumerate(lines):
    if line.startswith('```'):
        in_code_block = not in_code_block
        continue
    if in_code_block:
        continue

    stripped = line.strip()
    if stripped.startswith('|') and stripped.endswith('|'):
        current_table.append((i+1, stripped))
    else:
        if current_table:
            tables.append(current_table)
            current_table = []

if current_table:
    tables.append(current_table)

print(f"共发现 {len(tables)} 个表格\n")

issues = []
for idx, table in enumerate(tables):
    if len(table) < 2:
        continue

    sep_idx = -1
    for j, (line_num, content) in enumerate(table):
        cells = [c.strip() for c in content.split('|')[1:-1]]
        if cells and all(c in '-:' for c in cells[0].replace('-', '').replace(':', '')):
            sep_idx = j
            break

    if sep_idx > 0:
        header_cells = len([c.strip() for c in table[0][1].split('|')[1:-1]])
        sep_cells = len([c.strip() for c in table[sep_idx][1].split('|')[1:-1]])
        if header_cells != sep_cells:
            issues.append(f"表格{idx+1}（第{table[0][0]}行）列数不匹配：表头{header_cells}列，分隔符{sep_cells}列")
            print(f"❌ 表格{idx+1}（第{table[0][0]}行）列数不匹配：表头{header_cells}列，分隔符{sep_cells}列")
        else:
            print(f"✅ 表格{idx+1}（第{table[0][0]}行）：{header_cells}列 - OK")
    else:
        col_counts = set()
        for line_num, line_content in table:
            cells = [c.strip() for c in line_content.split('|')[1:-1]]
            col_counts.add(len(cells))
        if len(col_counts) > 1:
            issues.append(f"表格{idx+1}（第{table[0][0]}行）列数不一致：{col_counts}")
            print(f"❌ 表格{idx+1}（第{table[0][0]}行）列数不一致：{col_counts}")
        else:
            print(f"✅ 表格{idx+1}（第{table[0][0]}行）：{list(col_counts)[0]}列（无分隔符）- OK")

print(f"\n共检查 {len(tables)} 个表格，发现 {len(issues)} 个问题")

if issues:
    print("\n问题列表：")
    for issue in issues:
        print(f"  - {issue}")