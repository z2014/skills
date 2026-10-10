# 方案对比矩阵 comparison-matrix

回答：**几个方案选哪个、为什么。**

## 数据格式

```json
{
  "type": "comparison-matrix",
  "title": "工作流引擎选哪个",
  "summary": "推荐自研状态机：单机足够，依赖最少",
  "criteria": ["实现成本", "单机适配", "可测试性", "依赖体积"],
  "options": [
    { "name": "自研状态机", "recommended": true,
      "scores": ["good", "good", "good", "good"],
      "notes": ["约 1～2k 行", "", "事件回放", "无"] },
    { "name": "Temporal",
      "scores": ["bad", "bad", "mid", "bad"],
      "notes": ["", "为分布式设计", "", "需要服务端"] }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `criteria` | 评估维度，3～6 个，写人关心的维度 |
| `options[].scores` | 与 `criteria` 一一对应：`good` / `mid` / `bad` |
| `options[].notes` | 可选，每格一句话理由 |
| `options[].recommended` | 推荐项，最多一个 |

## 规则

- 方案 2～4 个。只有一个方案就不需要矩阵。
- 每个 `bad` 都应该有一句理由。
- 渲染脚本可以输出 Mermaid：每个方案一组，格子颜色表示 `good` / `mid` / `bad`。
