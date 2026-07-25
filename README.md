<div align="center">

# 🎙️ Dialect Converter

### 中国方言对白转换器

<p>
  <em>普通话 → 29 种重口音方言表述 · 适配 6 种主流 TTS/Audio 大模型</em>
</p>

---

<img src="https://img.shields.io/badge/version-v1.2.0-blue?style=flat-square" alt="version">
<img src="https://img.shields.io/badge/词条总数-302,018-brightgreen?style=flat-square" alt="entries">
<img src="https://img.shields.io/badge/方言-29种-orange?style=flat-square" alt="dialects">
<img src="https://img.shields.io/badge/TTS模型-6种-success?style=flat-square" alt="tts">
<img src="https://img.shields.io/badge/场景分类-160+-yellow?style=flat-square" alt="categories">
<img src="https://img.shields.io/badge/license-MIT-purple?style=flat-square" alt="license">
<img src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-teal?style=flat-square" alt="platform">

<br>

**每种方言附带完整语音学标注 · 分类词表 · 用法示例**

</div>

<br>

## ✨ 核心特性

<table>
<tr>
<td width="50%" valign="top">

### 🗣️ 方言转译
将普通话对白转换为 **29 种**中国方言的重口音表述，涵盖官话、吴语、粤语、闽南语、客家话等主要方言区。

</td>
<td width="50%" valign="top">

### 🔊 TTS 适配
同一方言对白可输出 **6 种**主流 TTS 模型格式：Seed Audio · MiniMax 2.8 · Eleven v3 · Eleven Music · Mureka v8 等。

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📚 海量词库
**302,018 条**词条覆盖 160+ 场景分类，从日常饮食到军事科技，每种方言均含独立语音学标注。

</td>
<td width="50%" valign="top">

### 🎯 三级转换
基础层 / 增强层 / 地道层三级策略，按需调整方言浓度，从轻度本地化到全方言沉浸。

</td>
</tr>
</table>

<br>

## 🎬 快速预览

> 同一段普通话，6 种方言的纯文本转译效果：

```
普通话  →  你在干什么？这个东西很好吃。你不知道吗？别骗我了。

北京话  →  你干嘛呢？这玩意儿倍儿好吃。你不儿道啊？甭忽悠我了。
四川话  →  你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
粤  语  →  你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。
东北话  →  你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。
湖北话  →  你在搞么斯咧？这个东西蛮好七。你不晓得？莫哄我。
上海话  →  侬勒做啥？搿只物事蛮好切额。侬勿晓得啊？覅骗吾了。
```

<details>
<summary><b>🔊 同一段方言对白的 6 种 TTS 模型输出格式</b></summary>

<br>

**① Seed Audio 1.0** — 角色脚本（场景 + 口音 + 情绪描述）
```text
【角色A - 老李，京片子，慢悠悠】你干嘛呢？这玩意儿倍儿好吃。
【角色B - 小王，语气冲】甭忽悠我了！你不儿道啊？
```

**② MiniMax 2.8 HD** — JSON（汉字 + 拼音数字调 + 语气标签）
```json
{
  "text": "你干嘛呢？(breath) 这玩意儿倍儿好吃。#0.8# 你不儿道啊？(sighs) 甭忽悠我了。#1.0#",
  "pronunciation_dict": { "tone": ["倍儿/(bei4)(er2)", "甭/(beng2)", "忽悠/(hu1)(you0)"] }
}
```

**③ Eleven v3** — TXT（IPA 国际音标 + 情绪标签）
```text
[curious] 你干嘛呢？这玩意儿/pei⁵¹ ɚ⁵¹/好吃。
[defiant] /pɤŋ³⁵/忽悠我了！
```

**④ Eleven Music v3** — 方言歌词 + 风格 Prompt
```text
你干嘛呢甭忽悠我 / 倍儿好吃你得信我 / 不儿道啊不儿道 / 胡同口儿见分晓
风格: 北京方言说唱，男声，痞气京片子，快板节奏，三弦+电子鼓
```

**⑤ Mureka v8** — 结构化歌词 JSON
```json
{
  "lyrics": "[Verse] 你干嘛呢甭忽悠我 / [Chorus] 倍儿好吃倍儿好吃 / [Outro] 走喽回见了您嘞",
  "prompt": "北京方言民谣，男声，京韵大鼓风格，中速，三弦+吉他"
}
```

**⑥ MiniMax 2.8 Turbo** — JSON（同 ② 格式，无语气标签）

