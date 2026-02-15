# Dictionary Ranking Evaluation Report

Generated: 2026-02-15 22:40:51

## Summary

- **Total queries**: 100
- **Passed**: 96 (96.0%)
- **Failed**: 4 (4.0%)

## Category Results

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| single_tone | 30 | 29 | 1 | 97% |
| single_no_tone | 10 | 10 | 0 | 100% |
| multi_syllable | 20 | 17 | 3 | 85% |
| cantonese_vocab | 10 | 10 | 0 | 100% |
| partial_prefix | 10 | 10 | 0 | 100% |
| english | 10 | 10 | 0 | 100% |
| character | 5 | 5 | 0 | 100% |
| edge_case | 5 | 5 | 0 | 100% |

## Failed Queries (4)

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

## Pattern Analysis

### Source Distribution in Top Results

- CCanto as top result: 33
- CEDict as top result: 64

### Failure Patterns

- Failures where top result has term_match_cost > 0 (partial/fuzzy match winning): 1
- Failures where top result has static_cost > 15000 (high base cost): 0
- Failures where CEDict partial match beats CCanto exact match: 1

### Cost Distribution in Failures

| Query | Expected | Got | Got Total Cost | Got Static | Got Source |
|-------|----------|-----|----------------|------------|-----------|
| `mat1` | 乜 | 貓 | 29000 | 9000 | CEDict |

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
