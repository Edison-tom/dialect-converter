<div align="center">

# 🎙️ Dialect Converter

### 中国方言对白转换器 · 多模型版

<p>
  <em>普通话 → 30 种方言重口音表述 · VoxCPM 为主，兼容 Seed Audio / MiniMax / ElevenLabs / Mureka</em>
</p>

---

<img src="https://img.shields.io/badge/version-v2.3.1-blue?style=flat-square" alt="version">
<img src="https://img.shields.io/badge/总词条-234,673-brightgreen?style=flat-square" alt="entries">
<img src="https://img.shields.io/badge/方言-30种-orange?style=flat-square" alt="dialects">
<img src="https://img.shields.io/badge/VoxCPM原生-9组21变体-red?style=flat-square" alt="voxcpm">
<img src="https://img.shields.io/badge/备选模型-4种-teal?style=flat-square" alt="alt-models">
<img src="https://img.shields.io/badge/场景分类-160+-yellow?style=flat-square" alt="categories">
<img src="https://img.shields.io/badge/license-Apache--2.0-purple?style=flat-square" alt="license">

<br>

**每次转换输出 Control Instruction + Target Text，VoxCPM 方言直接生成语音，备选模型方言按对应 API 调用**

</div>

<br>

## ✨ 核心特性

<table>
<tr>
<td width="50%" valign="top">

### 🗣️ 30 种方言全覆盖
将普通话对白转换为 **30 种方言**的重口音表述，覆盖西南官话、粤语、吴语、东北官话、中原官话、冀鲁/胶辽官话、闽语、湘语、赣语、晋语、江淮官话、兰银官话、北京官话、河湟方言等主要方言区。

</td>
<td width="50%" valign="top">

### 🔊 多模型语音适配
**VoxCPM**（主要）原生支持 9 大方言组 21 种变体，本地运行 48kHz 工作室级语音。**Seed Audio / MiniMax / ElevenLabs / Mureka**（备选）覆盖 VoxCPM 不支持的 9 种方言。

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📚 海量词库
**234,673 条**词条覆盖全部 30 种方言，从日常饮食到军事科技，每种方言均含独立语音学标注（声调、声韵母、连读变调）与谱系分类。

</td>
<td width="50%" valign="top">

### 🎯 三级转换
基础层 / 增强层 / 地道层三级策略，按需调整方言浓度，从轻度本地化到全方言沉浸。

</td>
</tr>
</table>

<br>

## 🎬 快速预览

> 同一段普通话，12 种方言的转译效果 + Control Instruction：

<details>
<summary><b>点击查看方言转译示例</b></summary>

<br>

```
普通话  →  你在干什么？这个东西很好吃。你不知道吗？别骗我了。

── VoxCPM 原生方言 ──

四川话  →  你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
粤  语  →  你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。
上海话  →  侬勒做啥？搿只物事蛮好切额。侬勿晓得啊？覅骗吾了。
东北话  →  你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。
河南话  →  你弄啥嘞？这东西可中可好吃。你不知情哩？白搁这儿骗我。
陕西话  →  你弄啥哩？这东西嫽滴很。你不得知道？包哄我。
山东话  →  你干啥呢？这玩意儿杠好吃。你不知道啊？别忽悠俺了。
天津话  →  你干嘛呢？介玩意儿倍儿好吃。你不儿道啊？甭忽悠我了。
闽南话  →  汝咧做啥物？这物事诚好食。汝毋知影？莫骗我。

── 备选模型方言 ──

北京话  →  你干嘛呢？这玩意儿倍儿好吃。您不知道啊？甭蒙我了。
湖南话  →  你搞么子咯？咯只东西好恰得很。你不晓得啵？莫骗我咧。
客家话  →  你做么个？这东西当好食。你毋知？莫骗捱。
```

</details>

<details>
<summary><b>🔊 VoxCPM 输出格式示例（四川话）</b></summary>

<br>

**完整 VoxCPM 输入** — Control Instruction 置于 Target Text 前，用括号包裹：

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

