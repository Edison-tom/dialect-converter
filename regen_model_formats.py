#!/usr/bin/env python3
"""
重新生成所有 TTS 模型适配输出文件
从 references/dialects/ 读取词条，生成 4 种格式：
  1. seed_audio.txt  - Seed Audio 1.0 角色脚本
  2. minimax_2.8.json - MiniMax 2.8 HD JSON
  3. eleven_v3.txt   - Eleven v3 情绪标签
  4. mureka_v8.json  - Mureka v8 结构化歌词
"""

import os
import re
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIALECTS_DIR = os.path.join(BASE_DIR, "references", "dialects")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "model_formats")

# 方言名映射：文件名 -> 显示名
DIALECT_NAMES = {
    "01_beijing": "北京话",
    "02_sichuan": "四川",
    "03_yueyu": "粤语",
    "04_dongbei": "东北",
    "05_shanghai": "上海话",
    "06_henan": "河南话",
    "07_shaanxi": "陕西话",
    "08_hunan": "湖南",
    "09_shandong": "山东话",
    "10_tianjin": "天津话",
    "11_minnan": "闽南语",
    "12_kejia": "客家话",
    "13_ganyu": "赣语",
    "14_jinyu": "晋语",
    "15_yunnan": "云南话",
    "16_hubei": "湖北",
    "17_guiyang": "贵阳话",
    "18_xuzhou": "徐州话",
    "19_zigong": "自贡话",
    "20_suzhou": "苏州话",
    "21_chengdu": "成都话",
    "22_chongqing": "重庆话",
    "23_jinan": "济南话",
    "24_qingdao": "青岛话",
    "25_luoyang": "洛阳话",
    "26_nanjing": "南京话",
    "27_wenzhou": "温州话",
    "28_fuzhou": "福州话",
    "29_lanzhou": "兰州话",
}

# 场景描述
DIALECT_SCENES = {
    "01_beijing": "北京胡同口，日常市井氛围",
    "02_sichuan": "成都茶馆，悠闲龙门阵氛围",
    "03_yueyu": "广州茶楼，市井生活氛围",
    "04_dongbei": "东北炕头，家常唠嗑氛围",
    "05_shanghai": "上海弄堂，石库门生活氛围",
    "06_henan": "郑州街头，中原市井氛围",
    "07_shaanxi": "西安城墙根，关中生活氛围",
    "08_hunan": "长沙街头，火辣市井氛围",
    "09_shandong": "济南泉边，齐鲁市井氛围",
    "10_tianjin": "天津茶馆，津味市井氛围",
    "11_minnan": "厦门骑楼，闽南生活氛围",
    "12_kejia": "梅县围屋，客家生活氛围",
    "13_ganyu": "南昌街头，赣鄱市井氛围",
    "14_jinyu": "太原老街，晋中市井氛围",
    "15_yunnan": "昆明翠湖，滇云生活氛围",
    "16_hubei": "武汉江边，楚天市井氛围",
    "17_guiyang": "贵阳甲秀楼，黔中市井氛围",
    "18_xuzhou": "徐州古彭，彭城市井氛围",
    "19_zigong": "自贡盐都，川南生活氛围",
    "20_suzhou": "苏州平江路，吴侬软语氛围",
    "21_chengdu": "成都宽窄巷子，慢生活氛围",
    "22_chongqing": "重庆山城步道，码头文化氛围",
    "23_jinan": "济南大明湖，泉城市井氛围",
    "24_qingdao": "青岛栈桥，海滨市井氛围",
    "25_luoyang": "洛阳老城，牡丹花都氛围",
    "26_nanjing": "南京秦淮河，金陵市井氛围",
    "27_wenzhou": "温州五马街，瓯越市井氛围",
    "28_fuzhou": "福州三坊七巷，闽都生活氛围",
    "29_lanzhou": "兰州黄河边，金城市井氛围",
}

