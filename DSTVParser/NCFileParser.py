from typing import List, Optional
import re
import os
from .models.NCPart import *
from .DSTVFileParser import DSTVFileParser

class NCFileParser(DSTVFileParser):
    """Parser per file NC standard"""
    def parse(self) -> Optional[NCPart]:
        """Metodo di parsing del file NC"""
        self.log(f"\nInizio parsing del file NC: {self.filename}")
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            
            header_data = []
            in_header = False
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                code = line[:2]
                self.log(f"Processo linea: '{line}' (codice: {code})")
                
                # Gestione header
                if code == 'ST':
                    in_header = True
                    continue
                
                if in_header:
                    if code in ['BO', 'AK', 'IK', 'SI', 'EN']:
                        in_header = False
                        self._create_profile_from_header(header_data)
                    else:
                        header_data.append(line)
                        continue

                # Gestione sezioni
                if code == 'BO':
                    current_section = 'BO'
                    self.log("Inizio sezione BO (fori e asole)")
                    continue
                elif code == 'AK':
                    current_section = 'AK'
                    self.log("Inizio sezione AK (contorni)")
                    continue
                elif code == 'SI':
                    current_section = 'SI'
                    self.log("Inizio sezione SI (marcature)")
                    continue
                elif code == 'EN':
                    self.log("Fine file")
                    break

                # Parsing del contenuto
                if line[0] in ['o', 'u', 'v', 'h']:
                    if current_section == 'BO':
                        self._parse_bo_line(line)
                    elif current_section == 'AK':
                        self._parse_ak_line(line)
                    elif current_section == 'SI':
                        self._parse_si_line(line)
            
            return self.current_profile
            
        except Exception as e:
            self.log(f"ERRORE durante il parsing: {e}")
            import traceback
            self.log(traceback.format_exc())
            return None

    def _create_profile_from_header(self, header_lines: List[str]):
        """Crea il profilo dai dati dell'header per file NC"""
        try:
            self.log("\nCreazione profilo da header NC:")
            profile_type = header_lines[7]
            
            # Dizionario delle dimensioni in base al tipo di profilo
            dimensions = {}
            
            if profile_type == 'I':
                dimensions = {
                    'flange_width': float(header_lines[9]),
                    'web_height': float(header_lines[10]),
                    'flange_thickness': float(header_lines[11]),
                    'web_thickness': float(header_lines[12])
                }
            elif profile_type == 'U':
                dimensions = {
                    'flange_width': float(header_lines[9]),
                    'web_height': float(header_lines[10]),
                    'thickness': float(header_lines[11])
                }
            elif profile_type == 'L':
                dimensions = {
                    'width': float(header_lines[9]),
                    'height': float(header_lines[10]),
                    'thickness': float(header_lines[11])
                }
            # Add profile when necessary
            
            self.current_profile = NCPart(
                order_id=header_lines[0],
                piece_id=header_lines[3],
                material=header_lines[4],
                quantity=int(header_lines[5]),
                profile_type=profile_type,
                code_profile=header_lines[6],
                length=float(header_lines[8].split(',')[0]),
                dimensions=dimensions
            )
            
            self.log(f"Creato profilo tipo {profile_type}: {self.current_profile.code_profile}")
            self.log(f"Dimensioni: {dimensions}")
            
        except Exception as e:
            self.log(f"ERRORE nella creazione del profilo: {e}")
            raise

    def _parse_holes(self, line: str) -> bool:
        """Parser dedicato per i fori (5 valori dopo BO)"""
        parts = line.split()
        if len(parts) != 5:  # face + x + y + diam + type
            return False
        
        try:
            face = parts[0]
            x = float(re.sub(r'[ouvh]', '', parts[1]))
            y = float(parts[2])
            diameter = float(parts[3])
            hole_type = float(parts[4])
            
            self.current_profile.add_hole(x, y, diameter, hole_type, face)
            self.log(f"Aggiunto foro: x={x}, y={y}, diameter={diameter}, type={hole_type}, face={face}")
            return True
        except ValueError:
            return False

    def _parse_slots(self, line: str) -> bool:
        """Parser dedicato per le asole"""
        parts = line.split()
        self.log(f"\nDebug asola - Analisi linea: {line}")
        self.log(f"Debug asola - Parti separate: {parts}")
        
        # Verifica se la linea contiene 'l'
        if 'l' not in line:
            self.log("Debug asola - 'l' non trovata nella linea")
            return False
            
        try:
            face = parts[0]
            x = float(re.sub(r'[ouvh]', '', parts[1]))
            y = float(parts[2])
            diameter = float(parts[3])
            # Cerca la parte che contiene 'l'
            for i, part in enumerate(parts[4:], 4):
                if 'l' in part:
                    hole_type = float(part.replace('l', ''))
                    self.log(f"Debug asola - Trovato 'l' in posizione {i}: {part}")
                    cc_distance = float(parts[i + 1])
                    height = float(parts[i + 2])
                    angle = float(parts[i + 3]) if len(parts) > i + 3 else 0.0
                    length = diameter + cc_distance
                    
                    self.current_profile.add_slot(x, y, diameter, hole_type, cc_distance, height, angle, length, face)
                    self.log(f"Aggiunta asola: x={x}, y={y}, diameter={diameter}, "
                            f"cc_dist={cc_distance}, height={height}, angle={angle}, "
                            f"length={length}, face={face}")
                    return True
            
            self.log("Debug asola - Non trovata struttura valida per asola")
            return False
            
        except ValueError as e:
            self.log(f"Debug asola - Errore nel parsing: {e}")
            return False
        except Exception as e:
            self.log(f"Debug asola - Errore generico: {e}")
            return False
    
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
        if not self.current_profile:
            return
            
        # Prima prova a parsare come asola (ha più parametri)
        if self._parse_slots(line):
            return
            
        # Se non è un'asola, prova a parsare come foro
        if self._parse_holes(line):
            return
            
        self.log(f"Linea BO non riconosciuta: {line}")

    def _parse_ak_line(self, line: str):
        """Gestisce le linee dopo AK (contorni)"""
        if not self.current_profile:
            return
            
        if self._parse_contour(line):
            return
            
        self.log(f"Linea AK non riconosciuta: {line}")

    def _parse_si_line(self, line: str):
        """Gestisce le linee dopo SI (marcature)"""
        self.log(f"Ignorata linea SI: {line}")
        pass  # Per ora ignoriamo le marcature



if __name__ == '__main__':
    base_dir = os.path.dirname(__file__) 
    parent_dir = os.path.dirname(base_dir)
    nc_path = os.path.join(parent_dir, "Examples", "4026.nc")

    if os.path.exists(nc_path):
        print("File found!")
    else:
        print("File NOT found!")
        
    part_nc = NCFileParser(nc_path)
    profile = part_nc.parse()
    header = profile.get_header()
    print(header)

    top_flange = profile.o_contour
    print(f"Top flange points: {top_flange}.")

    print("Dimensions: ", profile.dimensions)

    print("Material: ", profile.material)
