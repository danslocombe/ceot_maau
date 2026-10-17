#!/usr/bin/env python3
"""Process CC-Canto: pull the classifier (`M:`) info out of the definitions and
into a separate tab-separated column.

Input : full/cccanto-webdist.txt
Output: full/cccanto-webdist.processed.txt

Each data line keeps its original shape but with any `M:...` classifier
material removed, followed by a TAB and a comma-separated list of traditional
classifier characters (deduped, original order):

    事 事 [shi4] {si6} /matter/thing/item/work/affair/incident/.../	件,樁,回

The `M:` notation embeds Mandarin pinyin and (usually simplified) classifier
characters, e.g. `affair M: 件jiàn [件] / 桩zhuāng [桩] / 回huí [回]/incident`.
A clause starts at `M:` and its classifier tokens continue as later
`/`-separated elements until normal English definitions resume.  A single line
may contain several `M:` clauses.

Because the characters in the source are frequently simplified they are
normalised to traditional using the CC-Canto readings table
(`full/cccedict-canto-readings-150923.txt`, format `trad simp [pinyin]
{jyutping}`).  That table maps some simplified characters to more than one
traditional character (e.g. 只 -> 只/隻, 台 -> 台/檯/臺/颱, 面 -> 面/麵); those
collisions are resolved with the token's pinyin and, as a final tie-break, the
classifier convention already used for the CEDict transform
(`full/cedict_ts.u8`, `CL:trad|simp[pinyin]`).

Comment (#) and blank lines are passed through unchanged, and entries without
classifiers still get a trailing TAB and an empty second column.
"""
import os
import re
import sys

IN = sys.argv[1] if len(sys.argv) > 1 else 'full/cccanto-webdist.txt'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'full/cccanto-webdist.processed.txt'
READINGS = 'full/cccedict-canto-readings-150923.txt'
CEDICT = 'full/cedict_ts.u8'

CJK = r'\u3400-\u9fff'
# A classifier token: CJK char, latin pinyin (tone marks and/or a tone digit),
# then the character repeated inside square brackets: `件jiàn [件]`.
TOKEN_RE = re.compile(
    r'\s*'
    r'(?P<char>[' + CJK + r']+)'
    r'(?P<pinyin>[^\s\[\]0-9]+\d?)'
    r'\s*\[\s*[' + CJK + r']+\s*\]'
)
# Trailing whitespace and (in one source line) a stray `]` belong to the token.
TAIL_RE = re.compile(r'^\s*\]?\s*$')

# tone-marked vowel -> base letter + tone number
_TONES = {
    'ā': 'a1', 'á': 'a2', 'ǎ': 'a3', 'à': 'a4',
    'ē': 'e1', 'é': 'e2', 'ě': 'e3', 'è': 'e4',
    'ī': 'i1', 'í': 'i2', 'ǐ': 'i3', 'ì': 'i4',
    'ō': 'o1', 'ó': 'o2', 'ǒ': 'o3', 'ò': 'o4',
    'ū': 'u1', 'ú': 'u2', 'ǔ': 'u3', 'ù': 'u4',
    'ǖ': 'v1', 'ǘ': 'v2', 'ǚ': 'v3', 'ǜ': 'v4',
    'ü': 'v', 'ń': 'n2', 'ň': 'n3', 'ǹ': 'n4', 'ḿ': 'm2',
}


def normalise_pinyin(pinyin):
    """`jiàn` -> `jian4`, `lǚ` -> `lv3`, `tai2` -> `tai2`."""
    out = []
    for ch in pinyin.strip().lower():
        if ch in _TONES:
            out.append(_TONES[ch])
        elif ch == ' ':
            continue
        else:
            out.append(ch)
    return ''.join(out)


def build_readings_map(path):
    """simplified char -> {traditional char -> set(normalised pinyin)}."""
    mapping = {}
    if not os.path.exists(path):
        return mapping
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            fields = line.split()
            if len(fields) < 2:
                continue
            trad, simp = fields[0], fields[1]
            if len(trad) != 1 or len(simp) != 1:
                continue
            m = re.search(r'\[([^\]]*)\]', line)
            pinyin = normalise_pinyin(m.group(1)) if m else ''
            mapping.setdefault(simp, {}).setdefault(trad, set()).add(pinyin)
    return mapping


