from typing import List, Optional
import re
import os
from .DSTVFileParser import DSTVFileParser
from .models.NCPart import NCPart

class NC1FileParser(DSTVFileParser):
    """Parser per file NC1 con formato differente"""
    def parse(self) -> Optional[NCPart]:
        """Metodo di parsing del file NC1"""
        self.log(f"\nInizio parsing del file NC1: {self.filename}")
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            
            header_data = []
            in_header = False
            current_section = None
            
            # Implementa qui la logica specifica per i file NC1
            # Questo è un esempio basilare, da adattare alle differenze specifiche del formato NC1
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                code = line[:2]
                self.log(f"Processo linea NC1: '{line}' (codice: {code})")
                
                if code == 'ST':  # Esempio di codice diverso per l'header
                    in_header = True
                    continue
                
                if in_header:
                    if code in ['BO', 'AK', 'SI', 'EN']:  # Esempi di sezioni diverse
                        in_header = False
                        self._create_profile_from_header(header_data)
                    else:
                        header_data.append(line)
                        continue

                # Gestione sezioni specifiche del formato NC1
                if code == 'BO': 
                    current_section = 'BO' 
                    continue
                elif code == 'AK':  # Contours - equivalente all'AK
                    current_section = 'AK'
                    continue
                elif code == 'SI':  # Markings - equivalente al SI
                    current_section = 'SI'
                    continue
                elif code == 'EN':
                    self.log("Fine file NC1")
                    break

                # Parsing del contenuto (adattato al formato NC1)
                if current_section == 'BO':
                    self._parse_bo_line(line)
                elif current_section == 'AK':
                    self._parse_ak_line(line)
                elif current_section == 'SI':
                    self._parse_si_line(line)
            
            return self.current_profile
            
        except Exception as e:
            self.log(f"ERRORE durante il parsing NC1: {e}")
            import traceback
            self.log(traceback.format_exc())
            return None

    def _create_profile_from_header(self, header_lines: List[str]):
        """Crea il profilo dai dati dell'header per file NC1"""
        try:
            self.log("\nCreazione profilo da header NC1:")
            
            profile_type = header_lines[8]
            print('Profilo nc1', profile_type) 
            
            dimensions = {}
            
            if profile_type == 'I':
                dimensions = {
                    'flange_width': float(header_lines[10]),  # Posizioni diverse
                    'web_height': float(header_lines[11]),
                    'flange_thickness': float(header_lines[12]),
                    'web_thickness': float(header_lines[13])
                }
            elif profile_type == 'U':
                dimensions = {
                    'flange_width': float(header_lines[10]),
                    'web_height': float(header_lines[11]),
                    'thickness': float(header_lines[12])
                }
            elif profile_type == 'L':
                dimensions = {
                    'width': float(header_lines[10]),
                    'height': float(header_lines[11]),
                    'thickness': float(header_lines[12])
                }
            
            self.current_profile = NCPart(
                order_id=header_lines[1],
                piece_id=header_lines[2],  # Posizioni diverse
                material=header_lines[5],
                quantity=int(header_lines[3]),
                profile_type=profile_type,
                code_profile=header_lines[7],
                length=float(header_lines[9].split(',')[0]),  # Esempio di posizione diversa
                dimensions=dimensions
            )
            
            self.log(f"Creato profilo NC1 tipo {profile_type}: {self.current_profile.code_profile}")
            
        except Exception as e:
            self.log(f"ERRORE nella creazione del profilo NC1: {e}")
            raise

    def _parse_holes(self, line: str) -> bool:
        """Parser dedicato per i fori (5 valori dopo BO)"""
        self.log("Not yet implemented")
        pass # da implementare

    def _parse_slots(self, line: str) -> bool:
        """Parser dedicato per le asole"""
        self.log("Not yet implemented")
        pass # da implementare
        
    def _parse_contour(self, line: str) -> bool:
        """Parser dedicato per i punti del contorno (4 valori dopo AK)"""
        parts = line.split()
        if len(parts) < 4:
            return False
            
        try:
            face = parts[0]
            x = float(parts[1].replace('u', ''))
            y = float(parts[2])
            angle = float(parts[3])
            
            self.current_profile.add_contour_points(face, [(x, y, angle)])
            self.log(f"Aggiunto punto contorno: face={face}, x={x}, y={y}, angle={angle}")
            return True
        except ValueError:
            return False

    def _parse_bo_line(self, line: str):
        """Gestisce le linee dopo BO (fori e asole)"""
        self.log("Not yet implemented")
        pass # da implementare

    def _parse_ak_line(self, line: str):
        
        """Gestisce le linee dopo AK (contorni)"""
        self.log("Not yet implemented")
        pass # da implementare
        
    def _parse_si_line(self, line: str):
        """Gestisce le linee dopo SI (marcature)"""
        self.log(f"Ignorata linea SI: {line}")
        pass  # Per ora ignoriamo le marcature

if __name__ == '__main__':
    
    base_dir = os.path.dirname(__file__) 
    parent_dir = os.path.dirname(base_dir)
    nc1_path = os.path.join(parent_dir, "Examples", "2501.nc1")

    if os.path.exists(nc1_path):
        print("File trovato!")
    else:
        print("File NON trovato!")
        
    part_nc1 = NC1FileParser(nc1_path)
    profile = part_nc1.parse()
    header = profile.get_header()
    print(header)

    print("Dimensions: ", profile.dimensions)

    print("Material: ", profile.material)