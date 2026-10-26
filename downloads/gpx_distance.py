#!/usr/bin/env python3
"""Approximate GPX track length per segment using spherical haversine."""
import argparse
import math
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('file', help='GPX track file')
args = p.parse_args()
root = ET.parse(args.file).getroot()
local = lambda tag: tag.rsplit('}', 1)[-1]

def distance(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*6371008.8*math.asin(min(1.0, math.sqrt(h)))

segments, total_points, total_m = 0, 0, 0.0
for segment in root.iter():
    if local(segment.tag) != 'trkseg':
        continue
    segments += 1
    previous = None
    for pt in segment:
        if local(pt.tag) != 'trkpt':
            continue
        try:
            lat = float(pt.attrib['lat']); lon = float(pt.attrib['lon'])
            if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError('Invalid coordinates')
        except (KeyError, ValueError) as e:
            print('Skipped invalid trackpoint:', e)
            previous = None
            continue
        here = lat, lon
        total_points += 1
        if previous is not None:
            total_m += distance(previous, here)
        previous = here
print('Track segments:', segments)
print('Valid trackpoints:', total_points)
print(f'Approximate track length: {total_m/1000:.3f} km')
print('Route points and waypoints excluded. Elevation, drift and breaks ignored.')
