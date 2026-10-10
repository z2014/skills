# 流程图 flowchart

回答：**一件事怎么一步步走、在哪里分叉、每条路最后到哪儿。**

样式（飞书流程图）：起点/终点是浅紫胶囊，步骤是浅蓝矩形，判断是浅黄菱形，异常/打回分支是浅红矩形。主路径自上而下，分支放在右侧。

## 数据格式

```json
{
  "type": "flowchart",
  "title": "Agent 申请进入下一阶段时会发生什么",
  "summary": "产出物不全会被直接拒绝，齐全后必须等人放行",
  "nodes": [
    { "id": "s",  "kind": "start",    "text": "Agent 申请推进" },
    { "id": "v",  "kind": "step",     "text": "引擎校验产出物" },
    { "id": "d1", "kind": "decision", "text": "字段齐全？" },
    { "id": "r",  "kind": "error",    "text": "拒绝，列出缺项" },
    { "id": "e",  "kind": "end",      "text": "进入下一阶段" }
  ],
  "edges": [
    { "from": "s",  "to": "v" },
    { "from": "v",  "to": "d1" },
    { "from": "d1", "to": "e", "label": "是" },
    { "from": "d1", "to": "r", "label": "否", "branch": true },
    { "from": "r",  "to": "v", "back": true }
  ]
}
```

| 字段 | 说明 |
| --- | --- |
| `nodes[].kind` | `start` / `end` / `step` / `decision` / `error` |
| `nodes[].text` | ≤ 12 字；判断节点写成问句 |
| `edges[].label` | 判断出口必须写（是/否、通过/打回） |
| `edges[].branch` | `true` 表示侧向分支，画在主路径右侧 |
| `edges[].back` | `true` 表示回到前面某一步的回路 |

## 规则

- 只有一个 `start`；每条路径都要走到 `end` 或回到主路径。
- 每个 `decision` 恰好两个出口：一个沿主路径，一个标 `branch: true`。
- 主路径 ≤ 8 个节点，总节点 ≤ 12。更长时把子流程拆成另一张图，在主图里用一个 `step` 代表。
