#!/usr/bin/env python3
"""
方言词典大规模生成器
用法: python3 generate_extra.py /path/to/dialect_dictionary.md
自动为所有方言追加词条直到总数达到目标
"""

import re, sys

TARGET = 20000
BATCH_SIZE = 50  # per dialect per domain

def count_entries(content):
    return sum(1 for l in content.split('\n')
               if l.strip().startswith('|') and not l.strip().startswith('|---')
               and '普通话 |' not in l and '| 功用 |' not in l)

def main(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    current = count_entries(content)
    print(f"当前词条: {current}")
    print(f"目标: {TARGET}")
    
    # ============================================================
    # 你需要在这里添加更多词条数据
    # 格式: DOMAINS = {
    #   '领域名': {
    #     '方言名': [('普通话', '方言词', '分类'), ...],
    #   }
    # }
    # 
    # 参考已覆盖的领域:
    # v2.5: 自然气候/色彩形状/衣物穿戴/家居器物/交通出行/情感状态/常用动作
    # v2.6: 健康医疗/工作职场/动植物/骂人互怼
    # v2.7: 教育/购物/婚恋/节庆/通讯
    # v3.0: 习语歇后语/吃喝点菜/打牌搓麻/买房租房/次方言拆分/新方言
    # v3.1: 数字科技/法律政务/体育运动/艺术娱乐/银行金融/宗教民俗
    #
    # 待扩展领域:
    # - 农业种植 (播种/收割/施肥/庄稼等)
    # - 交通出行详细版 (导航/堵车/加油/停车场等)
    # - 美发美容 (剪发/烫发/染发/化妆等)
    # - 宠物饲养 (遛狗/猫粮/绝育等)
    # - 幼儿养育 (喂奶/换尿布/哄睡/早教等)
    # - 婚丧嫁娶详细版
    # - 更多次方言 (广州vs香港, 厦门vs泉州vs漳州等)
    # - 更多大方言 (宁波、扬州、合肥、南宁、海口等)
    # ============================================================
    
    DOMAINS = {}  # TODO: 填入词条数据
    
    for domain_name, dialect_data in DOMAINS.items():
        for dialect_key, entries in dialect_data.items():
            if not entries: continue
            table = '\n'.join([f'| {p} | {d} | {c} |' for p,d,c in entries])
            sup = f'\n### auto-{domain_name}\n\n| 普通话 | 方言词 | 分类 |\n|--------|--------|------|\n{table}\n'
            pat = rf'(## .*?{dialect_key}.*?)(\n### \d+\.\d+ 语法特点|\n### \d+\.\d+ 语法)'
            m = re.search(pat, content, re.DOTALL)
            if m:
                content = content.replace(m.group(0), m.group(0).replace(m.group(2), sup + '\n' + m.group(2)))
    
    new_count = count_entries(content)
    print(f"生成后词条: {new_count} (+{new_count - current})")
    
    if new_count >= TARGET:
        print(f"✅ 达到目标！")
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"已保存到: {filepath}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 generate_extra.py dialect_dictionary.md")
        sys.exit(1)
    main(sys.argv[1])
