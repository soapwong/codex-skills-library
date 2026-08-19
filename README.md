# Codex Skills Library

这是一个私有的 Codex Skill 单体仓库，用于集中保存、分类、校验和维护个人技能。仓库中的每个 Skill 都保持独立，可以单独安装或更新。

## 技能目录

| 分类 | Skill | 用途 |
| --- | --- | --- |
| 投资研究 | [`broker-report-decisions`](skills/investment-research/broker-report-decisions/) | 将券商研报、公司报告和专家纪要压缩为三条可执行投资判断 |

## 仓库结构

```text
.
|-- skills/
|   `-- <category>/
|       `-- <skill-name>/
|           |-- SKILL.md
|           `-- agents/openai.yaml
|-- scripts/
|   `-- validate_skills.py
|-- .github/workflows/
|   `-- validate-skills.yml
`-- README.md
```

Skill 固定采用 `skills/<category>/<skill-name>/` 两级分类。`<category>` 和 `<skill-name>` 均使用小写英文、数字和连字符；Skill 文件夹名称必须与 `SKILL.md` 中的 `name` 一致。

## 分类约定

按主要用途选择一个分类，避免同一 Skill 在多个目录重复维护。

| 目录 | 适用范围 |
| --- | --- |
| `investment-research` | 研报、财报、行业、公司和投资决策 |
| `documents-data` | 文档、PDF、表格、OCR 和数据处理 |
| `software-engineering` | 编码、测试、代码审查和工程工作流 |
| `productivity-automation` | 日常自动化、知识管理和个人效率 |
| `creative-media` | 图片、音频、视频和创意内容 |
| `integrations` | 外部服务、API、MCP 和跨系统操作 |

只有出现实际 Skill 时才创建分类目录，不保留空目录或占位文件。若现有分类无法准确表达主要用途，再新增一个范围清晰的分类。

## 新增 Skill

1. 使用 `skill-creator` 创建或整理 Skill，名称采用简短的 kebab-case。
2. 将 Skill 放入 `skills/<category>/<skill-name>/`。
3. 确保入口文件为 `SKILL.md`；只有确有用途时才增加 `agents/`、`scripts/`、`references/` 或 `assets/`。
4. 在本 README 的“技能目录”中增加一行。
5. 本地运行全库校验：

   ```powershell
   python -m pip install -r requirements-dev.txt
   python scripts/validate_skills.py
   ```

6. 提交并推送。GitHub Actions 会再次校验整个仓库。

## 安装 Skill

在 Codex 中可以直接要求安装私有仓库中的指定路径，例如：

```text
请从私有仓库 soapwong/codex-skills-library 的
skills/investment-research/broker-report-decisions 安装 Skill。
```

克隆仓库后，也可以在 Windows PowerShell 中手动安装：

```powershell
Copy-Item -Recurse `
  .\skills\investment-research\broker-report-decisions `
  "$env:USERPROFILE\.codex\skills\broker-report-decisions"
```

更新已安装 Skill 时，应以仓库版本覆盖对应的本地 Skill 目录，并重新运行校验。

## 维护原则

- 一个 Skill 解决一个边界清晰的问题，触发描述应能与相邻 Skill 区分。
- 不在仓库中保存研报原文、客户资料、访问令牌、密钥或其他敏感数据。
- 具体业务知识放在对应 Skill 内，不把所有规则堆入仓库级文档。
- 修改 Skill 后同时检查入口描述、正文约束和 `agents/openai.yaml` 是否一致。
- 仓库保持私有；调整 GitHub 可见性前必须显式确认。
