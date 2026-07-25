---
name: dialect-converter
description: 将普通话对白文字转换为重口音的方言表述。基于 VoxCPM 本地语音模型，覆盖四川话、粤语、吴语、东北话、河南话、陕西话、山东话、天津话、闽南话 9 大方言及其地方分支。支持三级转换模式（基础/增强/地道），含完整语音学标注（声调、声韵母、连读变调）与谱系分类。每次转换输出 Control Instruction（语音控制指令）+ Target Text（方言目标文本），可直接送入 VoxCPM 生成方言语音。自动通过自然语言分析匹配目标方言及对应词元文件，用户无需手动指定文件路径。触发词：方言转换、四川话、粤语、东北话、改写对白、方言台词、方言配音、方言段子、VoxCPM、方言语音。
agent_created: true
---

# Dialect Converter — 方言转换器 v2.0.0

## Overview

将普通话对白转换为 **9 大方言**（含地方分支共 21 种）的重口音表述。v2.0.0 重大变更：**全面切换至 VoxCPM 本地语音模型**，移除全部旧 TTS 模型适配（Seed Audio / MiniMax / Eleven / Mureka 等），输出格式统一为 VoxCPM 的 **Control Instruction + Target Text**。

> 🔧 **VoxCPM** 是 OpenBMB 开源的高质量多语言 TTS 模型（2B 参数，200 万+小时训练数据），支持 30 种语言 + 9 种中文方言，输出 48kHz 工作室级音频。GitHub: https://github.com/OpenBMB/VoxCPM

## 方言自动匹配系统

### 支持的方言总览

| 编号 | 方言组 | 地方分支 | VoxCPM 原生支持 |
|:----:|-------|---------|:---------------:|
| 1 | **四川话** | 成都话、重庆话、自贡话、贵阳话、云南话、湖北话 | ✅ 四川话 |
| 2 | **粤语** | — | ✅ 粤语 |
| 3 | **吴语** | 上海话、苏州话、温州话 | ✅ 吴语 |
| 4 | **东北话** | — | ✅ 东北话 |
| 5 | **河南话** | 洛阳话、徐州话 | ✅ 河南话 |
| 6 | **陕西话** | — | ✅ 陕西话 |
| 7 | **山东话** | 济南话、青岛话 | ✅ 山东话 |
| 8 | **天津话** | — | ✅ 天津话 |
| 9 | **闽南话** | — | ✅ 闽南话 |

> ⚠️ v2.0.0 移除了以下方言（VoxCPM 不支持）：北京话、湖南话、客家话、赣语、晋语、南京话、福州话、兰州话。

### 匹配原则

Skill 收到请求后，按以下优先级分析用户自然语言中的方言意图：

### Level 1 — 精确名称匹配（最高优先级）

用户直接说出方言标准名称时，立即定位词元文件：

| 方言组 | 用户表述 | 匹配方言 | 词元文件 |
|-------|---------|---------|---------|
| **四川话** | "四川话"、"川话"、"成都话"、"重庆话"、"自贡话"、"贵阳话"、"云南话"、"昆明话"、"湖北话"、"武汉话" | 按具体城市匹配 | `02_sichuan.md` ~ `22_chongqing.md` |
| **粤语** | "粤语"、"广东话"、"白话"、"广州话" | 粤语 | `03_yueyu.md` |
| **吴语** | "上海话"、"沪语"、"苏州话"、"吴侬软语"、"温州话" | 按具体城市匹配 | `05_shanghai.md` / `20_suzhou.md` / `27_wenzhou.md` |
| **东北话** | "东北话"、"东北腔" | 东北话 | `04_dongbei.md` |
| **河南话** | "河南话"、"洛阳话"、"徐州话" | 按具体城市匹配 | `06_henan.md` / `18_xuzhou.md` / `25_luoyang.md` |
| **陕西话** | "陕西话"、"西安话" | 陕西话 | `07_shaanxi.md` |
| **山东话** | "山东话"、"济南话"、"青岛话" | 按具体城市匹配 | `09_shandong.md` / `23_jinan.md` / `24_qingdao.md` |
| **天津话** | "天津话"、"天津卫" | 天津话 | `10_tianjin.md` |
| **闽南话** | "闽南话"、"闽南语"、"台语"、"台湾话" | 闽南语 | `11_minnan.md` |

### Level 2 — 模糊描述推断

当用户未给出明确方言名时，根据上下文推断：

