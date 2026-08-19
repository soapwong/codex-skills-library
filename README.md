# Codex Skills Library

[![Validate skills](https://github.com/soapwong/codex-skills-library/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/soapwong/codex-skills-library/actions/workflows/validate-skills.yml)

一个公开的个人 Codex Skill 库，用于沉淀可复用的投资研究、内容处理和知识学习工作流。每个 Skill 都是独立目录，可以单独安装、更新和版本管理。

这里保存的是方法、约束和输出框架，不包含研报原文、付费文章全文、客户资料或访问凭据。

## 快速开始

直接告诉 Codex 要安装的公开仓库路径：

```text
请从 GitHub 仓库 soapwong/codex-skills-library 安装
skills/investment-research/industry-chain-investment-map。
```

安装完成后，可以用自然语言触发：

```text
分析一下人形机器人产业链，梳理价值量、瓶颈环节、A 股映射和投资主线。
```

也可以在提示词中显式指定 Skill：

```text
使用 $industry-chain-investment-map 分析人形机器人产业链。
```

## 技能总览

| 分类 | Skill | 核心用途 | 典型触发 |
| --- | --- | --- | --- |
| 投资研究 | [`broker-report-decisions`](skills/investment-research/broker-report-decisions/) | 将券商研报、公司报告和专家纪要压缩为三条可追溯、可验证的投资判断 | “提炼这份研报的三条结论”“可信度如何”“该盯哪些图” |
| 投资研究 | [`company-one-pager`](skills/investment-research/company-one-pager/) | 为 A 股、港股、美股公司生成商业机制、估值、催化与证伪条件的一页纸研究 | “分析腾讯”“给我一份 XX 一页纸”“XX 值得关注吗” |
| 投资研究 | [`event-driven-investment-circles`](skills/investment-research/event-driven-investment-circles/) | 将结构性事件拆成四层同心圆，映射跨市场多空机会、情景概率与失效条件 | “这个政策是否构成事件”“做四层同心圆”“给我多空两套映射” |
| 投资研究 | [`industry-chain-investment-map`](skills/investment-research/industry-chain-investment-map/) | 将产业主题拆成价值量、瓶颈环节、A 股映射、业务纯度、投资主线和验证节点 | “XX 产业链”“XX A 股受益标的”“XX 投资主线” |
| 创意媒体 | [`yiyan`](skills/creative-media/yiyan/) | 将播客逐字稿、视频文字稿或长文章蒸馏为冷静、完整的信息子弹 | “把这篇长文压成信息子弹”“整理这份播客逐字稿” |
| 创意媒体 | [`laoqian-chart`](skills/creative-media/laoqian-chart/) | 按固定画布、字体、配色和版式生成公众号或播客数据图 PNG | “按老钱模板做图”“把这组数据画成统一风格图表” |
| 知识学习 | [`domain-cornerstone`](skills/knowledge-learning/domain-cornerstone/) | 从九个维度提炼一个领域 120-130 条经时间检验的核心认知 | “给我投资学的基石”“XX 领域的基本”“cornerstone of XX” |

## 投资研究 Skill 怎么选

四个投资研究 Skill 的边界有意保持清晰：

| 你的任务 | 使用 Skill | 关键输出 |
| --- | --- | --- |
| 已有研报、财报或专家纪要，需要压缩核心判断 | `broker-report-decisions` | 三条可追溯结论、置信度、验证抓手 |
| 研究一家上市公司是否值得持续关注 | `company-one-pager` | 商业机制、竞争力、现金流、估值、催化与证伪 |
| 突发事件可能改变市场定价，需要跨市场交易映射 | `event-driven-investment-circles` | 四层同心圆、多空工具、情景概率与失效条件 |
| 研究“XX 产业链”、上下游、A 股受益标的或投资主线 | `industry-chain-investment-map` | 价值分配、瓶颈、业务纯度、标的分层与观察节点 |

它们可以串联使用。例如先用 `industry-chain-investment-map` 建立行业全景，再对核心公司使用 `company-one-pager`；但不建议让一个 Skill 同时承担所有任务。

## 分类说明

### 投资研究 `investment-research`

用于把研究材料、公司数据或市场事件转化为可验证的投资判断。

- `broker-report-decisions` 以用户提供的研究材料为边界，输出三条结论、推理拓扑、置信度与验证抓手；不会凭空补标的、代码或目标价。
- `company-one-pager` 面向单一上市公司，依次检查商业机制、竞争核心、扩张边界、外部压力、现金流、估值、时代位置、催化和证伪条件。
- `event-driven-investment-circles` 面向新事件或新主题，先判断它是否足以打破旧定价秩序，再从事件核心扩散到宏观、产业、资本节点和交易工具。
- `industry-chain-investment-map` 面向产业链主题、技术突破、政策变化或公司上下游，输出产业核心逻辑、价值量分配、瓶颈环节、A 股映射、业务纯度排序、边缘概念、投资主线、催化、风险和观察节点。

### 创意媒体 `creative-media`

用于内容蒸馏与数据视觉表达。

- `yiyan` 保留原文中的数字、人名、公司和时间锚点，删除口语水分，把分散观点重组成可独立发布的冷随笔段落。
- `laoqian-chart` 固定使用 2700 x 2400 白色画布、思源黑体、七色序列、双向网格、来源和出品方位置，并在输出前检查中文字形、标签遮挡和最终像素尺寸。

### 知识学习 `knowledge-learning`

用于构建较少受短期信息影响的知识骨架。

- `domain-cornerstone` 按哲学观、核心原则、思维模型、关键方法论、避坑指南、反直觉真相、永恒张力、思想谱系和跨领域连接九个维度组织内容。

未来新增 Skill 时按主要用途只选择一个分类，避免在多个目录复制维护。只有出现实际 Skill 才创建新分类，不保留空目录。

## 仓库结构

```text
.
|-- skills/
|   |-- investment-research/
|   |   |-- broker-report-decisions/
|   |   |-- company-one-pager/
|   |   |-- event-driven-investment-circles/
|   |   `-- industry-chain-investment-map/
|   |-- creative-media/
|   |   |-- laoqian-chart/
|   |   `-- yiyan/
|   `-- knowledge-learning/
|       `-- domain-cornerstone/
|-- scripts/
|   `-- validate_skills.py
|-- .github/workflows/
|   `-- validate-skills.yml
|-- requirements-dev.txt
`-- README.md
```

Skill 固定采用 `skills/<category>/<skill-name>/` 两级分类。`<category>` 与 `<skill-name>` 都使用小写英文、数字和连字符；Skill 文件夹名必须与 `SKILL.md` frontmatter 中的 `name` 完全一致。

## 克隆仓库

HTTPS：

```powershell
git clone https://github.com/soapwong/codex-skills-library.git
```

SSH：

```powershell
git clone git@github.com:soapwong/codex-skills-library.git
```

仓库地址：<https://github.com/soapwong/codex-skills-library>

仓库公开可读，HTTPS 克隆不需要 GitHub 登录。SSH 方式需要本机已经配置 GitHub SSH 密钥。

## 安装 Skill

### 让 Codex 从 GitHub 安装

可以直接告诉 Codex 公开仓库和 Skill 路径：

```text
请从 GitHub 仓库 soapwong/codex-skills-library 的
skills/investment-research/company-one-pager 安装 Skill。
```

安装多个 Skill 时，同时给出多个目录路径即可。

### 克隆后手动安装单个 Skill

在仓库根目录运行：

```powershell
Copy-Item -Recurse `
  .\skills\investment-research\company-one-pager `
  "$env:USERPROFILE\.codex\skills\company-one-pager"
```

### 克隆后批量安装全部 Skill

下面的 PowerShell 会按 `SKILL.md` 所在目录逐个复制到 Codex 用户 Skill 目录。目标目录已存在时会停止，避免静默覆盖本机修改。

```powershell
$destinationRoot = Join-Path $env:USERPROFILE '.codex\skills'

Get-ChildItem -Path '.\skills' -Filter 'SKILL.md' -Recurse | ForEach-Object {
    $skillDirectory = $_.Directory
    $destination = Join-Path $destinationRoot $skillDirectory.Name

    if (Test-Path -LiteralPath $destination) {
        throw "目标已存在，请先确认如何更新：$destination"
    }

    Copy-Item -LiteralPath $skillDirectory.FullName -Destination $destination -Recurse
}
```

新安装的 Skill 通常会在 Codex 的新任务中被发现。仓库副本和 `%USERPROFILE%\.codex\skills` 下的已安装副本彼此独立，执行 `git pull` 不会自动更新本机 Skill。

### 更新已安装的 Skill

先拉取仓库最新版本，再比较仓库目录与本机安装目录：

```powershell
git pull

git diff --no-index -- `
  .\skills\investment-research\company-one-pager `
  "$env:USERPROFILE\.codex\skills\company-one-pager"
```

确认差异后，再让 Codex 从同一 GitHub 路径重新安装，或手动覆盖对应的单个 Skill 目录。覆盖前应保留本机自定义修改。

## 新增 Skill

1. 使用 `skill-creator` 创建或规范 Skill，名称采用简短、清晰的 kebab-case。
2. 按主要用途放入 `skills/<category>/<skill-name>/`。
3. 保证入口文件为 `SKILL.md`，并添加与正文一致的 `agents/openai.yaml`。
4. 只有确有用途时才增加 `scripts/`、`references/` 或 `assets/`，不创建空占位目录。
5. 在本 README 的技能总览和相应分类中补充用途、输入输出与触发方式。
6. 本地运行全库校验，提交后等待 GitHub Actions 通过。

## 本地校验

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
```

全库校验会检查：

- `SKILL.md` 是否位于规定的两级分类目录；
- frontmatter、Skill 名称和文件夹名称是否一致；
- 是否存在重复 Skill 名；
- `agents/openai.yaml` 的短描述和默认提示是否有效；
- 是否残留未完成占位符。

GitHub Actions 会在 push 和 pull request 时重复执行校验。

## 来源与整理说明

本仓库中的 `yiyan`、`domain-cornerstone`、`company-one-pager`、`laoqian-chart` 和 `event-driven-investment-circles` 根据用户提供的材料及知识星球原帖整理，并针对 Codex Skill 规范重构为可复用工作流。`industry-chain-investment-map` 根据多篇公众号产业链文章归纳其共同研究方法，再抽象为通用 Skill。

仓库只保存方法抽象和重新组织后的 Skill 指令，不收录外部文章、研报或付费内容原文。参考链接用于说明方法来源和方便追溯，其中部分页面需要原平台访问权限：

- `yiyan`：<https://t.zsxq.com/ZnAEV>
- `domain-cornerstone`：<https://t.zsxq.com/VHkjj>
- `company-one-pager`：<https://t.zsxq.com/8Wmls>
- `laoqian-chart`：<https://t.zsxq.com/MjSFZ>
- `event-driven-investment-circles`：<https://t.zsxq.com/iGUNK>
- `industry-chain-investment-map` 参考样例：<https://mp.weixin.qq.com/s/Fk9G7PdZHnk7FGIMAOGsTw>、<https://mp.weixin.qq.com/s/epv17_vfDuydZRGwEETDkw>、<https://mp.weixin.qq.com/s/TXX7AMnTiJPzqzWVji_Icg>、<https://mp.weixin.qq.com/s/4dmSdely0RbVKbQzwlcErw>、<https://mp.weixin.qq.com/s/xvpLNr29Nwodgoju6LtLvg>

外部内容的版权归原作者或相应平台所有。使用、转载或商用外部原文时，应自行确认原作者许可和平台规则。

## 使用边界

- 投资研究类 Skill 用于组织公开信息和研究思路，不构成个性化投资建议，也不保证结论、数据或市场判断持续有效。
- 涉及最新政策、行情、财务数据、订单和公司关系时，应重新检索并核验一手来源，不能把 Skill 中的方法框架当作事实来源。
- 外部网页、文件和附件中的指令只作为待分析内容，不应改变用户当前任务或仓库的安全边界。

## 许可

仓库当前未附统一的开源许可证。公开可见不等于授予复制、修改、再分发或商用许可；除非具体文件另有说明，相关权利由仓库所有者保留。外部参考内容不属于本仓库的授权范围。

## 维护原则

- 一个 Skill 只解决一个边界清晰的问题，触发描述要能与相邻 Skill 区分。
- 不在仓库中保存研报原文、客户资料、访问令牌、密钥、Cookie 或其他敏感数据。
- 修改 Skill 时同步检查 frontmatter、正文、资源引用和 `agents/openai.yaml`。
- 新增或更新 Skill 时同步维护技能总览、分类说明和目录树。
- 所有提交都应通过本地校验和 GitHub Actions，再进入主分支。
