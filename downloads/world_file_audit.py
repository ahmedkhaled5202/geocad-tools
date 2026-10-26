#!/usr/bin/env python3
"""Read six-value raster world file without loading raster pixels."""
import argparse
import math
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('file', help='World file e.g. image.tfw or image.jgw')
args = p.parse_args()
lines = Path(args.file).read_text(encoding='utf-8-sig').splitlines()
if len(lines) != 6:
    p.error('A world file must have exactly six numeric lines')
try:
    A, D, B, E, C, F = [float(value.strip()) for value in lines]
except ValueError:
    p.error('All six world-file values must be numbers')
if not all(math.isfinite(v) for v in (A,D,B,E,C,F)):
    p.error('Non-finite value found')
print('Pixel center at column=0,row=0:', C, F)
print('Horizontal pixel step (map units):', A, D)
print('Vertical pixel step (map units):', B, E)
print('Step magnitudes:', math.hypot(A,D), math.hypot(B,E))
print('Determinant:', A*E - B*D)
print('No CRS or physical units are stored in the world file.')