# 角色设定
CHARACTERS = [
    ("老张", "慢悠悠，老派口音", "casual"),
    ("小李", "语气活泼，年轻口音", "excited"),
    ("老王", "语气沉稳，讲述口吻", "serious"),
    ("阿妹", "语气俏皮，女孩子口音", "curious"),
]

# 情绪标签轮换
EMOTION_TAGS = ["casual", "curious", "excited", "serious", "nervous", "happy", "calm", "surprised"]

# 音乐风格
MUSIC_STYLES = {
    "01_beijing": "北京方言民谣，男声，京片子，中速，三弦+电子鼓，胡同氛围",
    "02_sichuan": "四川方言民谣，男声，川味，中速，竹笛+电子鼓，茶馆氛围",
    "03_yueyu": "粤语流行，男女对唱，广府味，中速，吉他+电子合成器，茶楼氛围",
    "04_dongbei": "东北方言民谣，男声，东北味，中速，手风琴+架子鼓，炕头氛围",
    "05_shanghai": "上海方言民谣，女声，吴侬软语，中速，钢琴+电子合成器，弄堂氛围",
    "06_henan": "河南方言民谣，男声，中原味，中速，二胡+电子鼓，街头氛围",
    "07_shaanxi": "陕西方言民谣，男声，关中味，中速，板胡+电子鼓，城墙氛围",
    "08_hunan": "湖南方言民谣，男女对唱，湘味，中速，笛子+电子鼓，火辣氛围",
    "09_shandong": "山东方言民谣，男声，齐鲁味，中速，唢呐+电子鼓，泉边氛围",
    "10_tianjin": "天津方言民谣，男声，津味，中速，三弦+电子鼓，茶馆氛围",
    "11_minnan": "闽南语民谣，男女对唱，闽南味，中速，南音+电子鼓，骑楼氛围",
    "12_kejia": "客家话民谣，男女对唱，客家味，中速，古筝+电子鼓，围屋氛围",
    "13_ganyu": "赣语民谣，男声，赣味，中速，笛子+电子鼓，街头氛围",
    "14_jinyu": "晋语民谣，男声，晋味，中速，板胡+电子鼓，老街氛围",
    "15_yunnan": "云南方言民谣，男女对唱，滇味，中速，葫芦丝+电子鼓，翠湖氛围",
    "16_hubei": "湖北方言民谣，男声，楚味，中速，笛子+电子鼓，江边氛围",
    "17_guiyang": "贵阳方言民谣，男声，黔味，中速，芦笙+电子鼓，甲秀楼氛围",
    "18_xuzhou": "徐州方言民谣，男声，彭城味，中速，笛子+电子鼓，古彭氛围",
    "19_zigong": "自贡方言民谣，男声，川南味，中速，竹笛+电子鼓，盐都氛围",
    "20_suzhou": "苏州方言民谣，女声，吴侬软语，中速，琵琶+电子合成器，平江路氛围",
    "21_chengdu": "成都方言民谣，男女对唱，川味，中速，竹笛+电子鼓，宽窄巷子氛围",
    "22_chongqing": "重庆方言民谣，男声，码头味，快节奏，号子+电子鼓，山城氛围",
    "23_jinan": "济南方言民谣，男声，泉城味，中速，笛子+电子鼓，大明湖氛围",
    "24_qingdao": "青岛方言民谣，男女对唱，海滨味，中速，手风琴+电子鼓，栈桥氛围",
    "25_luoyang": "洛阳方言民谣，男声，牡丹味，中速，二胡+电子鼓，老城氛围",
    "26_nanjing": "南京方言民谣，男女对唱，金陵味，中速，古筝+电子鼓，秦淮氛围",
    "27_wenzhou": "温州方言民谣，男声，瓯越味，中速，笛子+电子鼓，五马街氛围",
    "28_fuzhou": "福州方言民谣，男女对唱，闽都味，中速，古筝+电子鼓，三坊七巷氛围",
    "29_lanzhou": "兰州方言民谣，男声，金城味，中速，板胡+电子鼓，黄河边氛围",
}


