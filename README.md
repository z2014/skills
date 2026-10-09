# skills

[English](#english) | [中文](#中文)

## English

Agent skills that follow the open [Agent Skills](https://agentskills.io) format. They work with Claude Code, Codex, Cursor, and other agents that support `SKILL.md`.

| Skill | Description |
| --- | --- |
| [`dev-principles`](skills/dev-principles/SKILL.md) | Development principles: ubiquitous language, tracer bullets, deep modules |

The skill content is written in Chinese. The skill description is bilingual so that agents can select the skill in either language.

### Install

Use the [`skills`](https://github.com/vercel-labs/skills) CLI for any supported agent:

```bash
npx skills add z2014/skills -g
```

Use the plugin marketplace in Claude Code:

```
/plugin marketplace add z2014/skills
/plugin install skills@z2014
```

### Update

```bash
npx skills update -g
```

In Claude Code, run `/plugin marketplace update z2014`, then `/plugin update skills@z2014`.

### Optional: always apply the principles

Agents read skill descriptions in every session and load the full skill when a task matches. To require the skill for all non-trivial work, add this line to your global instructions (`~/.codex/AGENTS.md` or `~/.claude/CLAUDE.md`):

```markdown
- Before non-trivial feature work, cross-module changes, refactoring, or design review, use the `dev-principles` skill and follow its checklist.
```

### Sources

- Tracer bullets: *The Pragmatic Programmer*, David Thomas and Andrew Hunt
- Deep modules: *A Philosophy of Software Design*, John Ousterhout
- Ubiquitous language: *Domain-Driven Design*, Eric Evans

## 中文

遵循开放的 [Agent Skills](https://agentskills.io) 格式，可用于 Claude Code、Codex、Cursor 等支持 `SKILL.md` 的 Agent。

| Skill | 说明 |
| --- | --- |
| [`dev-principles`](skills/dev-principles/SKILL.md) | 开发原则 |

### 安装

使用 [`skills`](https://github.com/vercel-labs/skills) 命令行工具，适用于各类 Agent：

```bash
npx skills add z2014/skills -g
```

在 Claude Code 中使用插件市场：

```
/plugin marketplace add z2014/skills
/plugin install skills@z2014
```

### 更新

```bash
npx skills update -g
```

在 Claude Code 中执行 `/plugin marketplace update z2014`，然后执行 `/plugin update skills@z2014`。

### 可选：始终应用这些原则

Agent 在每次会话中都会读取 skill 的描述，并在任务匹配时加载完整内容。如果希望所有非琐碎工作都使用该 skill，在全局指令文件（`~/.codex/AGENTS.md` 或 `~/.claude/CLAUDE.md`）中加入：

```markdown
- 开始非琐碎的功能开发、跨模块修改、重构或设计评审前，调用 `dev-principles` skill 并按其清单执行。
```

### 来源

- 贯通路径（Tracer Bullet）：《程序员修炼之道》
- 深模块（Deep Modules）：《软件设计哲学》
- 统一语言（Ubiquitous Language）：《领域驱动设计》

## License

[MIT](LICENSE)
