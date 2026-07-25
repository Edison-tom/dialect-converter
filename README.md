# Dialect Converter — 中国方言对白转换器 v9.0

将普通话对白文字转换为 **29 种**中国方言的重口音表述，适配 6 种主流 TTS/Audio 大模型的输出格式。每种方言附带完整语音学标注、分类词表和用法示例。

**总词条：215867 条** | **覆盖方言：29 种** | **场景分类：137+**

## 快速预览

### 方言文本转译

同一段普通话，不同方言的纯文本转换：

```
普通话：你在干什么？这个东西很好吃。你不知道吗？别骗我了。

北京话：你干嘛呢？这玩意儿倍儿好吃。你不儿道啊？甭忽悠我了。
四川话：你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
粤语：你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。
东北话：你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。
湖北话：你在搞么斯咧？这个东西蛮好七。你不晓得？莫哄我。
```

以上北京话例句，本技能可输出多种 TTS 模型可用的格式：

**① Seed Audio 1.0（角色对白脚本）**：
> `【角色A - 老李，京片子，慢悠悠】你干嘛呢？这玩意儿倍儿好吃。【角色B - 小王，语气冲】甭忽悠我了！你不儿道啊？`

**② MiniMax 2.8 HD（拼音注音 JSON）** — `text` 字段始终可见：
> `"text": "你干嘛呢？(breath) 这玩意儿倍儿好吃。#0.8# 你不儿道啊？(sighs) 甭忽悠我了。#1.0#"`

<details>
<summary>点击展开其余 JSON 字段</summary>

```json
{
  "pronunciation_dict": {
    "tone": ["倍儿/(bei4)(er2)", "甭/(beng2)", "忽悠/(hu1)(you0)"]
  },
  "voice_setting": { "voice_id": "YOUR_ID", "speed": 1.0, "pitch": 0 },
  "audio_setting": { "sample_rate": 32000, "format": "mp3" }
}
```
</details>

**③ Eleven v3（IPA 国际音标 + 情绪标签）**：
> `[curious] 你干嘛呢？这玩意儿/pei⁵¹ ɚ⁵¹/好吃。[defiant] /pɤŋ³⁵/忽悠我了！`

**④ Eleven Music v3（方言歌词 + 风格 Prompt）** — 歌词文本：
> 你干嘛呢甭忽悠我 / 倍儿好吃你得信我 / 不儿道啊不儿道 / 胡同口儿见分晓

<details>
<summary>点击展开风格 Prompt</summary>

```
北京方言说唱，男声，痞气京片子，快板节奏，三弦+电子鼓，胡同生活氛围
```
</details>

**⑤ Mureka v8（结构化歌词 JSON）** — `lyrics` 字段：
> `"[Verse] 你干嘛呢甭忽悠我 / [Chorus] 倍儿好吃倍儿好吃 / [Outro] 走喽回见了您嘞"`

<details>
<summary>点击展开其余 JSON 字段</summary>

```json
{
  "prompt": "北京方言民谣，男声，京韵大鼓风格，中速，三弦+吉他",
  "n": 2
}
```
</details>

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

## 支持的 TTS/Audio 模型输出

同一段方言对白，可按目标模型生成不同格式的输出文件：

| # | 模型 | 输出格式 | 注音方案 | 方言适用 |
|---|------|---------|---------|---------|
| 1 | **Seed Audio 1.0** | 角色脚本（场景 + 对白） | 无（通过角色口音引导） | 官话方言 |
| 2 | **MiniMax 2.8 HD** | JSON（汉字 + 拼音数字调） | `(zhua3)(zi0)` | 官话 + 粤语原生 |
| 3 | **MiniMax 2.8 Turbo** | JSON（同上，无语气标签） | 同上 | 同上 |
| 4 | **Eleven v3** | TXT（IPA 音标 + 情绪标签） | `/tʂu̯a²¹⁴ tsɹ̩⁰/` | 所有方言 |
| 5 | **Eleven Music v3** | TXT（歌词 + 风格 Prompt） | 无 | 方言歌曲 |
| 6 | **Mureka v8** | JSON（歌词 + 风格 Prompt） | 无 | 方言歌曲 |

### 输出格式示例

<details>
<summary><b>Seed Audio 1.0 — 角色脚本</b>（点击展开）</summary>

```text
【场景：成都茶馆，市井氛围】

【角色A - 老王，地道成都口音，懒散】
你在搞爪子哦？

【角色B - 老张，重庆腔，急性子】
锤子！毛线！老子硬是不信。
```
→ 完整样例见 `outputs/model_formats/四川_seed_audio.txt`
</details>

<details>
<summary><b>MiniMax 2.8 HD — JSON + 拼音注音</b>（点击展开）</summary>

