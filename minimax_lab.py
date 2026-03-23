import random
import copy
import os


class Laberinto:
    def movimientos_permitidos(self, posicion, ocho_direcciones=False):
        y, x = posicion
        movimientos = []
        # movimientos: Arriba, Abajo, Izquierda, Derecha (basico)
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        #si la agilidad aumenta
        if ocho_direcciones:
            direcciones += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dy, dx in direcciones:
            new_y, new_x = y + dy, x + dx
        # verificacion para q no salga de la matriz
            if 0 <= new_y < self.dimensiones and 0 <= new_x < self.dimensiones:
                movimientos.append((new_y, new_x))
        return movimientos
    def __init__(self, dimensiones=5):
        self.dimensiones = dimensiones
        # creamos una matriz llena de puntos '.' que simulen el suelo del laberinto
        self.tablero = [['.' for _ in range(dimensiones)] for _ in range(dimensiones)]
        
        # posiciones iniciales (fila, columna)
        self.gato_pos = [0, 0]
        self.raton_pos = [dimensiones - 1, dimensiones - 1]
        self.actualizar_tablero()
    def calcular_distancia(self, pos1, pos2):
        """Calcula la distancia de Manhattan entre dos puntos."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    def actualizar_tablero(self):
        # limpiamos el tablero visualmente
        for f in range(self.dimensiones):
            for c in range(self.dimensiones):
                self.tablero[f][c] = '-'
        
        # colocamos las piezas en sus nuevas posiciones
        gy, gx = self.gato_pos
        ry, rx = self.raton_pos
        self.tablero[gy][gx] = 'G'
        self.tablero[ry][rx] = 'R'

    def mostrar(self):
        # para que se vea bien en la consola
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{'--- LABERINTO MINIMAX ---':^25}")
        for fila in self.tablero:
            print(" ".join(fila))
        print("-" * 25)
    def evaluar_posicion(self, pos_gato, pos_raton):
        # si el raton es atrapado, tambien pierde puntos
        if pos_gato == pos_raton:
            return -100
        
        # el raton quiere Maximizar la distancia entre ellos
        return self.calcular_distancia(pos_gato, pos_raton)
    def minimax(self, pos_gato, pos_raton, profundidad, es_maximizador): #MINIMAX
        # si se llega al limite o el raton es atrapado
        if profundidad == 0 or pos_gato == pos_raton:
            return self.evaluar_posicion(pos_gato, pos_raton)
                                                                          #MAXIMIZADOR
        if es_maximizador: # turno del raton (quiere el valor mas alto)
            max_eval = float('-inf')
            for movimiento in self.movimientos_permitidos(pos_raton, ocho_direcciones=True): # el raton tiene mas opciones de movimiento
                eval = self.minimax(pos_gato, list(movimiento), profundidad - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        
        else: # turno del gato (si asume que el raton se mueve a la mejor posicion)
            min_eval = float('inf')
            for movimiento in self.movimientos_permitidos(pos_gato, ocho_direcciones=False): # el gato no tiene tanta agilidad
                eval = self.minimax(list(movimiento), pos_raton, profundidad - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

def jugar():
    juego = Laberinto(dimensiones=8)
    turno_actual = 0
    limite_turnos = 20 # para evitar juegos infinitos, el raton gana al sobrevivir estos turnos
    while True:
        turno_actual += 1
        juego.mostrar()
        print(f"Turno: {turno_actual}/{limite_turnos}")
        # --- TURNO DEL GATO con MINIMAX---
        posibles_gato = juego.movimientos_permitidos(juego.gato_pos)
        mejor_puntuacion_gato = float('inf') # el gato busca la distancia minima al raton
        mejores_movimientos_gato = []

        for mov in posibles_gato:
            # el gato simula el futuro (Profundidad 3)
            # pasamos 'True' al final porque el siguiente turno en la simulación sería del Ratón (Maximizador)
            puntuacion = juego.minimax(list(mov), juego.raton_pos, 3, True)
            
            if puntuacion < mejor_puntuacion_gato:
                mejor_puntuacion_gato = puntuacion
                mejores_movimientos_gato = [mov]
            elif puntuacion == mejor_puntuacion_gato:
                mejores_movimientos_gato.append(mov)

        # el gato elige su mejor opción (con desempate aleatorio para evitar bucles)
        juego.gato_pos = list(random.choice(mejores_movimientos_gato))
        juego.actualizar_tablero()
        
        # si el gato alcanza al raton
        if juego.gato_pos == juego.raton_pos:
            juego.mostrar()
            print("¡EL GATO ATRAPÓ AL RATÓN! El queso está a salvo (con el gato).")
            break # Detiene el bucle While

        # --- TURNO DEL RATON ---
        # --- NUEVO MOVIMIENTO INTELIGENTE DEL RATÓN ---
        posibles_raton = juego.movimientos_permitidos(juego.raton_pos)
        mejor_puntuacion = float('-inf')
        mejor_mov_raton = juego.raton_pos

        for mov in posibles_raton:
            # el raton evalua cada movimiento usando una profundidad de 5
            puntuacion = juego.minimax(juego.gato_pos, list(mov), 5, False)
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_mov_raton = mov
        
        juego.raton_pos = list(mejor_mov_raton)
        juego.actualizar_tablero()
        
        # si el raton se encuentra con el gato
        if juego.raton_pos == juego.gato_pos:
            juego.mostrar()
            print("¡EL GATO ATRAPÓ AL RATÓN! El queso está a salvo (con el gato).")
            break
        if turno_actual >= limite_turnos:
            juego.mostrar()
            print(f"¡VICTORIA DEL RATÓN! Sobrevivió los {limite_turnos} turnos.")
            break
        input("Presiona Enter para el siguiente turno...")
        

if __name__ == "__main__":
    jugar() 