# TTS 模型适配指南

> Dialect Converter v2.1.0 — VoxCPM 为主，多模型并存
> 主要模型：VoxCPM（9 大方言组原生支持）
> 备选模型：Seed Audio / MiniMax / ElevenLabs / Mureka（覆盖全部 29 种方言）

---

## 模型总览

| 模型 | 类型 | 部署方式 | 原生方言支持 | 音频质量 | 许可证 |
|------|------|---------|-------------|---------|--------|
| **VoxCPM** ⭐ 主要 | 本地模型 | 本地 GPU / CPU | 9 大方言组（21 变体） | 48kHz 工作室级 | Apache-2.0 |
| **Seed Audio** | API 云服务 | 云端 API | 全方言（需自定义） | 高质量 | 商用 API |
| **MiniMax** | API 云服务 | 云端 API | 全方言（需自定义） | 高质量 | 商用 API |
| **ElevenLabs** | API 云服务 | 云端 API | 多语言 | 高质量 | 商用 API |
| **Mureka** | API 云服务 | 云端 API | 全方言（需自定义） | 高质量 | 商用 API |

### 方言与模型对应关系

| # | 方言 | VoxCPM | Seed Audio | MiniMax | ElevenLabs | Mureka |
|:--:|------|:------:|:----------:|:-------:|:----------:|:------:|
| 1 | 四川话 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | 粤语 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | 上海话 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | 东北话 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | 河南话 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | 陕西话 | ✅ | ✅ | ✅ | — | ✅ |
| 7 | 山东话 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 8 | 天津话 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 9 | 闽南话 | ✅ | ✅ | ✅ | — | ✅ |
| 10 | 北京话 | — | ✅ ⭐ | ✅ ⭐ | ✅ | ✅ |
| 11 | 湖南话 | — | ✅ | ✅ ⭐ | ✅ ⭐ | ✅ |
| 12 | 客家话 | — | ✅ ⭐ | ✅ | — | ✅ ⭐ |
| 13 | 赣语 | — | ✅ | ✅ ⭐ | — | ✅ ⭐ |
| 14 | 晋语 | — | ✅ ⭐ | ✅ ⭐ | — | ✅ |
| 15 | 南京话 | — | ✅ | ✅ ⭐ | ✅ ⭐ | ✅ |
| 16 | 福州话 | — | ✅ ⭐ | ✅ | — | ✅ ⭐ |
| 17 | 兰州话 | — | ✅ | ✅ ⭐ | — | ✅ |

> ⭐ = 推荐模型 | ✅ = 支持 | — = 不支持/未验证

### 模型选择策略

```
用户请求方言转换
       │
       ▼
  方言属于 9 大方言组？
     ├── 是 ──→ VoxCPM（主要模型，本地运行，免费）
     └── 否 ──→ 查推荐表选择备选模型
                   ├── Seed Audio（高质量，多方言）
                   ├── MiniMax（高质量，多方言）
                   ├── ElevenLabs（多语言，部分方言）
                   └── Mureka（多方言，灵活）
```

---

# 第一部分：VoxCPM（主要模型）

## 1. 模型简介

