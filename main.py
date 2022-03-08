"""
    Created by JOSE ANTONIO 
    in 10:50 and 03/12/2021
    UNIVERSIDAD CARLOS III DE MADRID
    ==== MARIO BROSS GAME ====
"""

# Importamos la libreria "pyxel", imprescindible para el proyecto (contiene
# todas las fucnciones, métodos, ... necesarios).
import pyxel

# Importamos la clase "Tablero" desde el archivo "Tablero.py".
from Tablero import Tablero

# Importamos todoel contenido del archivo "constante.py".
import constantes

# Ajustmos el tamaño de la pantalla a 216 pixel de alto y 210 pixel de ancho.
# Para ello asignamos valores de las constantes "WIDTH" Y "HEIGHT",
# definidos en el archivo "constantes.py", a la variable "tablero".
tablero = Tablero(constantes.WIDTH, constantes.HEIGHT)

# Ajustamos las características de la pantalla con el método "init()" que
# recibe los parámetros:
#   "tablero.width", "tablero.height", "constantes.CAPTION",
#   "constantes.fps", "constantes.palette", "False"
pyxel.init(tablero.width, tablero.height, caption=constantes.CAPTION, fps=constantes.FPS, palette=constantes.palette,
           fullscreen=False)

# Cargamos el archivo "my_resource.pyxres" que contiene todos los sprites y
# musica del juego
pyxel.load("assets/my_resource.pyxres")

# Cargamos el logo Mario Bros en el banco de imagenes para mostrarlos en el incio
pyxel.image(2).load(0, 0, "assets/titlescreen.png")

# Iniciamos el juego con el función "run()" con los parámetros:
# clase "Tablero" y método ".update", actualizar cada frame segun sea necesario
# clase "tablero" y método ".draw", para dibujar la escena segun sea necesario
# Hacemos que las funciones que se ejecuten cada frame sean las siguientes
pyxel.run(tablero.update, tablero.draw)
