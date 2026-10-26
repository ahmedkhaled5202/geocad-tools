#!/usr/bin/env python3
"""Count KML placemarks and report lon/lat extent of coordinates tags."""
import argparse
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('file', help='KML file (not KMZ)')
args = p.parse_args()
root = ET.parse(args.file).getroot()
local = lambda tag: tag.rsplit('}', 1)[-1]
placemarks = sum(local(e.tag) == 'Placemark' for e in root.iter())
points = []
invalid = 0
for element in root.iter():
    if local(element.tag) != 'coordinates' or not element.text:
        continue
    for part in element.text.split():
        fields = part.split(',')
        try:
            lon, lat = float(fields[0]), float(fields[1])
            if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                invalid += 1
            else:
                points.append((lon, lat))
        except (ValueError, IndexError):
            invalid += 1
print('Placemarks:', placemarks)
print('Coordinate tuples in range:', len(points))
print('Invalid/out-of-range tuples:', invalid)
if points:
    print('Longitude extent:', min(x for x, _ in points), max(x for x, _ in points))
    print('Latitude extent:', min(y for _, y in points), max(y for _, y in points))
print('Does not expand NetworkLinks, external resources or KMZ files.')
