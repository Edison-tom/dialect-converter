#!/usr/bin/env python3
"""
regen_voxcpm_formats.py — 为 29 种方言生成 VoxCPM 格式适配文件
输出: Control Instruction + Target Text

VoxCPM 原生方言（9 大方言组 21 变体）：直接生成 VoxCPM 调用示例
备选模型方言（8 种）：生成格式文件并标注推荐备选 TTS 模型
"""

import os
import re

DIALECTS_DIR = os.path.join(os.path.dirname(__file__), "references", "dialects")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "model_formats")

# 17 种主要方言的 VoxCPM 适配配置（9 大 VoxCPM 原生 + 8 种备选模型）
DIALECT_CONFIG = {
    # ── VoxCPM 原生方言 ──
    "02_sichuan": {
        "name": "四川话",
        "dialect_group": "四川话",
        "subgroup": "成渝片",
        "phylogeny": "西南官话·成渝片",
        "output_file": "四川_voxcpm.txt",
        "control_instruction": "四川方言，中年男性，慵懒语气，语速偏慢",
        "sample_text": "你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。",
        "translation_notes": "爪子=什么；硬是=真的很；日弄=骗/忽悠；要得=可以；巴适=舒服/好",
        "alt_models": None,
    },
    "03_yueyu": {
        "name": "粤语",
        "dialect_group": "粤语",
        "subgroup": "广府片",
        "phylogeny": "粤语·广府片",
        "output_file": "粤语_voxcpm.txt",
        "control_instruction": "粤语，中年男性，自信语气，正常语速",
        "sample_text": "你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。",
        "translation_notes": "乜嘢=什么；好鬼=非常；唔=不；咩=吗；呃=骗",
        "alt_models": None,
    },
    "05_shanghai": {
        "name": "上海话",
        "dialect_group": "吴语",
        "subgroup": "太湖片",
        "phylogeny": "吴语·太湖片",
        "output_file": "上海_voxcpm.txt",
        "control_instruction": "上海话，年轻女性，温柔语气，正常语速",
        "sample_text": "侬勒做啥？搿只物事蛮好切额。侬勿晓得啊？覅骗吾了。",
        "translation_notes": "侬=你；勒=在；搿=这；物事=东西；蛮=很；切=吃；覅=不要",
        "alt_models": None,
    },
    "04_dongbei": {
        "name": "东北话",
        "dialect_group": "东北话",
        "subgroup": "",
        "phylogeny": "东北官话",
        "output_file": "东北_voxcpm.txt",
        "control_instruction": "东北话，中年男性，洪亮嗓音，语速较快",
        "sample_text": "你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。",
        "translation_notes": "嘎哈=干什么；玩意儿=东西；嘎嘎=非常；忽悠=骗",
        "alt_models": None,
    },
    "06_henan": {
        "name": "河南话",
        "dialect_group": "河南话",
        "subgroup": "郑开片",
        "phylogeny": "中原官话·郑开片",
        "output_file": "河南_voxcpm.txt",
        "control_instruction": "河南话，中年男性，沉稳语气，正常语速",
        "sample_text": "你弄啥嘞？这东西可中可好吃。你不知情哩？白搁这儿骗我。",
        "translation_notes": "弄啥=干什么；中=行/好；可=很；白=别；搁=在",
        "alt_models": None,
    },
    "07_shaanxi": {
        "name": "陕西话",
        "dialect_group": "陕西话",
        "subgroup": "关中片",
        "phylogeny": "中原官话·关中片",
        "output_file": "陕西_voxcpm.txt",
        "control_instruction": "陕西话，中年男性，低沉嗓音，语速偏慢",
        "sample_text": "你弄啥哩？这东西嫽滴很。你不得知道？包哄我。",
        "translation_notes": "弄啥=干什么；嫽滴很=很好；不得=不；包=别；哄=骗",
        "alt_models": None,
    },
    "09_shandong": {
        "name": "山东话",
        "dialect_group": "山东话",
        "subgroup": "",
        "phylogeny": "冀鲁/胶辽官话",
        "output_file": "山东_voxcpm.txt",
        "control_instruction": "山东话，中年男性，豪爽语气，正常语速",
        "sample_text": "你干啥呢？这玩意儿杠好吃。你不知道啊？别忽悠俺了。",
        "translation_notes": "干啥=干什么；杠=非常；俺=我/我们；忽悠=骗",
        "alt_models": None,
    },
    "10_tianjin": {
        "name": "天津话",
        "dialect_group": "天津话",
        "subgroup": "天津片",
        "phylogeny": "冀鲁官话·天津片",
        "output_file": "天津_voxcpm.txt",
        "control_instruction": "天津话，中年男性，幽默语气，正常语速",
        "sample_text": "你干嘛呢？介玩意儿倍儿好吃。你不儿道啊？甭忽悠我了。",
        "translation_notes": "干嘛=干什么；介=这；倍儿=非常；不儿道=不知道；甭=别",
        "alt_models": None,
    },
    "11_minnan": {
        "name": "闽南话",
        "dialect_group": "闽南话",
        "subgroup": "闽南片",
        "phylogeny": "闽语·闽南片",
        "output_file": "闽南_voxcpm.txt",
        "control_instruction": "闽南话，中年男性，温和语气，语速偏慢",
        "sample_text": "汝咧做啥物？这物事诚好食。汝毋知影？莫骗我。",
        "translation_notes": "汝=你；啥物=什么；物事=东西；诚=很；毋=不；莫=别",
        "alt_models": None,
    },
    # ── 备选模型方言（VoxCPM 不支持） ──
    "01_beijing": {
        "name": "北京话",
        "dialect_group": "北京话",
        "subgroup": "京师片",
        "phylogeny": "北京官话·京师片",
        "output_file": "北京话_voxcpm.txt",
        "control_instruction": "北京话，中年男性，随和语气，正常语速",
        "sample_text": "你干嘛呢？这玩意儿倍儿好吃。您不知道啊？甭蒙我了。",
        "translation_notes": "干嘛=干什么；玩意儿=东西；倍儿=非常；甭=别；蒙=骗",
        "alt_models": "Seed Audio / MiniMax",
    },
    "08_hunan": {
        "name": "湖南话",
        "dialect_group": "湖南话",
        "subgroup": "长益片",
        "phylogeny": "湘语·长益片",
        "output_file": "湖南话_voxcpm.txt",
        "control_instruction": "湖南话，中年男性，爽朗语气，语速较快",
        "sample_text": "你搞么子咯？咯只东西好恰得很。你不晓得啵？莫骗我咧。",
        "translation_notes": "么子=什么；咯=这；恰=吃；啵=吗；咧=语气词",
        "alt_models": "MiniMax / ElevenLabs",
    },
    "12_kejia": {
        "name": "客家话",
        "dialect_group": "客家话",
        "subgroup": "粤台片",
        "phylogeny": "客语·粤台片",
        "output_file": "客家话_voxcpm.txt",
        "control_instruction": "客家话，中年男性，温和语气，正常语速",
        "sample_text": "你做么个？这东西当好食。你毋知？莫骗捱。",
        "translation_notes": "么个=什么；当=很；食=吃；毋=不；捱=我",
        "alt_models": "Seed Audio / Mureka",
    },
    "13_ganyu": {
        "name": "赣语",
        "dialect_group": "赣语",
        "subgroup": "昌靖片",
        "phylogeny": "赣语·昌靖片",
        "output_file": "赣语_voxcpm.txt",
        "control_instruction": "赣语，中年男性，沉稳语气，正常语速",
        "sample_text": "你做么事？咯只东西蛮好喫。你不晓得？莫骗我。",
        "translation_notes": "么事=什么；咯=这；蛮=很；喫=吃；莫=别",
        "alt_models": "MiniMax / Mureka",
    },
    "14_jinyu": {
        "name": "晋语",
        "dialect_group": "晋语",
        "subgroup": "并州片",
        "phylogeny": "晋语·并州片",
        "output_file": "晋语_voxcpm.txt",
        "control_instruction": "晋语，中年男性，低沉嗓音，语速偏慢",
        "sample_text": "你做啥咧？这东西可好吃了。你不知道？别哄我。",
        "translation_notes": "做啥=干什么；咧=语气词；可=很；哄=骗",
        "alt_models": "Seed Audio / MiniMax",
    },
    "26_nanjing": {
        "name": "南京话",
        "dialect_group": "南京话",
        "subgroup": "洪巢片",
        "phylogeny": "江淮官话·洪巢片",
        "output_file": "南京话_voxcpm.txt",
        "control_instruction": "南京话，中年男性，随和语气，正常语速",
        "sample_text": "你干么事啊？这东西蛮好吃滴。你不晓得啊？表骗我。",
        "translation_notes": "么事=什么；蛮=很；滴=语气词；表=别",
        "alt_models": "MiniMax / ElevenLabs",
    },
    "28_fuzhou": {
        "name": "福州话",
        "dialect_group": "福州话",
        "subgroup": "闽东片",
        "phylogeny": "闽语·闽东片",
        "output_file": "福州话_voxcpm.txt",
        "control_instruction": "福州话，中年男性，温和语气，语速偏慢",
        "sample_text": "汝做什乇？这物件野好食。汝伓知？莫骗我。",
        "translation_notes": "汝=你；什乇=什么；物件=东西；野=很；伓=不；莫=别",
        "alt_models": "Seed Audio / Mureka",
    },
    "29_lanzhou": {
        "name": "兰州话",
        "dialect_group": "兰州话",
        "subgroup": "金城片",
        "phylogeny": "兰银官话·金城片",
        "output_file": "兰州话_voxcpm.txt",
        "control_instruction": "兰州话，中年男性，豪爽语气，正常语速",
        "sample_text": "你做啥呢？这东西满好滴。你不知道？白骗我。",
        "translation_notes": "做啥=干什么；满=很；滴=语气词；白=别",
        "alt_models": "MiniMax / Seed Audio",
    },
}

