#!/usr/bin/env python3
"""Read GeoJSON and report geometry types and numeric lon/lat extent."""
import argparse
import json
import math
from collections import Counter

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('file', help='GeoJSON file')
args = p.parse_args()
with open(args.file, encoding='utf-8-sig') as f:
    data = json.load(f)
if not isinstance(data, dict):
    p.error('Top-level GeoJSON value must be an object')
if data.get('type') == 'FeatureCollection':
    features = data.get('features')
    if not isinstance(features, list):
        p.error('FeatureCollection.features must be an array')
    geometries = [f.get('geometry') if isinstance(f, dict) else None for f in features]
elif data.get('type') == 'Feature':
    geometries = [data.get('geometry')]
else:
    geometries = [data]

def walk_geometry(g):
    if not isinstance(g, dict):
        yield None, None
        return
    kind = g.get('type')
    if kind == 'GeometryCollection':
        nested = g.get('geometries', [])
        if not isinstance(nested, list):
            yield 'invalid_geometry', None
        else:
            for item in nested:
                yield from walk_geometry(item)
        return
    yield kind or 'unknown', g.get('coordinates')

def positions(value):
    if isinstance(value, list):
        if len(value) >= 2 and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in value[:2]):
            x, y = value[:2]
            if math.isfinite(x) and math.isfinite(y):
                yield (x, y)
        else:
            for part in value:
                yield from positions(part)

counts = Counter()
allpoints = []
for geom in geometries:
    for kind, coords in walk_geometry(geom):
        counts[kind or 'null_geometry'] += 1
        allpoints.extend(positions(coords))
print('Features / top-level geometries:', len(geometries))
print('Geometry types:', dict(counts))
print('Valid numeric positions:', len(allpoints))
if allpoints:
    print('Longitude extent:', min(p[0] for p in allpoints), max(p[0] for p in allpoints))
    print('Latitude extent:', min(p[1] for p in allpoints), max(p[1] for p in allpoints))
    outside = sum(abs(x) > 180 or abs(y) > 90 for x, y in allpoints)
    print('Positions outside usual lon/lat bounds:', outside)
print('This is a quick audit, not full RFC 7946 validation.')
