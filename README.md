# Proyecto: El Laberinto del Gato y el Ratón (Minimax Lab)

## Descripción del Experimento
He desarrollado un simulador de persecución en Python donde un **Ratón inteligente** se enfrenta a un **Gato implacable** en un tablero bidimensional de 8x8. El objetivo era implementar el algoritmo **Minimax** para dotar al ratón de la capacidad de predecir el futuro y evitar ser capturado.

## Tecnologías Utilizadas
* **Lenguaje:** Python 3.14
* **Librerías:** `random` (para desempates), `os` (para limpieza de consola),  .
* **Algoritmo:** Minimax con profundidad configurable (Depth 3).

## ¿Cómo funciona el cerebro del Ratón?
El ratón no se mueve al azar. En cada turno, ejecuta una búsqueda en árbol:
1. **Maximización:** El ratón busca la posición que maximice la distancia de Manhattan respecto al gato.
2. **Minimización:** El ratón asume que el gato es inteligente y que elegirá el movimiento que más lo acerque.
3. **Puntuación:** Si el gato atrapa al ratón en su "imaginación", ese camino recibe una puntuación de -100.

## Bitácora de Desarrollo (¡Aja! Moments)

### Lo que fue un desastre:
- **El Bucle Infinito** Al principio, el gato y el ratón se quedaban oscilando entre dos casillas para siempre. 
- **El Salto del Tigre** El gato a veces "atravesaba" al ratón porque el chequeo de victoria estaba mal ubicado en el flujo del código.

### Mi mejor "¡Ajá!":
- Descubrí que el **Minimax puro** es demasiado determinista. Si hay dos movimientos con la misma puntuación, el ratón siempre elegía el primero, causando los bucles. Lo solucioné implementando un **Desempate Aleatorio**: si dos caminos son igual de seguros, el ratón elige uno al azar, rompiendo la predictibilidad del gato.
- Convertir al gato en un **agente Minimax**  transformó el juego de una simple persecución a un duelo de estrategias. El gato ya no solo sigue al ratón, sino que intenta predecir sus rutas de escape, obligándome a aumentar la profundidad del ratón para que pueda sobrevivir.
- Implementar las **8 direcciones** para el ratón cambió drásticamente el equilibrio del juego. Aunque el gato use Minimax, la agilidad diagonal del ratón le permite encontrar rutas de escape que no existen en una cuadrícula tradicional de 4 movimientos.

## Condiciones de Finalización
* **Victoria del Gato:** Si alcanza la misma coordenada que el ratón.
* **Victoria del Ratón:** Si logra sobrevivir 20 turnos sin ser atrapado.

- **para q sirve upper.( )** :Es un método de cadenas de texto (strings) que se utiliza para convertir todos los caracteres alfabéticos de una cadena a mayúsculas. Los caracteres que no son letras (como números, símbolos o espacios) no se ven afectados.

- **para q se usa "abs"** :es una función incorporada que devuelve el valor absoluto de un número. El valor absoluto de un número es su valor numérico sin tener en cuenta su signo. En términos simples, convierte los números negativos en positivos y deja los positivos igual.

- **q hace max, min** : Son funciones incorporadas que se utilizan para encontrar el valor máximo y mínimo, respectivamente. Pueden recibir dos o más argumentos numéricos directos, o un objeto "iterable" (como una lista). Basicamente buscan el mayor o menor valor para poder utilizarlo.

- **:^30}\n**  :Esta es una sintaxis especial de formateo de cadenas (f-strings) en Python. Se usa dentro de las llaves {} para controlar cómo se muestra una variable. Vamos a desglosarla:

:: Indica el inicio de las opciones de formato.

^: Es el símbolo para centrar el texto.

30: Especifica el ancho total del campo en caracteres. El texto se centrará dentro de este espacio de 30 caracteres, rellenando con espacios en blanco a los lados si es necesario.

}: Cierra la expresión del f-string.

\n: Es un carácter especial que representa un salto de línea (como pulsar Enter). No es parte del formateo del texto en sí, sino que añade una línea en blanco después de imprimirlo.

- **min eval, max eval** : Se usan convencionalmente dentro del algoritmo Minimax para llevar la cuenta de la mejor evaluación encontrada hasta el momento durante la búsqueda.

- **float("inf")**: Es la forma en Python de representar el concepto matemático de infinito positivo ("inf") e infinito negativo ("-inf"). Al convertirlos a tipo flotante (float), obtenemos valores especiales que son garantizadamente mayores (o menores) que cualquier otro número real.

- **Heuristica** : En términos sencillos, la heurística se refiere a atajos mentales o reglas generales que utilizamos para resolver problemas y tomar decisiones de forma rápida y eficiente, especialmente cuando nos enfrentamos a situaciones complejas, con información incompleta o cuando el tiempo es limitado.

1. **Arquitectura y Estructura (POO)**
Programación Orientada a Objetos (POO): Explica que usaste una  *class Laberinto* para encapsular toda la lógica. Esto hace que el código sea organizado y reutilizable.

El Constructor (__init__): Menciona que aquí es donde se define el "estado inicial" del sistema (dimensiones del tablero y posiciones de los jugadores).

Métodos de Interfaz: Resalta  *mostrar()* y  *actualizar_tablero()* como la capa de visualización que permite al usuario interactuar con la lógica interna.

2.  **El Corazón de la IA: Algoritmo Minimax**
Este es el punto más importante de la exposición. 

 *Árbol de Decisión:* Explica que el gato no elige al azar, sino que construye un árbol de posibles futuros.

 *Recursividad:* Menciona que la función minimax se llama a sí misma para explorar niveles más profundos.

 *Caso Base:* Es vital mencionar que la recursión se detiene por profundidad (límite de visión) o por victoria (el gato atrapa al ratón).

 **Maximización vs. Minimización:* * El Ratón actúa como un agente que maximiza la distancia (quiere alejarse).

El Gato actúa como un agente que minimiza esa misma distancia (quiere acercarse).

3.  **Lógica Matemática y Espacial**
 *Distancia de Manhattan:* Explica por qué elegiste esta y no la Euclidiana (Pitágoras). Di que es más precisa para movimientos en una rejilla donde no hay diagonales (movimiento tipo "Taxi").

 *Representación Matricial:* El tablero es una matriz bidimensional (lista de listas), que es la estructura de datos estándar para entornos de juegos 2D.

 *Vectores de Movimiento:* Explica el uso de dr (Delta Row) y dc (Delta Column) para calcular desplazamientos de forma matemática y limpia.

4.  **Robustez y Control de Errores**
 *Clamping (Límites):* Menciona el uso de max() y min() para evitar que las coordenadas se salgan de los índices de la matriz, previniendo errores de "Index Out of Range".

 *Validación de Entradas:* Cómo el programa maneja las teclas (W, A, S, D) y rechaza cualquier otra entrada inválida.

5.  **Conceptos Avanzados de Python**
*List Comprehensions:* Menciona que usaste esta sintaxis avanzada para crear el tablero de forma eficiente en una sola línea.

*Copiado de Datos (list(mov)):* Explica la importancia de pasar copias de las posiciones a la recursión para no alterar el estado real del juego durante la simulación.

*Punto de Entrada (if __name__ == "__main__":):* Explica que esto asegura que el juego solo inicie si el archivo se ejecuta directamente, permitiendo que el código sea modular.

- Tip Extra:
Si el jurado te pregunta: "¿Cómo lo mejorarías?", tú responde:

"Para tableros más grandes, implementaría la Poda Alfa-Beta (Alpha-Beta Pruning) para descartar ramas del árbol que no son prometedoras y así ahorrar recursos computacionales".