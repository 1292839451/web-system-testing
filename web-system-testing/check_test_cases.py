#!/usr/bin/env python3
"""
用例清单合规性校验脚本

功能：检查用例清单是否符合规范
- 每个功能点必须有：查看、新增、编辑、删除（4条）
- 详情页每个子Tab必须单独1条
- 用例总数 = 功能点数×4 + 详情子Tab数

使用方法：python check_test_cases.py <用例清单文件路径>
"""

import sys
import re
import io
from pathlib import Path
from collections import defaultdict

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def parse_test_cases(content: str) -> dict:
    """解析用例清单，返回结构化数据"""

    # 提取表格行
    lines = content.split('\n')
    rows = []

    # 匹配表格行（以 | 开头和结尾）
    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            # 跳过表头和分隔符行
            if '用例ID' in line or all(c == '-' for c in line.replace('|', '').replace(' ', '')):
                continue
            rows.append(line)

    # 解析每行数据
    test_cases = []
    for row in rows:
        # 分割并清理单元格
        cells = [cell.strip() for cell in row.split('|')[1:-1]]  # 去掉首尾的空单元格

        if len(cells) >= 3:
            case_id = cells[0]
            func_point = cells[1]
            op_type = cells[2]

            if case_id.startswith('TC-'):
                test_cases.append({
                    'id': case_id,
                    'func_point': func_point,
                    'op_type': op_type
                })

    return test_cases


def validate_test_cases(test_cases: list) -> tuple:
    """
    校验用例清单

    返回：(是否通过, 统计信息, 缺失项列表)
    """

    # 按功能点分组
    func_op_map = defaultdict(set)  # func_point -> set of op_types
    detail_sub_tabs = defaultdict(int)  # func_point -> count of detail sub tabs

    all_op_types = {'查看', '新增', '编辑', '删除', '详情展示'}

    for case in test_cases:
        func = case['func_point']
        op = case['op_type']

        # 检查是否是详情展示的子Tab格式（如"样地管理-基本信息"）
        if '详情展示' in op:
            # 子Tab格式：功能点名称-子Tab名称
            func_op_map[func].add('详情展示')

            # 尝试提取子Tab名称
            if '-' in func:
                parts = func.split('-', 1)
                base_func = parts[0]
                sub_tab = parts[1]
                detail_sub_tabs[base_func] += 1
        else:
            func_op_map[func].add(op)

    # 计算统计信息
    func_points_count = len(func_op_map)

    # 计算每个功能点应有的用例数
    required_cases = 0
    for func, ops in func_op_map.items():
        # 基础4条（查看、新增、编辑、删除）
        required_cases += 4
        # 加上详情子Tab数
        required_cases += detail_sub_tabs.get(func, 0)

    actual_cases = len(test_cases)

    # 检查缺失项
    missing_items = []

    for func, ops in func_op_map.items():
        missing_ops = all_op_types - ops
        # 详情展示是可选的（如果没有详情页功能的话），所以只检查基础4种
        base_missing = missing_ops - {'详情展示'}
        if base_missing:
            missing_items.append({
                'func_point': func,
                'missing_ops': base_missing
            })

    # 检查是否每个功能点都有4种基础操作类型
    passed = len(missing_items) == 0

    stats = {
        'func_points_count': func_points_count,
        'actual_cases': actual_cases,
        'required_cases': required_cases,
        'detail_sub_tabs': dict(detail_sub_tabs)
    }

    return passed, stats, missing_items


def print_report(passed: bool, stats: dict, missing_items: list):
    """打印校验报告"""

    print()
    print("【用例清单合规性检查】")

    if passed:
        print(f"检查结果：✅ 通过")
        print(f"- 功能点数：{stats['func_points_count']}个")
        print(f"- 应测用例总数：{stats['required_cases']}条")
        print(f"- 实际用例数：{stats['actual_cases']}条")
        if stats['detail_sub_tabs']:
            print(f"- 详情子Tab数：{stats['detail_sub_tabs']}")
    else:
        print(f"检查结果：❌ 不通过")
        print()
        print("缺失项：")
        for item in missing_items:
            func = item['func_point']
            missing = '、'.join(sorted(item['missing_ops']))
            print(f"- 功能点\"{func}\"缺少：{missing}")
        print()
        print("请补充完整后重新运行校验。")

    print()

    return 0 if passed else 1


def main():
    if len(sys.argv) < 2:
        print("使用方法：python check_test_cases.py <用例清单文件路径>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"错误：文件不存在 - {file_path}")
        sys.exit(1)

    content = file_path.read_text(encoding='utf-8')

    test_cases = parse_test_cases(content)

    if not test_cases:
        print("错误：未能解析用例清单，请检查文件格式")
        sys.exit(1)

    passed, stats, missing_items = validate_test_cases(test_cases)

    exit_code = print_report(passed, stats, missing_items)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()