# Control Instruction + Target Text
wav = model.generate(
    text="(四川方言，中年男性，慵懒语气，语速偏慢)"
         "你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("sichuan.wav", wav, model.tts_model.sample_rate)
```

**输出结构拆解**：

| 部分 | 内容 | 说明 |
|------|------|------|
| **Control Instruction** | `(四川方言，中年男性，慵懒语气，语速偏慢)` | 声音控制指令，括号内中文自然语言描述 |
| **Target Text** | `你在搞爪子？这个硬是好吃得很。...` | 方言转换后的目标文本 |
| **完整输入** | `(Control Instruction)Target Text` | 拼接后送入 `text` 参数 |

</details>

<details>
<summary><b>🔊 备选模型输出格式示例（北京话）</b></summary>

<br>

北京话等 VoxCPM 不支持的方言，使用 Seed Audio / MiniMax 等备选模型：

```
Control Instruction：北京话，中年男性，随和语气，正常语速。
Target Text：你干嘛呢？这玩意儿倍儿好吃。您不知道啊？甭蒙我了。
```

将 Target Text 送入备选模型 API 即可生成语音。详见 [TTS_MODEL_GUIDE.md](TTS_MODEL_GUIDE.md)。

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

> 💡 **核心原理**：所有 Agent 均支持在上下文中注入外部文件。将 `references/dialects/` 下的方言词元文件作为参考文件附加给对话，AI 自动按词条转换并生成 Control Instruction + Target Text 输出。

<br>

## 🔊 TTS 语音模型

### 模型总览

| 模型 | 类型 | 部署 | 原生方言 | 质量 | 许可证 |
|------|------|------|---------|------|--------|
| **VoxCPM** ⭐ 主要 | 本地模型 | 本地 GPU/CPU | 9 组 21 变体 | 48kHz 工作室级 | Apache-2.0 |
| **Seed Audio** | API | 云端 | 全方言 | 高质量 | 商用 API |
| **MiniMax** | API | 云端 | 全方言 | 高质量 | 商用 API |
| **ElevenLabs** | API | 云端 | 部分方言 | 高质量 | 商用 API |
| **Mureka** | API | 云端 | 全方言 | 高质量 | 商用 API |

### VoxCPM（主要模型）

[VoxCPM](https://github.com/OpenBMB/VoxCPM) 是 OpenBMB 开源的高质量多语言 TTS 模型：

| 特性 | 规格 |
|------|------|
| 模型参数 | 2B |
| 训练数据 | 200 万+小时 |
| 支持语言 | 30 种 + 9 种中文方言 |
| 音频输出 | 48kHz（工作室级质量） |
| VRAM 需求 | ~8 GB |
| 架构 | Tokenizer-free, Diffusion Autoregressive |
| 许可证 | Apache-2.0（可商用） |

### 输入格式

所有模型统一使用 **Control Instruction + Target Text** 格式：

```
(Control Instruction)Target Text
```

| 模式 | 说明 | 示例 |
|------|------|------|
| **VoxCPM Voice Design** | 从描述创建全新声音 | `(四川方言，中年男性，慵懒语气)要合成的文本` |
| **VoxCPM Cloning** | 克隆已有声音 + 风格控制 | `(语速较快，激动语气)要合成的文本` + `reference_wav_path` |
| **备选模型** | 按各模型 API 调用 | Control Instruction 作为声音描述参数 |

### Python 调用

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

# VoxCPM 方言语音生成
wav = model.generate(
    text="(粤语，中年男性，自信语气，正常语速)"
         "你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("cantonese.wav", wav, model.tts_model.sample_rate)
```

### CLI 调用

```bash
# Voice Design
voxcpm design \
  --text "(四川方言，中年男性，慵懒语气，语速偏慢)你在搞爪子？这个硬是好吃得很。" \
  --output sichuan.wav

# 带风格控制
voxcpm design \
  --text "你在搞爪子？这个硬是好吃得很。" \
  --control "四川方言，中年男性，慵懒语气，语速偏慢" \
  --seed 42 --output sichuan.wav
```

> 📖 备选模型的详细调用方式见 [TTS_MODEL_GUIDE.md](TTS_MODEL_GUIDE.md)

<br>

## 📖 使用方法

### 场景一：生成方言对白 + 语音提示词

在任何 AI Agent 中附加方言词典文件后：

```text
请参考附件方言词典，把下面这段话改成四川话（增强层）：
"老板，这个多少钱？能不能便宜点？"
```

Agent 自动输出：**Target Text**（方言文本）+ **Control Instruction**（声音控制指令）。

**输出示例**（VoxCPM 方言）：

```
Control Instruction：四川方言，中年男性，慵懒语气，语速偏慢。
Target Text：老板，这个几多钱嘛？能不能少点嘛？
```

**输出示例**（备选模型方言）：

```
Control Instruction：北京话，中年男性，随和语气，正常语速。
Target Text：老板，这多少钱啊？能便宜点儿不？
```

### 场景二：直接送入 VoxCPM 生成语音

将 Skill 输出的 `完整输入` 复制到 VoxCPM 的 `text` 参数即可：

```python
text = "(四川方言，中年男性，慵懒语气，语速偏慢)老板，这个几多钱嘛？能不能少点嘛？"
wav = model.generate(text=text, cfg_value=2.0, inference_timesteps=10, seed=42)
```

### 场景三：使用示例文件

```bash
# 查看 VoxCPM 格式的方言输出样例
ls outputs/model_formats/

# 四川话 VoxCPM 格式
cat outputs/model_formats/四川_voxcpm.txt

# 北京话 VoxCPM 格式（备选模型标注）
cat outputs/model_formats/北京话_voxcpm.txt
```

<br>

## 🎚️ 转换层级

| 层级 | 名称 | 转换内容 | 适用场景 |
|:----:|------|---------|---------|
| **Layer 1** | 基础层 | 仅核心词汇替换 | AI 辅助理解 · 轻度本地化 |
| **Layer 2** | 增强层（默认） | 词汇 + 语气词 + 句式调整 | 方言对白创作 · 台词改写 |
| **Layer 3** | 地道层 | 全方言沉浸（含俚语粗口） | 段子 · 喜剧脚本 · 模仿秀 |

<br>

## 🗺️ 支持的方言

### 30 种方言全覆盖

<div align="center">

| # | 方言 | 谱系 | 词条数 | TTS 模型 |
|:--:|------|------|------:|:--------:|
| 1 | **四川话** | 西南官话·成渝片 | 8,379 | VoxCPM |
| 2 | **粤语** | 粤语·广府片 | 8,120 | VoxCPM |
| 3 | **东北话** | 东北官话 | 8,032 | VoxCPM |
| 4 | **上海话** | 吴语·太湖片 | 7,915 | VoxCPM |
| 5 | **河南话** | 中原官话·郑开片 | 7,798 | VoxCPM |
| 6 | **陕西话** | 中原官话·关中片 | 6,990 | VoxCPM |
| 7 | **山东话** | 冀鲁/胶辽官话 | 6,991 | VoxCPM |
| 8 | **天津话** | 冀鲁官话·天津片 | 6,985 | VoxCPM |
| 9 | **闽南话** | 闽语·闽南片 | 12,006 | VoxCPM |
| 10 | **湖北话** | 西南官话·武天片 | 10,127 | VoxCPM |
| 11 | **云南话** | 西南官话·滇中片 | 7,005 | VoxCPM |
| 12 | **贵阳话** | 西南官话·黔中片 | 7,797 | VoxCPM |
| 13 | **徐州话** | 中原官话·徐淮片 | 7,778 | VoxCPM |
| 14 | **自贡话** | 西南官话·仁富片 | 7,796 | VoxCPM |
| 15 | **苏州话** | 吴语·太湖片 | 7,777 | VoxCPM |
| 16 | **成都话** | 西南官话·成渝片 | 6,812 | VoxCPM |
| 17 | **重庆话** | 西南官话·成渝片 | 6,810 | VoxCPM |
| 18 | **济南话** | 冀鲁官话 | 6,815 | VoxCPM |
| 19 | **青岛话** | 胶辽官话 | 6,817 | VoxCPM |
| 20 | **洛阳话** | 中原官话·洛嵩片 | 6,811 | VoxCPM |
| 21 | **温州话** | 吴语·瓯江片 | 6,593 | VoxCPM |
| 22 | **北京话** | 北京官话·京师片 | 10,019 | Seed Audio / MiniMax |
| 23 | **湖南话** | 湘语·长益片 | 9,938 | MiniMax / ElevenLabs |
| 24 | **客家话** | 客语·粤台片 | 7,798 | Seed Audio / Mureka |
| 25 | **赣语** | 赣语·昌靖片 | 7,766 | MiniMax / Mureka |
| 26 | **晋语** | 晋语·并州片 | 7,781 | Seed Audio / MiniMax |
| 27 | **南京话** | 江淮官话·洪巢片 | 6,598 | MiniMax / ElevenLabs |
| 28 | **福州话** | 闽语·闽东片 | 6,587 | Seed Audio / Mureka |
| 29 | **兰州话** | 兰银官话·金城片 | 6,593 | MiniMax / Seed Audio |
| 30 | **青海话** | 中原官话·秦陇片 | 9,439 | Seed Audio / MiniMax / Mureka |

</div>

> 📝 前 21 种方言（✅ VoxCPM）可直接送入 VoxCPM 本地模型生成语音；后 9 种方言使用备选 TTS 模型。每种方言附带声调系统、入声演变、韵母特征、语法特点、示例转换等完整语言学标注。

<details>
<summary><b>展开各方言 Control Instruction 默认参考</b></summary>

**VoxCPM 原生方言：**

| 方言 | 默认 Control Instruction |
|------|--------------------------|
| **四川话** | `四川方言，中年男性，慵懒语气，语速偏慢` |
| **粤语** | `粤语，中年男性，自信语气，正常语速` |
| **吴语（上海话）** | `上海话，年轻女性，温柔语气，正常语速` |
| **东北话** | `东北话，中年男性，洪亮嗓音，语速较快` |
| **河南话** | `河南话，中年男性，沉稳语气，正常语速` |
| **陕西话** | `陕西话，中年男性，低沉嗓音，语速偏慢` |
| **山东话** | `山东话，中年男性，豪爽语气，正常语速` |
| **天津话** | `天津话，中年男性，幽默语气，正常语速` |
| **闽南话** | `闽南话，中年男性，温和语气，语速偏慢` |

**备选模型方言：**

| 方言 | 默认 Control Instruction |
|------|--------------------------|
| **北京话** | `北京话，中年男性，随和语气，正常语速` |
| **湖南话** | `湖南话，中年男性，爽朗语气，语速较快` |
| **客家话** | `客家话，中年男性，温和语气，正常语速` |
| **赣语** | `赣语，中年男性，沉稳语气，正常语速` |
| **晋语** | `晋语，中年男性，低沉嗓音，语速偏慢` |
| **南京话** | `南京话，中年男性，随和语气，正常语速` |
| **福州话** | `福州话，中年男性，温和语气，语速偏慢` |
| **兰州话** | `兰州话，中年男性，豪爽语气，正常语速` |
| **青海话** | `青海话，中年男性，随和语气，正常语速` |

</details>

<br>

## 📦 安装

<details>
<summary><b>安装方言转换器</b></summary>

<br>

**macOS:**

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

**Windows:**

```powershell
# 克隆仓库
git clone https://github.com/Edison-tom/dialect-converter.git

# WorkBuddy 用户
xcopy /E /I dialect-converter %USERPROFILE%\.workbuddy\skills\dialect-converter
```
</details>

<details>
<summary><b>安装 VoxCPM 语音模型（主要模型）</b></summary>

<br>

**方式一：pip 安装**

```bash
pip install voxcpm
```

**方式二：从源码安装**

```bash
git clone https://github.com/OpenBMB/VoxCPM.git
cd VoxCPM
pip install -e .
```

**方式三：从 ModelScope 下载**

```python
from modelscope import snapshot_download
snapshot_download("OpenBMB/VoxCPM2", local_dir='./pretrained_models/VoxCPM2')
```

**快速验证：**

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)
wav = model.generate(text="欢迎使用方言转换器。", cfg_value=2.0, inference_timesteps=10, seed=42)
sf.write("test.wav", wav, model.tts_model.sample_rate)
```

</details>

<br>

## 📁 文件结构

```
dialect-converter/
│
├── 📄 README.md                        # 本文件
├── 📄 SKILL.md                         # 技能定义（含三级转换策略 + 多模型格式）
├── 📄 TTS_MODEL_GUIDE.md               # TTS 模型适配指南（VoxCPM + 备选模型）
│
├── 🐍 regen_voxcpm_formats.py          # VoxCPM 适配文件生成脚本
│
├── 📂 references/
│   ├── 📂 dialects/                    # 30 种方言词元文件（全部活跃）
│   │   ├── INDEX.md                    #   方言索引
│   │   ├── 00_appendix.md             #   附录
│   │   ├── 01_beijing.md              #   北京话（Seed Audio / MiniMax）
│   │   ├── 02_sichuan.md              #   四川话（VoxCPM）
│   │   ├── 03_yueyu.md               #   粤语（VoxCPM）
│   │   ├── 04_dongbei.md            #   东北话（VoxCPM）
│   │   ├── 05_shanghai.md           #   上海话（VoxCPM）
│   │   ├── 06_henan.md              #   河南话（VoxCPM）
│   │   ├── 07_shaanxi.md            #   陕西话（VoxCPM）
│   │   ├── 08_hunan.md              #   湖南话（MiniMax / ElevenLabs）
│   │   ├── 09_shandong.md           #   山东话（VoxCPM）
│   │   ├── 10_tianjin.md            #   天津话（VoxCPM）
│   │   ├── 11_minnan.md             #   闽南语（VoxCPM）
│   │   ├── 12_kejia.md              #   客家话（Seed Audio / Mureka）
│   │   ├── 13_ganyu.md              #   赣语（MiniMax / Mureka）
│   │   ├── 14_jinyu.md              #   晋语（Seed Audio / MiniMax）
│   │   ├── 15_yunnan.md             #   云南话（VoxCPM）
│   │   ├── 16_hubei.md              #   湖北话（VoxCPM）
│   │   ├── 17_guiyang.md            #   贵阳话（VoxCPM）
│   │   ├── 18_xuzhou.md             #   徐州话（VoxCPM）
│   │   ├── 19_zigong.md             #   自贡话（VoxCPM）
│   │   ├── 20_suzhou.md             #   苏州话（VoxCPM）
│   │   ├── 21_chengdu.md            #   成都话（VoxCPM）
│   │   ├── 22_chongqing.md           #   重庆话（VoxCPM）
│   │   ├── 23_jinan.md              #   济南话（VoxCPM）
│   │   ├── 24_qingdao.md            #   青岛话（VoxCPM）
│   │   ├── 25_luoyang.md            #   洛阳话（VoxCPM）
│   │   ├── 26_nanjing.md            #   南京话（MiniMax / ElevenLabs）
│   │   ├── 27_wenzhou.md            #   温州话（VoxCPM）
│   │   ├── 28_fuzhou.md             #   福州话（Seed Audio / Mureka）
│   │   ├── 29_lanzhou.md            #   兰州话（MiniMax / Seed Audio）
│   │   └── 30_qinghai.md            #   青海话（河湟方言·Seed Audio / MiniMax / Mureka）
│   │
│   └── 📄 dialect_dictionary.md        # 合并版完整词典（向下兼容）
│
└── 📂 outputs/
    └── 📂 model_formats/               # 30 种方言输出样例
        ├── 四川_voxcpm.txt             #   四川话（VoxCPM）
        ├── 粤语_voxcpm.txt             #   粤语（VoxCPM）
        ├── 北京话_voxcpm.txt           #   北京话（备选模型标注）
        ├── 湖南话_voxcpm.txt           #   湖南话（备选模型标注）
        ├── 客家话_voxcpm.txt           #   客家话（备选模型标注）
        ├── 赣语_voxcpm.txt             #   赣语（备选模型标注）
        ├── 晋语_voxcpm.txt             #   晋语（备选模型标注）
        ├── 南京话_voxcpm.txt           #   南京话（备选模型标注）
        ├── 福州话_voxcpm.txt           #   福州话（备选模型标注）
        ├── 兰州话_voxcpm.txt           #   兰州话（备选模型标注）
        └── ...                      #   其余方言
