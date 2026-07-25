# VoxCPM 方言语音合成适配指南

> Dialect Converter v2.0.0 — 全面切换至 VoxCPM 本地语音模型

---

## 1. VoxCPM 模型简介

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

---

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

### CLI 工具

```bash
# 安装后可直接使用
voxcpm design --text "测试文本" --output test.wav
```

---

## 3. 输入格式：Control Instruction + Target Text

VoxCPM 的核心输入格式非常简洁：

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

---

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

---

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

### 批量处理

```bash
voxcpm batch --input examples/input.txt --output-dir outs
```

---

## 6. 各方言 Control Instruction 参考

### 6.1 默认 Control Instruction

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

### 6.2 Control Instruction 要素

| 要素 | 说明 | 可选值 |
|------|------|--------|
| **方言** | 方言名称 | 四川方言 / 粤语 / 东北话 |
| **性别+年龄** | 根据角色推断 | 中年男性 / 老年女性 / 年轻女性 |
| **口音浓度** | 口音轻重 | 浓重口音 / 轻度口音 |
| **语速** | 结合内容情绪 | 语速较快 / 语速偏慢 / 正常语速 |
| **情绪** | 从对白内容提取 | 激动 / 轻松 / 悲伤 / 严肃 |

### 6.3 情绪调整示例

```python
# 轻松市井
text = "(四川方言，中年男性，轻松语气，语速偏慢)巴适得板哟，今天硬是安逸。"

# 激动争吵
text = "(四川方言，中年男性，激动语气，语速较快)搞锤子搞！你硬是不听话是不是嘛！"

# 悲伤低落
text = "(四川方言，中年男性，悲伤语气，语速偏慢)今天嘛，心头硬是不舒服，啥子都不想搞。"

# 幽默调侃
text = "(天津话，中年男性，幽默语气)介不废话嘛，倍儿好吃了您嘞。"
```

---

## 7. 部署选项

| 部署方式 | RTF (RTX 4090) | 说明 |
|----------|----------------|------|
| 标准 PyTorch | ~0.30 | 基础推理 |
| Nano-vLLM | ~0.13 | 高吞吐量 GPU 服务 |
| vLLM-Omni | — | OpenAI 兼容 API，多 GPU 部署 |
| llama.cpp-omni | ~1.76 (M4 Pro) | 端侧推理，CPU/Metal/CUDA/Vulkan |

### Web Demo

```bash
python app.py --port 8808
# 设备选择: auto / cpu / mps / cuda / cuda:N
python app.py --device auto
```

---

## 8. 与 Dialect Converter 的配合流程

```
用户输入普通话
       │
       ▼
Dialect Converter Skill
  ├── 1. 方言匹配（9 大方言 + 分支）
  ├── 2. 分层转换（基础/增强/地道）
  ├── 3. 音韵规则检查
  └── 4. 输出
         ├── Target Text（方言文本）
         └── Control Instruction（声音控制指令）
                │
                ▼
         VoxCPM model.generate()
         text = "(Control Instruction)Target Text"
                │
                ▼
         48kHz 方言语音输出
```

---

## 9. 微调（可选）

如需进一步提升特定方言的合成质量，VoxCPM 支持 LoRA 微调：

```bash
# LoRA 微调（推荐）
python scripts/train_voxcpm_finetune.py \
    --config_path conf/voxcpm_v2/voxcpm_finetune_lora.yaml

# WebUI 微调
python lora_ft_webui.py   # http://localhost:7860
```

> 💡 仅需 5-10 分钟音频即可适配特定说话人、语言或领域。
