# Dictionary Ranking Evaluation Report

Generated: 2026-02-16 00:27:00

## Summary

- **Total queries**: 650
- **Passed**: 619 (95.2%)
- **Failed**: 31 (4.8%)

## Category Results

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| single_tone | 150 | 149 | 1 | 99% |
| single_no_tone | 50 | 50 | 0 | 100% |
| multi_syllable | 140 | 128 | 12 | 91% |
| cantonese_vocab | 60 | 59 | 1 | 98% |
| partial_prefix | 50 | 49 | 1 | 98% |
| english | 70 | 69 | 1 | 99% |
| character | 45 | 45 | 0 | 100% |
| edge_case | 35 | 30 | 5 | 86% |

## Failed Queries (31)

### #15: `mat1` (single_tone)

**Description**: what (mat not standard jyutping base)

**Reason**: Expected one of ['乜'] but got ['貓', '伩', '么', '文', '嘜', '媽', '孖', '蚊', '𢺳', '咪'] (jyutping: ['maau1', 'man1', 'maa1', 'man1', 'mak1', 'maa1', 'maa1', 'man1', 'maan1', 'mai1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 貓 | maau1 | 29000 | 9000 | 20000 | 0 | Jyutping | CEDict |
| 2 | 伩 | man1 | 29000 | 9000 | 20000 | 0 | Jyutping | CCanto |
| 3 | 么 | maa1 | 33003 | 13003 | 20000 | 0 | Jyutping | CCanto |
| 4 | 文 | man1 | 33559 | 13559 | 20000 | 0 | Jyutping | CCanto |
| 5 | 嘜 | mak1 | 34000 | 14000 | 20000 | 0 | Jyutping | CEDict |

### #44: `hou2 leng3` (multi_syllable)

**Description**: very pretty (may not exist as entry)

**Reason**: No results returned

### #50: `dak1 m4 dak1` (multi_syllable)

**Description**: OK or not OK (colloquial, may not be entry)

**Reason**: No results returned

### #52: `sei2 m4 sei2` (multi_syllable)

**Description**: dead or not (colloquial, may not be entry)

**Reason**: No results returned

### #300: `ji1 ging1` (multi_syllable)

**Description**: already

**Reason**: Expected one of ['已經'] but got ['燕京', '一經', '燕京大學'] (jyutping: ['jin1 ging1', 'jat1 ging1', 'jin1 ging1 daai6 hok6'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 燕京 | jin1 ging1 | 23500 | 21000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 一經 | jat1 ging1 | 38149 | 18149 | 20000 | 0 | Jyutping | CCanto |
| 3 | 燕京大學 | jin1 ging1 daai6 hok6 | 85712 | 33212 | 2500 | 50000 | Jyutping | CEDict |
| 4 | 燕京啤酒 | jin1 ging1 be1 zau2 | 87500 | 35000 | 2500 | 50000 | Jyutping | CEDict |
| 5 | 醫療經驗 | ji1 liu4 ging1 jim6 | 95000 | 35000 | 0 | 60000 | Jyutping | CEDict |

### #308: `gam1 nin2` (multi_syllable)

**Description**: this year

**Reason**: No results returned

### #327: `daai6 gaa1` (multi_syllable)

**Description**: everyone

**Reason**: Expected one of ['大家'] but got ['大街'] (jyutping: ['daai6 gaai1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 大街 | daai6 gaai1 | 16712 | 14212 | 2500 | 0 | Jyutping | CEDict |
| 2 | 大家 | daai6 gaa1 | 18151 | 18151 | 0 | 0 | Jyutping | CEDict |
| 3 | 加大 | gaa1 daai6 | 26889 | 18889 | 0 | 0 | Jyutping | CEDict |
| 4 | 交大 | gaau1 daai6 | 34712 | 24212 | 2500 | 0 | Jyutping | CEDict |
| 5 | 大吉 | daai6 gat1 | 39212 | 19212 | 20000 | 0 | Jyutping | CEDict |

### #334: `haa5 ci3` (multi_syllable)

**Description**: next time

**Reason**: Expected one of ['下次'] but got ['沙蟹桌', '炒蝦拆蟹'] (jyutping: ['saa1 haai5 coek3', 'caau2 haa1 caak3 haai5'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 沙蟹桌 | saa1 haai5 coek3 | 90500 | 28000 | 22500 | 40000 | Jyutping | CCanto |
| 2 | 炒蝦拆蟹 | caau2 haa1 caak3 haai5 | 155500 | 35000 | 22500 | 90000 | Jyutping | CCanto |

### #335: `soeng5 min6` (multi_syllable)

**Description**: above/on top

**Reason**: Expected one of ['上面'] but got ['七情上面'] (jyutping: ['cat1 cing4 soeng5 min6'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 七情上面 | cat1 cing4 soeng5 min6 | 121745 | 31745 | 0 | 90000 | Jyutping | CCanto |

### #336: `haa5 min6` (multi_syllable)

**Description**: below/underneath

**Reason**: Expected one of ['下面'] but got ['厚面皮', '面皮厚'] (jyutping: ['hau5 min6 pei4', 'min6 pei4 hau5'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 厚面皮 | hau5 min6 pei4 | 67120 | 27120 | 20000 | 20000 | Jyutping | CCanto |
| 2 | 面皮厚 | min6 pei4 hau5 | 85120 | 27120 | 20000 | 30000 | Jyutping | CCanto |

### #342: `jing1 man2` (multi_syllable)

**Description**: English language

**Reason**: Expected one of ['英文'] but got ['英文堂'] (jyutping: ['jing1 man2 tong4'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 英文堂 | jing1 man2 tong4 | 47559 | 27559 | 0 | 20000 | Jyutping | CCanto |

### #343: `zung1 man2` (multi_syllable)

**Description**: Chinese language

**Reason**: Expected one of ['中文'] but got ['繁體中文'] (jyutping: ['faan4 tai2 zung1 man2'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 繁體中文 | faan4 tai2 zung1 man2 | 122724 | 32724 | 0 | 90000 | Jyutping | CCanto |

### #368: `jau4 guk2` (multi_syllable)

**Description**: post office

**Reason**: Expected one of ['郵局'] but got ['油管'] (jyutping: ['jau4 gun2'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 油管 | jau4 gun2 | 41000 | 21000 | 20000 | 0 | Jyutping | CCanto |
| 2 | 古人 | gu2 jan4 | 66640 | 18640 | 40000 | 0 | Jyutping | CEDict |
| 3 | 游泳館 | jau4 wing6 gun2 | 78000 | 28000 | 20000 | 30000 | Jyutping | CEDict |
| 4 | 輸油管 | syu1 jau4 gun2 | 88000 | 28000 | 20000 | 40000 | Jyutping | CEDict |
| 5 | 古人類 | gu2 jan4 leoi6 | 93640 | 25640 | 40000 | 20000 | Jyutping | CEDict |

### #401: `gwaai3` (cantonese_vocab)

**Description**: well-behaved (Canto)

**Reason**: Expected one of ['乖'] but got ['夬', '怪', '解', '介', '刮'] (jyutping: ['gwaai3', 'gwaai3', 'gaai3', 'gaai3', 'gwaat3'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 夬 | gwaai3 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 2 | 怪 | gwaai3 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 3 | 解 | gaai3 | 33874 | 13874 | 20000 | 0 | Jyutping | CCanto |
| 4 | 介 | gaai3 | 34000 | 14000 | 20000 | 0 | Jyutping | CEDict |
| 5 | 刮 | gwaat3 | 34000 | 14000 | 20000 | 0 | Jyutping | CEDict |

### #440: `baa` (partial_prefix)

**Description**: prefix for baa- syllables

**Reason**: Expected one of ['巴', '爸', '吧'] but got ['壩', '包', '板', '班', '勹'] (jyutping: ['baa3', 'baau1', 'baan2', 'baan1', 'baau1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 壩 | baa3 | 9000 | 9000 | 0 | 0 | Jyutping | CEDict |
| 2 | 包 | baau1 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 3 | 板 | baan2 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 4 | 班 | baan1 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 5 | 勹 | baau1 | 11500 | 9000 | 2500 | 0 | Jyutping | CCanto |

### #521: `sun` (english)

**Description**: English sun

**Reason**: Expected one of ['日', '太陽'] but got ['娀', '崇', '悚', '慫', '聳'] (jyutping: ['sung1', 'sung4', 'sung2', 'sung2', 'sung2'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 娀 | sung1 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 崇 | sung4 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |
| 3 | 悚 | sung2 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |
| 4 | 慫 | sung2 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |
| 5 | 聳 | sung2 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |

### #588: `hai6 m4 hai6` (edge_case)

**Description**: yes or no question (3 syllable)

**Reason**: No results returned

### #589: `hou2 m4 hou2` (edge_case)

**Description**: good or not (3 syllable)

**Reason**: No results returned

### #592: `saam1 go3` (edge_case)

**Description**: three (classifier)

**Reason**: Expected one of ['三個'] but got ['三角', '衫腳', '三教'] (jyutping: ['saam1 gok3', 'saam1 goek3', 'saam1 gaau3'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 三角 | saam1 gok3 | 22955 | 20455 | 2500 | 0 | Jyutping | CEDict |
| 2 | 衫腳 | saam1 goek3 | 26000 | 21000 | 5000 | 0 | Jyutping | CCanto |
| 3 | 三教 | saam1 gaau3 | 40286 | 20286 | 20000 | 0 | Jyutping | CEDict |
| 4 | 三價 | saam1 gaa3 | 40455 | 20455 | 20000 | 0 | Jyutping | CEDict |
| 5 | 三國 | saam1 gwok3 | 40455 | 20455 | 20000 | 0 | Jyutping | CEDict |

### #594: `daai6 gaa1` (edge_case)

**Description**: everyone

**Reason**: Expected one of ['大家'] but got ['大街'] (jyutping: ['daai6 gaai1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 大街 | daai6 gaai1 | 16712 | 14212 | 2500 | 0 | Jyutping | CEDict |
| 2 | 大家 | daai6 gaa1 | 18151 | 18151 | 0 | 0 | Jyutping | CEDict |
| 3 | 加大 | gaa1 daai6 | 26889 | 18889 | 0 | 0 | Jyutping | CEDict |
| 4 | 交大 | gaau1 daai6 | 34712 | 24212 | 2500 | 0 | Jyutping | CEDict |
| 5 | 大吉 | daai6 gat1 | 39212 | 19212 | 20000 | 0 | Jyutping | CEDict |

### #600: `hou2 do1 ze6` (edge_case)

**Description**: thank you very much

**Reason**: Expected one of ['好多謝'] but got ['好得滯', '人多好做作', '可選擇丟棄', '多謝你咁好介紹', '好漢做事好漢當'] (jyutping: ['hou2 dak1 zai6', 'jan4 do1 hou2 zou6 zok3', 'ho2 syun2 zaak6 diu1 hei3', 'do1 ze6 nei5 gam3 hou2 gaai3 siu6', 'hou2 hon3 zou6 si6 hou2 hon3 dong1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 好得滯 | hou2 dak1 zai6 | 65878 | 25878 | 40000 | 0 | Jyutping | CCanto |
| 2 | 人多好做作 | jan4 do1 hou2 zou6 zok3 | 144663 | 36663 | 20000 | 80000 | Jyutping | CCanto |
| 3 | 可選擇丟棄 | ho2 syun2 zaak6 diu1 hei3 | 178589 | 40589 | 60000 | 70000 | Jyutping | CEDict |
| 4 | 多謝你咁好介紹 | do1 ze6 nei5 gam3 hou2 gaai3 siu6 | 228761 | 52761 | 0 | 160000 | Jyutping | CCanto |
| 5 | 好漢做事好漢當 | hou2 hon3 zou6 si6 hou2 hon3 dong1 | 276264 | 53264 | 25000 | 190000 | Jyutping | CEDict |

### #601: `ge` (exact_vs_prefix)

**Description**: ge (exact) should beat gei (prefix) - currently fails: gei1/機 at 11500 beats ge2/嘅 at 14000

**Reason**: Expected one of ['嘅'] but got ['機'] (jyutping: ['gei1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 機 | gei1 | 11500 | 9000 | 2500 | 0 | Jyutping | CCanto |
| 2 | 嘅 | ge2 | 14000 | 14000 | 0 | 0 | Jyutping | CCanto |
| 3 | 痂 | ge1 | 14000 | 14000 | 0 | 0 | Jyutping | CCanto |
| 4 | 其 | gei1 | 15674 | 13174 | 2500 | 0 | Jyutping | CCanto |
| 5 | 己 | gei2 | 16148 | 13648 | 2500 | 0 | Jyutping | CEDict |

### #602: `do` (exact_vs_prefix)

**Description**: do (exact) should beat dou (prefix) - currently fails: dou6/道 at 10391 beats do1/多 at 12995

**Reason**: Expected one of ['多'] but got ['道'] (jyutping: ['dou6'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 道 | dou6 | 10391 | 7891 | 2500 | 0 | Jyutping | CEDict |
| 2 | 刀 | dou1 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 3 | 島 | dou2 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 4 | 多 | do1 | 12995 | 12995 | 0 | 0 | Jyutping | CEDict |
| 5 | 黨 | dong2 | 14000 | 9000 | 5000 | 0 | Jyutping | CEDict |

### #603: `mo` (exact_vs_prefix)

**Description**: mo (exact) should beat mou (prefix) - currently fails: mou6/霧 at 11500 beats mo5/冇 at 12000

**Reason**: Expected one of ['冇'] but got ['霧'] (jyutping: ['mou6'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 霧 | mou6 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 冇 | mo5 | 12000 | 12000 | 0 | 0 | Jyutping | CCanto |
| 3 | 么 | mo1 | 13003 | 13003 | 0 | 0 | Jyutping | CCanto |
| 4 | 劘 | mo4 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 5 | 摩 | mo1 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |

### #604: `to` (exact_vs_prefix)

**Description**: to (exact) should beat tou (prefix) - currently fails: tou4/圖 at 11500 beats to1/他 at 11797

**Reason**: Expected one of ['他', '它'] but got ['圖'] (jyutping: ['tou4'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 圖 | tou4 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 他 | to1 | 11797 | 11797 | 0 | 0 | Jyutping | CCanto |
| 3 | 它 | to1 | 13326 | 13326 | 0 | 0 | Jyutping | CCanto |
| 4 | 堂 | tong4 | 14000 | 9000 | 5000 | 0 | Jyutping | CEDict |
| 5 | 糖 | tong4 | 14000 | 9000 | 5000 | 0 | Jyutping | CEDict |

### #606: `co` (exact_vs_prefix)

**Description**: co (exact) should beat cou/coi/cong (prefix) - currently all prefix matches win

**Reason**: Expected one of ['初', '搓'] but got ['草'] (jyutping: ['cou2'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 草 | cou2 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 菜 | coi3 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 3 | 艸 | cou2 | 11500 | 9000 | 2500 | 0 | Jyutping | CCanto |
| 4 | 床 | cong4 | 14000 | 9000 | 5000 | 0 | Jyutping | CEDict |
| 5 | 牀 | cong4 | 14000 | 9000 | 5000 | 0 | Jyutping | CCanto |

### #607: `do1` (exact_vs_prefix)

**Description**: do1 exact should beat dou1 prefix - currently fails: dou1/刀 at 11500 beats do1/多 at 12995

**Reason**: Expected one of ['多'] but got ['刀'] (jyutping: ['dou1'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 刀 | dou1 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 多 | do1 | 12995 | 12995 | 0 | 0 | Jyutping | CEDict |
| 3 | 哆 | do1 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 4 | 都 | dou1 | 15587 | 13087 | 2500 | 0 | Jyutping | CEDict |
| 5 | 叨 | dou1 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |

### #608: `do6` (exact_vs_prefix)

**Description**: do6 exact should beat dou6 prefix - currently fails: dou6/道 at 10391 beats do6/墮 at 14000

**Reason**: Expected one of ['墮'] but got ['道'] (jyutping: ['dou6'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 道 | dou6 | 10391 | 7891 | 2500 | 0 | Jyutping | CEDict |
| 2 | 墮 | do6 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 3 | 惰 | do6 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 4 | 隋 | do6 | 14000 | 14000 | 0 | 0 | Jyutping | CCanto |
| 5 | 馱 | do6 | 14000 | 14000 | 0 | 0 | Jyutping | CCanto |

### #609: `do3` (exact_vs_prefix)

**Description**: do3 exact should beat dou3 prefix

**Reason**: Expected one of ['剁'] but got ['道'] (jyutping: ['dou3'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 道 | dou3 | 10391 | 7891 | 2500 | 0 | Jyutping | CCanto |
| 2 | 剁 | do3 | 14000 | 14000 | 0 | 0 | Jyutping | CCanto |
| 3 | 到 | dou3 | 14800 | 12300 | 2500 | 0 | Jyutping | CEDict |
| 4 | 妒 | dou3 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |
| 5 | 斁 | dou3 | 16500 | 14000 | 2500 | 0 | Jyutping | CEDict |

### #637: `go3` (exact_vs_prefix)

**Description**: go3 exact should beat gok3/gon3/gong3 prefix - currently fails: gok3/角 at 11500 beats go3/嗰 at 12000

**Reason**: Expected one of ['嗰', '各'] but got ['角'] (jyutping: ['gok3'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 角 | gok3 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 嗰 | go3 | 12000 | 12000 | 0 | 0 | Jyutping | CCanto |
| 3 | 各 | go3 | 13908 | 13908 | 0 | 0 | Jyutping | CCanto |
| 4 | 腳 | goek3 | 14000 | 9000 | 5000 | 0 | Jyutping | CEDict |
| 5 | 個 | go3 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |

### #647: `do2` (exact_vs_prefix)

**Description**: do2 exact should beat dou2 prefix - currently fails: dou2/島 at 11500

**Reason**: Expected one of None but got ['島'] (jyutping: ['dou2'])

**Top results:**

| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |
|---|-----------|----------|------------|--------|------------|-----------|------|--------|
| 1 | 島 | dou2 | 11500 | 9000 | 2500 | 0 | Jyutping | CEDict |
| 2 | 黨 | dong2 | 14000 | 9000 | 5000 | 0 | Jyutping | CEDict |
| 3 | 嚲 | do2 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 4 | 垛 | do2 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |
| 5 | 埵 | do2 | 14000 | 14000 | 0 | 0 | Jyutping | CEDict |

## Pattern Analysis

### Source Distribution in Top Results

- CCanto as top result: 160
- CEDict as top result: 484

### Failure Patterns

- Failures where top result has term_match_cost > 0 (partial/fuzzy match winning): 20
- Failures where top result has static_cost > 15000 (high base cost): 9
- Failures where CEDict partial match beats CCanto exact match: 14

### Cost Distribution in Failures

| Query | Expected | Got | Got Total Cost | Got Static | Got Source |
|-------|----------|-----|----------------|------------|-----------|
| `mat1` | 乜 | 貓 | 29000 | 9000 | CEDict |
| `ji1 ging1` | 已經 | 燕京 | 23500 | 21000 | CEDict |
| `daai6 gaa1` | 大家 | 大街 | 16712 | 14212 | CEDict |
| `haa5 ci3` | 下次 | 沙蟹桌 | 90500 | 28000 | CCanto |
| `soeng5 min6` | 上面 | 七情上面 | 121745 | 31745 | CCanto |
| `haa5 min6` | 下面 | 厚面皮 | 67120 | 27120 | CCanto |
| `jing1 man2` | 英文 | 英文堂 | 47559 | 27559 | CCanto |
| `zung1 man2` | 中文 | 繁體中文 | 122724 | 32724 | CCanto |
| `jau4 guk2` | 郵局 | 油管 | 41000 | 21000 | CCanto |
| `gwaai3` | 乖 | 夬 | 14000 | 14000 | CEDict |
| `baa` | 巴, 爸, 吧 | 壩 | 9000 | 9000 | CEDict |
| `sun` | 日, 太陽 | 娀 | 16500 | 14000 | CEDict |
| `saam1 go3` | 三個 | 三角 | 22955 | 20455 | CEDict |
| `daai6 gaa1` | 大家 | 大街 | 16712 | 14212 | CEDict |
| `hou2 do1 ze6` | 好多謝 | 好得滯 | 65878 | 25878 | CCanto |
| `ge` | 嘅 | 機 | 11500 | 9000 | CCanto |
| `do` | 多 | 道 | 10391 | 7891 | CEDict |
| `mo` | 冇 | 霧 | 11500 | 9000 | CEDict |
| `to` | 他, 它 | 圖 | 11500 | 9000 | CEDict |
| `co` | 初, 搓 | 草 | 11500 | 9000 | CEDict |
| `do1` | 多 | 刀 | 11500 | 9000 | CEDict |
| `do6` | 墮 | 道 | 10391 | 7891 | CEDict |
| `do3` | 剁 | 道 | 10391 | 7891 | CCanto |
| `go3` | 嗰, 各 | 角 | 11500 | 9000 | CEDict |

## All Results

| # | Query | Status | Top Char | Top JP | Total Cost | Source |
|---|-------|--------|----------|--------|------------|--------|
| 1 | `ngo5` | PASS | 我 | ngo5 | 11740 | CEDict |
| 2 | `nei5` | PASS | 你 | nei5 | 12614 | CEDict |
| 3 | `hai6` | PASS | 係 | hai6 | 12000 | CCanto |
| 4 | `lo3` | PASS | 摞 | lo3 | 14000 | CEDict |
| 5 | `ge3` | PASS | 嘅 | ge3 | 14000 | CCanto |
| 6 | `aa3` | PASS | 鴨 | aap3 | 11500 | CEDict |
| 7 | `m4` | PASS | 唔 | m4 | 12000 | CCanto |
| 8 | `di1` | PASS | 的 | di1 | 10195 | CCanto |
| 9 | `go3` | PASS | 角 | gok3 | 11500 | CEDict |
| 10 | `zou6` | PASS | 做 | zou6 | 14000 | CEDict |
| 11 | `jat1` | PASS | 一 | jat1 | 11149 | CEDict |
| 12 | `gin3` | PASS | 勁 | ging3 | 11500 | CEDict |
| 13 | `sik1` | PASS | 色 | sik1 | 9000 | CEDict |
| 14 | `hou2` | PASS | 好 | hou2 | 13152 | CEDict |
| 15 | `mat1` | FAIL | 貓 | maau1 | 29000 | CEDict |
| 16 | `gam2` | PASS | 咁 | gam2 | 12000 | CCanto |
| 17 | `dou1` | PASS | 刀 | dou1 | 9000 | CEDict |
| 18 | `lei4` | PASS | 梨 | lei4 | 9000 | CEDict |
| 19 | `heoi3` | PASS | 去 | heoi3 | 13007 | CEDict |
| 20 | `waa6` | PASS | 話 | waa6 | 9000 | CEDict |
| 21 | `gong2` | PASS | 港 | gong2 | 9000 | CEDict |
| 22 | `tai2` | PASS | 睇 | tai2 | 12000 | CCanto |
| 23 | `jam2` | PASS | 飲 | jam2 | 14000 | CEDict |
| 24 | `faan1` | PASS | 番 | faan1 | 12000 | CCanto |
| 25 | `zyu6` | PASS | 住 | zyu6 | 14000 | CEDict |
| 26 | `bin1` | PASS | 邊 | bin1 | 11000 | CCanto |
| 27 | `dim2` | PASS | 點 | dim2 | 14000 | CEDict |
| 28 | `zoi3` | PASS | 再 | zoi3 | 13982 | CEDict |
| 29 | `daai6` | PASS | 大 | daai6 | 12212 | CEDict |
| 30 | `siu2` | PASS | 小 | siu2 | 13154 | CEDict |
| 31 | `ngo` | PASS | 鵝 | ngo4 | 9000 | CEDict |
| 32 | `nei` | PASS | 你 | nei5 | 12614 | CEDict |
| 33 | `hai` | PASS | 係 | hai6 | 12000 | CCanto |
| 34 | `hou` | PASS | 號 | hou6 | 9000 | CEDict |
| 35 | `gam` | PASS | 咁 | gam2 | 12000 | CCanto |
| 36 | `sik` | PASS | 色 | sik1 | 9000 | CEDict |
| 37 | `dim` | PASS | 店 | dim3 | 9000 | CEDict |
| 38 | `lok` | PASS | 樂 | lok6 | 14000 | CEDict |
| 39 | `jau` | PASS | 有 | jau5 | 11687 | CEDict |
| 40 | `dou` | PASS | 道 | dou6 | 7891 | CEDict |
| 41 | `nei5 hou2` | PASS | 你好 | nei5 hou2 | 18766 | CEDict |
| 42 | `m4 goi1` | PASS | 唔該 | m4 goi1 | 21000 | CCanto |
| 43 | `do1 ze6` | PASS | 多謝 | do1 ze6 | 19995 | CEDict |
| 44 | `hou2 leng3` | FAIL | - | - | - | - |
| 45 | `sik6 faan6` | PASS | 食飯 | sik6 faan6 | 21000 | CCanto |
| 46 | `gong2 jyut6 jyu5` | PASS | 廣州撐粵語行動 | gwong2 zau1 caang1 jyut6 jyu5 hang4 dung6 | 254896 | CCanto |
| 47 | `dim2 gaai2` | PASS | 點解 | dim2 gaai2 | 20874 | CCanto |
| 48 | `m4 hou2` | PASS | 唔好 | m4 hou2 | 20152 | CCanto |
| 49 | `zoi3 gin3` | PASS | 再建 | zoi3 gin3 | 20971 | CEDict |
| 50 | `dak1 m4 dak1` | FAIL | - | - | - | - |
| 51 | `gei2 do1` | PASS | 幾多 | gei2 do1 | 19995 | CCanto |
| 52 | `sei2 m4 sei2` | FAIL | - | - | - | - |
| 53 | `jat1 jat6` | PASS | 一日 | jat1 jat6 | 17425 | CCanto |
| 54 | `bat1 gwo3` | PASS | 不過 | bat1 gwo3 | 18459 | CEDict |
| 55 | `ji4 gaa1` | PASS | 而家 | ji4 gaa1 | 18636 | CCanto |
| 56 | `jyu4 gwo2` | PASS | 如果 | jyu4 gwo2 | 19729 | CEDict |
| 57 | `ting1 jat6` | PASS | 聽日 | ting1 jat6 | 20276 | CCanto |
| 58 | `cam4 jat6` | PASS | 噚日 | cam4 jat6 | 20276 | CCanto |
| 59 | `gam1 jat6` | PASS | 今日 | gam1 jat6 | 20276 | CEDict |
| 60 | `hou2 ci5` | PASS | 好似 | hou2 ci5 | 20152 | CEDict |
| 61 | `leng3` | PASS | 靚 | leng3 | 14000 | CCanto |
| 62 | `mou5` | PASS | 冇 | mou5 | 12000 | CCanto |
| 63 | `je5` | PASS | 嘢 | je5 | 12000 | CCanto |
| 64 | `gam3` | PASS | 咁 | gam3 | 12000 | CCanto |
| 65 | `saai3` | PASS | 曬 | saai3 | 12000 | CCanto |
| 66 | `maai4` | PASS | 埋 | maai4 | 14000 | CEDict |
| 67 | `zek3` | PASS | 只 | zek3 | 13259 | CCanto |
| 68 | `keoi5` | PASS | 佢 | keoi5 | 12000 | CCanto |
| 69 | `fan3` | PASS | 瞓 | fan3 | 12000 | CCanto |
| 70 | `zan1` | PASS | 真 | zan1 | 13882 | CEDict |
| 71 | `ng` | PASS | 鵝 | ngo4 | 11500 | CEDict |
| 72 | `ho` | PASS | 河 | ho4 | 9000 | CEDict |
| 73 | `ne` | PASS | 呢 | ne1 | 14000 | CEDict |
| 74 | `ge` | PASS | 機 | gei1 | 11500 | CCanto |
| 75 | `si` | PASS | 事 | si6 | 7960 | CCanto |
| 76 | `gw` | PASS | 國 | gwok3 | 14000 | CEDict |
| 77 | `zo` | PASS | 座 | zo6 | 9000 | CEDict |
| 78 | `ja` | PASS | 人 | jan4 | 9140 | CEDict |
| 79 | `heoi` | PASS | 佢 | heoi5 | 12000 | CCanto |
| 80 | `gon` | PASS | 杆 | gon1 | 9000 | CEDict |
| 81 | `hello` | PASS | 喂 | wai3 | 19000 | CEDict |
| 82 | `water` | PASS | 水 | seoi2 | 18880 | CEDict |
| 83 | `eat` | PASS | 座 | zo6 | 19100 | CEDict |
| 84 | `good` | PASS | 貨 | fo3 | 14000 | CEDict |
| 85 | `person` | PASS | 人 | jan4 | 11640 | CEDict |
| 86 | `house` | PASS | 房 | fong2 | 14000 | CEDict |
| 87 | `money` | PASS | 角 | gok3 | 17400 | CEDict |
| 88 | `big` | PASS | 渠 | keoi4 | 14000 | CEDict |
| 89 | `see` | PASS | 大 | daai6 | 17212 | CEDict |
| 90 | `beautiful` | PASS | 美 | mei5 | 18576 | CEDict |
| 91 | `咯` | PASS | 咯 | gok3 | 14000 | CEDict |
| 92 | `嘅` | PASS | 嘅 | koi3 | 14000 | CCanto |
| 93 | `食` | PASS | 食 | sik6 | 14000 | CEDict |
| 94 | `好` | PASS | 好 | hou2 | 13152 | CEDict |
| 95 | `你好` | PASS | 你好 | nei5 hou2 | 18766 | CEDict |
| 96 | `aa` | PASS | 鴨 | aap3 | 11500 | CEDict |
| 97 | `m` | PASS | 唔 | m4 | 12000 | CCanto |
| 98 | `ng5` | PASS | 五 | ng5 | 14000 | CEDict |
| 99 | `gwong2 dung1 waa2` | PASS | 廣東話 | gwong2 dung1 waa2 | 28000 | CEDict |
| 100 | `jyut6 jyu5` | PASS | 粵語 | jyut6 jyu5 | 21000 | CEDict |
| 101 | `sam1` | PASS | 心 | sam1 | 8201 | CEDict |
| 102 | `sei3` | PASS | 四 | sei3 | 13953 | CEDict |
| 103 | `ng5` | PASS | 五 | ng5 | 14000 | CEDict |
| 104 | `luk6` | PASS | 角 | luk6 | 9000 | CCanto |
| 105 | `cat1` | PASS | 漆 | cat1 | 9000 | CEDict |
| 106 | `baat3` | PASS | 八 | baat3 | 14000 | CEDict |
| 107 | `gau2` | PASS | 狗 | gau2 | 9000 | CEDict |
| 108 | `sap6` | PASS | 十 | sap6 | 13347 | CEDict |
| 109 | `jan4` | PASS | 人 | jan4 | 6640 | CEDict |
| 110 | `neoi5` | PASS | 女 | neoi5 | 13951 | CEDict |
| 111 | `naam4` | PASS | 男 | naam4 | 9000 | CCanto |
| 112 | `gaa1` | PASS | 家 | gaa1 | 7939 | CEDict |
| 113 | `hok6` | PASS | 學 | hok6 | 14000 | CEDict |
| 114 | `nin4` | PASS | 年 | nin4 | 7772 | CEDict |
| 115 | `jyut6` | PASS | 月 | jyut6 | 8690 | CEDict |
| 116 | `ming4` | PASS | 明 | ming4 | 13436 | CEDict |
| 117 | `san1` | PASS | 新 | san1 | 13636 | CEDict |
| 118 | `loi4` | PASS | 來 | loi4 | 14000 | CEDict |
| 119 | `tung4` | PASS | 銅 | tung4 | 9000 | CEDict |
| 120 | `gwong2` | PASS | 廣 | gwong2 | 14000 | CEDict |
| 121 | `zung1` | PASS | 鐘 | zung1 | 9000 | CEDict |
| 122 | `seoi2` | PASS | 水 | seoi2 | 13880 | CEDict |
| 123 | `fo2` | PASS | 房 | fong2 | 14000 | CEDict |
| 124 | `saan1` | PASS | 山 | saan1 | 9000 | CEDict |
| 125 | `tin1` | PASS | 天 | tin1 | 13133 | CEDict |
| 126 | `dei6` | PASS | 地 | dei6 | 7296 | CEDict |
| 127 | `fung1` | PASS | 風 | fung1 | 9000 | CEDict |
| 128 | `jyu5` | PASS | 雨 | jyu5 | 9000 | CEDict |
| 129 | `faa1` | PASS | 花 | faa1 | 9000 | CEDict |
| 130 | `syu4` | PASS | 船 | syun4 | 11500 | CEDict |
| 131 | `muk6` | PASS | 目 | muk6 | 13975 | CCanto |
| 132 | `gam1` | PASS | 今 | gam1 | 14000 | CEDict |
| 133 | `ngaan5` | PASS | 眼 | ngaan5 | 9000 | CEDict |
| 134 | `hau2` | PASS | 口 | hau2 | 13915 | CEDict |
| 135 | `sau2` | PASS | 手 | sau2 | 8536 | CEDict |
| 136 | `goek3` | PASS | 腳 | goek3 | 9000 | CEDict |
| 137 | `tau4` | PASS | 頭 | tau4 | 9000 | CEDict |
| 138 | `ji5` | PASS | 以 | ji5 | 12358 | CEDict |
| 139 | `ce1` | PASS | 車 | ce1 | 9000 | CEDict |
| 140 | `syun4` | PASS | 船 | syun4 | 9000 | CEDict |
| 141 | `fei1` | PASS | 妃 | fei1 | 14000 | CEDict |
| 142 | `maau1` | PASS | 貓 | maau1 | 9000 | CEDict |
| 143 | `gau2` | PASS | 狗 | gau2 | 9000 | CEDict |
| 144 | `jyu2` | PASS | 魚 | jyu2 | 9000 | CEDict |
| 145 | `niu5` | PASS | 鳥 | niu5 | 9000 | CEDict |
| 146 | `baak6` | PASS | 僰 | baak6 | 14000 | CEDict |
| 147 | `hak1` | PASS | 可 | hak1 | 12589 | CCanto |
| 148 | `hung4` | PASS | 洪 | hung4 | 14000 | CEDict |
| 149 | `wong4` | PASS | 凰 | wong4 | 14000 | CEDict |
| 150 | `laam4` | PASS | 婪 | laam4 | 14000 | CEDict |
| 151 | `luk6` | PASS | 角 | luk6 | 9000 | CCanto |
| 152 | `cin2` | PASS | 錢 | cin2 | 9000 | CEDict |
| 153 | `faan6` | PASS | 飯 | faan6 | 9000 | CEDict |
| 154 | `caa4` | PASS | 茶 | caa4 | 9000 | CEDict |
| 155 | `zau2` | PASS | 酒 | zau2 | 9000 | CEDict |
| 156 | `tong4` | PASS | 堂 | tong4 | 9000 | CEDict |
| 157 | `jit6` | PASS | 嚙 | jit6 | 14000 | CEDict |
| 158 | `dung3` | PASS | 棟 | dung3 | 12000 | CCanto |
| 159 | `faai3` | PASS | 傀 | faai3 | 14000 | CEDict |
| 160 | `maan6` | PASS | 幔 | maan6 | 14000 | CEDict |
| 161 | `gou1` | PASS | 膏 | gou1 | 9000 | CEDict |
| 162 | `dai1` | PASS | 低 | dai1 | 14000 | CEDict |
| 163 | `coeng4` | PASS | 牆 | coeng4 | 9000 | CEDict |
| 164 | `dyun2` | PASS | 短 | dyun2 | 14000 | CEDict |
| 165 | `fei4` | PASS | 肥 | fei4 | 14000 | CEDict |
| 166 | `sau3` | PASS | 秀 | sau3 | 9000 | CEDict |
| 167 | `gau6` | PASS | 柩 | gau6 | 14000 | CEDict |
| 168 | `cing1` | PASS | 秤 | cing1 | 9000 | CCanto |
| 169 | `maai5` | PASS | 買 | maai5 | 14000 | CEDict |
| 170 | `maai6` | PASS | 勱 | maai6 | 14000 | CEDict |
| 171 | `bei2` | PASS | 比 | bei2 | 13871 | CEDict |
| 172 | `wan2` | PASS | 穩 | wan2 | 14000 | CEDict |
| 173 | `paau2` | PASS | 跑 | paau2 | 14000 | CEDict |
| 174 | `co5` | PASS | 坐 | co5 | 14000 | CEDict |
| 175 | `kei5` | PASS | 徛 | kei5 | 14000 | CCanto |
| 176 | `se2` | PASS | 寫 | se2 | 14000 | CEDict |
| 177 | `duk6` | PASS | 毒 | duk6 | 12000 | CCanto |
| 178 | `sing1` | PASS | 勝 | sing1 | 14000 | CEDict |
| 179 | `hoeng1` | PASS | 香 | hoeng1 | 9000 | CEDict |
| 180 | `gong2` | PASS | 港 | gong2 | 9000 | CEDict |
| 181 | `si4` | PASS | 城 | sing4 | 14000 | CEDict |
| 182 | `din6` | PASS | 佃 | din6 | 14000 | CEDict |
| 183 | `waa2` | PASS | 剮 | waa2 | 14000 | CCanto |
| 184 | `cing4` | PASS | 成 | cing4 | 12960 | CCanto |
| 185 | `oi3` | PASS | 僾 | oi3 | 14000 | CEDict |
| 186 | `hei2` | PASS | 起 | hei2 | 13121 | CEDict |
| 187 | `lok6` | PASS | 樂 | lok6 | 14000 | CEDict |
| 188 | `hoi1` | PASS | 開 | hoi1 | 14000 | CCanto |
| 189 | `saan1` | PASS | 山 | saan1 | 9000 | CEDict |
| 190 | `ceot1` | PASS | 出 | ceot1 | 12545 | CEDict |
| 191 | `jap6` | PASS | 廿 | jap6 | 14000 | CCanto |
| 192 | `dak1` | PASS | 得 | dak1 | 12726 | CEDict |
| 193 | `jiu3` | PASS | 要 | jiu3 | 12474 | CEDict |
| 194 | `ho2` | PASS | 海 | hoi2 | 11329 | CEDict |
| 195 | `wui5` | PASS | 會 | wui5 | 14000 | CCanto |
| 196 | `zung6` | PASS | 重 | zung6 | 13528 | CCanto |
| 197 | `sing4` | PASS | 城 | sing4 | 9000 | CEDict |
| 198 | `do1` | PASS | 刀 | dou1 | 11500 | CEDict |
| 199 | `siu2` | PASS | 小 | siu2 | 13154 | CEDict |
| 200 | `cyun4` | PASS | 全 | cyun4 | 13451 | CEDict |
| 201 | `zing3` | PASS | 正 | zing3 | 13479 | CEDict |
| 202 | `cou4` | PASS | 嘈 | cou4 | 14000 | CEDict |
| 203 | `gwai3` | PASS | 季 | gwai3 | 14000 | CEDict |
| 204 | `peng4` | PASS | 平 | peng4 | 13919 | CCanto |
| 205 | `naan4` | PASS | 難 | naan4 | 14000 | CEDict |
| 206 | `ji4` | PASS | 弦 | jin4 | 11500 | CEDict |
| 207 | `gaan1` | PASS | 奸 | gaan1 | 14000 | CEDict |
| 208 | `lou5` | PASS | 佬 | lou5 | 12000 | CCanto |
| 209 | `zai2` | PASS | 仔 | zai2 | 14000 | CEDict |
| 210 | `mui1` | PASS | 咪 | mui1 | 14000 | CCanto |
| 211 | `gwo3` | PASS | 國 | gwok3 | 11500 | CEDict |
| 212 | `wun6` | PASS | 喚 | wun6 | 14000 | CEDict |
| 213 | `dong1` | PASS | 當 | dong1 | 14000 | CEDict |
| 214 | `zik1` | PASS | 即 | zik1 | 14000 | CEDict |
| 215 | `bo1` | PASS | 坡 | bo1 | 9000 | CEDict |
| 216 | `paai4` | PASS | 牌 | paai4 | 9000 | CEDict |
| 217 | `toi2` | PASS | 呔 | toi2 | 14000 | CCanto |
| 218 | `ji6` | PASS | 二 | ji6 | 13583 | CEDict |
| 219 | `saam1` | PASS | 三 | saam1 | 13455 | CEDict |
| 220 | `ling4` | PASS | 鈴 | ling4 | 9000 | CEDict |
| 221 | `sam` | PASS | 心 | sam1 | 8201 | CEDict |
| 222 | `sei` | PASS | 四 | sei3 | 13953 | CEDict |
| 223 | `jan` | PASS | 人 | jan4 | 6640 | CEDict |
| 224 | `gaa` | PASS | 家 | gaa1 | 7939 | CEDict |
| 225 | `san` | PASS | 神 | san4 | 8955 | CEDict |
| 226 | `fung` | PASS | 縫 | fung4 | 9000 | CEDict |
| 227 | `din` | PASS | 佃 | din6 | 14000 | CEDict |
| 228 | `ce` | PASS | 車 | ce1 | 9000 | CEDict |
| 229 | `sing` | PASS | 性 | sing3 | 8436 | CEDict |
| 230 | `ming` | PASS | 明 | ming4 | 13436 | CEDict |
| 231 | `cin` | PASS | 錢 | cin2 | 9000 | CEDict |
| 232 | `dung` | PASS | 洞 | dung6 | 9000 | CEDict |
| 233 | `wong` | PASS | 凰 | wong4 | 14000 | CEDict |
| 234 | `hung` | PASS | 孔 | hung2 | 9000 | CEDict |
| 235 | `gou` | PASS | 膏 | gou1 | 9000 | CEDict |
| 236 | `dai` | PASS | 睇 | dai6 | 12000 | CCanto |
| 237 | `hoi` | PASS | 海 | hoi2 | 8829 | CEDict |
| 238 | `faan` | PASS | 飯 | faan6 | 9000 | CEDict |
| 239 | `zau` | PASS | 酒 | zau2 | 9000 | CEDict |
| 240 | `bei` | PASS | 碑 | bei1 | 9000 | CEDict |
| 241 | `caa` | PASS | 茶 | caa4 | 9000 | CEDict |
| 242 | `gwai` | PASS | 季 | gwai3 | 14000 | CEDict |
| 243 | `tau` | PASS | 頭 | tau4 | 9000 | CEDict |
| 244 | `zou` | PASS | 做 | zou6 | 14000 | CEDict |
| 245 | `fo` | PASS | 科 | fo1 | 9000 | CEDict |
| 246 | `bo` | PASS | 坡 | bo1 | 9000 | CEDict |
| 247 | `tong` | PASS | 堂 | tong4 | 9000 | CEDict |
| 248 | `paai` | PASS | 牌 | paai4 | 9000 | CEDict |
| 249 | `wui` | PASS | 會 | wui2 | 9000 | CCanto |
| 250 | `zung` | PASS | 鐘 | zung1 | 9000 | CEDict |
| 251 | `zing` | PASS | 井 | zing2 | 11000 | CCanto |
| 252 | `gwok` | PASS | 國 | gwok3 | 9000 | CEDict |
| 253 | `tin` | PASS | 田 | tin4 | 9000 | CEDict |
| 254 | `mou` | PASS | 霧 | mou6 | 9000 | CEDict |
| 255 | `lei` | PASS | 梨 | lei4 | 9000 | CEDict |
| 256 | `heoi` | PASS | 佢 | heoi5 | 12000 | CCanto |
| 257 | `sai` | PASS | 些 | sai3 | 13180 | CCanto |
| 258 | `gei` | PASS | 機 | gei1 | 9000 | CCanto |
| 259 | `bat` | PASS | 筆 | bat1 | 9000 | CEDict |
| 260 | `keoi` | PASS | 區 | keoi1 | 9000 | CEDict |
| 261 | `hoeng1 gong2` | PASS | 香港 | hoeng1 gong2 | 21000 | CEDict |
| 262 | `zou2 san4` | PASS | 早晨 | zou2 san4 | 16000 | CEDict |
| 263 | `baai1 baai3` | PASS | 拜拜 | baai1 baai3 | 21000 | CEDict |
| 264 | `sing1 kei4` | PASS | 星期 | sing1 kei4 | 16000 | CEDict |
| 265 | `dim2 sam1` | PASS | 點心 | dim2 sam1 | 20201 | CEDict |
| 266 | `siu1 maai6` | PASS | 燒賣 | siu1 maai6 | 21000 | CEDict |
| 267 | `coeng2 fan2` | PASS | 腸粉 | coeng2 fan2 | 21000 | CEDict |
| 268 | `faan1 gung1` | PASS | 番工 | faan1 gung1 | 20412 | CCanto |
| 269 | `fong3 gung1` | PASS | 放工 | fong3 gung1 | 20412 | CEDict |
| 270 | `sik6 faan6` | PASS | 食飯 | sik6 faan6 | 21000 | CCanto |
| 271 | `jam2 caa4` | PASS | 飲茶 | jam2 caa4 | 19000 | CEDict |
| 272 | `gau2 lung4` | PASS | 九龍 | gau2 lung4 | 21000 | CEDict |
| 273 | `dei6 tit3` | PASS | 地鐵 | dei6 tit3 | 19296 | CEDict |
| 274 | `baa1 si2` | PASS | 巴士 | baa1 si2 | 21000 | CEDict |
| 275 | `din6 waa2` | PASS | 電話 | din6 waa2 | 16000 | CEDict |
| 276 | `din6 nou5` | PASS | 電腦 | din6 nou5 | 16000 | CEDict |
| 277 | `hok6 haau6` | PASS | 學校 | hok6 haau6 | 16000 | CEDict |
| 278 | `ji1 jyun2` | PASS | 醫院 | ji1 jyun2 | 16000 | CEDict |
| 279 | `ging2 caat3` | PASS | 警察 | ging2 caat3 | 16000 | CEDict |
| 280 | `lou5 si1` | PASS | 老師 | lou5 si1 | 15765 | CEDict |
| 281 | `pang4 jau5` | PASS | 朋友 | pang4 jau5 | 16000 | CEDict |
| 282 | `gung1 si1` | PASS | 公司 | gung1 si1 | 15409 | CEDict |
| 283 | `hou2 sik6` | PASS | 好食 | hou2 sik6 | 20152 | CCanto |
| 284 | `hou2 waan2` | PASS | 好玩 | hou2 waan2 | 20152 | CEDict |
| 285 | `ji6 sap6` | PASS | 二十 | ji6 sap6 | 19930 | CEDict |
| 286 | `jat1 baak3` | PASS | 一百 | jat1 baak3 | 18149 | CCanto |
| 287 | `jat1 cin1` | PASS | 一千 | jat1 cin1 | 18149 | CCanto |
| 288 | `dim2 joeng2` | PASS | 点样 | dim2 joeng2 | 19652 | CCanto |
| 289 | `bin1 dou6` | PASS | 焉道 | bin1 dou6 | 19891 | CCanto |
| 290 | `gei2 si4` | PASS | 幾時 | gei2 si4 | 21000 | CEDict |
| 291 | `mat1 je5` | PASS | 乜嘢 | mat1 je5 | 19000 | CEDict |
| 292 | `dim2 gaai2` | PASS | 點解 | dim2 gaai2 | 20874 | CCanto |
| 293 | `bin1 go3` | PASS | 邊个 | bin1 go3 | 19083 | CCanto |
| 294 | `gei2 noi6` | PASS | 幾耐 | gei2 noi6 | 21000 | CCanto |
| 295 | `sai3 lou6` | PASS | 細路 | sai3 lou6 | 21000 | CCanto |
| 296 | `hoi1 sam1` | PASS | 開心 | hoi1 sam1 | 20201 | CEDict |
| 297 | `san1 fu2` | PASS | 辛苦 | san1 fu2 | 21000 | CEDict |
| 298 | `ho2 ji5` | PASS | 可以 | ho2 ji5 | 17947 | CEDict |
| 299 | `daan6 hai6` | PASS | 但係 | daan6 hai6 | 20247 | CCanto |
| 300 | `ji1 ging1` | FAIL | 燕京 | jin1 ging1 | 23500 | CEDict |
| 301 | `jyun4 loi4` | PASS | 原來 | jyun4 loi4 | 20837 | CEDict |
| 302 | `gei1 wui6` | PASS | 機會 | gei1 wui6 | 16000 | CEDict |
| 303 | `man6 tai4` | PASS | 問題 | man6 tai4 | 16000 | CEDict |
| 304 | `zung1 ji3` | PASS | 中意 | zung1 ji3 | 18451 | CEDict |
| 305 | `gwaan1 hai6` | PASS | 關係 | gwaan1 hai6 | 16000 | CEDict |
| 306 | `si4 gaan3` | PASS | 時間 | si4 gaan3 | 16000 | CEDict |
| 307 | `zou2 san4` | PASS | 早晨 | zou2 san4 | 16000 | CEDict |
| 308 | `gam1 nin2` | FAIL | - | - | - | - |
| 309 | `ceot1 heoi3` | PASS | 出去 | ceot1 heoi3 | 18552 | CEDict |
| 310 | `faan1 lai4` | PASS | 返來 | faan1 lai4 | 21000 | CCanto |
| 311 | `zou2 can1` | PASS | 早餐 | zou2 caan1 | 36000 | CEDict |
| 312 | `aan3 zau3` | PASS | 晏晝 | aan3 zau3 | 21000 | CCanto |
| 313 | `maan5 faan6` | PASS | 晚飯 | maan5 faan6 | 16000 | CEDict |
| 314 | `daai6 hok6` | PASS | 大學 | daai6 hok6 | 14212 | CEDict |
| 315 | `zung1 hok6` | PASS | 中學 | zung1 hok6 | 14165 | CEDict |
| 316 | `siu2 hok6` | PASS | 小學 | siu2 hok6 | 20154 | CEDict |
| 317 | `daa2 bo1` | PASS | 打啵 | daa2 bo1 | 20946 | CEDict |
| 318 | `tai2 hei3` | PASS | 睇戲 | tai2 hei3 | 21000 | CCanto |
| 319 | `maai5 je5` | PASS | 買嘢 | maai5 je5 | 21000 | CCanto |
| 320 | `zung1 gwok3` | PASS | 中國 | zung1 gwok3 | 19165 | CEDict |
| 321 | `jing1 gwok3` | PASS | 英國 | jing1 gwok3 | 26000 | CEDict |
| 322 | `jat6 bun2` | PASS | 日本 | jat6 bun2 | 19487 | CEDict |
| 323 | `toi4 waan1` | PASS | 台灣 | toi4 waan1 | 21000 | CEDict |
| 324 | `leng3 zai2` | PASS | 靚仔 | leng3 zai2 | 21000 | CEDict |
| 325 | `leng3 neoi5` | PASS | 靚女 | leng3 neoi5 | 20951 | CEDict |
| 326 | `lek1 zai2` | PASS | 叻仔 | lek1 zai2 | 21000 | CCanto |
| 327 | `daai6 gaa1` | FAIL | 大街 | daai6 gaai1 | 16712 | CEDict |
| 328 | `zi6 gei2` | PASS | 自己 | zi6 gei2 | 19404 | CEDict |
| 329 | `keoi5 dei6` | PASS | 佢地 | keoi5 dei6 | 19296 | CCanto |
| 330 | `ngo5 dei6` | PASS | 我地 | ngo5 dei6 | 17036 | CCanto |
| 331 | `m4 sai2` | PASS | 唔使 | m4 sai2 | 20416 | CCanto |
| 332 | `m4 zi1` | PASS | 唔知 | m4 zi1 | 20448 | CCanto |
| 333 | `jau5 mou5` | PASS | 有冇 | jau5 mou5 | 18687 | CCanto |
| 334 | `haa5 ci3` | FAIL | 沙蟹桌 | saa1 haai5 coek3 | 90500 | CCanto |
| 335 | `soeng5 min6` | FAIL | 七情上面 | cat1 cing4 soeng5 min6 | 121745 | CCanto |
| 336 | `haa5 min6` | FAIL | 厚面皮 | hau5 min6 pei4 | 67120 | CCanto |
| 337 | `jat1 ding6` | PASS | 一定 | jat1 ding6 | 17275 | CEDict |
| 338 | `zoi3 gin3` | PASS | 再建 | zoi3 gin3 | 20971 | CEDict |
| 339 | `gam2 joeng2` | PASS | 噉樣 | gam2 joeng2 | 21000 | CCanto |
| 340 | `sou3 hok6` | PASS | 數學 | sou3 hok6 | 21000 | CEDict |
| 341 | `lik6 si2` | PASS | 歷史 | lik6 si2 | 16000 | CEDict |
| 342 | `jing1 man2` | FAIL | 英文堂 | jing1 man2 tong4 | 47559 | CCanto |
| 343 | `zung1 man2` | FAIL | 繁體中文 | faan4 tai2 zung1 man2 | 122724 | CCanto |
| 344 | `tau4 faat3` | PASS | 頭髮 | tau4 faat3 | 21000 | CEDict |
| 345 | `hoi2 sin1` | PASS | 海鮮 | hoi2 sin1 | 20829 | CEDict |
| 346 | `gaa1 fei1` | PASS | 噶霏 | gaa1 fei1 | 21000 | CEDict |
| 347 | `naai5 caa4` | PASS | 奶茶 | naai5 caa4 | 21000 | CEDict |
| 348 | `gai1 daan2` | PASS | 雞蛋 | gai1 daan2 | 16000 | CEDict |
| 349 | `ngau4 juk6` | PASS | 牛肉 | ngau4 juk6 | 21000 | CEDict |
| 350 | `zyu1 juk6` | PASS | 珠玉 | zyu1 juk6 | 21000 | CEDict |
| 351 | `gai1 juk6` | PASS | 雞肉 | gai1 juk6 | 21000 | CEDict |
| 352 | `sang1 jat6` | PASS | 生日 | saang1 jat6 | 33923 | CEDict |
| 353 | `san1 nin4` | PASS | 新年 | san1 nin4 | 14408 | CEDict |
| 354 | `sing3 daan3` | PASS | 聖誕 | sing3 daan3 | 26000 | CEDict |
| 355 | `tin1 hei3` | PASS | 天氣 | tin1 hei3 | 20133 | CEDict |
| 356 | `lok6 jyu5` | PASS | 落雨 | lok6 jyu5 | 21000 | CCanto |
| 357 | `ceoi1 fung1` | PASS | 吹風 | ceoi1 fung1 | 21000 | CCanto |
| 358 | `tai2 syu1` | PASS | 體書 | tai2 syu1 | 21000 | CEDict |
| 359 | `fan3 gaau3` | PASS | 瞓覺 | fan3 gaau3 | 19000 | CEDict |
| 360 | `sai2 min6` | PASS | 洗面 | sai2 min6 | 20120 | CEDict |
| 361 | `cung1 loeng4` | PASS | 沖涼 | cung1 loeng4 | 21000 | CEDict |
| 362 | `tai2 ji1 sang1` | PASS | 睇醫生 | tai2 ji1 sang1 | 26647 | CCanto |
| 363 | `haang4 gaai1` | PASS | 行街 | haang4 gaai1 | 19896 | CCanto |
| 364 | `daa2 din6 waa2` | PASS | 打電話 | daa2 din6 waa2 | 27946 | CEDict |
| 365 | `zou6 je5` | PASS | 做嘢 | zou6 je5 | 21000 | CCanto |
| 366 | `gung1 jyun2` | PASS | 公園 | gung1 jyun2 | 15409 | CEDict |
| 367 | `caai1 gwun2` | PASS | 差館 | caai1 gun2 | 41000 | CCanto |
| 368 | `jau4 guk2` | FAIL | 油管 | jau4 gun2 | 41000 | CCanto |
| 369 | `gei1 coeng4` | PASS | 機場 | gei1 coeng4 | 16000 | CEDict |
| 370 | `fo2 ce1` | PASS | 火車 | fo2 ce1 | 16000 | CEDict |
| 371 | `jau5 jat6` | PASS | 有日 | jau5 jat6 | 17963 | CCanto |
| 372 | `cin4 min6` | PASS | 前面 | cin4 min6 | 19349 | CEDict |
| 373 | `hau6 min6` | PASS | 後面 | hau6 min6 | 20120 | CEDict |
| 374 | `zo2 min6` | PASS | 左面 | zo2 min6 | 20120 | CEDict |
| 375 | `jau6 min6` | PASS | 右面 | jau6 min6 | 20120 | CCanto |
| 376 | `fei1 gei1` | PASS | 飛機 | fei1 gei1 | 16000 | CEDict |
| 377 | `siu2 sam1` | PASS | 小心 | siu2 sam1 | 19355 | CEDict |
| 378 | `m4 gam2` | PASS | 唔敢 | m4 gam2 | 21000 | CCanto |
| 379 | `hou2 do1` | PASS | 好多 | hou2 do1 | 19147 | CEDict |
| 380 | `hou2 siu2` | PASS | 好少 | hou2 siu2 | 20115 | CCanto |
| 381 | `laa1` | PASS | 了 | laa1 | 11509 | CCanto |
| 382 | `laa3` | PASS | 喇 | laa3 | 14000 | CEDict |
| 383 | `wo3` | PASS | 喎 | wo3 | 14000 | CCanto |
| 384 | `wo5` | PASS | 喎 | wo5 | 14000 | CCanto |
| 385 | `gaa3` | PASS | 覺 | gaau3 | 11500 | CEDict |
| 386 | `me1` | PASS | 孭 | me1 | 12000 | CCanto |
| 387 | `ze1` | PASS | 啫 | ze1 | 12000 | CCanto |
| 388 | `lo2` | PASS | 蓏 | lo2 | 14000 | CEDict |
| 389 | `aai3` | PASS | 隘 | aai3 | 14000 | CEDict |
| 390 | `gaau2` | PASS | 搞 | gaau2 | 12000 | CCanto |
| 391 | `lek1` | PASS | 叻 | lek1 | 14000 | CCanto |
| 392 | `naa2` | PASS | 乸 | naa2 | 12000 | CEDict |
| 393 | `lou5` | PASS | 佬 | lou5 | 12000 | CCanto |
| 394 | `bik1` | PASS | 壁 | bik1 | 14000 | CEDict |
| 395 | `king1` | PASS | 傾 | king1 | 14000 | CEDict |
| 396 | `cou4` | PASS | 嘈 | cou4 | 14000 | CEDict |
| 397 | `dau2` | PASS | 豆 | dau2 | 9000 | CEDict |
| 398 | `go2` | PASS | 嗰 | go2 | 12000 | CCanto |
| 399 | `pek3` | PASS | 劈 | pek3 | 14000 | CEDict |
| 400 | `caat3` | PASS | 刷 | caat3 | 14000 | CEDict |
| 401 | `gwaai3` | FAIL | 夬 | gwaai3 | 14000 | CEDict |
| 402 | `haam4` | PASS | 函 | haam4 | 14000 | CEDict |
| 403 | `laang5` | PASS | 冷 | laang5 | 14000 | CEDict |
| 404 | `song2` | PASS | 爽 | song2 | 12000 | CCanto |
| 405 | `dung3` | PASS | 棟 | dung3 | 12000 | CCanto |
| 406 | `gwaai1` | PASS | 乖 | gwaai1 | 14000 | CEDict |
| 407 | `ngaam1` | PASS | 啱 | ngaam1 | 12000 | CCanto |
| 408 | `gwai6` | PASS | 櫃 | gwai6 | 14000 | CEDict |
| 409 | `saai1` | PASS | 嘥 | saai1 | 12000 | CCanto |
| 410 | `daap3` | PASS | 搭 | daap3 | 14000 | CEDict |
| 411 | `gu2` | PASS | 鼓 | gu2 | 9000 | CEDict |
| 412 | `gai2` | PASS | 偈 | gai2 | 14000 | CCanto |
| 413 | `duk1` | PASS | 篤 | duk1 | 12000 | CCanto |
| 414 | `paau4` | PASS | 刨 | paau4 | 14000 | CEDict |
| 415 | `lok6 heoi3` | PASS | 落去 | lok6 heoi3 | 20007 | CCanto |
| 416 | `jat1 cai4` | PASS | 一齊 | jat1 cai4 | 18149 | CEDict |
| 417 | `m4 hai6` | PASS | 唔係 | m4 hai6 | 21000 | CCanto |
| 418 | `jau5 liu2` | PASS | 有料 | jau5 liu2 | 16687 | CCanto |
| 419 | `sai2 cin2` | PASS | 洗錢 | sai2 cin2 | 19000 | CCanto |
| 420 | `haang4 wan6` | PASS | 行運 | haang4 wan6 | 19896 | CCanto |
| 421 | `gwo3 hoi2` | PASS | 過海 | gwo3 hoi2 | 20829 | CCanto |
| 422 | `hoi1 gung1` | PASS | 開工 | hoi1 gung1 | 20412 | CEDict |
| 423 | `zyun2 tau4` | PASS | 轉頭 | zyun2 tau4 | 19000 | CCanto |
| 424 | `jat1 zan6` | PASS | 一陣 | jat1 zan6 | 18149 | CEDict |
| 425 | `ap1` | PASS | 噏 | ap1 | 12000 | CCanto |
| 426 | `zaa3` | PASS | 債 | zaai3 | 11500 | CEDict |
| 427 | `lai4` | PASS | 嚟 | lai4 | 12000 | CCanto |
| 428 | `maa3` | PASS | 嗎 | maa3 | 14000 | CEDict |
| 429 | `gau6` | PASS | 柩 | gau6 | 14000 | CEDict |
| 430 | `zo2` | PASS | 座 | zo2 | 9000 | CCanto |
| 431 | `lou` | PASS | 路 | lou6 | 9000 | CEDict |
| 432 | `gin` | PASS | 勁 | ging3 | 11500 | CEDict |
| 433 | `faa` | PASS | 花 | faa1 | 9000 | CEDict |
| 434 | `sin` | PASS | 線 | sin3 | 9000 | CEDict |
| 435 | `bei` | PASS | 碑 | bei1 | 9000 | CEDict |
| 436 | `daa` | PASS | 單 | daan1 | 11500 | CEDict |
| 437 | `wai` | PASS | 胃 | wai6 | 9000 | CEDict |
| 438 | `cung` | PASS | 松 | cung4 | 9000 | CEDict |
| 439 | `maa` | PASS | 罵 | maa6 | 9000 | CEDict |
| 440 | `baa` | FAIL | 壩 | baa3 | 9000 | CEDict |
| 441 | `tin` | PASS | 田 | tin4 | 9000 | CEDict |
| 442 | `ming` | PASS | 明 | ming4 | 13436 | CEDict |
| 443 | `syu` | PASS | 書 | syu1 | 9000 | CEDict |
| 444 | `hei` | PASS | 器 | hei3 | 9000 | CEDict |
| 445 | `gei` | PASS | 機 | gei1 | 9000 | CCanto |
| 446 | `jyu` | PASS | 雨 | jyu5 | 9000 | CEDict |
| 447 | `hok` | PASS | 殼 | hok3 | 12000 | CCanto |
| 448 | `din` | PASS | 佃 | din6 | 14000 | CEDict |
| 449 | `zoi` | PASS | 在 | zoi6 | 11567 | CEDict |
| 450 | `sik` | PASS | 色 | sik1 | 9000 | CEDict |
| 451 | `toi` | PASS | 能 | toi4 | 12672 | CCanto |
| 452 | `hou` | PASS | 號 | hou6 | 9000 | CEDict |
| 453 | `gwai` | PASS | 季 | gwai3 | 14000 | CEDict |
| 454 | `seoi` | PASS | 水 | seoi2 | 13880 | CEDict |
| 455 | `gung` | PASS | 弓 | gung1 | 9000 | CEDict |
| 456 | `fei` | PASS | 匪 | fei2 | 14000 | CEDict |
| 457 | `ceoi` | PASS | 脆 | ceoi3 | 12000 | CCanto |
| 458 | `ngau` | PASS | 牛 | ngau4 | 11000 | CCanto |
| 459 | `zing` | PASS | 井 | zing2 | 11000 | CCanto |
| 460 | `gwok` | PASS | 國 | gwok3 | 9000 | CEDict |
| 461 | `gaai` | PASS | 街 | gaai1 | 9000 | CEDict |
| 462 | `lok` | PASS | 樂 | lok6 | 14000 | CEDict |
| 463 | `bou` | PASS | 報 | bou3 | 9000 | CEDict |
| 464 | `jing` | PASS | 蠅 | jing4 | 9000 | CEDict |
| 465 | `pou` | PASS | 匍 | pou4 | 14000 | CEDict |
| 466 | `cin` | PASS | 錢 | cin2 | 9000 | CEDict |
| 467 | `keoi` | PASS | 區 | keoi1 | 9000 | CEDict |
| 468 | `lai` | PASS | 禮 | lai5 | 9000 | CEDict |
| 469 | `mou` | PASS | 霧 | mou6 | 9000 | CEDict |
| 470 | `fan` | PASS | 墳 | fan4 | 9000 | CEDict |
| 471 | `mother` | PASS | 姨 | ji4 | 19000 | CEDict |
| 472 | `father` | PASS | 伯 | baak3 | 19000 | CEDict |
| 473 | `brother` | PASS | 兄 | hing1 | 19600 | CEDict |
| 474 | `sister` | PASS | 甥 | sang1 | 19000 | CEDict |
| 475 | `rice` | PASS | 米 | mai5 | 14000 | CEDict |
| 476 | `fish` | PASS | 魚 | jyu2 | 14000 | CEDict |
| 477 | `chicken` | PASS | 雞 | gai1 | 19400 | CEDict |
| 478 | `tea` | PASS | 班 | baan1 | 14000 | CEDict |
| 479 | `coffee` | PASS | 咖 | gaa3 | 19000 | CEDict |
| 480 | `red` | PASS | 丹 | daan1 | 19000 | CEDict |
| 481 | `blue` | PASS | 滄 | cong1 | 19000 | CEDict |
| 482 | `green` | PASS | 碧 | bik1 | 19000 | CEDict |
| 483 | `black` | PASS | 淄 | zi1 | 19000 | CEDict |
| 484 | `white` | PASS | 白 | baak6 | 19000 | CEDict |
| 485 | `hand` | PASS | 手 | sau2 | 13536 | CEDict |
| 486 | `head` | PASS | 頭 | tau4 | 14000 | CEDict |
| 487 | `mouth` | PASS | 嘴 | zeoi2 | 14000 | CEDict |
| 488 | `walk` | PASS | 行 | hang4 | 18196 | CEDict |
| 489 | `sleep` | PASS | 覺 | gaau3 | 14700 | CEDict |
| 490 | `buy` | PASS | 糴 | dek6 | 19000 | CCanto |
| 491 | `sell` | PASS | 售 | sau6 | 19300 | CEDict |
| 492 | `give` | PASS | 生 | saang1 | 18947 | CEDict |
| 493 | `read` | PASS | 念 | nim6 | 14300 | CEDict |
| 494 | `write` | PASS | 筆 | bat1 | 16500 | CEDict |
| 495 | `hot` | PASS | 喝 | hot3 | 14000 | CEDict |
| 496 | `cold` | PASS | 冷 | laang5 | 19000 | CEDict |
| 497 | `fast` | PASS | 鎖 | so2 | 18700 | CCanto |
| 498 | `slow` | PASS | 徐 | ceoi4 | 19000 | CEDict |
| 499 | `new` | PASS | 新 | san1 | 18636 | CEDict |
| 500 | `old` | PASS | 店 | dim3 | 14500 | CEDict |
| 501 | `happy` | PASS | 氹 | tam5 | 17900 | CCanto |
| 502 | `school` | PASS | 校 | haau3 | 14000 | CCanto |
| 503 | `hospital` | PASS | 醫院 | ji1 jyun2 | 21000 | CEDict |
| 504 | `morning` | PASS | 晨 | san4 | 19000 | CEDict |
| 505 | `night` | PASS | 夜 | je6 | 19000 | CEDict |
| 506 | `year` | PASS | 年 | nin4 | 12772 | CEDict |
| 507 | `month` | PASS | 正 | zing3 | 19079 | CEDict |
| 508 | `week` | PASS | 週 | zau1 | 19000 | CCanto |
| 509 | `friend` | PASS | 友 | jau5 | 19000 | CEDict |
| 510 | `child` | PASS | 兒 | ji4 | 19000 | CEDict |
| 511 | `teacher` | PASS | 師 | si1 | 19000 | CEDict |
| 512 | `student` | PASS | 李 | lei5 | 19000 | CCanto |
| 513 | `doctor` | PASS | 醫生 | ji1 sang1 | 19647 | CEDict |
| 514 | `car` | PASS | 車 | ce1 | 14000 | CEDict |
| 515 | `food` | PASS | 飯 | faan6 | 14000 | CCanto |
| 516 | `book` | PASS | 書 | syu1 | 14000 | CEDict |
| 517 | `love` | PASS | 嫣 | jin1 | 19000 | CEDict |
| 518 | `work` | PASS | 作 | zok3 | 17876 | CEDict |
| 519 | `rain` | PASS | 雨 | jyu5 | 14000 | CEDict |
| 520 | `wind` | PASS | 窗 | coeng1 | 14000 | CEDict |
| 521 | `sun` | FAIL | 娀 | sung1 | 16500 | CEDict |
| 522 | `moon` | PASS | 月 | jyut6 | 13690 | CEDict |
| 523 | `flower` | PASS | 花 | faa1 | 14000 | CEDict |
| 524 | `mountain` | PASS | 山 | saan1 | 14000 | CEDict |
| 525 | `river` | PASS | 江 | gong1 | 14000 | CEDict |
| 526 | `road` | PASS | 道 | dou6 | 12891 | CEDict |
| 527 | `telephone` | PASS | 電話 | din6 waa2 | 21000 | CEDict |
| 528 | `police` | PASS | 警察 | ging2 caat3 | 21000 | CEDict |
| 529 | `thank` | PASS | 謝 | ze6 | 19300 | CEDict |
| 530 | `sorry` | PASS | 惋 | jyun2 | 24000 | CCanto |
| 531 | `人` | PASS | 人 | jan4 | 6640 | CEDict |
| 532 | `大` | PASS | 大 | daai6 | 12212 | CEDict |
| 533 | `小` | PASS | 小 | siu2 | 13154 | CEDict |
| 534 | `天` | PASS | 天 | tin1 | 13133 | CEDict |
| 535 | `地` | PASS | 地 | dei6 | 7296 | CEDict |
| 536 | `水` | PASS | 水 | seoi2 | 13880 | CEDict |
| 537 | `火` | PASS | 火 | fo2 | 14000 | CEDict |
| 538 | `山` | PASS | 山 | saan1 | 9000 | CEDict |
| 539 | `日` | PASS | 日 | jat6 | 13276 | CEDict |
| 540 | `月` | PASS | 月 | jyut6 | 8690 | CEDict |
| 541 | `手` | PASS | 手 | sau2 | 8536 | CEDict |
| 542 | `口` | PASS | 口 | hau2 | 13915 | CEDict |
| 543 | `心` | PASS | 心 | sam1 | 8201 | CEDict |
| 544 | `目` | PASS | 目的 | muk6 dik1 | 12170 | CEDict |
| 545 | `車` | PASS | 車 | ce1 | 9000 | CEDict |
| 546 | `馬` | PASS | 馬 | maa5 | 9000 | CEDict |
| 547 | `花` | PASS | 花 | faa1 | 9000 | CEDict |
| 548 | `魚` | PASS | 魚 | jyu2 | 9000 | CEDict |
| 549 | `鳥` | PASS | 鳥 | niu5 | 9000 | CEDict |
| 550 | `學校` | PASS | 學校 | hok6 haau6 | 16000 | CEDict |
| 551 | `醫院` | PASS | 醫院 | ji1 jyun2 | 16000 | CEDict |
| 552 | `巴士` | PASS | 巴士 | baa1 si2 | 21000 | CEDict |
| 553 | `地鐵` | PASS | 地鐵 | dei6 tit3 | 19296 | CEDict |
| 554 | `電話` | PASS | 電話 | din6 waa2 | 16000 | CEDict |
| 555 | `電腦` | PASS | 電腦 | din6 nou5 | 16000 | CEDict |
| 556 | `警察` | PASS | 警察 | ging2 caat3 | 16000 | CEDict |
| 557 | `老師` | PASS | 老師 | lou5 si1 | 15765 | CEDict |
| 558 | `中國` | PASS | 中國 | zung1 gwok3 | 19165 | CEDict |
| 559 | `香港` | PASS | 香港 | hoeng1 gong2 | 21000 | CEDict |
| 560 | `朋友` | PASS | 朋友 | pang4 jau5 | 16000 | CEDict |
| 561 | `唔該` | PASS | 唔該 | m4 goi1 | 21000 | CCanto |
| 562 | `多謝` | PASS | 多謝 | do1 ze6 | 19995 | CEDict |
| 563 | `飛機` | PASS | 飛機 | fei1 gei1 | 16000 | CEDict |
| 564 | `公司` | PASS | 公司 | gung1 si1 | 15409 | CEDict |
| 565 | `時間` | PASS | 時間 | si4 gaan3 | 16000 | CEDict |
| 566 | `開心` | PASS | 開心 | hoi1 sam1 | 20201 | CEDict |
| 567 | `今日` | PASS | 今日 | gam1 jat6 | 20276 | CEDict |
| 568 | `明天` | PASS | 天明 | tin1 ming4 | 19569 | CEDict |
| 569 | `生日` | PASS | 生日 | saang1 jat6 | 13923 | CEDict |
| 570 | `新年` | PASS | 新年 | san1 nin4 | 14408 | CEDict |
| 571 | `Nei5` | PASS | 你 | nei5 | 12614 | CEDict |
| 572 | `HOU2` | PASS | 好 | hou2 | 13152 | CEDict |
| 573 | `s` | PASS | 所 | so2 | 10413 | CEDict |
| 574 | `g` | PASS | 歌 | go1 | 11500 | CEDict |
| 575 | `l` | PASS | 鑼 | lo4 | 11500 | CEDict |
| 576 | `go` | PASS | 歌 | go1 | 9000 | CEDict |
| 577 | `ga` | PASS | 家 | gaa1 | 10439 | CEDict |
| 578 | `la` | PASS | 林 | lam4 | 11500 | CEDict |
| 579 | `gam1` | PASS | 今 | gam1 | 14000 | CEDict |
| 580 | `gam2` | PASS | 咁 | gam2 | 12000 | CCanto |
| 581 | `gam3` | PASS | 咁 | gam3 | 12000 | CCanto |
| 582 | `si1` | PASS | 絲 | si1 | 9000 | CEDict |
| 583 | `si6` | PASS | 事 | si6 | 7960 | CCanto |
| 584 | `ngaang6` | PASS | 硬 | ngaang6 | 14000 | CEDict |
| 585 | `gwik1` | PASS | 郤 | gwik1 | 14000 | CEDict |
| 586 | `zoeng1` | PASS | 將 | zoeng1 | 14000 | CEDict |
| 587 | `jau5 mou5` | PASS | 有冇 | jau5 mou5 | 18687 | CCanto |
| 588 | `hai6 m4 hai6` | FAIL | - | - | - | - |
| 589 | `hou2 m4 hou2` | FAIL | - | - | - | - |
| 590 | `jat1 go3 jan4` | PASS | 一個人 | jat1 go3 jan4 | 22789 | CEDict |
| 591 | `jat1 di1` | PASS | 一啲 | jat1 di1 | 18149 | CCanto |
| 592 | `saam1 go3` | FAIL | 三角 | saam1 gok3 | 22955 | CEDict |
| 593 | `gaa1 jan4` | PASS | 家人 | gaa1 jan4 | 17579 | CEDict |
| 594 | `daai6 gaa1` | FAIL | 大街 | daai6 gaai1 | 16712 | CEDict |
| 595 | `aa1` | PASS | 丫 | aa1 | 14000 | CEDict |
| 596 | `aa4` | PASS | 啊 | aa4 | 14000 | CCanto |
| 597 | `sap6 ji6` | PASS | 十二 | sap6 ji6 | 19930 | CEDict |
| 598 | `baat3 jyut6` | PASS | 八月 | baat3 jyut6 | 20690 | CEDict |
| 599 | `sing1 kei4 jat1` | PASS | 星期一 | sing1 kei4 jat1 | 25149 | CEDict |
| 600 | `hou2 do1 ze6` | FAIL | 好得滯 | hou2 dak1 zai6 | 65878 | CCanto |
| 601 | `ge` | FAIL | 機 | gei1 | 11500 | CCanto |
| 602 | `do` | FAIL | 道 | dou6 | 10391 | CEDict |
| 603 | `mo` | FAIL | 霧 | mou6 | 11500 | CEDict |
| 604 | `to` | FAIL | 圖 | tou4 | 11500 | CEDict |
| 605 | `di` | PASS | 的 | di1 | 10195 | CCanto |
| 606 | `co` | FAIL | 草 | cou2 | 11500 | CEDict |
| 607 | `do1` | FAIL | 刀 | dou1 | 11500 | CEDict |
| 608 | `do6` | FAIL | 道 | dou6 | 10391 | CEDict |
| 609 | `do3` | FAIL | 道 | dou3 | 10391 | CCanto |
| 610 | `si` | PASS | 事 | si6 | 7960 | CCanto |
| 611 | `go` | PASS | 歌 | go1 | 9000 | CEDict |
| 612 | `lo` | PASS | 鑼 | lo4 | 9000 | CEDict |
| 613 | `se` | PASS | 蛇 | se4 | 9000 | CEDict |
| 614 | `bo` | PASS | 坡 | bo1 | 9000 | CEDict |
| 615 | `zo` | PASS | 座 | zo6 | 9000 | CEDict |
| 616 | `fo` | PASS | 科 | fo1 | 9000 | CEDict |
| 617 | `so` | PASS | 所 | so2 | 7913 | CEDict |
| 618 | `no` | PASS | 那 | no5 | 12713 | CCanto |
| 619 | `ge3` | PASS | 嘅 | ge3 | 14000 | CCanto |
| 620 | `ge2` | PASS | 嘅 | ge2 | 14000 | CCanto |
| 621 | `mo5` | PASS | 冇 | mo5 | 12000 | CCanto |
| 622 | `di1` | PASS | 的 | di1 | 10195 | CCanto |
| 623 | `to1` | PASS | 他 | to1 | 11797 | CCanto |
| 624 | `se1` | PASS | 些 | se1 | 13180 | CEDict |
| 625 | `da` | PASS | 豆 | dau2 | 11500 | CEDict |
| 626 | `ba` | PASS | 壩 | baa3 | 11500 | CEDict |
| 627 | `ga` | PASS | 家 | gaa1 | 10439 | CEDict |
| 628 | `ge do` | PASS | 基多 | gei1 do1 | 22495 | CEDict |
| 629 | `si go` | PASS | 詩歌 | si1 go1 | 16000 | CEDict |
| 630 | `do di` | PASS | 多啲 | do1 di1 | 19995 | CCanto |
| 631 | `lo ge` | PASS | 圈 | hyun1 | 23500 | CEDict |
| 632 | `zo ge` | PASS | 座機 | zo6 gei1 | 23500 | CEDict |
| 633 | `so` | PASS | 所 | so2 | 7913 | CEDict |
| 634 | `zo2` | PASS | 座 | zo2 | 9000 | CCanto |
| 635 | `bo1` | PASS | 坡 | bo1 | 9000 | CEDict |
| 636 | `fo1` | PASS | 科 | fo1 | 9000 | CEDict |
| 637 | `go3` | FAIL | 角 | gok3 | 11500 | CEDict |
| 638 | `lo3` | PASS | 摞 | lo3 | 14000 | CEDict |
| 639 | `si6` | PASS | 事 | si6 | 7960 | CCanto |
| 640 | `si1` | PASS | 絲 | si1 | 9000 | CEDict |
| 641 | `go1` | PASS | 歌 | go1 | 9000 | CEDict |
| 642 | `lo4` | PASS | 鑼 | lo4 | 9000 | CEDict |
| 643 | `se4` | PASS | 蛇 | se4 | 9000 | CEDict |
| 644 | `do di` | PASS | 多啲 | do1 di1 | 19995 | CCanto |
| 645 | `mo ge` | PASS | 月 | jyut6 | 21390 | CEDict |
| 646 | `so do` | PASS | 所多 | so2 do1 | 18908 | CEDict |
| 647 | `do2` | FAIL | 島 | dou2 | 11500 | CEDict |
| 648 | `mo1` | PASS | 么 | mo1 | 13003 | CCanto |
| 649 | `co1` | PASS | 初 | co1 | 14000 | CEDict |
| 650 | `no5` | PASS | 那 | no5 | 12713 | CCanto |
