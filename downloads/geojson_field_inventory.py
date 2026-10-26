#!/usr/bin/env python3
"""Summarize GeoJSON feature attribute keys and null coverage."""
import argparse
import json
from collections import Counter

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('file', help='GeoJSON FeatureCollection')
args = p.parse_args()
with open(args.file, encoding='utf-8-sig') as f:
    data = json.load(f)
if not isinstance(data, dict) or data.get('type') != 'FeatureCollection':
    p.error('Expected a FeatureCollection object')
features = data.get('features')
if not isinstance(features, list):
    p.error('Expected features array')
seen = Counter()
not_null = Counter()
for i, feat in enumerate(features, start=1):
    if not isinstance(feat, dict) or feat.get('type') != 'Feature':
        print(f'Warning: entry {i} is not a Feature')
        continue
    props = feat.get('properties')
    if props is None:
        props = {}
    if not isinstance(props, dict):
        print(f'Warning: feature {i} has non-object properties')
        continue
    for name, value in props.items():
        seen[name] += 1
        not_null[name] += value is not None
print('Feature entries:', len(features))
print('Field | present | non-null')
for name in sorted(seen, key=str.casefold):
    print(f'{name} | {seen[name]} | {not_null[name]}')
print('No input files were changed.')
