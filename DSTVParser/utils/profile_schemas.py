PROFILE_SCHEMAS = {
    'NC1': {
        'I': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness'], [10, 11, 12, 13]), # I profiles
        'U': (['flange_width', 'web_height', 'thickness'], [10, 11, 12]),        # U profiles
        'L': (['width', 'height', 'thickness'], [10, 11, 12]),                   # Angle profiles
        'B': (['lenght', 'width', 'thickness'], [8, 9, 12]),                   # Sheets/Plates
        'RU': ([ ]), # Rounds
        'RO': ([ ]), # Rounded Tube
        'M': (['side_1_size', 'side_2_size', 'thickness'], []),    # Rectangular tube
        'C': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness']),    # Profile 'C'
        'T': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness']),    # Profile 'T'
    },
    'NC': {
        'I': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness'], [9, 10, 11, 12]),
        'U': (['flange_width', 'web_height', 'thickness'], [9, 10, 11]),
        'L': (['width', 'height', 'thickness'], [9, 10, 11]),
        'B': (['lenght', 'width', 'thickness'], [8, 9, 12]),
        'RU': ([ ]), # Rounds
        'RO': (['radious', 'thickness'], [9, 10]), # Rounded Tube     
        'M': (['side_1_size', 'side_2_size', 'thickness'], [9, 10, 11]),    # Rectangular tube
        'C': (['flange_width', 'web_height', 'thickness']),    # Profile 'C'    
        'T': (['flange_width', 'web_height', 'flange_thickness', 'web_thickness']),    # Profile 'T'
    }
}