```

<br>

## ⚠️ 技术说明

本词典基于大规模语言模型 + 网络爬取 + 脚本批量生成，**非学术成果**。用字和注音可能存在偏差，仅供辅助创作参考。

### 版本历史

**v2.3.1**（当前）：周期维护 — 校验 30 种方言分布均衡性（极差比 1.82:1，低于 2:1 阈值）；验证词条总数 234,673 与 README 一致；词典版本保持 1.2.0。

**v2.3.0**：合并青海话至 dialect_dictionary.md；词典版本升至 1.2.0；更新各方言词条数为词典实际统计值（共 234,673 条）；修正方言数量描述统一为 30 种。

**v2.2.0**：新增青海话（河湟方言，中原官话·秦陇片，湟源/乐都/湟中一带）；方言总数达 30 种；VoxCPM 为主要模型，9 种 VoxCPM 不支持的方言使用 Seed Audio / MiniMax / ElevenLabs / Mureka 备选模型；词条总数 311,129 条。

**v2.1.0**：恢复全部 29 种方言为活跃状态；VoxCPM 设为主要模型，保留 Seed Audio / MiniMax / ElevenLabs / Mureka 作为备选 TTS 模型；8 种 VoxCPM 不支持的方言使用备选模型生成语音；词条总数 303,398 条。

**v2.0.2**：修正词条统计数据（词典实际 225,234 条，29 种方言）；更新方言表为 29 方言完整视图（21 活跃 + 8 归档）；词典版本升至 1.1.1。

**v2.0.1**：Control Instruction 从英文改为中文自然语言；修复四川话示例混入粤语的错误；简化输出格式。归档 8 种待支持方言词条（共 63,080 条），以备后续使用。

**v2.0.0**：移除全部旧 TTS 模型适配（Seed Audio / MiniMax / Eleven / Mureka），方言从 29 种缩减为 VoxCPM 支持的 9 大方言组（含 21 种方言变体），输出格式统一为 VoxCPM Control Instruction + Target Text。

<br>

---

<div align="center">

<sub>📦 仓库地址：https://github.com/Edison-tom/dialect-converter</sub>

<sub>🔊 主要语音模型：https://github.com/OpenBMB/VoxCPM</sub>

<sub>© 2025-2026 Dialect Converter · Made with ❤️ for Chinese dialect preservation</sub>

</div>