</details>

<br>

## 🤖 支持的 AI Agent

| Agent | 接入方式 | 说明 |
|:-----:|---------|------|
| <b>WorkBuddy</b> | 原生 Skill | 开箱即用，`~/.workbuddy/skills/dialect-converter/` |
| <b>Claude Code</b> | CLAUDE.md | Project Knowledge 注入词典文件 |
| <b>Cursor</b> | .cursorrules | `@` 引用词典文件 |
| <b>GitHub Copilot</b> | Custom Instructions | 策略注入方式 |
| <b>ChatGPT</b> | Custom GPTs | 上传为 Knowledge Base |
| <b>DeepSeek / Kimi / 通义千问</b> | 长上下文 | 直接上传词典文件 |

> 💡 **核心原理**：所有 Agent 均支持在上下文中注入外部文件。将 `references/dialects/` 下的方言词元文件作为参考文件附加给对话，AI 自动按词条转换。

<br>

## 🔊 TTS/Audio 模型适配

| # | 模型 | 输出格式 | 注音方案 | 适用方言 |
|:---:|------|---------|---------|---------|
| 1 | **Seed Audio 1.0** | 角色脚本（场景 + 对白） | 无（角色口音引导） | 官话方言 |
| 2 | **MiniMax 2.8 HD** | JSON（汉字 + 拼音数字调） | `(zhua3)(zi0)` | 官话 + 粤语 |
| 3 | **MiniMax 2.8 Turbo** | JSON（同上，无语气标签） | 同上 | 同上 |
| 4 | **Eleven v3** | TXT（IPA 音标 + 情绪标签） | `/tʂu̯a²¹⁴ tsɹ̩⁰/` | 所有方言 |
| 5 | **Eleven Music v3** | TXT（歌词 + 风格 Prompt） | 无 | 方言歌曲 |
| 6 | **Mureka v8** | JSON（歌词 + 风格 Prompt） | 无 | 方言歌曲 |

<details>
<summary><b>📋 各模型输出格式完整示例（点击展开）</b></summary>

<br>

**Seed Audio 1.0 — 角色脚本**
```text
【场景：成都茶馆，市井氛围】

【角色A - 老王，地道成都口音，懒散】
你在搞爪子哦？

【角色B - 老张，重庆腔，急性子】
锤子！毛线！老子硬是不信。
```
> 完整样例见 `outputs/model_formats/四川_seed_audio.txt`

---

**MiniMax 2.8 HD — JSON + 拼音注音**
```json
{
  "model": "speech-2.8-hd",
  "text": "你在搞爪子哦？(breath) 这个东西硬是好吃得很。#0.8# 你不晓得嗦？(breath) 走撒去哆饭。#1.0# 硬是巴适得板哟",
  "pronunciation_dict": {
    "tone": ["爪子/(zhua3)(zi0)", "硬是/(ying4)(shi4)", "晓得/(xiao3)(de0)", "嗦/(so1)", "巴适/(ba1)(shi4)"]
  },
  "voice_setting": { "voice_id": "YOUR_VOICE_ID", "speed": 1.0 }
}
```
> 完整样例见 `outputs/model_formats/四川_minimax_2.8.json`

---

**Eleven v3 — IPA 音标 + 情绪标签**
```text
[curious] 你在搞/tʂu̯a²¹⁴ tsɹ̩⁰/哦？
[excited] 锤子！毛线！老子/iŋ⁵¹ ʂʅ⁵¹/不信。
[casual] 走撒，去/duo⁵⁵/饭！/pa⁵⁵ ʂʅ⁵¹ tɤ⁵¹ pan²¹⁴/哟
```
> 完整样例见 `outputs/model_formats/四川_eleven_v3.txt`

---

**Mureka v8 — 歌词 JSON**
```json
{
  "model": "mureka-8",
  "lyrics": "[Verse]\n在搞爪子哦在搞爪子\n硬是巴适得板喽\n[Chorus]\n巴适得板哟安逸得板\n[Outro]\n走喽走喽，明天再来",
  "prompt": "四川方言民谣，男声，痞气，中速，吉他+川剧锣鼓，火锅店氛围",
  "n": 2
}
```
> 完整样例见 `outputs/model_formats/四川_mureka_v8.json`

</details>

> 📁 **全部适配文件**：`outputs/model_formats/` — 29 种方言 × 4 格式 = **116 个文件**

<br>

## 📖 使用方法