# 地方分支配置（VoxCPM 原生）
BRANCH_CONFIG = {
    "15_yunnan": ("四川话", "云南话", "西南官话·滇中片", "云南话_voxcpm.txt"),
    "16_hubei": ("四川话", "湖北话", "西南官话·武天片", "湖北话_voxcpm.txt"),
    "17_guiyang": ("四川话", "贵阳话", "西南官话·黔中片", "贵阳话_voxcpm.txt"),
    "18_xuzhou": ("河南话", "徐州话", "中原官话·徐淮片", "徐州话_voxcpm.txt"),
    "19_zigong": ("四川话", "自贡话", "西南官话·仁富片", "自贡话_voxcpm.txt"),
    "20_suzhou": ("吴语", "苏州话", "吴语·太湖片", "苏州话_voxcpm.txt"),
    "21_chengdu": ("四川话", "成都话", "西南官话·成渝片", "成都话_voxcpm.txt"),
    "22_chongqing": ("四川话", "重庆话", "西南官话·成渝片", "重庆话_voxcpm.txt"),
    "23_jinan": ("山东话", "济南话", "冀鲁官话", "济南话_voxcpm.txt"),
    "24_qingdao": ("山东话", "青岛话", "胶辽官话", "青岛话_voxcpm.txt"),
    "25_luoyang": ("河南话", "洛阳话", "中原官话·洛嵩片", "洛阳话_voxcpm.txt"),
    "27_wenzhou": ("吴语", "温州话", "吴语·瓯江片", "温州话_voxcpm.txt"),
}


