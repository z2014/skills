# 样例：规则引擎

需求一句话：用不含 AI 的状态机推进研发流程，Agent 只能"申请"推进，是否进入下一阶段由人放行。

- `architecture.json`：规则引擎由什么组成（分层架构图）
- `advance-flow.json`：Agent 申请进入下一阶段时会发生什么（流程图）
- `engine-options.json`：工作流引擎选哪个（方案对比矩阵）
- `release-sequence.json`：放行后谁做什么（时序图，Mermaid）

渲染：`python3 ../../scripts/render.py architecture.json`