| 用户描述 | 推断方言 | 词元文件 |
|---------|---------|---------|
| "四川重庆那边" | 四川话 / 重庆话 | `02_sichuan.md` / `22_chongqing.md` |
| "粤港澳那边" | 粤语 | `03_yueyu.md` |
| "江浙沪"、"长三角" | 上海话 / 苏州话 | `05_shanghai.md` / `20_suzhou.md` |
| "东北那嘎达" | 东北话 | `04_dongbei.md` |
| "中原地区" | 河南话 | `06_henan.md` |
| "西北地区" | 陕西话 | `07_shaanxi.md` |
| "齐鲁大地" | 山东话 | `09_shandong.md` |
| "天津卫"、"津门" | 天津话 | `10_tianjin.md` |
| "闽南"、"厦漳泉" | 闽南语 | `11_minnan.md` |

### Level 3 — 多方言处理

当用户要求"全部方言"或同时提到多个方言时，逐一加载对应词元文件。

## 转换工作流

### Step 0: 意图解析与词元加载

1. **解析目标方言**：分析用户自然语言，按匹配系统定位方言组及具体分支
2. **加载词元文件**：从 `references/dialects/` 加载对应 `.md` 文件
3. **确认方言谱系**：判定官话系 vs 非官话系，分流转换策略
4. **判定转换深度**：默认增强层；用户指定"地道"/"基础"时按指定执行

### Step 1: 分层转换 (Layered Conversion)

#### Layer 1 — 基础层（词汇替换）
- 只替换标志性高频词汇：疑问词、人称代词、否定词、程度副词
- 不修改句式和语序
- 适合：AI 辅助理解、轻度本地化

#### Layer 2 — 增强层（词汇 + 语气词 + 句式调整）⭐ 默认
- 完整词汇替换（包括动词、形容词、俚语）
- 密集添加方言特色语气词（每句至少 1-2 个）
- 应用方言特有句式
- 应用方言体标记（完成体、进行体、经历体）
- 适合：方言对白创作、台词改写

#### Layer 3 — 地道层（全方言沉浸）
- 增强层的全部基础上
- 大量使用方言俚语、习语、熟语
- 加入轻度粗口（使用词典中的俚语·粗/俚语·贬条目）
- 调整语音层用字选择
- 适合：方言段子、喜剧脚本、模仿秀

### Step 2: 音韵规则检查

转换南方非官话方言时必做：
1. 入声字处理（-p/-t/-k 或 -ʔ 韵尾对应）
2. 浊声母保留（吴语/湘语）
3. 连读变调（参考 `00_appendix.md` 声调对照表）
4. 文白异读（口语层用白读，书面层用文读）

### Step 3: 质量检查

- [ ] 标志性词汇是否全部替换
- [ ] 语气词密度 ≥1/句
- [ ] 否定形式是否正确方言化
- [ ] 体标记是否调整
- [ ] 程度副词是否方言化
- [ ] 句式是否符合方言语法
- [ ] 无普通话残留
- [ ] 整体有方言味

### Step 4: 输出格式（VoxCPM Control Instruction + Target Text）

每次转换完成后，输出两个核心部分：

1. **Target Text** — 方言对白文本（直接送入 VoxCPM 的 text 参数）
2. **Control Instruction** — 语音生成控制指令（括号包裹的自然语言描述，置于 text 最前面）

#### 输出模板

```
【目标方言】四川话·成渝片（增强层）

【原文】
{原始普通话文本}

【Target Text — 方言目标文本】
{方言转换结果}

【词汇注释】（按需输出）
爪子 = 什么 ； 硬是 = 真的很 ； 要得 = 可以

---

> **🔊 VoxCPM Control Instruction**
>
> **Control Instruction**: {控制指令}
> **Target Text**: {方言目标文本}
> **完整输入**: ({控制指令}){方言目标文本}
> **推荐参数**: cfg_value=2.0, inference_timesteps=10, seed=42
```

#### 输出示例

```
【目标方言】四川话·成渝片（增强层）

【原文】
你在干什么？这个东西很好吃。你不知道吗？别骗我了。

【Target Text — 方言目标文本】
你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。

【词汇注释】
爪子 = 什么 ； 硬是 = 真的很 ； 日弄 = 骗/忽悠

---

> **🔊 VoxCPM Control Instruction**
>
> **Control Instruction**: A middle-aged Sichuan male, relaxed and lazy tone, slightly slow pace, with local Chengdu accent, trailing particles like "o" and "sa"
> **Target Text**: 你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
> **完整输入**: (A middle-aged Sichuan male, relaxed and lazy tone, slightly slow pace, with local Chengdu accent, trailing particles like "o" and "sa")你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。
> **推荐参数**: cfg_value=2.0, inference_timesteps=10, seed=42
```

### Control Instruction 生成规则

控制指令必须包含以下要素，以英文自然语言书写（VoxCPM 官方示例格式），用括号 `()` 包裹：

