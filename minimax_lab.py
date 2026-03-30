import random
import os

class Laberinto:
    def movimientos_permitidos(self, posicion):
        y, x = posicion
        movimientos = []
        # MOVIMIENTOS BÁSICOS (UNICOS PERMITIDOS): Arriba, Abajo, Izquierda, Derecha
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
        for dy, dx in direcciones:
            new_y, new_x = y + dy, x + dx # posicion + direccion = nueva posicion
            # Verificación para que no salga de la matriz
            if 0 <= new_y < self.dimensiones and 0 <= new_x < self.dimensiones:  
                movimientos.append((new_y, new_x))
        return movimientos

    def __init__(self, dimensiones=8):
        self.dimensiones = dimensiones   #self es la forma en que cada objeto se refiere a sí mismo, lo ayuda a englobarse para poder ser utilizado en el futuro
        # posiciones iniciales (fila, columna)
        self.gato_pos = [-1, 0]
        self.raton_pos = [dimensiones - 1, dimensiones - 1]
        self.tablero = [] # se inicializa vacío y se llena en actualizar_tablero
        self.actualizar_tablero()

    def calcular_distancia(self, pos1, pos2):
        """Calcula la distancia de Manhattan entre dos puntos."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def actualizar_tablero(self):
        # creamos una matriz limpia llena de guiones '-'
        self.tablero = [['-' for _ in range(self.dimensiones)] for _ in range(self.dimensiones)]  # la _ es para no usar una vartable innecesaria
        
        # colocamos las piezas en sus posiciones actuales
        gy, gx = self.gato_pos
        ry, rx = self.raton_pos
        
        # asegurarnos de que las posiciones estén dentro de los límites
        gy = max(0, min(gy, self.dimensiones - 1))   # aca le dices a Python: "Elige el menor entre la posición actual y el límite máximo
        gx = max(0, min(gx, self.dimensiones - 1))   # ahora tomamos ese resultado y lo comparamos con el límite mínimo (0)
        ry = max(0, min(ry, self.dimensiones - 1))   # si el resultado anterior fue 7: max(0, 7) devuelve 7. (Sigue igual).Si el resultado anterior fue -2,
        rx = max(0, min(rx, self.dimensiones - 1))   # (porque el gato intentó subir más allá de la fila 0), max(0, -2) devuelve 0. (Lo frenamos en el borde superior)

        self.tablero[gy][gx] = 'G'
        self.tablero[ry][rx] = 'R'

    def mostrar(self):
        # para que se vea bien en la consola limpia
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{'--- GATO VS RATÓN (TÚ) ---':^30}")
        print(f"{'Usa W, A, S, D para mover al Ratón (R)':^30}\n")
        for fila in self.tablero:
            print(" ".join(fila))
        print("-" * 30)

    def evaluar_posicion(self, pos_gato, pos_raton):
        # si el raton es atrapado,
        if pos_gato == pos_raton:
            return -100
        # el raton quiere Maximizar la distancia, el gato Minimizarla
        return self.calcular_distancia(pos_gato, pos_raton)

    def minimax(self, pos_gato, pos_raton, profundidad, es_maximizador):
        # Caso base
        if profundidad == 0 or pos_gato == pos_raton:
            return self.evaluar_posicion(pos_gato, pos_raton)
        
        if es_maximizador: # Turno simulado del RATÓN (el gato se pone en los zapatos del raton)
            max_eval = float('-inf')
            # AHORA TAMBIÉN USAMOS 4 DIRECCIONES AQUÍ
            for movimiento in self.movimientos_permitidos(pos_raton):
                eval = self.minimax(pos_gato, list(movimiento), profundidad - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        
        else: # Turno simulado del GATO (analiza q consecuencia tiene su posible movimiento))
            min_eval = float('inf')
            for movimiento in self.movimientos_permitidos(pos_gato):
                eval = self.minimax(list(movimiento), pos_raton, profundidad - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

def movimiento_usuario(juego):
    """Pide al usuario una dirección (WASD) y devuelve la nueva posición."""
    while True:
        entrada = input("Tu turno (Ratón 'R'). Mueve con W(↑), A(←), S(↓), D(→): ").upper()
        
        if entrada not in ['W', 'A', 'S', 'D']:
            print("¡Entrada inválida! Usa W, A, S o D.")
            continue
        
        dr, dc = 0, 0   # uso de vectores en lugar de muchos if,  Delta Row (Cambio en la Fila / vertical).  Delta Column (Cambio en la Columna / horizontal)
        if entrada == 'W': dr = -1 # Arriba
        elif entrada == 'S': dr = 1  # Abajo
        elif entrada == 'A': dc = -1 # Izquierda
        elif entrada == 'D': dc = 1  # Derecha
        
        r, c = juego.raton_pos
        nueva_pos = [r + dr, c + dc]  # row + direccion row, column + direccion column
        
        # verifica si el movimiento esta dentro de la matriz
        if 0 <= nueva_pos[0] < juego.dimensiones and 0 <= nueva_pos[1] < juego.dimensiones:
            return nueva_pos
        else:
            print("¡Movimiento fuera de los límites! Intenta otra dirección.")

def jugar():
    dimensiones_tablero = 8 # aca se controla las dimensiones del tablero
    juego = Laberinto(dimensiones=dimensiones_tablero)
    turno_actual = 0
    limite_turnos = 3
    
    while True:
        turno_actual += 1
        juego.mostrar()
        print(f"Turno: {turno_actual}/{limite_turnos}")
        print("Pensando el movimiento del Gato con Minimax (4 dir)...")
        
        # --- TURNO DEL GATO con MINIMAX ---
        posibles_gato = juego.movimientos_permitidos(juego.gato_pos)
        mejor_puntuacion_gato = float('inf')  # la mejor posicion del gato esta en positivo infinito y el lo que busca es bajar lo mas posible su punatuacion
        mejores_movimientos_gato = []

        for mov in posibles_gato:
            # el gato simula el futuro, Profundidad 4
            puntuacion = juego.minimax(list(mov), juego.raton_pos, 4, True) # es "true" pq el gato ya eligio su movimiento (en el punto1), luego dentro de la simulacion
            # le toca al raton y busca su mejor puntuacion posible, y le pasamos "true" para que busque la mejor escapatoria posible en su siguiente turno simulado
            if puntuacion < mejor_puntuacion_gato:
                mejor_puntuacion_gato = puntuacion
                mejores_movimientos_gato = [mov]
            elif puntuacion == mejor_puntuacion_gato:
                mejores_movimientos_gato.append(mov)

        # el gato elige su mejor opción
        if mejores_movimientos_gato:
            juego.gato_pos = list(random.choice(mejores_movimientos_gato))  # por si hay dos opciones que den la misma puntuacion, q no se repita siempre el mismo
        
        juego.actualizar_tablero()
        juego.mostrar() 
        # si el gato atrapa al raton
        if juego.gato_pos == juego.raton_pos:
            print(f"\n¡EL GATO ATRAPÓ AL RATÓN en el turno {turno_actual}!")
            print("Game Over. El queso está a salvo (con el gato).")
            break

        if turno_actual >= limite_turnos:
            print(f"\n¡VICTORIA DEL RATÓN! Sobreviviste los {limite_turnos} turnos.")
            print("¡Disfruta de tu queso virtual! 🧀")
            break

        # --- TURNO DEL RATÓN (USUARIO) ---
        print(f"Turno: {turno_actual}/{limite_turnos}")
        nueva_pos_raton = movimiento_usuario(juego)
        juego.raton_pos = nueva_pos_raton
        
        juego.actualizar_tablero()
        juego.mostrar()

        if juego.raton_pos == juego.gato_pos:
            print(f"\n¡EL RATÓN SE MOVIÓ DIRECTAMENTE HACIA EL GATO!")
            print("Game Over... un movimiento poco inteligente.")
            break

if __name__ == "__main__":   # si este archivo está siendo ejecutado directamente por el usuario (y no siendo importado por otro programa), entonces haz lo siguiente...
    jugar()