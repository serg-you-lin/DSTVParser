import os
from .NCFileParser import NCFileParser
from .NC1FileParser import NC1FileParser
from .DSTVFileParser import DSTVFileParser

class NCFileParserFactory:
    """Factory per creare il parser appropriato in base all'estensione del file"""
    @staticmethod
    def create_parser(filename: str) -> DSTVFileParser:
        """Crea il parser appropriato in base all'estensione del file"""
        if filename.lower().endswith('.nc'):
            return NCFileParser(filename)
        elif filename.lower().endswith('.nc1'):
            return NC1FileParser(filename)
        else:
            raise ValueError(f"Formato file non supportato: {filename}")
        


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__) 
    parent_dir = os.path.dirname(base_dir)
    nc_path = os.path.join(parent_dir, "Examples", "722.nc")
    nc1_path = os.path.join(parent_dir, "Examples", "2501.nc1")

    if os.path.exists(nc_path):
        print("File trovato!")
    else:
        print("File NON trovato!")
    if os.path.exists(nc1_path):
        print("File trovato!")
    else:
        print("File NON trovato!")
        
    nc_part = NCFileParserFactory.create_parser(nc_path)
    nc_profile = nc_part.parse()

    nc_header = nc_profile.get_header()
    print(nc_header)

    nc1_part = NCFileParserFactory.create_parser(nc1_path)
    nc1_profile = nc1_part.parse()

    nc1_header = nc1_profile.get_header()
    print(nc1_header)