| 要素 | 说明 | 示例 |
|------|------|------|
| **性别** | 根据对白内容推断或默认 | male / female |
| **年龄** | 根据角色设定推断 | young / middle-aged / elderly |
| **方言口音** | 方言名称 + 口音特征 | Sichuan accent, with trailing particles |
| **语速** | 结合内容情绪 | slow / moderate / fast / rapid |
| **情绪/语气** | 从对白内容提取 | relaxed / excited / angry / sad / humorous |
| **嗓音特征** | 方言特色声音描述 | slightly raspy, trailing tone |

#### 各方言 Control Instruction 默认参考

| 方言 | 默认 Control Instruction |
|------|--------------------------|
| **四川话** | `A middle-aged Sichuan male, relaxed and lazy tone, slightly slow pace, with Chengdu accent, trailing particles like "o" and "sa"` |
| **粤语** | `A middle-aged Cantonese male, confident and energetic tone, moderate pace, with Guangzhou accent, short and punchy delivery` |
| **吴语（上海话）** | `A young Shanghai female, gentle and soft voice, moderate pace, with Wu dialect accent, melodic rising tones` |
| **东北话** | `A middle-aged Northeastern male, loud and bold voice, fast pace, with Dongbei accent, hearty and direct delivery` |
| **河南话** | `A middle-aged Henan male, steady and grounded tone, moderate pace, with Central Plains accent, nasal quality` |
| **陕西话** | `A middle-aged Shaanxi male, deep and resonant voice, slow pace, with Guanzhong accent, heavy nasal tones` |
| **山东话** | `A middle-aged Shandong male, robust and straightforward voice, moderate pace, with Ji-Lu accent, bold delivery` |
| **天津话** | `A middle-aged Tianjin male, witty and humorous tone, moderate pace, with Tianjin accent, playful rising intonation` |
| **闽南话** | `A middle-aged Minnan male, warm and friendly voice, slow pace, with Southern Fujian accent, soft trailing tones` |

> 💡 当对白中有多个角色时，为每个角色分别生成 Control Instruction，用分隔线 `---` 隔开。

#### 多角色输出示例

```
【目标方言】粤语·广府片（增强层）

【原文】
老板，这个多少钱？能不能便宜点？
便宜点嘛，我经常来买嘢的。

【Target Text — 方言目标文本】
老板，呢个几多钱啊？可唔可以平啲啊？
平啲啦，我成日嚟买嘢㗎。

---

> **🔊 VoxCPM Control Instruction（角色 1 — 顾客）**
>
> **Control Instruction**: A young Cantonese female, casual and friendly tone, moderate pace, with Guangzhou accent
> **Target Text**: 老板，呢个几多钱啊？可唔可以平啲啊？
> **完整输入**: (A young Cantonese female, casual and friendly tone, moderate pace, with Guangzhou accent)老板，呢个几多钱啊？可唔可以平啲啊？

> **🔊 VoxCPM Control Instruction（角色 2 — 老板）**
>
> **Control Instruction**: A middle-aged Cantonese male, warm and businesslike tone, moderate pace, with Guangzhou accent
> **Target Text**: 平啲啦，我成日嚟买嘢㗎。
> **完整输入**: (A middle-aged Cantonese male, warm and businesslike tone, moderate pace, with Guangzhou accent)平啲啦，我成日嚟买嘢㗎。
```

## 重口音原则

1. **标志性词汇强制替换**：疑问词、人称代词、否定词、程度副词必须替换
2. **语气词密度 ≥1/句**：语气词是方言"味道"的主要载体
3. **程度副词加重**：优先使用最重口版本
4. **俚语/粗口适度**：地道层默认使用，增强层酌情，基础层不使用
5. **句式口语化**：去书面化
6. **避免直译感**：宁过度替换不留普通话残留

## Resources

### references/dialects/
- `INDEX.md` — 方言文件索引
- `00_appendix.md` — 声调对照表、谱系树、类型学矩阵
- `02_sichuan.md` — 四川话（西南官话·成渝片）
- `03_yueyu.md` — 粤语（粤语·广府片）
- `04_dongbei.md` — 东北话（东北官话）
- `05_shanghai.md` — 上海话（吴语·太湖片）
- `06_henan.md` — 河南话（中原官话·郑开片）
- `07_shaanxi.md` — 陕西话（中原官话·关中片）
- `09_shandong.md` — 山东话（冀鲁/胶辽官话）
- `10_tianjin.md` — 天津话（冀鲁官话·天津片）
- `11_minnan.md` — 闽南语（闽语·闽南片）
- `15_yunnan.md` ~ `25_luoyang.md` — 地方分支词元文件

### references/
- `dialect_dictionary.md` — 合并版完整词典（向下兼容）

### outputs/model_formats/
- 9 大方言 × VoxCPM 格式 = 9 个输出文件
- 每个文件包含 Control Instruction + Target Text 完整示例

使用方式：Skill 自动根据用户意图加载所需方言文件，用户无需关心底层路径。
