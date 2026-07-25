#!/usr/bin/env python3
"""
regen_voxcpm_formats.py — 为 9 大方言生成 VoxCPM 格式适配文件
输出: Control Instruction + Target Text
"""

import os
import re
import json

DIALECTS_DIR = os.path.join(os.path.dirname(__file__), "references", "dialects")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "model_formats")

# 9 大方言的 VoxCPM 适配配置
DIALECT_CONFIG = {
    "02_sichuan": {
        "name": "四川话",
        "dialect_group": "四川话",
        "subgroup": "成渝片",
        "phylogeny": "西南官话·成渝片",
        "output_file": "四川_voxcpm.txt",
        "control_instruction": "A middle-aged Sichuan male, relaxed and lazy tone, slightly slow pace, with Chengdu accent, trailing particles",
        "sample_text": "你在搞爪子？这个硬是好吃得很。你不晓得嗦？莫日弄老子哈。",
        "translation_notes": "爪子=什么；硬是=真的很；日弄=骗/忽悠；要得=可以；巴适=舒服/好",
    },
    "03_yueyu": {
        "name": "粤语",
        "dialect_group": "粤语",
        "subgroup": "广府片",
        "phylogeny": "粤语·广府片",
        "output_file": "粤语_voxcpm.txt",
        "control_instruction": 'A middle-aged Cantonese male, confident and energetic tone, moderate pace, with Guangzhou accent, short and punchy delivery',
        "sample_text": "你做紧乜嘢啊？呢个好鬼好食㗎。你唔知咩？唔好呃我啦。",
        "translation_notes": "乜嘢=什么；好鬼=非常；唔=不；咩=吗；呃=骗",
    },
    "05_shanghai": {
        "name": "上海话",
        "dialect_group": "吴语",
        "subgroup": "太湖片",
        "phylogeny": "吴语·太湖片",
        "output_file": "上海_voxcpm.txt",
        "control_instruction": 'A young Shanghai female, gentle and soft voice, moderate pace, with Wu dialect accent, melodic rising tones',
        "sample_text": "侬勒做啥？搿只物事蛮好切额。侬勿晓得啊？覅骗吾了。",
        "translation_notes": "侬=你；勒=在；搿=这；物事=东西；蛮=很；切=吃；覅=不要",
    },
    "04_dongbei": {
        "name": "东北话",
        "dialect_group": "东北话",
        "subgroup": "",
        "phylogeny": "东北官话",
        "output_file": "东北_voxcpm.txt",
        "control_instruction": 'A middle-aged Northeastern male, loud and bold voice, fast pace, with Dongbei accent, hearty and direct delivery',
        "sample_text": "你嘎哈呢？这玩意儿嘎嘎好吃。你不知道啊？别忽悠我了。",
        "translation_notes": "嘎哈=干什么；玩意儿=东西；嘎嘎=非常；忽悠=骗",
    },
    "06_henan": {
        "name": "河南话",
        "dialect_group": "河南话",
        "subgroup": "郑开片",
        "phylogeny": "中原官话·郑开片",
        "output_file": "河南_voxcpm.txt",
        "control_instruction": 'A middle-aged Henan male, steady and grounded tone, moderate pace, with Central Plains accent, nasal quality',
        "sample_text": "你弄啥嘞？这东西可中可好吃。你不知情哩？白搁这儿骗我。",
        "translation_notes": "弄啥=干什么；中=行/好；可=很；白=别；搁=在",
    },
    "07_shaanxi": {
        "name": "陕西话",
        "dialect_group": "陕西话",
        "subgroup": "关中片",
        "phylogeny": "中原官话·关中片",
        "output_file": "陕西_voxcpm.txt",
        "control_instruction": 'A middle-aged Shaanxi male, deep and resonant voice, slow pace, with Guanzhong accent, heavy nasal tones',
        "sample_text": "你弄啥哩？这东西嫽滴很。你不得知道？包哄我。",
        "translation_notes": "弄啥=干什么；嫽滴很=很好；不得=不；包=别；哄=骗",
    },
    "09_shandong": {
        "name": "山东话",
        "dialect_group": "山东话",
        "subgroup": "",
        "phylogeny": "冀鲁/胶辽官话",
        "output_file": "山东_voxcpm.txt",
        "control_instruction": 'A middle-aged Shandong male, robust and straightforward voice, moderate pace, with Ji-Lu accent, bold delivery',
        "sample_text": "你干啥呢？这玩意儿杠好吃。你不知道啊？别忽悠俺了。",
        "translation_notes": "干啥=干什么；杠=非常；俺=我/我们；忽悠=骗",
    },
    "10_tianjin": {
        "name": "天津话",
        "dialect_group": "天津话",
        "subgroup": "天津片",
        "phylogeny": "冀鲁官话·天津片",
        "output_file": "天津_voxcpm.txt",
        "control_instruction": 'A middle-aged Tianjin male, witty and humorous tone, moderate pace, with Tianjin accent, playful rising intonation',
        "sample_text": "你干嘛呢？介玩意儿倍儿好吃。你不儿道啊？甭忽悠我了。",
        "translation_notes": "干嘛=干什么；介=这；倍儿=非常；不儿道=不知道；甭=别",
    },
    "11_minnan": {
        "name": "闽南话",
        "dialect_group": "闽南话",
        "subgroup": "闽南片",
        "phylogeny": "闽语·闽南片",
        "output_file": "闽南_voxcpm.txt",
        "control_instruction": 'A middle-aged Minnan male, warm and friendly voice, slow pace, with Southern Fujian accent, soft trailing tones',
        "sample_text": "汝咧做啥物？这物事诚好食。汝毋知影？莫骗我。",
        "translation_notes": "汝=你；啥物=什么；物事=东西；诚=很；毋=不；莫=别",
    },
}

