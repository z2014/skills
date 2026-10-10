# 里程碑时间线 timeline

回答：**分几步做、每步交付什么、大概什么时候。**

## 数据格式

```json
{
  "type": "timeline",
  "title": "首版分几步交付",
  "summary": "先用一周验掉三个风险，再分三步做到可用",
  "milestones": [
    { "name": "技术验证", "when": "第 1 周", "deliverables": ["订阅合规结论", "审批往返跑通"], "status": "risk" },
    { "name": "编排内核", "when": "第 2～3 周", "deliverables": ["状态机", "事件日志"] }
  ]
}
```

- 里程碑 ≤ 6 个，每个交付物 ≤ 3 条。
- `status` 同样只用 `new` / `changed` / `risk`。
