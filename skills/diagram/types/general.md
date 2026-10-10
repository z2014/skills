# 通用图 general（兜底）

以上五种都不合适时（例如状态图、泳道图、ER 图），直接写 Mermaid，套用飞书主题。排版效果不保证。如果某种图反复用到，应该提议把它做成正式的图类型。

## 数据格式

```json
{
  "type": "general",
  "title": "需求的状态有哪些",
  "summary": "需求只有在拍板点会挂起",
  "mermaid": "stateDiagram-v2\n  [*] --> 进行中\n  进行中 --> 待放行\n  待放行 --> 进行中: 放行\n  待放行 --> [*]: 完成"
}
```

## 没有渲染脚本时的飞书主题

在 Mermaid 代码第一行加上：

```text
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#EEF3FF","primaryBorderColor":"#7A9CF5","primaryTextColor":"#1F2329","lineColor":"#646A73","secondaryColor":"#FFF5C2","tertiaryColor":"#F8F9FA","fontFamily":"PingFang SC, Noto Sans CJK SC, sans-serif","fontSize":"13px"}}}%%
```
