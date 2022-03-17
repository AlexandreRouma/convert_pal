#!/bin/python

# .PAL to SDR++ colormap converter
# Ryzerth 2022

from genericpath import isfile
import sys
import os.path as path
import json

# Check arguments
if len(sys.argv) < 5:
    print("convert_pal.py [input.pal] [output.json] [name] [author]")
    exit(-1)

PAL_PATH = sys.argv[1]
JSON_PATH = sys.argv[2]
COLORMAP_NAME = sys.argv[3]
COLORMAP_AUTHOR = sys.argv[4]

if (not path.exists(PAL_PATH)) or (not path.isfile(PAL_PATH)):
    print("Given pal file does not exists or is not accessible")
    exit(-1)

# Load PAL file
fpal = open(PAL_PATH)
pal_data = fpal.read()
fpal.close()

# Generate pallet
reversed = []
pal_lines = pal_data.split("\n")
for line in pal_lines:
    # Clean up line and skip if empty
    trimmed = line.strip()
    if trimmed == "":
        continue

    # Split color values
    rgb = trimmed.split()
    if len(rgb) != 3 or (not rgb[0].isdigit()) or (not rgb[1].isdigit()) or (not rgb[2].isdigit()):
        print("Invalid RGB color code in pal file '" + trimmed + "'")
        exit(-1)

    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])

    # Check if the values are in range
    if r > 255 or g > 255 or b > 255:
        print("RGB value out of range in pal file '" + trimmed + "'")
        exit(-1)

    # Append to reversed list
    reversed.append("#{:02X}{:02X}{:02X}".format(r, g, b))

# Reverse array
reversed.reverse()

# Create map object
map = {
    "name": COLORMAP_NAME,
    "author": COLORMAP_AUTHOR,
    "map": reversed
}

# Serialize and save to file
fjson = open(JSON_PATH, "w")
json.dump(map, fjson, indent=4)
fjson.close()

print("Created new colormap file '" + JSON_PATH + "'.")