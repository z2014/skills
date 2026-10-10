# 方案对比矩阵 comparison-matrix

回答：**几个方案选哪个、为什么。**

## 数据格式

```json
{
  "type": "comparison-matrix",
  "title": "工作流引擎选哪个",
  "summary": "推荐自研状态机：单机足够，依赖最少",
  "criteria": [
    { "id": "cost", "name": "实现成本" },
    { "id": "single", "name": "单机适配" },
    { "id": "test", "name": "可测试性" },
    { "id": "deps", "name": "依赖体积" }
  ],
  "options": [
    { "id": "fsm", "name": "自研状态机", "recommended": true,
      "scores": ["good", "good", "good", "good"],
      "notes": ["约 1～2k 行", "", "事件回放", "无"] },
    { "id": "temporal", "name": "Temporal",
      "scores": ["bad", "bad", "mid", "bad"],
      "notes": ["", "为分布式设计", "", "需要服务端"] }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `criteria[].id` | 必填，行锚点。修订时沿用，不改名。表头 `data-id` |
| `criteria[].name` | 维度名称，3～6 个，写人关心的维度 |
| `options[].id` | 必填，列锚点。修订时沿用，不改名。表头 `data-id` |
| `options[].scores` | 与 `criteria` 一一对应：`good` / `mid` / `bad` |
| `options[].notes` | 可选，每格一句话理由 |
| `options[].recommended` | 推荐项，最多一个 |
| 单元格锚点 | `{维度id} x {方案id}`，例如 `cost x fsm`。渲染为单元格的 `data-id` |

## 规则

- 方案 2～4 个。只有一个方案就不需要矩阵。
- 每个 `bad` 都应该有一句理由。
- 维度 id、方案 id、单元格锚点互不重复。修订时沿用已有 id，只给新维度或新方案分配新 id。
- 渲染脚本可以输出 Mermaid：每个方案一组，格子颜色表示 `good` / `mid` / `bad`。