```json
{
  "model": "speech-2.8-hd",
  "text": "你在搞爪子哦？(breath) 这个东西硬是好吃得很。#0.8# 你不晓得嗦？(breath) 走撒去哆饭。#1.0# 硬是巴适得板哟",
  "language_boost": "zh",
  "pronunciation_dict": {
    "tone": [
      "爪子/(zhua3)(zi0)",
      "硬是/(ying4)(shi4)",
      "晓得/(xiao3)(de0)",
      "嗦/(so1)",
      "巴适/(ba1)(shi4)",
      "要得/(yao4)(de2)"
    ]
  },
  "voice_setting": { "voice_id": "YOUR_VOICE_ID", "speed": 1.0 }
}
```
→ 完整样例见 `outputs/model_formats/四川_minimax_2.8.json`
</details>

<details>
<summary><b>Eleven v3 — IPA 音标 + 情绪标签</b>（点击展开）</summary>

```text
[curious] 你在搞/tʂu̯a²¹⁴ tsɹ̩⁰/哦？

[excited] 锤子！毛线！老子/iŋ⁵¹ ʂʅ⁵¹/不信。

[casual] 走撒，去/duo⁵⁵/饭！/pa⁵⁵ ʂʅ⁵¹ tɤ⁵¹ pan²¹⁴/哟
```
→ 完整样例见 `outputs/model_formats/四川_eleven_v3.txt`
</details>

<details>
<summary><b>Mureka v8 — 歌词</b>（点击展开）</summary>

```json
{
  "model": "mureka-8",
  "lyrics": "[Verse]\n在搞爪子哦在搞爪子\n硬是巴适得板喽\n[Chorus]\n巴适得板哟安逸得板\n锤子哦锤子哦\n[Outro]\n走喽走喽，明天再来",
  "prompt": "四川方言民谣，男声，痞气，中速，吉他+川剧锣鼓，火锅店氛围",
  "n": 2
}
```
→ 完整样例见 `outputs/model_formats/四川_mureka_v8.json`
</details>

> 📁 所有模型适配样例存放在 `outputs/model_formats/` 目录下（四川/东北/湖北/湖南 × 4 格式 + 粤语 MiniMax）。

---

## 使用方法

### 场景一：直接生成方言对白

在任何支持的 Agent（ChatGPT / Claude / DeepSeek 等）中：

```
请参考附件方言词典，把下面这段话改成河北武汉话（增强层）：
"老板，这个多少钱？能不能便宜点？"
```

Agent 会检索词典中的湖北话词条，自动替换为方言表述。

### 场景二：导出 TTS 模型可用格式

在 WorkBuddy 中触发方言转换 Skill 后，指定目标模型：

```
把这段话改成四川话，输出 Seed Audio 角色脚本格式。
把这段话改成粤语，输出 MiniMax 拼音注音 JSON。
```

Skill 会自动按对应模型的写法生成。

### 场景三：直接用仓库示例文件

```bash
# 直接查看各模型的方言输出样例
ls outputs/model_formats/

# Seed Audio 角色脚本
cat outputs/model_formats/四川_seed_audio.txt

# MiniMax 拼音注音 JSON
cat outputs/model_formats/四川_minimax_2.8.json

# Eleven v3 IPA 文本
cat outputs/model_formats/四川_eleven_v3.txt
```

### 场景四：按话题找词条

词典覆盖 80+ 个话题场景，打开 `references/dialect_dictionary.md`，直接 `Ctrl+F` 搜：

| 搜这个 | 找到的是 |
|--------|---------|
| `bulk-家居电器` | 冰箱/洗衣机/空调…50 个家电词汇 |
| `bulk-职场办公` | 面试/打卡/年终奖…30 个职场词汇 |
| `x30-烹饪技法` | 炒/煎/蒸/炖/涮…50 个烹饪动词 |
| `x30-传统文化` | 书法/国画/刺绣/陶艺…50 个文化词汇 |
| `x20-生物学` | 细胞/基因/疫苗/抗生素…50 个生物医学术语 |
| `x20-心理学` | 人格/情绪/潜意识/抑郁症…50 个心理学术语 |
| `x30-军事武器` | 航母/核潜艇/战斗机/导弹…50 个军事词汇 |
| `x40-社会发展` | 改革/创新/扶贫/法治…40 个社会关键词 |
| `x11-建筑工程` | 地基/钢结构/消防通道…50 个建筑词汇 |
| `四川话` 或 `粤语` | 跳到对应方言全部词条 |

每个话题下所有 29 种方言的词条排列在一起，方便横向对比。

---

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

---

## 文件结构

