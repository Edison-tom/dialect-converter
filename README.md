# Dialect Converter — 中国方言对白转换器 v2.2

将普通话对白文字转换为 **19 种**中国常见方言的重口音表述，每种方言包含 **60-115 条分类词条**、完整语音学标注（声调系统、声韵母要点、连读变调规则）、语法特点分析和用法示例。

**总词条数：1233 条** | **方言谱系覆盖：9 大方言区**

## 快速预览

```
普通话：你在干什么？这个东西很好吃。你不知道吗？别骗我了。

东北话：你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。
湖南话：你在搞么子咯？这个蛮好呷。你不晓得啵？莫哄我咯。
湖北话：你在搞么斯咧？这个东西蛮好七。你不晓得？莫哄我。
四川话：你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
```

---

## 支持的 AI Agent

| Agent | 说明 |
|-------|------|
| **WorkBuddy** | 原生 Skill 格式，开箱即用 |
| **Claude Code / Desktop** | 通过 CLAUDE.md 或 Project Knowledge 注入词典 |
| **Cursor** | 通过 .cursorrules 或 @ 引用词典文件 |
| **GitHub Copilot** | 通过 Custom Instructions 注入策略 |
| **ChatGPT** | Custom GPTs 上传为 Knowledge；Web 版直接附加文件 |
| **DeepSeek / Kimi / 通义千问** | 长上下文优势，直接上传词典文件即可 |

> 核心原理：所有 Agent 都支持在上下文中注入外部文件。把 `references/dialect_dictionary.md` 作为参考文件附给对话，AI 自动按词条转换。

## 安装

### macOS

```bash
# 克隆仓库
git clone https://github.com/Edison-tom/dialect-converter.git

# WorkBuddy 用户 — 直接安装为 Skill
cp -r dialect-converter ~/.workbuddy/skills/

# Claude Code 用户 — 放入项目引用
cp dialect-converter/references/dialect_dictionary.md 你的项目目录/

# Cursor 用户 — 放入 .cursor 目录
mkdir -p 你的项目目录/.cursor/references
cp dialect-converter/references/dialect_dictionary.md 你的项目目录/.cursor/references/
```

### Windows

```powershell
# 克隆仓库
git clone https://github.com/Edison-tom/dialect-converter.git

# WorkBuddy 用户 — 直接安装为 Skill
xcopy /E /I dialect-converter %USERPROFILE%\.workbuddy\skills\dialect-converter

# Claude Code 用户 — 放入项目引用
copy dialect-converter\references\dialect_dictionary.md 你的项目目录\

# Cursor 用户 — 放入 .cursor 目录
mkdir 你的项目目录\.cursor\references
copy dialect-converter\references\dialect_dictionary.md 你的项目目录\.cursor\references\
```

## 文件结构

```
dialect-converter/
├── README.md                       # 本文件
├── SKILL.md                        # 技能定义（含三级转换策略、质量检查清单）
└── references/
    └── dialect_dictionary.md       # 19种方言完整词典（1233词条 + 声调对照 + 谱系树）
```

## 转换层级

| 层级 | 名称 | 内容 | 适用场景 |
|------|------|------|---------|
| Layer 1 | 基础层 | 仅核心词汇替换 | AI 辅助理解、轻度本地化 |
| Layer 2 | **增强层**（默认） | 词汇 + 语气词 + 句式调整 | 方言对白创作、台词改写 |
| Layer 3 | 地道层 | 全方言沉浸（含俚语粗口） | 段子、喜剧脚本、模仿秀 |

## 语言学标注

每种方言附带：
- 声调系统（调类 + 调值）
- 入声保留/演变情况
- 标志性词汇表
- 分类语法特点（人称/疑问/否定/程度/动词/形容词/俚语/语气词）
- 语气词系统
- 示例转换对照

附录含：
- 附录A：方言谱系树（汉藏语系→大方言区→片）
- 附录B：19种方言声调对照表
- 附录C：类型学特征矩阵（入声/浊声母/翘舌音/-m韵尾/修饰后置/连读变调/儿化音）

## 支持的方言

| # | 方言 | 词条 | 谱系 |
|---|------|------|------|
| 1 | 四川话 | 96 | 西南官话·成渝片 |
| 2 | 粤语 | 111 | 粤语·广府片 |
| 3 | 东北话 | 91 | 东北官话 |
| 4 | 上海话 | 89 | 吴语·太湖片 |
| 5 | 河南话 | 39 | 中原官话·郑开片 |
| 6 | 陕西话 | 38 | 中原官话·关中片 |
| 7 | 湖南话 | 49 | 湘语·长益片 |
| 8 | 山东话 | 39 | 冀鲁/胶辽官话 |
| 9 | 天津话 | 33 | 冀鲁官话·天津片 |
| 10 | 闽南语 | 73 | 闽语·闽南片 |
| 11 | 客家话 | 55 | 客语·粤台片 |
| 12 | 赣语 | 33 | 赣语·昌靖片 |
| 13 | 晋语 | 45 | 晋语·并州片 |
| 14 | 云南话 | 51 | 西南官话·滇中片 |
| 15 | 湖北话 | 115 | 西南官话·武天片 |
| 16 | 贵阳话 | 70 | 西南官话·黔中片 |
| 17 | 徐州话 | 58 | 中原官话·徐淮片 |
| 18 | 自贡话 | 73 | 西南官话·仁富片 |
| 19 | 苏州话 | 47 | 吴语·太湖片 |

## 技术说明

本词典基于大规模语言模型统计知识整理，**非学术成果**，用字和注音可能存在偏差，仅供辅助参考。

---

> 📦 仓库地址：https://github.com/Edison-tom/dialect-converter
