import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_lines(lines_sets=[], points_sets=[]):
    fig, ax = plt.subplots()

    # Plotta ogni set di linee con un colore diverso
    colors = ['b', 'g', 'c', 'm', 'y', 'k']  # Aggiungi più colori se necessario
    for idx, lines in enumerate(lines_sets):
        x_values, y_values = [], []
        for i in range(len(lines) - 1):
            x_values.append([lines[i][0], lines[i+1][0]])
            y_values.append([lines[i][1], lines[i+1][1]])
        
        color = colors[idx % len(colors)]  # Cicla tra i colori
        for x, y in zip(x_values, y_values):
            ax.plot(x, y, color + '-')  # Linee colorate

    # Plotta ogni set di punti con un simbolo diverso
    markers = ['ro', 'go', 'co', 'mo', 'yo', 'ko']
    for idx, points in enumerate(points_sets):
        marker = markers[idx % len(markers)]  # Cicla tra i marker
        for point in points:
            ax.plot(point[0], point[1], marker)  # Punti colorati

    # Imposta i limiti degli assi
    all_x = [p[0] for lines in lines_sets for p in lines] + [p[0] for points in points_sets for p in points]
    all_y = [p[1] for lines in lines_sets for p in lines] + [p[1] for points in points_sets for p in points]

    ax.set_xlim(min(all_x) - 10, max(all_x) + 10)
    ax.set_ylim(min(all_y) - 10, max(all_y) + 10)
    ax.set_aspect('equal', adjustable='datalim')

    # Disegna le linee rosse orizzontali
    ax.axhline(y=1044.82, color='red', linestyle='--')
    ax.axhline(y=1244.83, color='red', linestyle='--')

    # Mostra il grafico
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('DXF Plot')
    plt.show()


    
# linee = [-0.6249980469]
if __name__ == '__main__':
    linee = [(1414.0, 0.0, 0.0), (48.0, 0.0, 0.0), (48.0, 100.0, 0.0), (1414.0, 100.0, 0.0), (1414.0, 0.0, 0.0)]
    punti = []
    # punti = [(649.21293767043,7), (659.705634124542,7) ,(683.2846994321671,7) ,(690.78706232957,7), (658.79570776823,2), (681.20429223177,2)]


    if len(linee) > 0 and len(punti) == 0:
        plot_lines(lines_sets=[linee])
    elif len(punti) > 0 and len([linee]) == 0:
        plot_lines(points_sets=[punti])
    elif len(linee) > 0 and len(punti) > 0:
        plot_lines(lines_sets=[linee], points_sets=[punti])
    else:
        plot_lines()
