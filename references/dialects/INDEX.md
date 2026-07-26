# 方言词典索引

> 版本 v2.1.0 | 总词条约 303,398 条 | 29 种方言全覆盖
> 主要语音模型：VoxCPM（9 大方言组原生支持）| 备选模型：Seed Audio / MiniMax / ElevenLabs / Mureka

每个方言独立一个文件，按需加载，避免一次性读入超大文件。

## 9 大方言组（VoxCPM 原生支持）

| 方言组 | 主要方言 | 谱系 | 词元文件 | VoxCPM |
|-------|---------|------|---------|:------:|
| **四川话** | 四川话 | 西南官话·成渝片 | [02_sichuan.md](02_sichuan.md) | ✅ |
| **粤语** | 粤语 | 粤语·广府片 | [03_yueyu.md](03_yueyu.md) | ✅ |
| **吴语** | 上海话 | 吴语·太湖片 | [05_shanghai.md](05_shanghai.md) | ✅ |
| **东北话** | 东北话 | 东北官话 | [04_dongbei.md](04_dongbei.md) | ✅ |
| **河南话** | 河南话 | 中原官话·郑开片 | [06_henan.md](06_henan.md) | ✅ |
| **陕西话** | 陕西话 | 中原官话·关中片 | [07_shaanxi.md](07_shaanxi.md) | ✅ |
| **山东话** | 山东话 | 冀鲁/胶辽官话 | [09_shandong.md](09_shandong.md) | ✅ |
| **天津话** | 天津话 | 冀鲁官话·天津片 | [10_tianjin.md](10_tianjin.md) | ✅ |
| **闽南话** | 闽南语 | 闽语·闽南片 | [11_minnan.md](11_minnan.md) | ✅ |

## 地方分支（VoxCPM 原生支持）

| 方言组 | 分支方言 | 谱系 | 词元文件 | VoxCPM |
|-------|---------|------|---------|:------:|
| **四川话** | 成都话 | 西南官话·成渝片 | [21_chengdu.md](21_chengdu.md) | ✅ |
| | 重庆话 | 西南官话·成渝片 | [22_chongqing.md](22_chongqing.md) | ✅ |
| | 自贡话 | 西南官话·仁富片 | [19_zigong.md](19_zigong.md) | ✅ |
| | 贵阳话 | 西南官话·黔中片 | [17_guiyang.md](17_guiyang.md) | ✅ |
| | 云南话 | 西南官话·滇中片 | [15_yunnan.md](15_yunnan.md) | ✅ |
| | 湖北话 | 西南官话·武天片 | [16_hubei.md](16_hubei.md) | ✅ |
| **吴语** | 苏州话 | 吴语·太湖片 | [20_suzhou.md](20_suzhou.md) | ✅ |
| | 温州话 | 吴语·瓯江片 | [27_wenzhou.md](27_wenzhou.md) | ✅ |
| **河南话** | 洛阳话 | 中原官话·洛嵩片 | [25_luoyang.md](25_luoyang.md) | ✅ |
| | 徐州话 | 中原官话·徐淮片 | [18_xuzhou.md](18_xuzhou.md) | ✅ |
| **山东话** | 济南话 | 冀鲁官话 | [23_jinan.md](23_jinan.md) | ✅ |
| | 青岛话 | 胶辽官话 | [24_qingdao.md](24_qingdao.md) | ✅ |

## 其他方言（备选 TTS 模型）

> 以下 8 种方言 VoxCPM 暂不支持原生合成，推荐使用 Seed Audio / MiniMax / ElevenLabs / Mureka 等备选模型生成语音。

| # | 方言 | 谱系 | 词元文件 | 词条数 | 推荐模型 |
|:--:|------|------|---------|-------:|---------|
| 1 | **北京话** | 北京官话·京师片 | [01_beijing.md](01_beijing.md) | 12,627 | Seed Audio / MiniMax |
| 2 | **湖南话** | 湘语·长益片 | [08_hunan.md](08_hunan.md) | 12,545 | MiniMax / ElevenLabs |
| 3 | **客家话** | 客语·粤台片 | [12_kejia.md](12_kejia.md) | 10,409 | Seed Audio / Mureka |
| 4 | **赣语** | 赣语·昌靖片 | [13_ganyu.md](13_ganyu.md) | 10,377 | MiniMax / Mureka |
| 5 | **晋语** | 晋语·并州片 | [14_jinyu.md](14_jinyu.md) | 10,392 | Seed Audio / MiniMax |
| 6 | **南京话** | 江淮官话·洪巢片 | [26_nanjing.md](26_nanjing.md) | 9,400 | MiniMax / ElevenLabs |
| 7 | **福州话** | 闽语·闽东片 | [28_fuzhou.md](28_fuzhou.md) | 9,389 | Seed Audio / Mureka |
| 8 | **兰州话** | 兰银官话·金城片 | [29_lanzhou.md](29_lanzhou.md) | 9,395 | MiniMax / Seed Audio |

## 附录

| 文件 | 内容 |
|------|------|
| [00_appendix.md](00_appendix.md) | 声调对照表、谱系树、类型学矩阵 |

---

## 使用方式

```
# 只加载需要的方言文件
请参考 dialects/02_sichuan.md，把这段话改成四川话：...

# 或者加载多个方言做对比
请参考 dialects/02_sichuan.md 和 dialects/22_chongqing.md，比较四川话和重庆话的差异。
```

> 💡 v2.1.0 恢复全部 29 种方言为活跃状态。VoxCPM 原生支持 9 大方言组（21 种变体），其余 8 种方言使用备选 TTS 模型生成语音。
