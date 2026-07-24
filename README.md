# Dialect Converter — 中国方言对白转换器 v2.2

将普通话对白文字转换为 **19 种**中国常见方言的重口音表述，每种方言包含 **60-115 条分类词条**、完整语音学标注（声调系统、声韵母要点、连读变调规则）、语法特点分析和用法示例。

**总词条数：1233 条** | **方言谱系覆盖：9 大方言区**

## 快速预览

```
普通话：你在干什么？这个东西很好吃。你不知道吗？别骗我了。

四川话：你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
东北话：你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。
粤语：你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。
```

---

## 在各 AI Agent / 平台中使用

本项目是一个参考词典 + 技能定义文件，可按以下方式接入各类 AI 工具。

---

### 1. WorkBuddy（原生支持 ⭐）

**支持度：★★★★★ 开箱即用**

WorkBuddy 原生支持 Skill 格式，导入后可通过自然语言触发方言转换。

**安装**：
```bash
cp -r dialect-converter ~/.workbuddy/skills/
```

**触发方式**（WorkBuddy 对话中直接说）：
```
把这段话改成四川话：你好，今天天气真不错，我们出去走走吧。
用东北话重写：别磨蹭了，赶紧把这事儿办完。
这封邮件用粤语写，要地道一点。
```

**支持的方言**：全部 19 种，三级转换深度可用 `基础`/`增强`/`地道` 关键词控制。

---

### 2. Claude Code / Claude Desktop

**支持度：★★★★☆ 通过上下文注入**

Claude Code 和 Claude Desktop 不原生支持 Skill 格式，但可以通过项目上下文注入词典。

**方法 A：作为项目上下文**
```bash
# 将词典放入项目目录，在 CLAUDE.md 中引用
mkdir -p .claude/references
cp references/dialect_dictionary.md .claude/references/

# 在 CLAUDE.md 中添加：
# 方言转换时请参考 .claude/references/dialect_dictionary.md
```

**方法 B：对话中直接附加上下文**
```
@references/dialect_dictionary.md

请参考上述方言词典，把下面这段话转换成湖北话：
"你在干什么？这东西真好吃。"
```

**方法 C：作为 Claude Project 知识库**
在 Claude Web 创建 Project → 上传 `dialect_dictionary.md` 作为 Knowledge，然后在 Project 内对话即可。

**支持度说明**：Claude 中文方言知识丰富，配合词典注入效果最佳，尤其粤语/闽南语/客家话等南方方言表现突出。

---

### 3. Cursor

**支持度：★★★★☆ 通过 .cursorrules 注入**

**方法 A：.cursorrules 引用**
```bash
cp references/dialect_dictionary.md .cursor/references/

# 在 .cursorrules 中添加：
# 涉及方言转换任务时，优先查阅 .cursor/references/dialect_dictionary.md 中的对应词条
```

**方法 B：Composer / Chat 中 @ 引用**
在 Cursor Chat 中直接 `@references/dialect_dictionary.md` 附加上下文，然后发送转换指令。

**方法 C：作为 Rules for AI**
将 SKILL.md 的转换策略部分复制到 Cursor Rules 中（Settings → Rules for AI → 添加规则）。

**支持度说明**：Cursor 的 Agent 模式可直接读取项目文件，词典附到项目中即可自动引用。

---

### 4. GitHub Copilot

**支持度：★★★☆☆ 通过 Custom Instructions**

GitHub Copilot 不直接支持外部知识库，但可通过 Custom Instructions 注入核心规则。

**方法 A：VS Code Custom Instructions**
在 VS Code 设置 `github.copilot.chat.instructions` 中添加方言转换的核心规则摘要（精简版 SKILL.md 的策略部分）。

**方法 B：Copilot Workspace**
在 Copilot Workspace（https://copilot-workspace.githubnext.com）中上传 `dialect_dictionary.md` 作为参考文件，然后发起转换任务。

**方法 C：提示词模板**
将每种方言的标志词提取为精简的提示词模板，存为 `.github/copilot-instructions.md`。

**限制**：Copilot 的上下文窗口有限，无法一次性加载全部 1233 词条，建议按需引用单一方言的词条。

---

### 5. ChatGPT（Web / Custom GPTs）

**支持度：★★★★☆ Custom GPTs 最佳**

**方法 A：Custom GPT（推荐）**
1. 进入 ChatGPT → "Explore GPTs" → "Create"
2. 在 Knowledge 区域上传 `dialect_dictionary.md`
3. 在 Instructions 中粘贴 `SKILL.md` 的 Overview 和转换策略部分
4. 保存后即可在 GPT 对话中使用

**方法 B：ChatGPT Web（直接上传）**
- 每次对话中直接附加 `dialect_dictionary.md`（ChatGPT Plus 支持文件上传）
- 提示词示例：`请根据附件的方言词典，把以下文本改成四川话：{内容}`

**方法 C：用精简版提示词**
如果上下文受限，可以复制某一种方言的词条表格粘贴到对话中，指定转换该方言。

---

### 6. DeepSeek / Kimi / 通义千问 (Qwen)