# 地方分支配置
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

    # Extract data rows from tables
    entries = []
    lines = content.split('\n')
    for line in lines:
        # Match table data rows: | 普通话 | 方言 | ... |
        if re.match(r'^\| [^|]+\| [^|]+\|', line) and '普通话' not in line and not line.startswith('|---'):
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                entries.append(parts)

    return entries


def generate_main_dialect_file(config, entries):
    """Generate VoxCPM format file for a main dialect."""
    ci = config["control_instruction"]
    sample = config["sample_text"]
    notes = config["translation_notes"]

    # Pick first 5 entries as vocabulary showcase
    showcase = entries[:5] if entries else []

    content = f"""# {config['name']} — VoxCPM 适配文件

> 方言组：{config['dialect_group']} | 谱系：{config['phylogeny']}
> 生成模型：VoxCPM2 (openbmb/VoxCPM2)
> 格式：Control Instruction + Target Text

---

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
({ci.replace('middle-aged', 'young')}, casual and relaxed tone){sample}
```

### 激动语气
```
({ci}, excited and loud tone, fast pace){sample}
```

### 慢速低沉
```
({ci}, slow and deep tone){sample}
```
"""

    # Add vocabulary showcase
    if showcase:
        content += "\n## 代表性词条（前 5 条）\n\n"
        content += "| 普通话 | 方言 |\n|--------|------|\n"
        for e in showcase:
            if len(e) >= 2:
                content += f"| {e[0]} | {e[1]} |\n"

    content += f"\n---\n\n> 完整词条见 `references/dialects/{list(DIALECT_CONFIG.keys())[list(DIALECT_CONFIG.values()).index(config)]}.md`\n"

    return content


def generate_branch_file(filepath, branch_name, parent_group, phylogeny, output_file):
    """Generate VoxCPM format file for a branch dialect."""
    entries = parse_dialect_file(filepath)

    if not entries:
        return f"# {branch_name} — VoxCPM 适配文件\n\n> 无可用词条\n"

    # Use parent group's control instruction as base
    parent_ci = DIALECT_CONFIG.get(
        {"四川话": "02_sichuan", "吴语": "05_shanghai", "河南话": "06_henan", "山东话": "09_shandong"}.get(parent_group, "02_sichuan"),
        {}
    ).get("control_instruction", "A middle-aged male, moderate pace, with local accent")

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

    # Generate 9 main dialect files
    for key, config in DIALECT_CONFIG.items():
        filepath = os.path.join(DIALECTS_DIR, f"{key}.md")
        if not os.path.exists(filepath):
            print(f"  ⚠ Skip {key}: file not found")
            continue

        entries = parse_dialect_file(filepath)
        content = generate_main_dialect_file(config, entries)

        output_path = os.path.join(OUTPUT_DIR, config["output_file"])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        generated.append(config["output_file"])
        print(f"  ✅ {config['name']}: {len(entries)} entries → {config['output_file']}")

    # Generate branch dialect files
    for key, (parent_group, branch_name, phylogeny, output_file) in BRANCH_CONFIG.items():
        filepath = os.path.join(DIALECTS_DIR, f"{key}.md")
        if not os.path.exists(filepath):
            print(f"  ⚠ Skip {key}: file not found")
            continue

        content = generate_branch_file(filepath, branch_name, parent_group, phylogeny, output_file)

        output_path = os.path.join(OUTPUT_DIR, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        generated.append(output_file)
        print(f"  ✅ {branch_name} (分支) → {output_file}")

    print(f"\n=== Done: {len(generated)} VoxCPM format files generated ===")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