### 场景一：生成方言对白

在任何 AI Agent 中附加方言词典文件后：

```text
请参考附件方言词典，把下面这段话改成湖北话（增强层）：
"老板，这个多少钱？能不能便宜点？"
```

Agent 自动检索对应方言词条，完成转换。

### 场景二：导出 TTS 模型格式

```text
把这段话改成四川话，输出 Seed Audio 角色脚本格式。
把这段话改成粤语，输出 MiniMax 拼音注音 JSON。
```

### 场景三：直接使用示例文件

```bash
# 查看所有模型方言输出样例
ls outputs/model_formats/

# Seed Audio 角色脚本
cat outputs/model_formats/四川_seed_audio.txt

# MiniMax 拼音注音 JSON
cat outputs/model_formats/四川_minimax_2.8.json

# Eleven v3 IPA 文本
cat outputs/model_formats/四川_eleven_v3.txt
```

### 场景四：按话题检索词条

词典覆盖 160+ 场景，打开 `references/dialects/` 目录，按文件内分类标题搜索：

| 搜索关键词 | 场景内容 | 词条量 |
|-----------|---------|:------:|
| `家居电器` | 冰箱/洗衣机/空调… | ~50 |
| `职场办公` | 面试/打卡/年终奖… | ~50 |
| `烹饪技法` | 炒/煎/蒸/炖/涮… | ~50 |
| `传统文化` | 书法/国画/刺绣/陶艺… | ~50 |
| `生物学` | 细胞/基因/疫苗/抗生素… | ~50 |
| `心理学` | 人格/情绪/潜意识/抑郁症… | ~50 |
| `军事武器` | 航母/核潜艇/战斗机/导弹… | ~50 |
| `社会发展` | 改革/创新/扶贫/法治… | ~50 |
| `建筑工程` | 地基/钢结构/消防通道… | ~50 |

> 每个话题下所有 29 种方言的词条排列在一起，支持横向对比。

<br>

## 🎚️ 转换层级

| 层级 | 名称 | 转换内容 | 适用场景 |
|:----:|------|---------|---------|
| **Layer 1** | 基础层 | 仅核心词汇替换 | AI 辅助理解 · 轻度本地化 |
| **Layer 2** | 增强层（默认） | 词汇 + 语气词 + 句式调整 | 方言对白创作 · 台词改写 |
| **Layer 3** | 地道层 | 全方言沉浸（含俚语粗口） | 段子 · 喜剧脚本 · 模仿秀 |

<br>

## 🗺️ 支持的方言

### 20 种主要方言

<div align="center">

| # | 方言 | 谱系 | 词条数 |
|:--:|------|------|-------:|
| 1 | 北京话 | 北京官话·京师片 | 12,595 |
| 2 | 四川话 | 西南官话·成渝片 | 10,812 |
| 3 | 粤语 | 粤语·广府片 | 10,552 |
| 4 | 东北话 | 东北官话 | 10,468 |
| 5 | 上海话 | 吴语·太湖片 | 10,362 |
| 6 | 河南话 | 中原官话·郑开片 | 10,252 |
| 7 | 陕西话 | 中原官话·关中片 | 9,669 |
| 8 | 湖南话 | 湘语·长益片 | 12,328 |
| 9 | 山东话 | 冀鲁/胶辽官话 | 9,670 |
| 10 | 天津话 | 冀鲁官话·天津片 | 9,664 |

</div>

<details>
<summary><b>展开全部 29 种方言列表（含 9 种次方言/扩增区）</b></summary>

<div align="center">

| # | 方言 | 谱系 | 词条数 |
|:--:|------|------|-------:|
| 11 | 闽南语 | 闽语·闽南片 | 14,332 |
| 12 | 客家话 | 客语·粤台片 | 10,253 |
| 13 | 赣语 | 赣语·昌靖片 | 10,223 |
| 14 | 晋语 | 晋语·并州片 | 10,238 |
| 15 | 云南话 | 西南官话·滇中片 | 9,683 |
| 16 | 湖北话 | 西南官话·武天片 | 12,509 |
| 17 | 贵阳话 | 西南官话·黔中片 | 10,254 |
| 18 | 徐州话 | 中原官话·徐淮片 | 10,235 |
| 19 | 自贡话 | 西南官话·仁富片 | 10,253 |
| 20 | 苏州话 | 吴语·太湖片 | 10,235 |
| 21 | 成都话 | 西南官话·成渝片 | 9,496 |
| 22 | 重庆话 | 西南官话·成渝片 | 9,494 |
| 23 | 济南话 | 冀鲁官话 | 9,499 |
| 24 | 青岛话 | 胶辽官话 | 9,501 |
| 25 | 洛阳话 | 中原官话·洛嵩片 | 9,495 |
| 26 | 南京话 | 江淮官话·洪巢片 | 9,287 |
| 27 | 温州话 | 吴语·瓯江片 | 9,282 |
| 28 | 福州话 | 闽语·闽东片 | 9,276 |
| 29 | 兰州话 | 兰银官话·金城片 | 9,282 |

