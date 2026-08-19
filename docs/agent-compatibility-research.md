# SKILL.md 跨 Agent 使用与兼容性研究

> 核验日期：2026-08-19  
> 适用仓库：[`soapwong/codex-skills-library`](https://github.com/soapwong/codex-skills-library)

## 结论先行

本仓库的 7 个 Skill 都以 `SKILL.md` 为核心，除 `agents/openai.yaml` 外没有脚本、二进制或平台专属依赖。因此：

- **Codex**：原生支持，兼容性最完整；`agents/openai.yaml` 会生效。
- **Claude Code**：原生支持 `SKILL.md` Skills；核心指令可复用，但 OpenAI 专属 UI 元数据不可依赖。
- **Kimi Code CLI**：官方文档确认支持 Agent Skills 与 `SKILL.md`；本次核验没有取得足够证据安全写出 Windows/macOS 本地目录，因此不猜路径。
- **Tencent WorkBuddy**：官方确认有 Skill Marketplace，但当前公开文档没有说明如何从任意 GitHub 仓库导入，也没有公开本地 Skill 目录；不能把“有 Skill 市场”等同于“可直接安装本仓库”。
- **Kimi 网页版/桌面 App**：未核验到目录式 Agent Skills 的官方说明，只建议把 `SKILL.md` 作为提示词手工使用；这不属于原生安装。

## 兼容性矩阵

| 平台 | `SKILL.md` 原生支持 | 本仓库可直接目录安装 | GitHub 导入 | 自动发现/调用 | `agents/openai.yaml` | 结论 |
|---|---|---|---|---|---|---|
| Codex | 是 | 是 | 可通过 `$skill-installer` 从其他仓库下载；也可手工复制 | 可按 `description` 隐式触发，也可 `$skill-name` 或 `/skills` 显式调用 | 官方支持 | **完整兼容** |
| Claude Code | 是 | 是 | 本次未核验到“一键从 GitHub 导入”的官方流程；可克隆后复制目录 | 官方产品支持 Skills；可用 `/skill-name` 调用 | Anthropic 文档未说明，不应依赖 | **核心格式兼容** |
| Kimi Code CLI | 是 | 原理上兼容，但本次不提供未经核验的目录命令 | 未核验 | 官方 Agent Skills 页面确认会读取并遵循 `SKILL.md` | 未文档化 | **原生支持，安装细节待复核** |
| Tencent WorkBuddy | 有官方 Skill Marketplace | 未证实 | 未证实可导入任意 GitHub 仓库 | 市场安装后可启用/禁用/更新 | 未文档化 | **封闭市场兼容性未知** |
| Kimi 网页版/桌面 App | 未证实 | 不适用/未证实 | 未证实 | 未证实 | 不适用/未文档化 | **仅建议提示词回退** |

兼容等级的含义：

- **完整兼容**：平台原生识别目录、`SKILL.md` 与本仓库附带元数据。
- **核心格式兼容**：平台原生识别 `SKILL.md`，但平台专属扩展不会跨平台生效。
- **提示词回退**：手工把 `SKILL.md` 内容交给模型；不会获得自动发现、资源加载或稳定触发能力。

## 通用格式与本仓库特点

[Agent Skills 开放规范](https://agentskills.io/specification)把 Skill 定义为一个至少包含 `SKILL.md` 的目录；`SKILL.md` 使用 YAML frontmatter 声明 `name` 和 `description`，正文存放工作流指令。`scripts/`、`references/`、`assets/` 等属于可选资源。

本仓库当前结构多了一层分类目录：

```text
skills/
  investment-research/
    industry-chain-investment-map/
      SKILL.md
      agents/openai.yaml
```

安装到其他 Agent 时，应把**单个 Skill 目录**放到目标 Agent 的 Skills 根目录下，建议不要把 `investment-research` 等分类层一并复制过去，以免依赖平台是否递归扫描。

`agents/openai.yaml` 是 OpenAI 官方扩展，用于 ChatGPT/Codex 的展示信息、调用策略和工具依赖。它不是 Agent Skills 核心规范的一部分。其他平台没有明确说明时，最稳妥的判断是：保留该文件通常不影响 `SKILL.md`，但不要期待其中配置生效，也不要把“未文档化”写成绝对保证的“必然忽略”。

## Codex

### 官方加载位置

Codex 官方文档使用跨平台的 home-relative 路径，因此 Windows 与 macOS 写法相同：

| 范围 | Windows | macOS |
|---|---|---|
| 用户级 | `$HOME/.agents/skills` | `$HOME/.agents/skills` |
| 项目级 | `<项目>/.agents/skills` | `<项目>/.agents/skills` |

在 Git 仓库中启动时，Codex 会从当前目录向仓库根目录扫描每一级 `.agents/skills`。官方还确认支持符号链接。Skill 变更通常会自动识别；未出现时重启 Codex。

注意：旧资料常见的 `$HOME/.codex/skills` 不是当前官方“Build skills”页面列出的用户级目录。本指南以当前文档的 `$HOME/.agents/skills` 为准。

### Windows：安装全部 Skill

```powershell
$repo = Join-Path $HOME "codex-skills-library"
git clone https://github.com/soapwong/codex-skills-library.git $repo

$targetRoot = Join-Path $HOME ".agents\skills"
New-Item -ItemType Directory -Force $targetRoot | Out-Null

Get-ChildItem (Join-Path $repo "skills") -Recurse -Filter SKILL.md | ForEach-Object {
    $target = Join-Path $targetRoot $_.Directory.Name
    Copy-Item $_.Directory.FullName $target -Recurse -Force
}
```

### macOS：安装全部 Skill

```bash
git clone https://github.com/soapwong/codex-skills-library.git "$HOME/codex-skills-library"
mkdir -p "$HOME/.agents/skills"

find "$HOME/codex-skills-library/skills" -name SKILL.md -print0 |
while IFS= read -r -d '' skill_file; do
  skill_dir="$(dirname "$skill_file")"
  cp -R "$skill_dir" "$HOME/.agents/skills/"
done
```

安装后可输入 `$industry-chain-investment-map` 显式调用，也可以直接问“人形机器人产业链”，由 `description` 参与隐式匹配。Codex CLI/IDE 中还可用 `/skills` 查看和选择。

来源：

- [OpenAI：Build skills](https://developers.openai.com/codex/build-skills)
- [Agent Skills specification](https://agentskills.io/specification)

## Claude Code

### 支持方式

Claude Code 原生支持以 `SKILL.md` 为入口的 Skills。官方约定的主要位置是：

| 范围 | Windows | macOS |
|---|---|---|
| 用户级 | `$HOME/.claude/skills/<skill-name>/SKILL.md` | `$HOME/.claude/skills/<skill-name>/SKILL.md` |
| 项目级 | `<项目>/.claude/skills/<skill-name>/SKILL.md` | `<项目>/.claude/skills/<skill-name>/SKILL.md` |

这里保留官方的 `$HOME`/`~` 表达，不额外猜测某个安装器的绝对目录。项目级目录可以随仓库提交；用户级目录适合在所有项目中使用。

调用时使用 `/skill-name`，例如：

```text
/industry-chain-investment-map 人形机器人产业链
```

Claude Code 可使用 Skill 的 `name`、`description` 和正文；本仓库的 `agents/openai.yaml` 不属于 Anthropic 文档定义的配置面，不能用于 Claude Code 的展示、权限或触发策略。

### Windows：安装全部 Skill

将上一节 PowerShell 示例中的目标根目录改为：

```powershell
$targetRoot = Join-Path $HOME ".claude\skills"
```

### macOS：安装全部 Skill

将上一节 shell 示例中的目标根目录改为：

```bash
mkdir -p "$HOME/.claude/skills"
# 循环中的复制目标改为 "$HOME/.claude/skills/"
```

当前没有在已核验资料中确认 Claude Code 提供“输入 GitHub URL 后自动安装任意 Skill 仓库”的标准流程。因此稳妥做法是先 `git clone`，再复制每个包含 `SKILL.md` 的目录。

来源：

- [Anthropic：Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Agent Skills specification](https://agentskills.io/specification)

## Tencent WorkBuddy

这里的 WorkBuddy 指[腾讯 WorkBuddy](https://www.workbuddy.ai/)，官方称其为面向办公场景的 AI Agent 桌面工作站，不是泛指“工作搭子”，也不是 CodeBuddy CLI。

官方文档已经确认：

- Windows 与 macOS 都有独立安装指南。
- 产品内有 Skill Marketplace，可浏览、搜索和安装官方或社区 Skill。
- 已安装 Skill 可以启用、禁用、更新和卸载。
- 安装前会做自动安全扫描。

但官方公开文档当前**没有说明**：

- Windows 或 macOS 的本地 Skill 目录；
- 如何把任意 `SKILL.md` 文件夹导入 WorkBuddy；
- 如何从任意 GitHub 仓库 URL 安装；
- 是否遵循 Agent Skills 开放规范的全部字段；
- 是否读取 `agents/openai.yaml`。

因此，本仓库不能给出经过官方验证的 WorkBuddy 复制命令。当前可靠路径只有：在 WorkBuddy 侧通过 Skill Marketplace 查找相同 Skill；若市场没有，则把目标 `SKILL.md` 正文作为任务指令手工提供。后者只是提示词回退，不具备原生 Skill 的发现、更新和管理能力。

来源：

- [WorkBuddy Overview](https://www.workbuddy.ai/docs/workbuddy/Overview)
- [WorkBuddy Skill Marketplace](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [WorkBuddy Windows Installation Guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide)
- [WorkBuddy Mac Installation Guide](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Mac-Guide)

## Kimi

### Kimi Code CLI

月之暗面的官方文档确认 Kimi Code CLI 支持 Agent Skills，并以 `SKILL.md` 提供知识和工作流指令。这足以确认本仓库的核心文件格式可复用。

本次核验没有取得足够证据确认当前版本在 Windows 和 macOS 上的具体用户级、项目级目录，也没有确认从 GitHub URL 一键导入的官方流程。为避免把 issue、旧版本行为或第三方教程写成官方事实，本指南不提供未经核验的复制命令。安装前应以 Kimi Code CLI 的 Agent Skills 页面列出的当前加载路径为准，再把每个 Skill 目录单独放入相应位置。

同样，Kimi 官方资料没有说明会处理 `agents/openai.yaml`；应把它视为无可依赖功能的 OpenAI 专属附加文件。

来源：

- [Kimi Code CLI：Agent Skills](https://moonshotai.github.io/kimi-cli/en/customization/skills.html)
- [MoonshotAI/kimi-cli 官方仓库](https://github.com/MoonshotAI/kimi-cli)

### Kimi 网页版与桌面 App

本次已核验资料没有证明 Kimi 网页版或桌面 App 支持从本地目录/GitHub 仓库安装 `SKILL.md` Agent Skills，也没有可引用的 Windows/macOS Skill 路径。

可行但降级的使用方式是：打开某个 Skill 的 `SKILL.md`，把正文与具体任务一并交给 Kimi。此方式有三项限制：

1. 不会按 `description` 自动发现和触发；
2. 不会自动加载同目录资源；
3. 不会随 GitHub 仓库更新。

## 更新与卸载

通过复制方式安装时，`git pull` 只会更新克隆仓库，不会自动更新 Agent 的 Skills 目录。需要重新执行复制循环覆盖目标目录。删除或停用 Skill 时，优先使用平台提供的管理界面；若平台只按目录加载，则删除对应的单个 Skill 目录即可。

不要把整个 `skills/` 分类树直接软链接成一个 Skill。若使用符号链接，应让每个链接直接指向包含 `SKILL.md` 的目录。

## 已知边界

- 本文只把官方产品文档、官方源码仓库和 Agent Skills 规范作为结论依据。
- “未文档化”不等于“产品内部绝对不会读取”，只表示不能把该行为写成稳定承诺。
- WorkBuddy 与 Kimi 的产品更新较快；涉及本地目录和 GitHub 导入时，应先复核对应官方页面。
- 本轮按收口要求未扩展到 OpenCode、GitHub Copilot、Cursor、Gemini CLI、Cline 或 Roo Code，以免在未完成一手资料核验时给出过度结论。
