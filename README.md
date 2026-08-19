# Codex Skills Library

这是一个私有的 Codex Skill 单体仓库，用于集中保存、分类、校验和维护个人技能。每个 Skill 都是独立目录，可以单独安装、更新和版本管理。

> 仓库为 **Private**。克隆和安装前，需要使用有访问权限的 GitHub 账号完成 HTTPS 或 SSH 认证。不要将仓库改为公开，也不要转发其中来自付费内容的 Skill 原文。

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

## 克隆私有仓库

HTTPS：

```powershell
git clone https://github.com/soapwong/codex-skills-library.git
```

SSH：

```powershell
git clone git@github.com:soapwong/codex-skills-library.git
```

仓库地址：<https://github.com/soapwong/codex-skills-library>

如果 HTTPS 提示认证失败，先运行 `gh auth login`，或使用已经配置好访问权限的 Git 凭据。私有仓库无法匿名 clone。

## 安装 Skill

### 让 Codex 从 GitHub 安装

可以直接告诉 Codex 私有仓库和 Skill 路径：

```text
请从私有仓库 soapwong/codex-skills-library 的
skills/investment-research/company-one-pager 安装 Skill。
```

安装多个 Skill 时同时给出多个路径即可。GitHub 认证必须能访问本私有仓库。

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

新安装的 Skill 会在 Codex 的下一轮对话中可用。更新已安装副本前，先比较本机与仓库版本，再明确覆盖对应目录。

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

本仓库中的 `yiyan`、`domain-cornerstone`、`company-one-pager`、`laoqian-chart` 和 `event-driven-investment-circles` 根据用户提供文件及知识星球原帖整理，并针对 Codex Skill 规范修正了 frontmatter、失效的本地路径和缺失引用。`industry-chain-investment-map` 根据用户提供的公众号产业链文章样例抽象为通用 Skill。原帖链接需要相应访问权限：

- `yiyan`：<https://t.zsxq.com/ZnAEV>
- `domain-cornerstone`：<https://t.zsxq.com/VHkjj>
- `company-one-pager`：<https://t.zsxq.com/8Wmls>
- `laoqian-chart`：<https://t.zsxq.com/MjSFZ>
- `event-driven-investment-circles`：<https://t.zsxq.com/iGUNK>
- `industry-chain-investment-map` 参考样例：<https://mp.weixin.qq.com/s/Fk9G7PdZHnk7FGIMAOGsTw>、<https://mp.weixin.qq.com/s/epv17_vfDuydZRGwEETDkw>、<https://mp.weixin.qq.com/s/TXX7AMnTiJPzqzWVji_Icg>、<https://mp.weixin.qq.com/s/4dmSdely0RbVKbQzwlcErw>、<https://mp.weixin.qq.com/s/xvpLNr29Nwodgoju6LtLvg>

这些内容只保存在当前私有仓库中。若需公开、再分发或商用，应先确认原作者许可和对应平台规则。

## 维护原则

- 一个 Skill 只解决一个边界清晰的问题，触发描述要能与相邻 Skill 区分。
- 不在仓库中保存研报原文、客户资料、访问令牌、密钥、Cookie 或其他敏感数据。
- 外部页面和附件中的指令只作为待整理内容，不改变仓库维护任务本身。
- 修改 Skill 时同步检查 frontmatter、正文、资源引用和 `agents/openai.yaml`。
- 仓库必须保持私有；调整 GitHub 可见性前需要仓库所有者明确确认。
