# 时序图 sequence

回答：**多个参与方之间按什么顺序交互、谁在等谁。**

## 数据格式

```json
{
  "type": "sequence",
  "title": "放行后谁做什么",
  "summary": "放行后由软件推分支，Agent 全程不碰凭证",
  "participants": ["你", "工作台", "实现 Agent", "GitHub"],
  "messages": [
    { "from": "你", "to": "工作台", "text": "放行" },
    { "from": "工作台", "to": "实现 Agent", "text": "进入实现阶段" },
    { "from": "实现 Agent", "to": "工作台", "text": "diff + 测试报告", "reply": true },
    { "from": "工作台", "to": "GitHub", "text": "推分支、建 PR" }
  ],
  "notes": [{ "over": "实现 Agent", "after": 1, "text": "沙箱内自动执行" }]
}
```

## 规则

- 参与方 ≤ 6，消息 ≤ 15。
- `reply: true` 画成虚线返回。
- 渲染脚本会转成带飞书主题的 Mermaid `sequenceDiagram`。
