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

- **Control Instruction**：放在括号 `()` 内的自然语言声音描述，控制性别、年龄、口音、语速、情绪等
- **Target Text**：紧随括号之后的实际要合成的文本（方言文本）

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
    text="(A middle-aged Sichuan male, relaxed and lazy tone, slightly slow pace, "
         "with Chengdu accent, trailing particles)"
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
    text="(slightly faster, cheerful tone)你在搞爪子？这个硬是好吃得很。",
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
    text="(A middle-aged Cantonese male, confident tone)"
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
  --text "(A middle-aged Sichuan male, relaxed tone)你在搞爪子？这个硬是好吃得很。" \
  --output sichuan.wav
```

### 带风格控制

```bash
voxcpm design \
  --text "你在搞爪子？这个硬是好吃得很。" \
  --control "A middle-aged Sichuan male, relaxed and lazy tone" \
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
| **四川话** | `(A middle-aged Sichuan male, relaxed and lazy tone, slightly slow pace, with Chengdu accent, trailing particles like "o" and "sa")` |
| **粤语** | `(A middle-aged Cantonese male, confident and energetic tone, moderate pace, with Guangzhou accent, short and punchy delivery)` |
| **吴语（上海话）** | `(A young Shanghai female, gentle and soft voice, moderate pace, with Wu dialect accent, melodic rising tones)` |
| **东北话** | `(A middle-aged Northeastern male, loud and bold voice, fast pace, with Dongbei accent, hearty and direct delivery)` |
| **河南话** | `(A middle-aged Henan male, steady and grounded tone, moderate pace, with Central Plains accent, nasal quality)` |
| **陕西话** | `(A middle-aged Shaanxi male, deep and resonant voice, slow pace, with Guanzhong accent, heavy nasal tones)` |
| **山东话** | `(A middle-aged Shandong male, robust and straightforward voice, moderate pace, with Ji-Lu accent, bold delivery)` |
| **天津话** | `(A middle-aged Tianjin male, witty and humorous tone, moderate pace, with Tianjin accent, playful rising intonation)` |
| **闽南话** | `(A middle-aged Minnan male, warm and friendly voice, slow pace, with Southern Fujian accent, soft trailing tones)` |

### 6.2 Control Instruction 要素

| 要素 | 说明 | 可选值 |
|------|------|--------|
| **性别** | 根据对白角色推断 | male / female |
| **年龄** | 根据角色设定 | young / middle-aged / elderly |
| **口音** | 方言名称 + 特征 | Sichuan accent, Cantonese accent, etc. |
| **语速** | 结合内容情绪 | slow / moderate / fast / rapid |
| **情绪** | 从对白内容提取 | relaxed / excited / angry / sad / cheerful / serious |
| **嗓音特征** | 声音质感描述 | gentle / raspy / resonant / soft / bold |

### 6.3 情绪调整示例

```python
# 轻松市井
text = "(A middle-aged Sichuan male, relaxed tone, slow pace)巴适得板哟，今天硬是安逸。"

# 激动争吵
text = "(A middle-aged Sichuan male, excited and loud tone, fast pace)搞锤子搞！你硬是不听话是不是嘛！"

# 悲伤低落
text = "(A middle-aged Sichuan male, sad tone, slow pace)今天嘛，心头硬是不舒服，啥子都不想搞。"

# 幽默调侃
text = "(A middle-aged Tianjin male, witty and humorous tone)介不废话嘛，倍儿好吃了您嘞。"
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