def extract_entries(filepath):
    """从方言参考文件中提取所有词条"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('|') and not line.startswith('|---') and '普通话' not in line and '功用' not in line and line.count('|') >= 4:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                standard = parts[1]
                dialect = parts[2]
                category = parts[3] if len(parts) > 3 else ""
                if standard and dialect and standard != '---':
                    entries.append((standard, dialect, category))
    return entries


def gen_seed_audio(dialect_name, dialect_key, entries):
    """生成 Seed Audio 1.0 格式"""
    scene = DIALECT_SCENES.get(dialect_key, f"{dialect_name}日常氛围")
    lines = [f"【场景：{scene}】\n"]

    char_idx = 0
    for i, (standard, dialect, cat) in enumerate(entries):
        char = CHARACTERS[char_idx % len(CHARACTERS)]
        char_idx += 1
        lines.append(f"【角色{char[0][-1]} - {char[0]}，{char[1]}】")
        lines.append(dialect)
        lines.append("")

    return "\n".join(lines)


def gen_minimax(dialect_name, dialect_key, entries):
    """生成 MiniMax 2.8 HD JSON 格式"""
    # 取前500条作为文本（避免过长）
    sample = entries[:500]
    words = [d for _, d, _ in sample]
    text = "(breath) ".join(words)

    result = {
        "model": "speech-2.8-hd",
        "text": text,
        "language_boost": "zh",
        "pronunciation_dict": {
            "tone": []
        },
        "voice_setting": {
            "voice_id": "YOUR_VOICE_ID",
            "speed": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "format": "mp3"
        }
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def gen_eleven_v3(dialect_name, dialect_key, entries):
    """生成 Eleven v3 情绪标签格式"""
    sample = entries[:2000]
    lines = []
    for i, (standard, dialect, cat) in enumerate(sample):
        tag = EMOTION_TAGS[i % len(EMOTION_TAGS)]
        lines.append(f"[{tag}] {dialect}")
        lines.append("")
    return "\n".join(lines)


def gen_mureka_v8(dialect_name, dialect_key, entries):
    """生成 Mureka v8 结构化歌词格式"""
    sample = entries[:500]
    # 分段
    verse_words = [d for _, d, _ in sample[:100]]
    chorus_words = [d for _, d, _ in sample[100:200]] if len(sample) > 100 else []

    verse_text = "\n".join(verse_words)
    chorus_text = "\n".join(chorus_words) if chorus_words else f"（{dialect_name}方言）"

    music_style = MUSIC_STYLES.get(dialect_key, f"{dialect_name}方言民谣")

    result = {
        "model": "mureka-8",
        "lyrics": f"[Verse]\n{verse_text}\n\n[Chorus]\n{chorus_text}\n\n[Outro]\n走喽走喽",
        "prompt": music_style,
        "n": 2
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    dialect_files = sorted(glob.glob(os.path.join(DIALECTS_DIR, "[0-9][0-9]_*.md")))

    total_generated = 0

    for filepath in dialect_files:
        filename = os.path.basename(filepath).replace(".md", "")

        # 跳过附录
        if filename.startswith("00_"):
            continue

        dialect_name = DIALECT_NAMES.get(filename, filename)
        entries = extract_entries(filepath)

        if not entries:
            print(f"  跳过 {filename}: 无词条")
            continue

        # 生成4种格式
        formats = {
            "seed_audio.txt": gen_seed_audio(dialect_name, filename, entries),
            "minimax_2.8.json": gen_minimax(dialect_name, filename, entries),
            "eleven_v3.txt": gen_eleven_v3(dialect_name, filename, entries),
            "mureka_v8.json": gen_mureka_v8(dialect_name, filename, entries),
        }

        for ext, content in formats.items():
            outpath = os.path.join(OUTPUT_DIR, f"{dialect_name}_{ext}")
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)

        total_generated += 4
        print(f"  {dialect_name}: {len(entries)} 词条 -> 4 格式文件")

    print(f"\n总共生成 {total_generated} 个文件")


if __name__ == "__main__":
    main()
