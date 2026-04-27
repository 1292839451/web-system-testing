"""
网页系统测试执行器
负责执行具体的测试操作：登录、导航、功能测试、截图
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class TestResult:
    """测试结果数据类"""

    def __init__(self, seq: int, case_id: str, function_name: str, operation_type: str, priority: str = "P1"):
        self.seq = seq
        self.case_id = case_id  # 用例ID，如 TC-001
        self.function_name = function_name
        self.operation_type = operation_type  # 新增/查看/编辑/删除
        self.priority = priority
        self.steps = ""
        self.expected_result = ""
        self.actual_result = ""
        self.test_time = ""
        self.ui_test = ""  # UI测试结果，无异常写"无"
        self.performance = ""  # 性能测试，如"1250ms"
        self.remarks = ""  # 备注
        self.status = ""  # 通过/失败/阻塞/未测试
        self.screenshot_name = ""  # 截图文件名

    def to_dict(self) -> dict:
        return {
            "序号": self.seq,
            "用例ID": self.case_id,
            "功能点": self.function_name,
            "操作类型": self.operation_type,
            "优先级": self.priority,
            "操作步骤": self.steps,
            "预期结果": self.expected_result,
            "实际结果": self.actual_result,
            "测试时间": self.test_time,
            "UI测试": self.ui_test,
            "性能测试": self.performance,
            "截图名称": self.screenshot_name,
            "备注": self.remarks,
            "status": self.status,
        }


class TestBug:
    """Bug数据类"""

    def __init__(self, bug_id: str, case_id: str, function_name: str, severity: str,
                 description: str, expected: str, actual: str,
                 status: str = "待确认", suggestion: str = ""):
        self.bug_id = bug_id
        self.case_id = case_id  # 对应的用例ID，如 TC-001
        self.function_name = function_name
        self.severity = severity
        self.description = description
        self.expected = expected
        self.actual = actual
        self.status = status
        self.suggestion = suggestion

    def to_dict(self) -> dict:
        return {
            "Bug ID": self.bug_id,
            "用例ID": self.case_id,
            "功能点": self.function_name,
            "严重程度": self.severity,
            "问题描述": self.description,
            "预期结果": self.expected,
            "实际结果": self.actual,
            "状态": self.status,
            "建议": self.suggestion
        }


class TestRunData:
    """测试运行数据容器"""

    def __init__(self, run_name: str, module: str, test_time: str):
        self.run_name = run_name
        self.module = module
        self.test_time = test_time
        self.test_results: List[TestResult] = []
        self.bugs: List[TestBug] = []
        self.blocked_items: List[str] = []

    def add_result(self, result: TestResult):
        self.test_results.append(result)

    def add_bug(self, bug: TestBug):
        self.bugs.append(bug)

    def add_blocked_item(self, item: str):
        self.blocked_items.append(item)

    def to_dict(self) -> dict:
        return {
            "run_name": self.run_name,
            "module": self.module,
            "test_time": self.test_time,
            "test_results": [r.to_dict() for r in self.test_results],
            "bugs": [b.to_dict() for b in self.bugs],
            "blocked_items": self.blocked_items,
            "total_functions": len(set(r.function_name for r in self.test_results)),
            "tested_count": len([r for r in self.test_results if r.actual_result]),
            "passed_count": len([r for r in self.test_results if r.actual_result and r.remarks != "失败"]),
            "failed_count": len([r for r in self.test_results if r.remarks == "失败"]),
            "blocked_count": len([r for r in self.test_results if r.remarks == "阻塞"]),
        }

    def save_to_json(self, output_dir: str):
        """保存测试数据到JSON文件"""
        output_path = Path(output_dir) / "test_data.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        return str(output_path)


def create_test_result(seq: int, case_id: str, function_name: str, operation_type: str, priority: str = "P1") -> TestResult:
    """创建测试结果对象

    Args:
        seq: 序号
        case_id: 用例ID（如 TC-001）
        function_name: 功能点名称
        operation_type: 操作类型（新增/查看/编辑/删除）
        priority: 优先级（P0/P1/P2）
    """
    return TestResult(seq, case_id, function_name, operation_type, priority)


def create_bug(bug_id: str, case_id: str, function_name: str, severity: str,
               description: str, expected: str, actual: str,
               status: str = "待确认", suggestion: str = "") -> TestBug:
    """创建Bug对象"""
    return TestBug(bug_id, case_id, function_name, severity, description, expected, actual, status, suggestion)


def load_test_data_from_json(json_path: str) -> TestRunData:
    """从JSON文件加载测试数据"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    run_data = TestRunData(data["run_name"], data["module"], data["test_time"])

    for r in data.get("test_results", []):
        result = TestResult(
            r["序号"],
            r.get("用例ID", ""),
            r["功能点"],
            r.get("操作类型", "查看"),
            r.get("优先级", "P1")
        )
        result.steps = r.get("操作步骤", "")
        result.expected_result = r.get("预期结果", "")
        result.actual_result = r.get("实际结果", "")
        result.test_time = r.get("测试时间", "")
        result.ui_test = r.get("UI测试", "")
        result.performance = r.get("性能测试", "")
        result.remarks = r.get("备注", "")
        result.status = r.get("status", "")
        result.screenshot_name = r.get("截图名称", "")
        run_data.add_result(result)

    for b in data.get("bugs", []):
        bug = TestBug(
            b["Bug ID"], b.get("用例ID", ""), b["功能点"], b["严重程度"],
            b["问题描述"], b["预期结果"], b["实际结果"],
            b.get("状态", "待确认"), b.get("建议", "")
        )
        run_data.add_bug(bug)

    run_data.blocked_items = data.get("blocked_items", [])

    return run_data


if __name__ == "__main__":
    # 测试代码
    run_data = TestRunData("第一轮", "测试模块", "2026-04-21")

    # 添加测试结果 - 每个操作单独一行
    result = create_test_result(1, "TC-001", "功能A", "新增", "P0")
    result.steps = "1. 点击功能A Tab 2. 点击新增按钮 3. 填写表单字段 4. 点击保存"
    result.expected_result = "弹出保存成功提示，列表显示新记录"
    result.actual_result = "弹出保存成功提示，列表显示新记录"
    result.test_time = "2026-04-21 10:30"
    result.ui_test = "无"
    result.performance = "1250ms"
    result.screenshot_name = "TC-001_功能A_新增.png"
    result.status = "通过"
    run_data.add_result(result)

    result2 = create_test_result(2, "TC-002", "功能A", "查看", "P0")
    result2.steps = "1. 在功能A列表中点击任意记录查看详情"
    result2.expected_result = "显示完整的表单信息"
    result2.actual_result = "显示完整的表单信息"
    result2.test_time = "2026-04-21 10:35"
    result2.ui_test = "无"
    result2.performance = "890ms"
    result2.screenshot_name = "TC-002_功能A_查看.png"
    result2.status = "通过"
    run_data.add_result(result2)

    # 保存数据
    output = run_data.save_to_json(r"c:\PythonWork\autoTest\test_runs\testRun-001-20260421")
    print(f"测试数据已保存: {output}")

    print(json.dumps(run_data.to_dict(), ensure_ascii=False, indent=2))
