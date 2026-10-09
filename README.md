# skills

个人 Agent skills 与全局指令。

| 路径 | 内容 |
| --- | --- |
| `AGENTS.md` | 加入全局指令文件的核心开发原则 |
| `dev-principles/SKILL.md` | 统一语言、贯通路径和深模块的执行清单 |

## 安装

安装 skill：

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -R dev-principles ~/.claude/skills/
# Codex
mkdir -p ~/.codex/skills && cp -R dev-principles ~/.codex/skills/
```

安装全局指令：将 `AGENTS.md` 中的内容追加到 `~/.codex/AGENTS.md` 或 `~/.claude/CLAUDE.md`。

## 来源

- Tracer Bullet：《程序员修炼之道》（The Pragmatic Programmer）
- Deep Modules：《软件设计哲学》（A Philosophy of Software Design）
- Ubiquitous Language：《领域驱动设计》（Domain-Driven Design）
