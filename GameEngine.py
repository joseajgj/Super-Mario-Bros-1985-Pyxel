"""
    Created by JOSE ANTONIO 
    in 10:50 and 03/12/2021
    UNIVERSIDAD CARLOS III DE MADRID
    ==== MARIO BROSS GAME ====
"""
# Importamos la libreria "pyxel", imprescindible para el proyecto (contiene
# todas las fucnciones, métodos, ... necesarios).
import pyxel

# Importamostodo el contenido del archivo "constante.py".
import constantes

# Importamos la clase "Mario" desde el archivo "mario.py".
from mario import Mario

# Importamos la Bloques "Tablero" desde el archivo "bloques.py".
from bloques import Bloques

# Creamos la clase "GameEngine" y dentro generamos código necesario.
class GameEngine():
    def __init__(self):
        self.mario = Mario(10, 171, 3)
        # Puntuacion de Mario
        self.score = 0
        # Bloques del nivel
        self.bloques = Bloques
        # Puntos al matar un enemigo
        self.puntos = 0
        # Animacion de esos puntos
        self.animacion = 0
        # Monedas del nivel
        self.monedas = 0
        # Booleano que detecta si esta dentro del juego o no
        self.ingame = False

    # ====== PANTALLA DEL TITULO ======
    def title_screen(self, avance):
        #Pintamos el fondo de azul
        pyxel.cls(6)
        #Mostramos los datos al usuario
        self.datos(self.monedas)
        self.avance = avance
        #Pintamos una colina al fondo
        pyxel.blt(0, 0, 2, 0, 0, 256, 210, colkey=3)
        pyxel.blt(0, 156, constantes.COLINA[0], constantes.COLINA[1], constantes.COLINA[2],
                  constantes.COLINA[3], constantes.COLINA[4], colkey=7)
        pyxel.blt(256, 168, constantes.COLINA[0], constantes.COLINA[1], constantes.COLINA[2],
                  constantes.COLINA[3], constantes.COLINA[4], colkey=7)
        #Pintamos un Mario
        pyxel.blt(40, 172, self.mario.sprite[0], self.mario.sprite[1], self.mario.sprite[2],
                  self.mario.animacion_derecha * self.mario.sprite[3], self.mario.sprite[4], colkey=7)
        #Pintamos los bloques del nivel
        for i in range(len(constantes.BLOQUES)):
            if constantes.BLOQUES[i][2] == 'SUELO':
                pyxel.blt(constantes.BLOQUES[i][0], constantes.BLOQUES[i][1], constantes.BLOQUE_SPRITE[0],
                          constantes.BLOQUE_SPRITE[1],
                          constantes.BLOQUE_SPRITE[2], constantes.BLOQUE_SPRITE[3], constantes.BLOQUE_SPRITE[4])
        pyxel.text(constantes.WIDTH / 2 + 28, constantes.HEIGHT / 2, str('(c) UC3M 2021'), 7)
        #Mostramos un texto que parpadea
        if pyxel.frame_count // 30 % 2 == 0:
            pyxel.text(constantes.WIDTH / 2 - 21.5, constantes.HEIGHT / 2 + 31.5, 'PRESS SPACE', 0)
            pyxel.text(constantes.WIDTH / 2 - 22, constantes.HEIGHT / 2 + 32, 'PRESS SPACE', 7)
        #Puntuacion maxima del jugador
        pyxel.text(constantes.WIDTH / 2 - 24, constantes.HEIGHT / 2 + 52, 'TOP - ' + str(max(constantes.tabla_puntuaciones)).zfill(6), 7)

    # ====== PANTALLA ANTES DEL NIVEL ======
    def pre_game(self, vidas):
        self.vida = vidas
        pyxel.cls(0)
        pyxel.text(constantes.WIDTH / 2 - 22, constantes.HEIGHT / 2 - 32, 'WORLD  1-1', 7)
        pyxel.text(constantes.WIDTH / 2 - 3, constantes.HEIGHT / 2, 'x', 7)
        pyxel.text(constantes.WIDTH / 2 + 11, constantes.HEIGHT / 2, str(self.vida), 7)
        pyxel.blt(constantes.WIDTH / 2 - 30, constantes.HEIGHT / 2 - 8, self.mario.sprite[0], self.mario.sprite[1],
                  self.mario.sprite[2],
                  self.mario.animacion_derecha * self.mario.sprite[3], self.mario.sprite[4], colkey=7)
        self.datos(self.monedas)

     # ====== PANTALLA GAME OVER ======
    def game_over(self):
        pyxel.cls(0)
        pyxel.text(constantes.WIDTH / 2 - 16, constantes.HEIGHT / 2 - 8, 'GAME OVER', 7)
        self.datos(self.monedas)

    # ====== ANIMACION CUANDO MARIO CONSIGUE LOS PUNTOS ======
    def puntuacion(self, puntos, posx, posy, avance):
        self.puntos = puntos
        self.posx = posx
        self.posy = posy
         #Mostramos la puntuacion que va subiendo por la pantalla hasta que se añade al marcador
        if self.animacion > -60:
            if self.puntos == 100:
                self.animacion = self.animacion - 1
                pyxel.blt(self.posx, self.posy - 16 + self.animacion, constantes.PUNTUACIONES_SPRITE[0][0],
                          constantes.PUNTUACIONES_SPRITE[0][1],
                          constantes.PUNTUACIONES_SPRITE[0][2], constantes.PUNTUACIONES_SPRITE[0][3],
                          constantes.PUNTUACIONES_SPRITE[0][4], colkey=1)
            if self.puntos == 200:
                self.animacion = self.animacion - 1
                pyxel.blt(self.posx, self.posy - 16 + self.animacion, constantes.PUNTUACIONES_SPRITE[1][0],
                          constantes.PUNTUACIONES_SPRITE[1][1],
                          constantes.PUNTUACIONES_SPRITE[1][2], constantes.PUNTUACIONES_SPRITE[1][3],
                          constantes.PUNTUACIONES_SPRITE[1][4], colkey=1)
        else:
            self.score += self.puntos
            self.puntos = 0
            self.animacion = 0

    # ====== PULSA ESPACIO ======
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.ingame = True
            if not self.ingame:
                constantes.TIEMPO_MAX += pyxel.frame_count // 30

    # ====== DATOS DE LA PUNTUACION, NIVEL, TIEMPO ======
    def datos(self, monedas):
        self.monedas = monedas
        pyxel.text(constantes.WIDTH - 30, 10, constantes.PANTALLA[6:10], 7)
        pyxel.text(constantes.WIDTH - 62, 19, '1-1', 7)
        pyxel.text(20, 10, constantes.PANTALLA[0:5], 7)
        pyxel.text(20, 19, str(self.score).zfill(6), 7)
        pyxel.text(constantes.WIDTH - 70, 10, constantes.PANTALLA[10:], 7)
        pyxel.text(100, 19, 'COIN ' + str(self.monedas).zfill(2), 7)
