#!/usr/bin/env python3
"""
generate_qinghai.py — 生成青海话（河湟方言）词条文件 30_qinghai.md

以兰州话（29_lanzhou.md）的领域词库为模板：
- 第 1 列（普通话）保持不变
- 第 2 列（青海话词）按河湟方言特征词映射替换，未命中则保留普通话写法
- 追加「河湟方言特色词」分类，集中呈现青海话核心俚语

青海话（河湟方言）谱系：中原官话·秦陇片（陇中片）
主要方言点：湟源、乐都、湟中、西宁、平安、互助等河湟谷地
VoxCPM 暂不支持原生合成，推荐使用 Seed Audio / MiniMax / Mureka 备选模型。
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "references", "dialects", "29_lanzhou.md")
OUT = os.path.join(BASE, "references", "dialects", "30_qinghai.md")

# 普通话 -> 河湟方言（青海话）特征词映射（整词精确匹配）
QH = {
    # 疑问 / 指代
    "什么": "啥",
    "怎么": "咋",
    "怎样": "咋样",
    "怎么样": "咋样",
    "哪里": "阿扎",
    "哪儿": "阿扎",
    "谁": "阿个",
    "为什么": "阿门家",
    # 否定 / 程度
    "别": "嫑",
    "不要": "嫑",
    "非常": "麻利",
    "好": "歹",
    "漂亮": "心疼",
    "可爱": "心疼",
    "小": "尕",
    "小孩": "尕娃",
    "孩子": "尕娃",
    "干净": "干散",
    "利索": "干散",
    "舒服": "舒坦",
    "棒": "攒劲",
    "厉害": "歹",
    "可以": "能行",
    # 动词
    "聊天": "拉家常",
    "闲聊": "谝闲传",
    "干什么": "做啥",
    "做什么": "做啥",
    "胡说": "胡谝",
    "完": "罢",
    # 方位 / 时间
    "这里": "这搭",
    "那里": "那搭",
    "现在": "这会儿",
    "明天": "明儿个",
    "今天": "今儿个",
    "昨天": "夜来",
    "一起": "一挂",
}

HEADER = """# 青海话（河湟方言·中原官话秦陇片）

## 青海话（河湟方言·中原官话秦陇片） 🆕

> 主要分布：青海省河湟谷地，以湟源、乐都、湟中、西宁、平安、互助等为核心方言点。
> 谱系：中原官话·秦陇片（也称陇中片）。VoxCPM 暂不支持原生合成，推荐使用 Seed Audio / MiniMax / Mureka 备选模型生成语音。

"""

EXTRA = """### 河湟方言特色词

| 普通话 | 方言词 | 分类 |
|--------|--------|------|
| 好 / 厉害 | 歹 | 形容词 |
| 小 | 尕 | 形容词 |
| 漂亮 | 心疼 | 形容词 |
| 干净利索 | 干散 | 形容词 |
| 舒服 | 舒坦 | 形容词 |
| 棒 / 好 | 攒劲 | 形容词 |
| 什么 | 啥 | 疑问代词 |
| 怎么 | 咋 | 疑问代词 |
| 哪里 | 阿扎 | 疑问代词 |
| 谁 | 阿个 | 疑问代词 |
| 为什么 | 阿门家 | 疑问代词 |
| 不要 / 别 | 嫑 | 否定副词 |
| 一起 | 一挂 | 副词 |
| 这里 | 这搭 | 方位词 |
| 那里 | 那搭 | 方位词 |
| 现在 | 这会儿 | 时间词 |
| 今天 | 今儿个 | 时间词 |
| 明天 | 明儿个 | 时间词 |
| 昨天 | 夜来 | 时间词 |
| 小孩 | 尕娃 | 称谓 |
| 聊天 | 拉家常 | 动词 |
| 闲聊 | 谝闲传 | 动词 |
| 胡说 | 胡谝 | 动词 |
| 完 / 结束 | 罢 | 动词 |
| 干啥 | 做啥 | 短语 |
| 行 / 可以 | 能行 | 应答 |

"""


def to_qinghai(word):
    return QH.get(word, word)


def main():
    with open(SRC, encoding="utf-8") as f:
        content = f.read()

    parts = re.split(r"(?m)^(### .+)$", content)
    out = [HEADER]
    count = 0

    for i in range(1, len(parts), 2):
        title = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        lines = body.split("\n")
        new_lines = []
        for line in lines:
            stripped = line.strip()
            m = re.match(r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", stripped)
            if (
                m
                and m.group(1).strip() != "普通话"
                and not stripped.startswith("|---")
            ):
                put = m.group(1).strip()
                cat = m.group(3).strip()
                qh = to_qinghai(put)
                new_lines.append(f"| {put} | {qh} | {cat} |")
                count += 1
            else:
                new_lines.append(line)
        out.append(title)
        out.append("\n".join(new_lines))
        out.append("")

    out.append(EXTRA)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"Generated {OUT}")
    print(f"Domain entries (mapped + passthrough): {count}")
    print(f"Extra 河湟特色词: 26")
    print(f"Total: {count + 26}")


if __name__ == "__main__":
    main()
