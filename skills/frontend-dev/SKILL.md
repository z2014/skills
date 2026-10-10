---
name: frontend-dev
description: "React frontend conventions: Vite, TypeScript, Tailwind v4, shadcn/ui, React Router, TanStack Query, Zustand, React Hook Form + Zod, pnpm, and a modules/common/api/store project layout. Use when creating or changing React frontend code, pages, components, styles, state, or frontend tooling. React 前端开发规范：在新建或修改 React 页面、组件、样式、状态管理或前端工程配置时使用。"
---

# React 前端开发

新项目使用下面的默认技术栈和项目结构。已有项目沿用现有的技术选型和约定；没有用户要求时，不引入替代方案，也不迁移现有工具。与 `dev-principles` 同时适用。

## 默认技术栈

| 方面 | 默认选择 |
| --- | --- |
| 构建与开发服务器 | Vite |
| 语言 | TypeScript（`strict`） |
| 样式 | Tailwind CSS v4，通过 `@tailwindcss/vite` 引入 |
| 组件 | shadcn/ui |
| 路由 | React Router |
| 服务端数据 | TanStack Query |
| 全局客户端状态 | Zustand |
| 表单与校验 | React Hook Form + Zod |
| 代码检查与格式化 | ESLint（typescript-eslint、react-hooks）+ Prettier（prettier-plugin-tailwindcss） |
| 包管理 | pnpm；已有项目按 lockfile 使用对应的包管理器 |

需要服务端渲染、SEO 或全栈能力时，不默认使用 Vite 单页应用，先与用户确认框架。

## 项目结构

```text
src/
├── main.tsx              # 应用入口，挂载全局 Provider
├── router.tsx            # 路由表，每个路由指向 modules 下的模块
├── modules/              # 每个路由一个模块
│   └── <module>/
│       ├── index.tsx     # 页面组件（路由入口）
│       ├── components/   # 仅本模块使用的组件
│       ├── hooks/        # 本模块的 hooks
│       └── store.ts      # 本模块的页面状态（需要时）
├── common/
│   ├── components/       # 全局公共组件；shadcn/ui 组件放在 common/components/ui
│   └── utils/            # 全局公共工具函数，包括 cn()
├── api/                  # 后端接口：请求函数、Zod schema、query key，按业务领域分文件
└── store/                # 只存放全局状态（Zustand）
```

- 每个路由对应 `modules/` 下的一个模块。嵌套路由的子页面放在父模块内部的子目录中。
- 只在一个模块里使用的组件、hooks 和状态，放在该模块内部。两个及以上模块要用时，再提取到 `common/`。
- 依赖方向：`modules` → `api`、`store`、`common`；`api`、`store` → `common/utils`。`common` 不依赖 `modules`、`api` 或 `store`。
- 模块之间不互相 import。需要共享的内容提取到 `common/`；需要共享的状态放进 `store/`。
- 配置 shadcn/ui 的 `components.json`，把组件路径设为 `@/common/components/ui`，工具函数路径设为 `@/common/utils`。

## 状态

按状态类型选择存放位置：

- 服务端数据使用 TanStack Query，不复制到 Zustand 或组件 state 中。query key 和请求函数定义在 `api/` 中，模块中调用 `useQuery` / `useMutation`。
- `store/` 只存放跨页面共享的全局状态，例如登录态、主题、全局配置。每个 store 只负责一个领域。
- 页面状态放在所属模块内部：简单状态用 `useState` / `useReducer`；模块内多个组件共享的状态，放在模块的 `store.ts` 中。
- 筛选条件、分页和当前标签页放在 URL 参数中。
- 能从已有状态计算出来的值，直接计算，不另外存储。

## 数据与 API

- 所有后端请求定义在 `api/` 中，模块和组件不直接调用 `fetch`。
- 在 `api/` 中使用 Zod 校验响应数据，并从 schema 推导 TypeScript 类型。
- 每个数据视图都要处理加载中、空数据和出错三种状态。在路由层设置错误边界（Error Boundary）。
- 修改数据后，使相关 query 失效或更新缓存，不手动同步多份数据。

## 组件与样式

- 优先使用 shadcn/ui 组件，并在其基础上组合。需要新的基础组件时，通过 shadcn CLI 添加，不重复手写。
- 设计变量（颜色、间距、圆角、字体）定义在 CSS 的 `@theme` 中。不散落硬编码的颜色值；少用任意值（如 `w-[437px]`）。
- 使用 `cn()`（clsx + tailwind-merge）合并类名。条件样式通过 `cn()` 或组件变体实现。
- 同一组类名重复出现时，提取为组件，而不是使用 `@apply`。
- 组件接收数据和回调作为 props；数据请求和全局状态的访问放在页面组件或 hooks 中。

## 可访问性

- 使用语义化 HTML：按钮用 `<button>`，链接用 `<a>`，不给 `<div>` 绑定点击事件代替按钮。
- 表单控件都有对应的 label；图标按钮提供 `aria-label`。
- 所有交互都可以通过键盘完成，焦点状态清晰可见。

## 性能

- 不预防性地添加 `useMemo`、`useCallback` 或 `memo`。只在测量到性能问题，或项目约定要求时使用；项目启用 React Compiler 时，交给编译器处理。
- 路由级页面按需加载（`lazy`）。
- 长列表考虑虚拟滚动；图片指定尺寸并延迟加载。

## 安全

- 以 `VITE_` 开头的环境变量会打包进前端代码，不在其中存放密钥。
- 不使用 `dangerouslySetInnerHTML` 渲染未经清理的内容。

## 验证

完成前执行：

1. 类型检查和 lint 全部通过。
2. 启动开发服务器，在浏览器中检查修改过的页面：正常状态、加载中、空数据、出错，以及窄屏布局。
3. 报告实际检查过的内容和未覆盖的部分；本规范不要求编写自动化测试。
