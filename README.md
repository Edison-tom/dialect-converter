<div align="center">

# 🎙️ Dialect Converter

### 中国方言对白转换器 · VoxCPM Edition

<p>
  <em>普通话 → 9 大方言重口音表述 · 适配 VoxCPM 本地语音合成模型</em>
</p>

---

<img src="https://img.shields.io/badge/version-v2.0.1-blue?style=flat-square" alt="version">
<img src="https://img.shields.io/badge/活跃词条-218,500+-brightgreen?style=flat-square" alt="entries">
<img src="https://img.shields.io/badge/归档词条-83,400+-yellowgreen?style=flat-square" alt="archived">
<img src="https://img.shields.io/badge/方言组-9种-orange?style=flat-square" alt="dialects">
<img src="https://img.shields.io/badge/方言变体-21种-success?style=flat-square" alt="variants">
<img src="https://img.shields.io/badge/TTS引擎-VoxCPM-red?style=flat-square" alt="tts">
<img src="https://img.shields.io/badge/场景分类-160+-yellow?style=flat-square" alt="categories">
<img src="https://img.shields.io/badge/license-Apache--2.0-purple?style=flat-square" alt="license">

<br>

**每次转换输出 Control Instruction + Target Text，可直接送入 VoxCPM 生成方言语音**

</div>

<br>

## ✨ 核心特性

<table>
<tr>
<td width="50%" valign="top">

### 🗣️ 方言转译
将普通话对白转换为 **9 大方言**（含地方分支共 21 种）的重口音表述，覆盖西南官话、粤语、吴语、东北官话、中原官话、冀鲁/胶辽官话、闽语等主要方言区。

</td>
<td width="50%" valign="top">

### 🔊 VoxCPM 语音适配
每次转换自动生成 **Control Instruction**（声音控制指令）+ **Target Text**（方言目标文本），直接送入 VoxCPM `model.generate()` 即可合成 48kHz 工作室级方言语音。

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📚 海量词库
**218,500+ 条**活跃词条覆盖 160+ 场景分类，另有 **83,400+ 条**归档词条（8 种待支持方言）以备后续使用，从日常饮食到军事科技，每种方言均含独立语音学标注。

</td>
<td width="50%" valign="top">

### 🎯 三级转换
基础层 / 增强层 / 地道层三级策略，按需调整方言浓度，从轻度本地化到全方言沉浸。

</td>
</tr>
</table>

<br>

## 🎬 快速预览

> 同一段普通话，9 种方言的转译效果 + VoxCPM Control Instruction：

<details>
<summary><b>点击查看方言转译示例</b></summary>

<br>

```
普通话  →  你在干什么？这个东西很好吃。你不知道吗？别骗我了。

四川话  →  你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
粤  语  →  你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。
上海话  →  侬勒做啥？搿只物事蛮好切额。侬勿晓得啊？覅骗吾了。
东北话  →  你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。
河南话  →  你弄啥嘞？这东西可中可好吃。你不知情哩？白搁这儿骗我。
陕西话  →  你弄啥哩？这东西嫽滴很。你不得知道？包哄我。
山东话  →  你干啥呢？这玩意儿杠好吃。你不知道啊？别忽悠俺了。
天津话  →  你干嘛呢？介玩意儿倍儿好吃。你不儿道啊？甭忽悠我了。
闽南话  →  汝咧做啥物？这物事诚好食。汝毋知影？莫骗我。
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

> 💡 **核心原理**：所有 Agent 均支持在上下文中注入外部文件。将 `references/dialects/` 下的方言词元文件作为参考文件附加给对话，AI 自动按词条转换并生成 VoxCPM 格式输出。

<br>

## 🔊 VoxCPM 语音模型

### 模型简介

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

VoxCPM 使用 **Control Instruction + Target Text** 格式，通过括号包裹的中文自然语言描述控制声音特征：

```
(Control Instruction)Target Text
```

| 模式 | 说明 | 示例 |
|------|------|------|
| **Voice Design** | 从描述创建全新声音，无需参考音频 | `(四川方言，中年男性，慵懒语气)要合成的文本` |
| **Controllable Cloning** | 克隆已有声音 + 风格控制 | `(语速较快，激动语气)要合成的文本` + `reference_wav_path` |
| **纯 TTS** | 无控制指令，使用默认声音 | `要合成的文本` |

### Python 调用

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

# 方言语音生成
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

<br>

## 📖 使用方法

### 场景一：生成方言对白 + 语音提示词

在任何 AI Agent 中附加方言词典文件后：

```text
请参考附件方言词典，把下面这段话改成四川话（增强层）：
"老板，这个多少钱？能不能便宜点？"
```

Agent 自动输出：**Target Text**（方言文本）+ **Control Instruction**（VoxCPM 控制指令）。

**输出示例**：

```
Control Instruction：四川方言，中年男性，慵懒语气，语速偏慢。
Target Text：老板，这个几多钱嘛？能不能少点嘛？
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

# 粤语 VoxCPM 格式
cat outputs/model_formats/粤语_voxcpm.txt
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