def parse_dialect_file(filepath):
    """Parse a dialect .md file and extract first few entries as samples."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    lines = content.split('\n')
    for line in lines:
        if re.match(r'^\| [^|]+\| [^|]+\|', line) and '普通话' not in line and not line.startswith('|---'):
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                entries.append(parts)

    return entries


def generate_main_dialect_file(config, entries, dialect_key):
    """Generate VoxCPM format file for a main dialect."""
    ci = config["control_instruction"]
    sample = config["sample_text"]
    notes = config["translation_notes"]
    alt = config.get("alt_models")

    showcase = entries[:5] if entries else []

    if alt:
        model_note = f"> 生成模型：VoxCPM2 (openbmb/VoxCPM2) — VoxCPM 暂不支持此方言，推荐备选模型：{alt}"
        alt_section = f"""
## ⚠️ 备选模型说明

> VoxCPM 暂不支持 **{config['name']}** 的原生合成。推荐使用以下备选 TTS 模型：
>
> **{alt}**
>
> 详见 `TTS_MODEL_GUIDE.md` 第二部分。Control Instruction + Target Text 格式同样适用于备选模型。

"""
    else:
        model_note = "> 生成模型：VoxCPM2 (openbmb/VoxCPM2)"
        alt_section = ""

    content = f"""# {config['name']} — VoxCPM 适配文件

> 方言组：{config['dialect_group']} | 谱系：{config['phylogeny']}
{model_note}
> 格式：Control Instruction + Target Text