**支持度：★★★★★ 长上下文优势明显**

这三个国产模型以中文理解力和超长上下文著称，特别适合方言转换场景。

**DeepSeek（推荐）**
- DeepSeek Chat Web 版支持 1M 上下文，直接上传 `dialect_dictionary.md`
- 提示词：`参考附件的方言词典（19种方言对应1200+词条），把以下文本转换为湖北武汉话：{内容}`
- DeepSeek API 中作为 system prompt + user message 附件

**Kimi**
- 支持 200K 上下文，上传词典后直接对话
- 优点：中文口语理解力极强，方言转换自然度高于多数模型

**通义千问 (Qwen)**
- 通义千问 Web / APP 支持文件上传
- 将词典上传后，用对话模式逐步转换
- Qwen-Max 对方言词汇覆盖面广

**豆包 / 文心一言**
- 同样支持文档上传，上传 `dialect_dictionary.md` 作为参考
- 提示词：`你是方言转换专家，请参考附件词典，将这段话改成{XX方言}…`

---

### 7. Coze / Dify（Bot 构建平台）

**支持度：★★★★★ 企业级集成**

**Coze（扣子）**
1. 创建 Bot → 知识库 → 上传 `dialect_dictionary.md`
2. 在 Bot 的 Persona（人设）中粘贴 SKILL.md 的策略部分
3. 添加 Workflow 节点实现格式化输出
4. 发布到飞书/微信/Web 等渠道

**Dify**
1. 创建知识库 → 上传 `dialect_dictionary.md` → 选择分段模式（建议按 ## 标题分段，每个方言一段）
2. 创建 Chatflow 应用 → 关联知识库
3. 在 system prompt 中指定：`你是方言转换助手，转换时优先从知识库检索对应方言语料`
4. 可扩展为 API 接口供其他应用调用

**提示**：Dify 知识库分段建议按方言分，确保检索时能精确命中目标方言。

---

### 8. Cline / Roo Code（VS Code 插件）

**支持度：★★★☆☆ 通过 .clinerules 注入**

Cline 和 Roo Code 不原生支持 Skill，但支持自定义系统提示。

**安装**：
```bash
# 放置词典到项目
cp references/dialect_dictionary.md .cline/references/

# 在 .clinerules 中引用：
# 方言转换任务 — 参考 .cline/references/dialect_dictionary.md
```

**触发**：在 Cline 对话中直接说明转换需求，Cline 会读取 `.clinerules` 并引用词典。

---

### 9. Windsurf (Codeium)

**支持度：★★★☆☆ 通过 Rules 注入**

```
# 在 .windsurfrules 中添加：
方言转换任务应参考项目中的 references/dialect_dictionary.md
```

Windsurf 的 Cascade 模式会自动读取项目文件，将词典放入项目根目录即可。

---

### 10. 通用 API / LangChain（开发者）

**支持度：★★★★☆ 灵活集成**

**Python 示例**：
```python
# 加载词典为上下文
with open('references/dialect_dictionary.md', 'r') as f:
    dialect_dict = f.read()

system_prompt = f"""你是方言转换专家。以下是19种中国方言的完整词典。

{dialect_dict}

请根据词典将用户输入的普通话转换为指定方言。"""

# 调用任意 LLM API
response = llm.chat(
    system=system_prompt,
    user="把这段话改成四川话：你好，今天天气真好。"
)
```

**LangChain**：
```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter

# 按方言分段
loader = TextLoader("references/dialect_dictionary.md")
documents = loader.load()

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("##", "方言"), ("###", "子类")]
)
docs = splitter.split_text(documents[0].page_content)

# 检索 → 注入 → 生成
```

---

## 各平台支持度总览

| 平台 | 集成方式 | 难度 | 效果 |
|------|---------|------|------|
| **WorkBuddy** | 原生 Skill | ⭐ 极简 | ⭐⭐⭐⭐⭐ |
| **Claude Code/Desktop** | CLAUDE.md / Project Knowledge | ⭐⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **Cursor** | .cursorrules / @引用 | ⭐⭐ 简单 | ⭐⭐⭐⭐ |
| **GitHub Copilot** | Custom Instructions | ⭐⭐⭐ 中等 | ⭐⭐⭐ |
| **ChatGPT Custom GPT** | Knowledge 上传 | ⭐⭐ 简单 | ⭐⭐⭐⭐ |
| **DeepSeek** | 直接上传/粘贴 | ⭐ 极简 | ⭐⭐⭐⭐⭐ |
| **Kimi** | 直接上传/粘贴 | ⭐ 极简 | ⭐⭐⭐⭐⭐ |
| **通义千问** | 直接上传/粘贴 | ⭐ 极简 | ⭐⭐⭐⭐ |
| **Coze** | 知识库 | ⭐⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **Dify** | 知识库 + Chatflow | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ |
| **Cline / Roo Code** | .clinerules | ⭐⭐ 简单 | ⭐⭐⭐ |
| **Windsurf** | .windsurfrules | ⭐⭐ 简单 | ⭐⭐⭐ |
| **LangChain / API** | 文档加载器 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐ |

---

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