def build_cedict_classifiers(path):
    """simplified char -> {traditional char -> occurrence count} from CEDict CL: fields."""
    counts = {}
    if not os.path.exists(path):
        return counts
    cl_re = re.compile(r'CL:([^/\]]*)')
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            for m in cl_re.finditer(line):
                for tok in m.group(1).split(','):
                    head = tok.split('[')[0].strip()
                    parts = head.split('|')
                    trad = parts[0].strip()
                    simp = parts[-1].strip()
                    if len(trad) == 1 and len(simp) == 1:
                        counts.setdefault(simp, {})
                        counts[simp][trad] = counts[simp].get(trad, 0) + 1
    return counts


def top_traditional(char, pinyin, readings, cl_counts):
    """Resolve the simplified classifier char to a traditional character."""
    candidates = readings.get(char)
    if not candidates:
        return char, False
    trads = list(candidates)
    if len(trads) == 1:
        return trads[0], True

    normalised = normalise_pinyin(pinyin)
    by_pinyin = [t for t in trads if normalised in candidates[t]]
    if len(by_pinyin) == 1:
        return by_pinyin[0], True

    pool = by_pinyin or trads
    seen = cl_counts.get(char, {})
    ranked = [t for t in pool if t in seen]
    if ranked:
        return max(ranked, key=lambda t: seen[t]), True

    # last resort: a character that is both simplified and traditional is the
    # least surprising pick (e.g. 面 over 麵 when nothing else decides).
    if char in pool:
        return char, True
    return sorted(pool)[0], True


def process_definitions(region, sink, readings, cl_counts, unresolved):
    """Return `region` with all M: clauses removed, appending classifiers to sink."""
    elements = region.split('/')
    kept = []
    i = 0
    while i < len(elements):
        elem = elements[i]
        if 'M:' in elem:
            pre, post = elem.split('M:', 1)
            kept.append(pre.rstrip())
            m = TOKEN_RE.match(post)
            if m and TAIL_RE.match(post[m.end():]):
                _add_token(m.group('char'), m.group('pinyin'), sink,
                           readings, cl_counts, unresolved)
            i += 1
            # classifier tokens continue until normal definitions resume
            while i < len(elements):
                candidate = elements[i]
                m = TOKEN_RE.match(candidate)
                if not m or not TAIL_RE.match(candidate[m.end():]):
                    break
                _add_token(m.group('char'), m.group('pinyin'), sink,
                           readings, cl_counts, unresolved)
                i += 1
            continue
        kept.append(elem)
        i += 1
    return re.sub(r'/{2,}', '/', '/'.join(kept))


def _add_token(char, pinyin, sink, readings, cl_counts, unresolved):
    traditional, resolved = top_traditional(char, pinyin, readings, cl_counts)
    if not resolved:
        unresolved.add(char)
    sink.append(traditional)


def main():
    readings = build_readings_map(READINGS)
    cl_counts = build_cedict_classifiers(CEDICT)

    n_lines = n_with = n_cls = 0
    distinct = set()
    unresolved = set()
    with open(IN, encoding='utf-8') as f, \
            open(OUT, 'w', encoding='utf-8', newline='\n') as g:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                g.write(line + '\n')
                continue

            try:
                lb = line.index('[')
                rb = line.index(']', lb)
            except ValueError:
                g.write(line + '\n')
                continue

            n_lines += 1
            head = line[:rb + 1]
            rest = line[rb + 1:]

            hash_pos = rest.find('#')
            if hash_pos != -1:
                defs_region, comment = rest[:hash_pos], rest[hash_pos:]
            else:
                defs_region, comment = rest, ''

            classifiers = []
            kept_region = process_definitions(
                defs_region, classifiers, readings, cl_counts, unresolved)

            seen, cls = set(), []
            for c in classifiers:
                if c not in seen:
                    seen.add(c)
                    cls.append(c)
                    distinct.add(c)

            if classifiers:
                n_with += 1
                n_cls += len(classifiers)

            g.write(head + kept_region + comment + '\t' + ','.join(cls) + '\n')

    print(f'lines={n_lines} with_classifiers={n_with} '
          f'classifier_tokens={n_cls} distinct_classifiers={len(distinct)}')
    if unresolved:
        print('unresolved simplified characters (kept as-is): '
              + ' '.join(sorted(unresolved)), file=sys.stderr)
    else:
        print('all classifier characters resolved via the readings map')


if __name__ == '__main__':
    main()