---
{alt_section}
## 默认 Control Instruction

```
{ci}
```

## 完整输入示例

```
({ci}){sample}
```

## Python 调用示例

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

wav = model.generate(
    text="({ci}){sample}",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("{config['output_file'].replace('.txt', '.wav')}", wav, model.tts_model.sample_rate)
```

## 词汇注释

{notes}

## CLI 调用

```bash
voxcpm design \\
  --text "({ci}){sample}" \\
  --output {config['output_file'].replace('.txt', '.wav')}
```

## 情绪变体示例

### 轻松日常
```
({ci.split('，')[0]}，{ci.split('，')[1]}，轻松语气，语速偏慢){sample}
```

### 激动语气
```
({ci.split('，')[0]}，{ci.split('，')[1]}，激动语气，语速较快){sample}
```

### 悲伤低沉
```
({ci.split('，')[0]}，{ci.split('，')[1]}，悲伤语气，语速偏慢){sample}
```
"""

    if showcase:
        content += "\n## 代表性词条（前 5 条）\n\n"
        content += "| 普通话 | 方言 |\n|--------|------|\n"
        for e in showcase:
            if len(e) >= 2:
                content += f"| {e[0]} | {e[1]} |\n"

    content += f"\n---\n\n> 完整词条见 `references/dialects/{dialect_key}.md`\n"

    return content


def generate_branch_file(filepath, branch_name, parent_group, phylogeny, output_file):
    """Generate VoxCPM format file for a branch dialect."""
    entries = parse_dialect_file(filepath)

    if not entries:
        return f"# {branch_name} — VoxCPM 适配文件\n\n> 无可用词条\n"

    parent_ci = DIALECT_CONFIG.get(
        {"四川话": "02_sichuan", "吴语": "05_shanghai", "河南话": "06_henan", "山东话": "09_shandong"}.get(parent_group, "02_sichuan"),
        {}
    ).get("control_instruction", "浓重口音，正常语速")

    sample_entries = entries[:5]
    sample_text = sample_entries[0][1] if sample_entries else "方言示例文本"

    content = f"""# {branch_name} — VoxCPM 适配文件

> 方言组：{parent_group}（分支） | 谱系：{phylogeny}
> 生成模型：VoxCPM2 (openbmb/VoxCPM2)
> 格式：Control Instruction + Target Text

---

## 默认 Control Instruction

```
{parent_ci}
```

## 完整输入示例

```
({parent_ci}){sample_text}
```

## Python 调用示例

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

wav = model.generate(
    text="({parent_ci}){sample_text}",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("{output_file.replace('.txt', '.wav')}", wav, model.tts_model.sample_rate)
```

## 代表性词条（前 5 条）

| 普通话 | 方言 |
|--------|------|
"""
    for e in sample_entries:
        if len(e) >= 2:
            content += f"| {e[0]} | {e[1]} |\n"

    filename = os.path.basename(filepath)
    content += f"\n---\n\n> 完整词条见 `references/dialects/{filename}`\n"

    return content


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generated = []

    # Generate 17 main dialect files (9 VoxCPM + 8 alternative model)
    for key, config in DIALECT_CONFIG.items():
        filepath = os.path.join(DIALECTS_DIR, f"{key}.md")
        if not os.path.exists(filepath):
            print(f"  [SKIP] {key}: file not found")
            continue

        entries = parse_dialect_file(filepath)
        content = generate_main_dialect_file(config, entries, key)

        output_path = os.path.join(OUTPUT_DIR, config["output_file"])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        generated.append(config["output_file"])
        status = "VoxCPM" if not config.get("alt_models") else f"alt: {config['alt_models']}"
        print(f"  [OK] {config['name']}: {len(entries)} entries ({status}) -> {config['output_file']}")

    # Generate branch dialect files
    for key, (parent_group, branch_name, phylogeny, output_file) in BRANCH_CONFIG.items():
        filepath = os.path.join(DIALECTS_DIR, f"{key}.md")
        if not os.path.exists(filepath):
            print(f"  [SKIP] {key}: file not found")
            continue

        content = generate_branch_file(filepath, branch_name, parent_group, phylogeny, output_file)

        output_path = os.path.join(OUTPUT_DIR, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        generated.append(output_file)
        print(f"  [OK] {branch_name} (branch) -> {output_file}")

    print(f"\n=== Done: {len(generated)} format files generated ===")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
