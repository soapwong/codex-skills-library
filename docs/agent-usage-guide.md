# 跨 Agent 与跨平台使用指南

> 核验日期：2026-08-19
> 适用仓库：[`soapwong/codex-skills-library`](https://github.com/soapwong/codex-skills-library)

本仓库采用开放的 [Agent Skills 规范](https://agentskills.io/specification)：每个 Skill 都是一个以 `SKILL.md` 为入口的独立目录。当前 7 个 Skill 的核心指令没有绑定 Codex、Windows 或某个模型；`agents/openai.yaml` 只是 OpenAI 产品使用的可选界面元数据。

## 先看结论

| Agent / 产品 | 支持级别 | 推荐的用户级目录 | 显式调用 | 备注 |
| --- | --- | --- | --- | --- |
| Codex | 原生完整支持 | `~/.agents/skills` | `$skill-name`，或 `/skills` | `agents/openai.yaml` 会生效 |
| ChatGPT Desktop / Work | 原生支持 | 使用产品内 Skills 或插件 | `@skill-name` | 本仓库尚未封装为插件 |
| Claude Code | 原生支持 | `~/.claude/skills` | `/skill-name` | 使用 `SKILL.md`；不依赖 OpenAI 元数据 |
| Kimi Code CLI | 原生支持 | `~/.config/agents/skills`；也支持 `~/.agents/skills` | `/skill:name` | 可按 `description` 自动匹配 |
| Cursor | 原生支持 | `~/.agents/skills` 或 `~/.cursor/skills` | `/skill-name` | 会自动发现和按需使用 |
| OpenCode | 原生支持 | `~/.agents/skills` 或 `~/.config/opencode/skills` | 由 Agent 的 `skill` 工具加载 | 也读取 Claude 兼容目录 |
| Gemini CLI | 原生支持 | `~/.agents/skills` 或 `~/.gemini/skills` | `/skills` 管理 | `.agents` 目录优先 |
| GitHub Copilot | 原生支持 | `~/.agents/skills` 或 `~/.copilot/skills` | 自动按任务匹配 | CLI 还提供 `copilot skill` 管理命令 |
| Tencent WorkBuddy | 有原生 Skill 系统，但导入格式不同 | 使用 Skill Marketplace 或让 WorkBuddy 自行转换 | 安装后自然语言触发 | 任意 `SKILL.md` 目录导入未形成官方稳定接口 |
| Kimi 网页版 / 普通聊天产品 | 未确认本地目录式支持 | 不适用 | 提示词回退 | 上传或粘贴 `SKILL.md`，仅对当前对话生效 |

这里的 `~` 或 `$HOME` 都表示当前用户主目录：

- Windows PowerShell：通常是 `C:\Users\你的用户名`；
- macOS：通常是 `/Users/你的用户名`。

## 最省事的安装策略

Codex、Cursor、OpenCode、Gemini CLI 和 GitHub Copilot 都能读取 `~/.agents/skills`。如果你同时使用这些 Agent，只需把本仓库安装到这个公共目录一次。

Claude Code 使用自己的 `~/.claude/skills`。Kimi Code CLI 虽然也能读取 `~/.agents/skills`，但如果 `~/.config/agents/skills` 已经存在，Kimi 会优先选择后者；出现“其他 Agent 能看到、Kimi 看不到”时，先检查这个优先级。

WorkBuddy 不建议直接套用上述目录，见后面的专门说明。

## 获取仓库

### Windows

在 PowerShell 中运行：

```powershell
git clone https://github.com/soapwong/codex-skills-library.git `
  "$HOME\codex-skills-library"
```

### macOS

在 Terminal 中运行：

```bash
git clone https://github.com/soapwong/codex-skills-library.git \
  "$HOME/codex-skills-library"
```

如果已经克隆过，进入该目录运行 `git pull --ff-only` 即可取得仓库最新版本。

## 安装到公共目录

### Windows：安装单个 Skill

```powershell
$repo = Join-Path $HOME 'codex-skills-library'
$skillName = 'industry-chain-investment-map'
$source = Join-Path $repo "skills\investment-research\$skillName"
$targetRoot = Join-Path $HOME '.agents\skills'
$target = Join-Path $targetRoot $skillName

New-Item -ItemType Directory -Force $targetRoot | Out-Null
if (Test-Path -LiteralPath $target) {
    throw "目标已存在，请先比较或备份：$target"
}
Copy-Item -LiteralPath $source -Destination $target -Recurse
```

### macOS：安装单个 Skill

```bash
repo="$HOME/codex-skills-library"
skill_name="industry-chain-investment-map"
source_dir="$repo/skills/investment-research/$skill_name"
target_root="$HOME/.agents/skills"
target="$target_root/$skill_name"

mkdir -p "$target_root"
if [ -e "$target" ]; then
  echo "目标已存在，请先比较或备份：$target" >&2
  exit 1
fi
cp -R "$source_dir" "$target"
```

### Windows：安装全部 Skill

```powershell
$repo = Join-Path $HOME 'codex-skills-library'
$targetRoot = Join-Path $HOME '.agents\skills'
New-Item -ItemType Directory -Force $targetRoot | Out-Null

Get-ChildItem -Path (Join-Path $repo 'skills') -Filter 'SKILL.md' -Recurse |
ForEach-Object {
    $source = $_.Directory
    $target = Join-Path $targetRoot $source.Name

    if (Test-Path -LiteralPath $target) {
        throw "目标已存在，请先比较或备份：$target"
    }
    Copy-Item -LiteralPath $source.FullName -Destination $target -Recurse
}
```

### macOS：安装全部 Skill

```bash
repo="$HOME/codex-skills-library"
target_root="$HOME/.agents/skills"
mkdir -p "$target_root"

for skill_file in "$repo"/skills/*/*/SKILL.md; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  target="$target_root/$skill_name"

  if [ -e "$target" ]; then
    echo "目标已存在，请先比较或备份：$target" >&2
    exit 1
  fi
  cp -R "$skill_dir" "$target"
done
```

仓库中的分类目录只用于维护。安装时必须让目标目录直接包含 `SKILL.md`，不要把 `investment-research`、`creative-media` 等分类层当作一个 Skill。

## 各 Agent 的差异

### ChatGPT Desktop / Work

OpenAI 官方文档确认 ChatGPT Desktop 可使用独立 Skill，ChatGPT Chat/Work 还可使用插件中打包的 Skill。在 ChatGPT 中用 `@` 选择 Skill。公开分发到 ChatGPT 网页、桌面和移动端时，官方推荐把 Skill 封装为插件；本仓库目前还是目录式 Skill 集合，因此不要把 Codex 的 `~/.agents/skills` 复制命令当成 ChatGPT 网页安装方法。

### Codex

用户级目录使用 `~/.agents/skills`，项目级目录使用 `<项目>/.agents/skills`。安装后可以直接输入：

```text
$industry-chain-investment-map 分析人形机器人产业链
```

也可以只说“分析人形机器人产业链”，让 Codex 根据 `description` 自动匹配。Codex 通常会自动发现变更；没有出现时重启 Codex。

旧资料中的 `~/.codex/skills` 不是当前 OpenAI 官方 Build skills 页面列出的用户级目录，本指南统一使用 `~/.agents/skills`。

### Claude Code

把上述安装命令中的目标根目录改为：

- Windows：`$HOME\.claude\skills`
- macOS：`$HOME/.claude/skills`

调用示例：

```text
/industry-chain-investment-map 人形机器人产业链
```

Claude Code 也会根据 `description` 自动选择相关 Skill。新建顶层 `skills` 目录后若当前会话没有发现，重启 Claude Code。

### Kimi Code CLI

推荐目标目录：

- Windows：`$HOME\.config\agents\skills`
- macOS：`$HOME/.config/agents/skills`

也可以使用公共目录 `~/.agents/skills`，或 Kimi 专属目录 `~/.kimi/skills`。调用示例：

```text
/skill:industry-chain-investment-map 人形机器人产业链
```

普通对话中，Kimi Code CLI 也会依据上下文自动读取 Skill。可用 `/skills list` 查看发现结果；需要临时指定其他集合时，可以启动：

```bash
kimi --skills-dir /path/to/skills
```

`--skills-dir` 会替代自动发现目录；需要在默认目录之外追加集合时，应使用 Kimi 配置中的 `extra_skill_dirs`。

### Cursor、OpenCode、Gemini CLI 与 GitHub Copilot

这四类工具都可直接复用公共的 `~/.agents/skills`：

- Cursor：在 Agent 聊天中输入 `/` 并搜索 Skill 名称，或让 Agent 自动匹配。
- OpenCode：Agent 会看到 Skill 元数据，需要时通过原生 `skill` 工具加载。
- Gemini CLI：使用 `/skills list`、`/skills enable`、`/skills disable` 和 `/skills reload` 管理。
- GitHub Copilot：个人级使用 `~/.agents/skills`，项目级可使用 `.agents/skills`、`.github/skills` 或 `.claude/skills`；由 Copilot 在相关任务中自动加载。

`agents/openai.yaml` 不属于 Agent Skills 核心规范；这些 Agent 的官方文档没有承诺使用其中的 OpenAI 界面配置，因此不要依赖它。`SKILL.md` 的 `name`、`description` 和正文仍可工作。

### Tencent WorkBuddy

官方支持 Skill Marketplace，也支持让 WorkBuddy 创建自定义 Skill；官方“创建自己的 Skill”示例使用 WorkBuddy 自己的 `skill.yml + implementation` 结构。因此，推荐做法是：

1. 在 WorkBuddy 新建任务；
2. 附上目标 Skill 的 `SKILL.md`，或让 WorkBuddy 读取克隆仓库中的文件；
3. 使用下面的转换指令；
4. 安装生成的 WorkBuddy Skill，再开新对话测试。

```text
请读取这个 SKILL.md，把它转换为当前版本 WorkBuddy 支持的自定义 Skill。
保留 name、description、触发边界、执行步骤和质量检查；
忽略 agents/openai.yaml，不要改变原方法的事实纪律和风险边界。
生成后安装，并告诉我最终 Skill 名称和测试方式。
```

Windows 与 macOS 都可使用这个官方自生成流程，不依赖手工查找隐藏目录。

补充说明：本次在 WorkBuddy 5.3.12 的 Windows 客户端实测到 `$HOME\.workbuddy\skills`，其中确有 `SKILL.md` 类型的已安装 Skill；但官方公开文档没有把该目录声明为稳定导入接口。不要据此推断 macOS 一定相同，也不要把直接复制作为首选安装方式。

### Kimi 网页版和其他普通聊天产品

网页聊天通常不能读取本机的 Skills 目录。若产品没有可见的 Skill 导入或管理入口，可以把 `SKILL.md` 作为附件上传，使用提示词回退：

```text
请把附件 SKILL.md 作为本轮任务的工作流规范。
先判断我的任务是否命中 frontmatter 中的 description；
命中后按正文完整执行，忽略 agents/openai.yaml。
任务：分析人形机器人产业链。
```

这种方式不会自动发现 Skill、不会自动加载同目录资源，也不会随 GitHub 更新，只适合临时使用。

## 更新与卸载

`git pull` 只会更新克隆仓库，不会自动更新复制到各 Agent 目录的副本。更新前先比较仓库版本和已安装版本，保留本地修改，再覆盖对应的单个 Skill。

删除或停用时，优先使用 Agent 自带的 Skills 管理界面或命令；纯目录加载的 Agent 可以删除对应 Skill 目录。不要删除整个 Skills 根目录。

## 官方来源

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI：Build skills](https://developers.openai.com/codex/skills)
- [Anthropic：Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Kimi Code CLI：Agent Skills](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/zh/customization/skills.md)
- [Tencent WorkBuddy：Skill Marketplace](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [Tencent WorkBuddy：Creating Custom Skills](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)
- [Cursor：Agent Skills](https://cursor.com/docs/skills)
- [OpenCode：Agent Skills](https://opencode.ai/docs/skills/)
- [Gemini CLI：Agent Skills](https://geminicli.com/docs/cli/skills/)
- [GitHub Copilot：About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## 已知边界

- “原生支持”只代表 Agent 能发现并读取 `SKILL.md`，不代表它拥有完成任务所需的浏览器、文件、代码执行或数据工具。
- `agents/openai.yaml` 不属于 Agent Skills 核心规范，除 OpenAI 产品外不要依赖它。
- 各 Agent 更新较快。目录、命令或导入方式变化时，以本页列出的第一方文档为准。
