filas = 4
columnas = 4
matriz = []
for i in range(filas):
    fila = []
    for j in range (columnas):
        fila.append('.')

    matriz.append(fila)

matriz[0][0] = 'r'
matriz[3][3] = 'g'
for fila in matriz:
    print(fila)