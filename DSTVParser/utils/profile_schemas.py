PROFILE_SCHEMAS = {
    'NC1': {
        'I': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness'], [10, 11, 12, 13]), # I profiles V
        'U': (['flange_width', 'web_height', 'thickness'], [10, 11, 12]),        # U profiles V
        'L': (['width', 'height', 'thickness'], [10, 11, 12]),                   # Angle profiles V
        'B': (['lenght', 'width', 'thickness'], []),                   # Sheets/Plates X
        'RU': ([ ]), # Rounds  X
        'RO': (['radious', 'thickness' ], []), # Rounded Tube   X
        'M': (['side_1_size', 'side_2_size', 'thickness'], []),    # Rectangular tube   X
        'C': (['flange_width', 'web_height', 'thickness'], []),    # Profile 'C'   X
        'T': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness']),    # Profile 'T'   X
    },
    'NC': {
        'I': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness'], [9, 10, 11, 12]),   # I profiles V
        'U': (['flange_width', 'web_height', 'thickness'], [9, 10, 11]),                               # U profiles V
        'L': (['width', 'height', 'thickness'], [9, 10, 11]),                                  # Angle profiles V
        'B': (['lenght', 'width', 'thickness'], [8, 9, 12]),                                  # Sheets/Plates V
        'RU': ([ ]), # Rounds                                                        X
        'RO': (['radious', 'thickness'], [9, 10]), # Rounded Tube      V
        'M': (['side_1_size', 'side_2_size', 'thickness'], [9, 10, 11]),    # Rectangular tube   V
        'C': (['flange_width', 'web_height', 'thickness']),    # Profile 'C'    V
        'T': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness']),    # Profile 'T'    X
    }
}