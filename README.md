<img width="1869" height="245" alt="image" src="https://github.com/user-attachments/assets/36045a04-dcad-4a15-8dc4-07699bec101d" />
<img width="355" height="580" alt="image" src="https://github.com/user-attachments/assets/80f70881-97d3-4038-90a2-f80ae417ad80" />

# Web System Testing Skill

网页系统自动化测试技能。适用于对网页系统/网页应用的增删改查功能进行功能测试、验证表单提交和业务流程、生成标准化测试报告。

## 核心能力

- **功能测试**：验证系统的增删改查、详情查看等标准功能
- **业务测试**：验证自定义业务流程（如：新增数据 → 查询 → 验证结果）
- **标准化报告**：输出四个基础 Sheet 的中文 Excel 报告，支持业务测试 Sheet 5
- **Agent 团队协作**：通过 project-manager 和 project-tester 协作执行

## 测试流程

| 阶段 | 说明 |
|------|------|
| 阶段零：环境预检 | 检测 Python、playwright、openpyxl、Chromium、验证码识别工具、Playwright MCP |
| 阶段一：信息收集 | 确认系统URL、账号、密码、模块、轮次、测试类型 |
| 阶段二：用例制定 | 制定功能测试用例清单或业务测试用例清单 |
| 阶段三：测试执行 | 使用 Playwright MCP 执行测试，降级时使用 Chrome DevTools MCP |
| 阶段四：报告生成 | 生成四个基础 Sheet + 业务测试 Sheet（如有） |
| 阶段五：评审与返工 | project-manager 评审报告，不合格则返工 |

## 浏览器工具策略

- **优先使用**：Playwright MCP（常规操作）
- **降级使用**：Chrome DevTools MCP（Playwright MCP 导航失败时）

**【重要】环境预检时只检测 Playwright MCP，不检测 Chrome DevTools MCP，避免同时启动导致冲突。**

## 前置条件

| 依赖 | 说明 |
|------|------|
| Python 3.7+ | 运行环境 |
| playwright | 浏览器自动化 |
| openpyxl | Excel 报告生成 |
| Chromium | Playwright 浏览器 |
| mcp__MiniMax__understand_image | 验证码识别（必须使用此工具，禁止 OCR） |
| Playwright MCP | 浏览器自动化 |

## 安装

1. 下载 zip 压缩包
2. 解压到 `~/.claude/skills/` 目录下
3. 目录结构：
   ```
   ~/.claude/skills/web-system-testing/
   ├── SKILL.md
   ├── README.md
   ├── scripts/
   │   ├── generate_test_report.py
   │   └── test_executor.py
   └── references/
       └── report_template.md
   ```
4. 重启 Claude Code

## CLAUDE.md 配置

为确保测试需求自动触发此 Skill，请在你的 CLAUDE.md 中添加以下触发规则：

```markdown
### 触发词规则

| 关键词 | 触发的目标 |
|--------|------------|
| 测试、验证 | web-system-testing skill |
```

## 使用方式

提出测试需求即可自动触发团队协作：

```
我要测试采伐证核发模块
```

Skill 自动执行：环境预检 → 信息确认 → 用例制定 → 测试执行 → 报告生成 → 评审与返工

## 报告格式

**四个基础 Sheet（必须）**：
- Sheet 1: 测试概要
- Sheet 2: 详细测试结果（14列，每个操作一行）
- Sheet 3: Bug 列表
- Sheet 4: 测试结果统计

**业务测试 Sheet 5（当用户有自定义业务流程时生成）**：
- 业务流程测试的详细操作步骤和结果

## 关键规则

| 规则 | 说明 |
|------|------|
| 验证码处理 | 必须使用 `mcp__MiniMax__understand_image` 工具，禁止 OCR |
| 报告语言 | 所有内容必须使用中文，禁止英文 |
| 截图命名 | `{用例ID}.png` 或 `{用例ID}_序号.png` |
| 操作步骤真实性 | 必须包含完整的数据操作，禁止"点到为止" |

详细规则见 SKILL.md。