### 9 大方言组 + 21 种方言变体

<div align="center">

| # | 方言组 | 谱系 | 地方分支 | VoxCPM |
|:--:|------|------|---------|:------:|
| 1 | **四川话** | 西南官话·成渝片 | 成都话、重庆话、自贡话、贵阳话、云南话、湖北话 | ✅ |
| 2 | **粤语** | 粤语·广府片 | — | ✅ |
| 3 | **吴语** | 吴语·太湖片/瓯江片 | 上海话、苏州话、温州话 | ✅ |
| 4 | **东北话** | 东北官话 | — | ✅ |
| 5 | **河南话** | 中原官话·郑开片 | 洛阳话、徐州话 | ✅ |
| 6 | **陕西话** | 中原官话·关中片 | — | ✅ |
| 7 | **山东话** | 冀鲁/胶辽官话 | 济南话、青岛话 | ✅ |
| 8 | **天津话** | 冀鲁官话·天津片 | — | ✅ |
| 9 | **闽南话** | 闽语·闽南片 | — | ✅ |

</div>

> 📝 每种方言附带声调系统、入声演变、韵母特征、语法特点、示例转换等完整语言学标注。

<details>
<summary><b>展开各方言 Control Instruction 默认参考</b></summary>

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
<summary><b>安装 VoxCPM 语音模型</b></summary>

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
├── 📄 SKILL.md                         # 技能定义（含三级转换策略 + VoxCPM 格式）
├── 📄 TTS_MODEL_GUIDE.md               # VoxCPM 模型适配指南
│
├── 🐍 regen_voxcpm_formats.py          # VoxCPM 适配文件生成脚本
│
├── 📂 references/
│   ├── 📂 dialects/                    # 9 大方言 + 12 地方分支词元文件
│   │   ├── INDEX.md                    #   方言索引
│   │   ├── 00_appendix.md             #   附录
│   │   ├── 02_sichuan.md              #   四川话（含成都/重庆/自贡等分支）
│   │   ├── 03_yueyu.md               #   粤语
│   │   ├── 04_dongbei.md            #   东北话
│   │   ├── 05_shanghai.md           #   上海话（吴语）
│   │   ├── 06_henan.md              #   河南话
│   │   ├── 07_shaanxi.md            #   陕西话
│   │   ├── 09_shandong.md           #   山东话
│   │   ├── 10_tianjin.md            #   天津话
│   │   ├── 11_minnan.md             #   闽南语
│   │   └── ...                      #   (地方分支文件)
│   │
│   └── 📂 dialects_archive/            # 已归档方言（VoxCPM 暂不支持）
│       ├── INDEX.md                    #   归档索引
│       ├── 01_beijing.md              #   北京话（12,595 条）
│       ├── 08_hunan.md                #   湖南话（12,328 条）
│       ├── 12_kejia.md                #   客家话（10,253 条）
│       ├── 13_ganyu.md               #   赣语（10,223 条）
│       ├── 14_jinyu.md               #   晋语（10,238 条）
│       ├── 26_nanjing.md             #   南京话（9,287 条）
│       ├── 28_fuzhou.md              #   福州话（9,276 条）
│       └── 29_lanzhou.md            #   兰州话（9,282 条）
│
└── 📂 outputs/
    └── 📂 model_formats/               # VoxCPM 方言输出样例
        ├── 四川_voxcpm.txt             #   四川话 Control Instruction + Target Text
        ├── 粤语_voxcpm.txt             #   粤语
        ├── 上海_voxcpm.txt             #   上海话（吴语）
        ├── 东北_voxcpm.txt             #   东北话
        ├── 河南_voxcpm.txt             #   河南话
        ├── 陕西_voxcpm.txt             #   陕西话
        ├── 山东_voxcpm.txt             #   山东话
        ├── 天津_voxcpm.txt             #   天津话
        └── 闽南_voxcpm.txt             #   闽南话
```

<br>

## ⚠️ 技术说明

本词典基于大规模语言模型 + 网络爬取 + 脚本批量生成，**非学术成果**。用字和注音可能存在偏差，仅供辅助创作参考。

v2.0.0 重大变更：移除全部旧 TTS 模型适配（Seed Audio / MiniMax / Eleven / Mureka），方言从 29 种缩减为 VoxCPM 支持的 9 大方言组（含 21 种方言变体），输出格式统一为 VoxCPM Control Instruction + Target Text。

v2.0.1 更新：Control Instruction 从英文改为中文自然语言（如：`四川方言，中老年女性，浓重口音，语速较快`）；修复四川话示例混入粤语的错误；简化输出格式。归档 8 种待支持方言词条至 `references/dialects_archive/`（共 83,482 条），以备后续 VoxCPM 扩展方言支持时启用。

<br>

---

<div align="center">

<sub>📦 仓库地址：https://github.com/Edison-tom/dialect-converter</sub>

<sub>🔊 语音模型：https://github.com/OpenBMB/VoxCPM</sub>

<sub>© 2025-2026 Dialect Converter · Made with ❤️ for Chinese dialect preservation</sub>

</div>
