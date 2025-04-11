from typing import List, Optional
from .models.NCPart import NCPart

class DSTVFileParser:
    """Classe base per parser di file NC/NC1"""
    def __init__(self, filename: str):
        self.filename = filename
        self.current_profile = None
        self.debug = False

    def log(self, message: str):
        """Utility per logging"""
        if self.debug:
            print(message)
            
    def parse(self) -> Optional[NCPart]:
        """Metodo principale di parsing del file - da implementare nelle sottoclassi"""
        raise NotImplementedError("Il metodo parse deve essere implementato nelle sottoclassi")
    
    def _create_profile_from_header(self, header_lines: List[str]):
        """Metodo base per creare profilo dall'header - potrebbe essere sovrascritto"""
        raise NotImplementedError("Metodo da implementare nelle sottoclassi")