[VoxCPM](https://github.com/OpenBMB/VoxCPM) 是 OpenBMB 开源的高质量多语言 TTS 模型，支持 30 种语言 + 9 种中文方言。

| 特性 | 规格 |
|------|------|
| 模型参数 | 2B |
| 骨干网络 | MiniCPM-4 |
| 训练数据 | 200 万+小时 |
| 支持语言 | 30 种 + 9 种中文方言 |
| 音频输出 | 48kHz 工作室级质量 |
| VRAM 需求 | ~8 GB |
| 架构 | Tokenizer-free, Diffusion Autoregressive |
| 流水线 | LocEnc → TSLM → RALM → LocDiT |
| 许可证 | Apache-2.0（可商用） |
| RTF | ~0.3 (RTX 4090, PyTorch) / ~0.13 (Nano-vLLM) |

### 支持的 9 种中文方言

| # | 方言 | 本项目对应词元文件 |
|:--:|------|------------------|
| 1 | 四川话 | `02_sichuan.md` + 成都/重庆/自贡/贵阳/云南/湖北分支 |
| 2 | 粤语 | `03_yueyu.md` |
| 3 | 吴语 | `05_shanghai.md` + 苏州/温州分支 |
| 4 | 东北话 | `04_dongbei.md` |
| 5 | 河南话 | `06_henan.md` + 洛阳/徐州分支 |
| 6 | 陕西话 | `07_shaanxi.md` |
| 7 | 山东话 | `09_shandong.md` + 济南/青岛分支 |
| 8 | 天津话 | `10_tianjin.md` |
| 9 | 闽南话 | `11_minnan.md` |

## 2. 安装

### pip 安装

```bash
pip install voxcpm
```

### 从源码安装

```bash
git clone https://github.com/OpenBMB/VoxCPM.git
cd VoxCPM
pip install -e .
```

### 从 ModelScope 下载

```python
from modelscope import snapshot_download
snapshot_download("OpenBMB/VoxCPM2", local_dir='./pretrained_models/VoxCPM2')
```

## 3. 输入格式：Control Instruction + Target Text

```
(Control Instruction)Target Text
```

- **Control Instruction**：放在括号 `()` 内的中文自然语言描述，控制方言、性别、年龄、口音、语速、情绪等
- **Target Text**：紧随括号之后的方言转换文本

> 模型会自动从文本推断语言/方言，**无需指定语言标签**。

### 三种生成模式

| 模式 | 输入 | 所需参数 | 特点 |
|------|------|---------|------|
| **纯 TTS** | `Target Text` | `text` | 无控制指令，使用默认声音 |
| **Voice Design** | `(描述)Target Text` | `text` | 从描述创建全新声音，无需参考音频 |
| **Controllable Cloning** | `(控制)Target Text` + 参考音频 | `text` + `reference_wav_path` | 克隆音色 + 风格控制 |

## 4. Python API 用法

### 4.1 基础方言语音生成

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

# 四川话 — Voice Design 模式
wav = model.generate(
    text="(四川方言，中年男性，慵懒语气，语速偏慢)"
         "你在搞爪子？这个硬是好吃得很。你不晓得嗦？",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("sichuan.wav", wav, model.tts_model.sample_rate)
```

### 4.2 参数说明

| 参数 | 类型 | 说明 | 推荐值 |
|------|------|------|--------|
| `text` | str | Control Instruction + Target Text | — |
| `reference_wav_path` | str | 参考音频路径（声音克隆） | 可选 |
| `prompt_wav_path` | str | 提示音频路径（极致克隆） | 可选 |
| `prompt_text` | str | 提示音频的精确转录文本 | 极致克隆必需 |
| `cfg_value` | float | CFG 引导强度 | 2.0 |
| `inference_timesteps` | int | 推理步数 | 10 |
| `seed` | int | 随机种子（可复现） | 42 |

### 4.3 声音克隆 + 方言控制

```python
# 使用参考音频克隆音色 + 方言风格控制
wav = model.generate(
    text="(语速较快，激动语气)你在搞爪子？这个硬是好吃得很。",
    reference_wav_path="path/to/dialect_voice.wav",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
```

### 4.4 流式生成

```python
import numpy as np

chunks = []
for chunk in model.generate_streaming(
    text="(粤语，中年男性，自信语气，正常语速)"
         "你做紧乜嘢啊？呢个好鬼好食㗎。",
):
    chunks.append(chunk)
wav = np.concatenate(chunks)
sf.write("cantonese.wav", wav, model.tts_model.sample_rate)
```

## 5. CLI 用法

### Voice Design

```bash
voxcpm design \
  --text "(四川方言，中年男性，慵懒语气，语速偏慢)你在搞爪子？这个硬是好吃得很。" \
  --output sichuan.wav
```

### 带风格控制

```bash
voxcpm design \
  --text "你在搞爪子？这个硬是好吃得很。" \
  --control "四川方言，中年男性，慵懒语气，语速偏慢" \
  --seed 42 \
  --output sichuan.wav
```

### 声音克隆

```bash
voxcpm clone \
  --text "你在搞爪子？这个硬是好吃得很。" \
  --reference-audio path/to/voice.wav \
  --output sichuan.wav
```

## 6. 部署选项

| 部署方式 | RTF (RTX 4090) | 说明 |
|----------|----------------|------|
| 标准 PyTorch | ~0.30 | 基础推理 |
| Nano-vLLM | ~0.13 | 高吞吐量 GPU 服务 |
| vLLM-Omni | — | OpenAI 兼容 API，多 GPU 部署 |
| llama.cpp-omni | ~1.76 (M4 Pro) | 端侧推理，CPU/Metal/CUDA/Vulkan |

## 7. 微调（可选）

如需进一步提升特定方言的合成质量，VoxCPM 支持 LoRA 微调：

```bash
# LoRA 微调（推荐）
python scripts/train_voxcpm_finetune.py \
    --config_path conf/voxcpm_v2/voxcpm_finetune_lora.yaml

# WebUI 微调
python lora_ft_webui.py   # http://localhost:7860
```

> 仅需 5-10 分钟音频即可适配特定说话人、语言或领域。

---

# 第二部分：备选 TTS 模型

> 以下模型用于 VoxCPM 不支持的 8 种方言（北京话、湖南话、客家话、赣语、晋语、南京话、福州话、兰州话），也可作为 VoxCPM 方言的备选方案。

## 8. Seed Audio

### 模型简介

Seed Audio 是字节跳动推出的高质量 TTS 服务，支持多种中文方言和口音，适合生成自然流畅的方言语音。

### 适用方言

| 方言 | 推荐场景 |
|------|---------|
| 北京话 | 京味儿对白、老北京场景 |
| 客家话 | 客家文化内容 |
| 晋语 | 山西地方题材 |
| 福州话 | 闽东文化内容 |
| 全部 9 大 VoxCPM 方言 | 作为 VoxCPM 备选 |

### 调用方式

```python
# Seed Audio API 调用示例
# 详见官方文档获取最新 API 接口

import requests

# 1. 准备方言文本
text = "你干嘛呢？这玩意儿倍儿好吃。"
control = "北京话，中年男性，随和语气，正常语速"

# 2. 调用 API
# response = requests.post(...)
```

### 输出格式

Seed Audio 接收方言文本 + 声音描述，输出格式与 VoxCPM 的 Control Instruction + Target Text 一致：

```
Control Instruction：北京话，中年男性，随和语气，正常语速。
Target Text：你干嘛呢？这玩意儿倍儿好吃。
```

## 9. MiniMax

### 模型简介

MiniMax 提供高质量的中文 TTS 服务，支持多种方言口音，语音自然度高，适合商业化场景。

### 适用方言

| 方言 | 推荐场景 |
|------|---------|
| 北京话 | 京味儿对白 |
| 湖南话 | 湖南方言题材 |
| 赣语 | 江西方言题材 |
| 晋语 | 山西地方题材 |
| 南京话 | 南京方言题材 |
| 兰州话 | 兰州方言题材 |
| 全部 9 大 VoxCPM 方言 | 作为 VoxCPM 备选 |

### 调用方式

```python
# MiniMax API 调用示例
# 详见 MiniMax 官方文档获取最新 API 接口

text = "你搞么子咯？这个东西好恰得很。"
control = "湖南话，中年男性，爽朗语气，语速较快"
```

### 输出格式

与 Control Instruction + Target Text 格式一致。

## 10. ElevenLabs

### 模型简介

ElevenLabs 是国际领先的 TTS 服务，支持多语言语音合成，中文方言支持部分覆盖，适合需要多语言混合的场景。

### 适用方言

| 方言 | 推荐场景 |
|------|---------|
| 湖南话 | 湘语题材 |
| 南京话 | 江淮官话题材 |
| 全部 9 大 VoxCPM 方言 | 作为 VoxCPM 备选 |

### 调用方式

```python
# ElevenLabs API 调用示例
# 详见 ElevenLabs 官方文档

text = "你搞么子咯？这个东西好恰得很。"
voice_settings = {
    "stability": 0.5,
    "similarity_boost": 0.75,
}
```

## 11. Mureka

### 模型简介

Mureka 提供灵活的 TTS 服务，支持多种中文方言，可通过参考音频克隆方言口音。

### 适用方言

| 方言 | 推荐场景 |
|------|---------|
| 客家话 | 客家文化内容 |
| 赣语 | 江西方言题材 |
| 福州话 | 闽东文化内容 |
| 全部 9 大 VoxCPM 方言 | 作为 VoxCPM 备选 |

### 调用方式

```python
# Mureka API 调用示例
# 详见 Mureka 官方文档

text = "汝食饱未？这东西好好食。"
control = "客家话，中年男性，温和语气，正常语速"
```

---

# 第三部分：配合流程

## 12. 与 Dialect Converter 的配合流程

```
用户输入普通话
       │
       ▼
Dialect Converter Skill
  ├── 1. 方言匹配（29 种方言全覆盖）
  ├── 2. 确定 TTS 模型
  │      ├── 9 大方言组 → VoxCPM（主要）
  │      └── 8 种其他方言 → 备选模型
  ├── 3. 分层转换（基础/增强/地道）
  ├── 4. 音韵规则检查
  └── 5. 输出
         ├── Target Text（方言文本）
         └── Control Instruction（声音控制指令）
                │
                ▼
         TTS 模型生成语音
         ├── VoxCPM: model.generate(text="(CI)Target Text")
         └── 备选模型: 按各模型 API 调用
                │
                ▼
         方言语音输出
```

## 13. 各方言默认 Control Instruction 参考

### VoxCPM 原生方言

| 方言 | Control Instruction |
|------|---------------------|
| **四川话** | `四川方言，中年男性，慵懒语气，语速偏慢` |
| **粤语** | `粤语，中年男性，自信语气，正常语速` |
| **吴语（上海话）** | `上海话，年轻女性，温柔语气，正常语速` |
| **东北话** | `东北话，中年男性，洪亮嗓音，语速较快` |
| **河南话** | `河南话，中年男性，沉稳语气，正常语速` |
| **陕西话** | `陕西话，中年男性，低沉嗓音，语速偏慢` |
| **山东话** | `山东话，中年男性，豪爽语气，正常语速` |
| **天津话** | `天津话，中年男性，幽默语气，正常语速` |
| **闽南话** | `闽南话，中年男性，温和语气，语速偏慢` |

### 备选模型方言

| 方言 | Control Instruction | 推荐模型 |
|------|---------------------|---------|
| **北京话** | `北京话，中年男性，随和语气，正常语速` | Seed Audio / MiniMax |
| **湖南话** | `湖南话，中年男性，爽朗语气，语速较快` | MiniMax / ElevenLabs |
| **客家话** | `客家话，中年男性，温和语气，正常语速` | Seed Audio / Mureka |
| **赣语** | `赣语，中年男性，沉稳语气，正常语速` | MiniMax / Mureka |
| **晋语** | `晋语，中年男性，低沉嗓音，语速偏慢` | Seed Audio / MiniMax |
| **南京话** | `南京话，中年男性，随和语气，正常语速` | MiniMax / ElevenLabs |
| **福州话** | `福州话，中年男性，温和语气，语速偏慢` | Seed Audio / Mureka |
| **兰州话** | `兰州话，中年男性，豪爽语气，正常语速` | MiniMax / Seed Audio |

### Control Instruction 要素

| 要素 | 说明 | 可选值 |
|------|------|--------|
| **方言** | 方言名称 | 四川方言 / 粤语 / 北京话 |
| **性别+年龄** | 根据角色推断 | 中年男性 / 老年女性 / 年轻女性 |
| **口音浓度** | 口音轻重 | 浓重口音 / 轻度口音 |
| **语速** | 结合内容情绪 | 语速较快 / 语速偏慢 / 正常语速 |
| **情绪** | 从对白内容提取 | 激动 / 轻松 / 悲伤 / 严肃 |

### 情绪调整示例

```python
# 轻松市井
text = "(四川方言，中年男性，轻松语气，语速偏慢)巴适得板哟，今天硬是安逸。"

# 激动争吵
text = "(四川方言，中年男性，激动语气，语速较快)搞锤子搞！你硬是不听话是不是嘛！"

# 悲伤低落
text = "(四川方言，中年男性，悲伤语气，语速偏慢)今天嘛，心头硬是不舒服，啥子都不想搞。"

# 幽默调侃
text = "(天津话，中年男性，幽默语气)介不废话嘛，倍儿好吃了您嘞。"

# 京味儿随和
text = "(北京话，中年男性，随和语气，正常语速)您猜怎么着？今儿这事儿倍儿有意思。"
```