</div>

</details>

> 📝 每种方言附带声调系统、入声演变、韵母特征、语法特点、示例转换等完整语言学标注。

<br>

## 🔡 注音方案对照

| 注音类型 | 适用方言 | 示例 | 适用模型 |
|---------|---------|------|---------|
| 无注音（纯汉字） | 所有方言 | 你在搞爪子？ | Seed Audio |
| 拼音数字调 | 官话方言 | `zhua3 zi0` | MiniMax 2.8 |
| 粤拼 (Jyutping) | 粤语 | `mat1 je5` | MiniMax 2.8 |
| IPA 国际音标 | 所有方言 | `/tʂu̯a²¹⁴ tsɹ̩⁰/` | Eleven v3 |

<br>

## 📦 安装

<details>
<summary><b>macOS</b></summary>

```bash
# 克隆仓库
git clone https://github.com/Edison-tom/dialect-converter.git

# WorkBuddy 用户 — 直接安装为 Skill
cp -r dialect-converter ~/.workbuddy/skills/

# Claude Code 用户 — 放入项目引用
cp dialect-converter/references/dialects/ 你的项目目录/

# Cursor 用户 — 放入 .cursor 目录
mkdir -p 你的项目目录/.cursor/references
cp dialect-converter/references/dialects/ 你的项目目录/.cursor/references/
```
</details>

<details>
<summary><b>Windows</b></summary>

```powershell
# 克隆仓库
git clone https://github.com/Edison-tom/dialect-converter.git

# WorkBuddy 用户 — 直接安装为 Skill
xcopy /E /I dialect-converter %USERPROFILE%\.workbuddy\skills\dialect-converter

# Claude Code 用户 — 放入项目引用
xcopy /E /I dialect-converter\references\dialects 你的项目目录\

# Cursor 用户 — 放入 .cursor 目录
mkdir 你的项目目录\.cursor\references
xcopy /E /I dialect-converter\references\dialects 你的项目目录\.cursor\references\
```
</details>

<br>

## 📁 文件结构

```
dialect-converter/
│
├── 📄 README.md                        # 本文件
├── 📄 SKILL.md                         # 技能定义（含三级转换策略）
├── 📄 TTS_MODEL_GUIDE.md               # 6种TTS/Audio模型适配指南
│
├── 🐍 expand_entries.py                # 大规模词条扩充脚本
├── 🐍 regen_model_formats.py           # 模型适配文件重新生成脚本
├── 🐍 generate_extra.py               # 批量扩词条脚本
│
├── 📂 references/
│   └── 📂 dialects/                    # 29个方言词元文件（按需加载）
│       ├── INDEX.md                    #   方言索引
│       ├── 00_appendix.md             #   附录
│       ├── 01_beijing.md              #   北京话
│       ├── 02_sichuan.md             #   四川话
│       └── ...                        #   (29种方言独立文件)
│
└── 📂 outputs/
    └── 📂 model_formats/               # 各模型方言输出样例
        ├── *_seed_audio.txt           #   Seed Audio 角色脚本
        ├── *_minimax_2.8.json         #   MiniMax 拼音注音
        ├── *_eleven_v3.txt            #   Eleven IPA 音标
        ├── *_mureka_v8.json          #   Mureka 歌词
        └── ...                        #   (29方言 × 4格式 = 116文件)
```

<br>

## ⚠️ 技术说明

本词典基于大规模语言模型 + 网络爬取 + 脚本批量生成，**非学术成果**。用字和注音可能存在偏差，仅供辅助创作参考。如需语言学级精度，请参考各方言学术文献。

<br>

---

<div align="center">

<sub>📦 仓库地址：https://github.com/Edison-tom/dialect-converter</sub>

<sub>© 2025-2026 Dialect Converter · Made with ❤️ for Chinese dialect preservation</sub>

</div>
