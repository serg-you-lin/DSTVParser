# DSTV Reader
DSTV Reader is a Python library for parsing and analyzing DSTV (NC/NC1) files commonly used in the structural steel industry.
It allows easy extraction of profile information, detection of inclined cuts, and basic automation of file classification.

## Features
Parse DSTV files and extract profile headers and geometry

Detect inclined cuts on flanges and webs

Classify and sort NC files based on detected features

Modular structure: easy to extend or integrate into larger workflows

## Requirements
Python 3.9+

No external dependencies (for now)

To install dependencies in the future:

```bash
pip install -r requirements.txt
```
## Notes
This project is under active development.
Supporting .nc1 files will be ready soon (just print header now).
Plotting and DXF export features will be added in the future.

# How to Use
## Basic example
```bash
from DSTVParser import NCFileParser

nc_file = "your_file.nc"
parser = NCFileParser(str(nc_file))
profile = parser.parse()

print(profile.get_header())
```
For a complete example, see RunExample.py.
