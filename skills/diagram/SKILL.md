---
name: diagram
description: "Feishu-whiteboard-style diagrams for distilling AI output into one picture per question: layered architecture, flowchart, sequence, comparison matrix, milestone timeline. Agent writes structured JSON, a bundled renderer produces a self-contained HTML/SVG preview. Use when presenting a design, architecture, process, option comparison or plan to a human, or when asked to draw a diagram. 画图规范：需要把方案、架构、流程、方案对比或计划用图呈现给人看，或用户要求画图时使用。"
---

# 画图

目标：把 AI 产出里人真正关心的信息提炼出来，用一张最直观的图呈现。**你只负责想清楚内容，输出结构化数据；样式和排版交给渲染脚本**，保证谁来画都长得一样（飞书画板风格）。

## 工作步骤

1. **先写一句话结论**：这张图想让人得出什么判断。写不出来就说明还没想清楚，先别画。
2. **选图**：按下表，一张图只回答一个问题。一个问题需要两种图时，画两张。
3. **写数据**：按 `types/<类型>.md` 里的格式写一个 JSON 文件，例如 `diagram.json`。
4. **渲染**：`python3 <本 skill 目录>/scripts/render.py diagram.json -o diagram.html`，打开 HTML 检查。
5. **自检**（见文末清单），不通过就改数据重新渲染。
6. **交付**：一句话结论 + HTML 文件路径；需要贴进 Markdown 时，加 `--mermaid` 参数输出 Mermaid 代码。

如果环境里有 `draw_*` 这类 MCP 画图工具，优先直接调用工具（参数就是同一份 JSON）。没有 Python 时，直接输出 Mermaid，并在开头带上 `types/general.md` 里的飞书主题配置。

## 选图

| 要回答的问题 | 图类型 | 定义 |
| --- | --- | --- |
| 系统由什么组成、谁依赖谁 | 分层架构图 `layered-architecture` | `types/layered-architecture.md` |
| 一件事怎么一步步走、在哪里分叉 | 流程图 `flowchart` | `types/flowchart.md` |
| 多个参与方按什么顺序交互 | 时序图 `sequence` | `types/sequence.md` |
| 几个方案选哪个 | 方案对比矩阵 `comparison-matrix` | `types/comparison-matrix.md` |
| 分几步做、各在什么时候 | 里程碑时间线 `timeline` | `types/timeline.md` |
| 以上都不合适 | 通用图 `general`（Mermaid） | `types/general.md` |

不要画"影响范围图"（这次改动碰到哪些文件/模块）。它是事实，应该由工具从 `git diff` 和代码依赖计算出来，不能由 Agent 凭印象画；设计阶段只在架构图里标注"计划新增/修改"。

## 画图原则

- **一张图一个问题**。架构图里不画先后顺序；流程图里不画模块组成；不在一张图里混用"调用"和"读写数据"两种关系。
- **节点数 ≤ 12**（硬上限 15）。超了就拆：架构图按 C4 思路分层下钻（先系统全景，再展开某个模块），流程图把子流程单独画。
- **命名和代码一致**：模块名用代码里真实的目录/服务名，或者"中文名 + 代码名"。
- **颜色有固定含义，不能挪作他用**：绿 = 新增，橙 = 修改，灰/白 = 不变，红 = 风险或异常分支。用 `status` 字段表达，不要自己指定颜色。
- **文字短**：节点内 ≤ 12 个字，细节放到图外的说明里。
- **先结论后图**：每张图都带 `title`（回答什么问题）和 `summary`（一句话结论）。

## 自检清单

- [ ] JSON 能被 `render.py` 正常渲染，没有报错或警告
- [ ] 一张图只回答 `title` 里那一个问题
- [ ] 节点数没超限
- [ ] `status` 只用在真的新增、修改、有风险的地方
- [ ] 流程图有且只有一个起点，每条路径都能走到终点
- [ ] 人只看这张图和一句话结论，就能做出判断