```
dialect-converter/
├── README.md                          # 本文件
├── SKILL.md                           # 技能定义（含三级转换策略）
├── TTS_MODEL_GUIDE.md                 # 6种TTS/Audio模型适配指南
├── generate_extra.py                  # Python 批量扩词条脚本
├── references/
│   └── dialects/                  # 29个方言词元文件（按需加载）
    │   ├── INDEX.md
    │   ├── 00_appendix.md
    │   ├── 01_beijing.md
    │   ├── 02_sichuan.md
    │   ├── 03_yueyu.md
    │   └── ... (29 种方言独立文件)└── outputs/
    └── model_formats/                 # 各模型方言输出样例
        ├── 四川_seed_audio.txt        #   Seed Audio 角色脚本
        ├── 四川_minimax_2.8.json      #   MiniMax 拼音注音
        ├── 四川_eleven_v3.txt         #   Eleven IPA 音标
        ├── 四川_mureka_v8.json        #   Mureka 歌词
        ├── 湖北_*                     #   湖北话 × 4 格式
        ├── 东北_*                     #   东北话 × 4 格式
        ├── 湖南_*                     #   湖南话 × 4 格式
        └── 粤语_minimax_2.8.json      #   粤拼 Jyutping 原生
```

---

## 注音方案对照

| 注音类型 | 适用方言 | 示例 | 适用模型 |
|---------|---------|------|---------|
| 无注音（纯汉字） | 所有 | 你在搞爪子？ | Seed Audio |
| 拼音数字调 | 官话方言 | `zhua3 zi0` | MiniMax 2.8 |
| 粤拼 (Jyutping) | 粤语 | `mat1 je5` | MiniMax 2.8 |
| IPA 国际音标 | 所有 | `/tʂu̯a²¹⁴ tsɹ̩⁰/` | Eleven v3 |

---

## 转换层级

| 层级 | 名称 | 内容 | 适用场景 |
|------|------|------|---------|
| Layer 1 | 基础层 | 仅核心词汇替换 | AI 辅助理解、轻度本地化 |
| Layer 2 | **增强层**（默认） | 词汇 + 语气词 + 句式调整 | 方言对白创作、台词改写 |
| Layer 3 | 地道层 | 全方言沉浸（含俚语粗口） | 段子、喜剧脚本、模仿秀 |

---

## 支持的方言（29种）

### 20 种大方言

| # | 方言 | 谱系 | 词条 |
|---|------|------|------|
| 1 | 北京话 | 北京官话·京师片 | 10018 |
| 2 | 四川话 | 西南官话·成渝片 | 8378 |
| 3 | 粤语 | 粤语·广府片 | 8119 |
| 4 | 东北话 | 东北官话 | 8036 |
| 5 | 上海话 | 吴语·太湖片 | 7919 |
| 6 | 河南话 | 中原官话·郑开片 | 7801 |
| 7 | 陕西话 | 中原官话·关中片 | 6994 |
| 8 | 湖南话 | 湘语·长益片 | 9941 |
| 9 | 山东话 | 冀鲁/胶辽官话 | 6995 |
| 10 | 天津话 | 冀鲁官话·天津片 | 6989 |
| 11 | 闽南语 | 闽语·闽南片 | 12009 |
| 12 | 客家话 | 客语·粤台片 | 7802 |
| 13 | 赣语 | 赣语·昌靖片 | 7770 |
| 14 | 晋语 | 晋语·并州片 | 7785 |
| 15 | 云南话 | 西南官话·滇中片 | 7008 |
| 16 | 湖北话 | 西南官话·武天片 | 10130 |
| 17 | 贵阳话 | 西南官话·黔中片 | 7800 |
| 18 | 徐州话 | 中原官话·徐淮片 | 7781 |
| 19 | 自贡话 | 西南官话·仁富片 | 7799 |
| 20 | 苏州话 | 吴语·太湖片 | 7781 |

### 9 种次方言/扩增区

| # | 方言 | 谱系 | 词条 |
|---|------|------|------|
| 21 | 成都话 | 西南官话·成渝片 | 6816 |
| 22 | 重庆话 | 西南官话·成渝片 | 6814 |
| 23 | 济南话 | 冀鲁官话 | 6819 |
| 24 | 青岛话 | 胶辽官话 | 6821 |
| 25 | 洛阳话 | 中原官话·洛嵩片 | 6815 |
| 26 | 南京话 | 江淮官话·洪巢片 | 6602 |
| 27 | 温州话 | 吴语·瓯江片 | 6597 |
| 28 | 福州话 | 闽语·闽东片 | 6591 |
| 29 | 兰州话 | 兰银官话·金城片 | 6597 |

> 语言学标注：每种方言附带声调系统、入声演变、韵母特征、语法特点、示例转换。

---

## 技术说明

本词典基于大规模语言模型 + 网络爬取 + 脚本批量生成，**非学术成果**。用字和注音可能存在偏差，仅供辅助创作参考。

---

> 📦 仓库地址：https://github.com/Edison-tom/dialect-converter
