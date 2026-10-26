#!/usr/bin/env python3
"""Check numeric X/Y columns in a UTF-8 CSV. Never modifies the input file."""
import argparse
import csv
import math
from collections import Counter

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('file', help='UTF-8 CSV file')
p.add_argument('--x', default='X', help='X column name (default: X)')
p.add_argument('--y', default='Y', help='Y column name (default: Y)')
args = p.parse_args()

seen = set()
issues = Counter()
xs, ys = [], []
with open(args.file, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    if not reader.fieldnames or args.x not in reader.fieldnames or args.y not in reader.fieldnames:
        p.error(f'Expected columns {args.x!r} and {args.y!r}; found {reader.fieldnames!r}')
    total = 0
    for line, row in enumerate(reader, start=2):
        total += 1
        try:
            x = float(row[args.x])
            y = float(row[args.y])
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError('non-finite')
        except (ValueError, TypeError, OverflowError):
            issues['invalid_or_missing_xy'] += 1
            print(f'Row {line}: invalid or missing X/Y')
            continue
        pair = (x, y)
        if pair in seen:
            issues['duplicate_xy'] += 1
            print(f'Row {line}: repeated coordinate pair')
        seen.add(pair)
        xs.append(x); ys.append(y)
print(f'Total rows: {total} | Numeric XY: {len(xs)}')
print('Issues:', dict(issues))
if xs:
    print(f'Extent X: {min(xs):g} .. {max(xs):g}')
    print(f'Extent Y: {min(ys):g} .. {max(ys):g}')
print('Coordinate reference system and units: NOT checked')
