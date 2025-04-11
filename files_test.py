from DSTVParser import *
import os

nc_path = r"Examples\722.nc"
nc1_path = r"Examples\2501.nc1"

if os.path.exists(nc_path):
    print("File found!")
else:
    print("File NOT found!")
if os.path.exists(nc1_path):
    print("File found!")
else:
    print("File NOT found!")
    
nc_part = NCFileParserFactory.create_parser(nc_path)
nc_profile = nc_part.parse()

nc_header = nc_profile.get_header()
print(nc_header)

nc1_part = NCFileParserFactory.create_parser(nc1_path)
nc1_profile = nc1_part.parse()

nc1_header = nc1_profile.get_header()
print(nc1_header)