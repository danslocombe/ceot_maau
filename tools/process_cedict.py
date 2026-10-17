#!/usr/bin/env python3
"""Process CEDict: pull the classifier (CL:) info out of the definitions and
into a separate tab-separated column.

Input : full/cedict_ts.u8
Output: full/cedict_ts.processed.u8

Each data line keeps its original shape but with any `CL:...` classifier
material removed, followed by a TAB and a comma-separated list of traditional
classifier characters (deduped, original order):

    老師 老师 [lao3 shi1] /teacher/	個,位
    鴨 鸭 [ya1] /duck/	隻

Two forms occur in the source and both are handled:
  * a standalone definition element : /CL:個|个[ge4],位[wei4]/
  * inline in a definition          : /duck (CL:隻|只[zhi1])/, /frog; CL:隻|只[zhi1]/

Comment (#) and blank lines are passed through unchanged.
"""
import re
import sys

IN = sys.argv[1] if len(sys.argv) > 1 else 'full/cedict_ts.u8'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'full/cedict_ts.processed.u8'


def parse_body(body):
    """'個|个[ge4],位[wei4]' -> ['個', '位']"""
    out = []
    for tok in body.split(','):
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r'^([^\[\|]+)', tok)  # traditional is before '|' or '['
        if m:
            out.append(m.group(1).strip())
    return out


def strip_element(elem, sink):
    """Remove CL: material from one /-delimited definition element."""
    def take(m):
        sink.extend(parse_body(m.group(1)))
        return ''
    # /... (CL:業|业[ye4]) .../  (also catches a leading "(CL:...)" element)
    elem = re.sub(r'\s*\(\s*CL:([^)]*)\)', take, elem)
    # /frog; CL:隻|只[zhi1]/  and a bare trailing "CL:..." element
    elem = re.sub(r'\s*;?\s*CL:([^;)]*)', take, elem)
    return elem


n_lines = n_with = n_cls = 0
with open(IN, encoding='utf-8') as f, open(OUT, 'w', encoding='utf-8', newline='\n') as g:
    for line in f:
        line = line.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#'):
            g.write(line + '\n')
            continue

        try:
            bracket = line.index('[')
            pinyin_end = line.index(']', bracket)
        except ValueError:
            g.write(line + '\n')
            continue

        n_lines += 1
        prefix = line[:pinyin_end + 1]
        defs_region = line[pinyin_end + 1:]

        comment = ''
        hash_pos = defs_region.find('#')
        if hash_pos != -1:
            comment = defs_region[hash_pos:]
            defs_region = defs_region[:hash_pos]

        classifiers, kept = [], []
        for elem in defs_region.split('/'):
            kept.append(strip_element(elem, classifiers))

        # dropping a whole /CL:.../ element can leave an empty slot ("//"); the
        # builder skips empty defs, but collapse it so the file stays tidy.
        kept_region = re.sub(r'/+', '/', '/'.join(kept))

        seen, cls = set(), []
        for c in classifiers:
            if c and c not in seen:
                seen.add(c)
                cls.append(c)

        if cls:
            n_with += 1
            n_cls += len(cls)

        g.write(prefix + kept_region + comment + '\t' + ','.join(cls) + '\n')

print(f'lines={n_lines} with_classifiers={n_with} classifier_tokens={n_cls}')
