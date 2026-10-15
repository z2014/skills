# skills

[English](#english) | [中文](#中文)

## English

Agent skills that follow the open [Agent Skills](https://agentskills.io) format. They work with Claude Code, Codex, Cursor, and other agents that support `SKILL.md`.

| Skill | Description |
| --- | --- |
| [`dev-principles`](skills/dev-principles/SKILL.md) | Development principles: ubiquitous language, tracer bullets, deep modules, unidirectional dependencies |
| [`frontend-dev`](skills/frontend-dev/SKILL.md) | React frontend conventions: Vite, Tailwind v4, shadcn/ui, TanStack Query, Zustand, project layout |
| [`ui-ux`](skills/ui-ux/SKILL.md) | Reference-based design systems and interaction refinement: visual hierarchy, typography, motion, responsive layouts, dragging, keyboard interaction |
| [`diagram`](skills/diagram/SKILL.md) | Feishu-whiteboard-style diagrams: layered architecture, flowchart, sequence, comparison matrix |
| [`feature-dev`](skills/feature-dev/SKILL.md) | Guided feature development: discovery, codebase exploration, clarifying questions, architecture design, implementation, quality review, summary |

The skill content is written in Chinese. Skill descriptions state when each skill applies.

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
- Unidirectional dependencies: the Acyclic and Stable Dependencies Principles in *Agile Software Development: Principles, Patterns, and Practices*, and the Dependency Rule in *Clean Architecture*, Robert C. Martin
- `feature-dev`: Chinese translation of the [`feature-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev) plugin in anthropics/claude-plugins-official, licensed under Apache License 2.0
- `ui-ux`: design-system and interaction guidance synthesized from [`open-claude-ui`](https://github.com/Caho1/open-claude-ui), with browser and accessibility references linked in the skill

## 中文

遵循开放的 [Agent Skills](https://agentskills.io) 格式，可用于 Claude Code、Codex、Cursor 等支持 `SKILL.md` 的 Agent。

| Skill | 说明 |
| --- | --- |
| [`dev-principles`](skills/dev-principles/SKILL.md) | 开发原则：统一语言、贯通路径、深模块、单向依赖 |
| [`frontend-dev`](skills/frontend-dev/SKILL.md) | React 前端开发规范：Vite、Tailwind v4、shadcn/ui、TanStack Query、Zustand、项目结构 |
| [`ui-ux`](skills/ui-ux/SKILL.md) | UI/UX 设计与交互打磨：参考界面设计系统提取、视觉层级、排版、动效、响应式布局、拖拽、键盘交互 |
| [`diagram`](skills/diagram/SKILL.md) | 飞书画板风格画图规范：分层架构图、流程图、时序图、方案对比矩阵 |
| [`feature-dev`](skills/feature-dev/SKILL.md) | 引导式功能开发：需求理解、代码库探索、澄清问题、架构设计、实现、质量审查、总结 |

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
- 单向依赖（Unidirectional Dependencies）：《敏捷软件开发：原则、模式与实践》中的无环依赖原则与稳定依赖原则，《架构整洁之道》中的依赖规则
- `feature-dev`：译自 anthropics/claude-plugins-official 的 [`feature-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev) 插件，采用 Apache License 2.0
- `ui-ux`：参考 [`open-claude-ui`](https://github.com/Caho1/open-claude-ui) 归纳设计系统与交互方法，浏览器及可访问性参考见 skill 内文档

## License

[MIT](LICENSE), except [`skills/feature-dev`](skills/feature-dev), which is a translation of an Apache License 2.0 project and remains under the [Apache License 2.0](skills/feature-dev/LICENSE).
