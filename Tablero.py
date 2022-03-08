"""
    Created by JOSE ANTONIO
    in 10:50 and 03/12/2021
    UNIVERSIDAD CARLOS III DE MADRID
    ==== MARIO BROSS GAME ====
"""
# Importamos la libreria "pyxel", imprescindible para el proyecto (contiene
# todas las fucnciones, métodos, ... necesarios).
import pyxel
from mario import Mario
from enemigos import Enemigos
from GameEngine import GameEngine
from bloques import Bloques
from power_up import PowerUp
import copy
import constantes

# Creamos la clase "Tablero" y dentro generamos código necesario.
class Tablero:
    # Con el método "def __init__()" construimos las atributos de la clase.
    def __init__(self, w: int, h: int):
        # Paremetros el ancho y el alto del tablero
        self.width = w
        self.height = h
        # Parametro para animacion goomba muerto Duda
        self.a = 10000
        # Posicion Banderin
        self.__ybanderin = 0
        # Avance de la camara
        self.avance = 0
        # Crea a Mario en la pantalla
        self.mario = Mario(40, 170, 3)
        # Crea un atributo koppa para manipular a todos los enemigos en la pantalla
        self.koppa = Enemigos(200, 163)
        # Crea un objeto para los PowerUP
        self.powerup = PowerUp()
        # Posicon X , Y de todoel mapa
        self.x = 0
        self.y = 187
        # Puntuacion de monedas
        self.monedas = 0
        # Llama al objeto GameEngine
        self.gameengine = GameEngine()
        # Llama al objeto Bloques
        self.bloques = Bloques()
        #Cre una lista vacia donde almacenar todos los bloques del nivel
        self.listabloques = []
        # Define si el jugador a ganaado o no
        self.win = False
        #Defino las vidas totales que va a tener Mario
        self.vidas = 3

    # Con el método "def update()" actualiza cada frame según código interior.
    def update(self):

        # Actualiza el movimento de Mario
        self.mario.move(self.width, self.win)
        # Actuliza a Mario
        self.mario.update()
        # Actualiza las monedas y la info de la pantalla
        self.gameengine.update()

        # Si se queda sin tiempo Mario muere directamente
        if int(constantes.TIEMPO_MAX - pyxel.frame_count // 30) <= 0:
            self.mario.mario_power = -1

        # Si presionamos la tecla "Q" salimos del juego.
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        # Camara del juego que avanza si Mario esta en la mitad de la pantalla
        if self.mario.x >= (constantes.WIDTH / 2 - 8) and pyxel.btn(
                pyxel.KEY_RIGHT) and not self.win and self.mario.mario_power >= 0:
            # Si mantenemos presionamos la tecla "Z", mientras mantenemos a
            # Mario en movimineto aumenta su velocidad.
            if pyxel.btn(pyxel.KEY_Z):
                self.avance -= 1 * self.mario.velocidad
            else:
                self.avance -= 1
        else:
            self.avance = self.avance

        '''====== COLISIONES ======'''
        # Colisiones Enemigos y Mario
        if (self.koppa.colisiones(16, self.mario.sprite[4], self.mario,
                                  self.avance, self.listabloques)) == 'arriba' and self.mario.mario_power != -1 and self.mario.vectorY >0:
            # Si Mario toca al Goomba por arriba el Goomba muere y aparece la puntuacion
            pyxel.play(0, 3)
            self.gameengine.puntuacion(100, self.mario.x, self.mario.y, self.avance)
            #Si justo Mario presiona UP este salta más
            if pyxel.btnp(pyxel.KEY_UP):
                self.mario.vectorY = -14
            else:
                self.mario.vectorY = -8
            self.mario.saltando = False
        elif (self.koppa.colisiones(16, self.mario.sprite[4], self.mario,
              self.avance, self.listabloques) == 'izquierda' or
              self.koppa.colisiones(16, self.mario.sprite[4], self.mario, self.avance, self.listabloques) == 'derecha'):
            #Si los enemigos tocan a Mario por la izquierda o derech este pierde poder
            self.mario.daño()
            if self.mario.mario_power <0:
                self.vidas -=1

        # Colisones Flor y Mario
        if (self.colisiones2([self.powerup.xflor, self.powerup.yflor-16], 16, 16,
                            self.mario) == 'izquierda' or self.colisiones2([self.powerup.xflor, self.powerup.yflor-16], 16,
                                                                           16,
                                                                           self.mario) == 'derecha' or self.colisiones2(
                [self.powerup.xflor, self.powerup.yflor-16], 16, 16, self.mario) == 'arriba' or self.colisiones2(
                [self.powerup.xflor, self.powerup.yflor-16], 16, 16, self.mario) == 'abajo') and self.powerup.onflor:
            # Cambiamos el numero de poder de Mario
            self.mario.mario_power = 2
            if self.powerup.onflor:
                self.gameengine.puntuacion(100, self.mario.x, self.mario.y, self.avance)
            self.powerup.onflor = False

        # Colisones Seta y Mario
        if (self.colisiones2([self.powerup.xseta, self.powerup.yseta], 16, 16,
                            self.mario) == 'izquierda' or self.colisiones2(
            [self.powerup.xseta, self.powerup.yseta], 16, 16, self.mario) == 'derecha' or self.colisiones2(
            [self.powerup.xseta, self.powerup.yseta], 16, 16, self.mario) == 'arriba' or self.colisiones2(
            [self.powerup.xseta, self.powerup.yseta], 16, 16, self.mario) == 'abajo')and self.powerup.onseta:
            # Cambiamos el numero de poder de Mario
            self.mario.mario_power = 1
            if self.powerup.onseta:
                self.gameengine.puntuacion(100, self.mario.x, self.mario.y, self.avance)
            self.powerup.onseta = False


        # Actualizo la puntuacion  del marcador
        self.gameengine.puntuacion(self.gameengine.puntos, self.mario.x, self.mario.y, self.avance)

    '''====== COLISIONES CON LOS BLOQUES ======'''
    def bloque(self, x, y):
        for i in range(len(self.listabloques)):
            # Colisiones con Mario y Bloques
            if self.listabloques[i][2] == 'TUBERIA':
                if self.colisiones2([self.listabloques[i][0], self.listabloques[i][1]], 26, 16,
                                    self.mario) == 'arriba':
                    self.mario.vectorY = 0
                    self.mario.y = self.colider[1] - self.mario.sprite[4]
                    self.mario.suelo = True
                elif self.colisiones2([self.listabloques[i][0], self.listabloques[i][1]], 26, 16,
                                      self.mario) == 'izquierda' or (
                        self.mario.y + 16 >= self.listabloques[i][1] and - 14 < self.mario.x - (
                        self.listabloques[i][0] + self.avance) < 0):

                    self.mario.x = self.colider[0] + self.avance - 14
                    self.mario.vectorX = 0
                elif self.colisiones2([self.listabloques[i][0], self.listabloques[i][1]], 26, 16,
                                      self.mario) == 'derecha' or (
                        self.mario.y + 16 >= self.listabloques[i][1] and - 24 <= (
                        self.listabloques[i][0] + self.avance) - self.mario.x <= 0):

                    self.mario.x = self.colider[0] + self.avance + self.ancho - 2
                    self.mario.vectorX = 0
            elif self.listabloques[i][2] == 'MONEDA':
                if self.colisiones2(self.listabloques[i], 10, 14, self.mario) == 'arriba' or self.colisiones2(self.listabloques[i], 10, 14, self.mario) == 'abajo' or self.colisiones2(self.listabloques[i], 10, 14, self.mario) == 'izquierda' or self.colisiones2(self.listabloques[i], 10, 14, self.mario) == 'derecha':
                    self.monedas += 1
                    pyxel.play(0, 0)
                    del(self.listabloques[i])
            if self.colisiones2(self.listabloques[i], 16, 16, self.mario) == 'arriba':
                self.mario.vectorY = 0
                self.mario.y = self.colider[1] - self.mario.sprite[4]
                self.mario.suelo = True
            elif self.colisiones2(self.listabloques[i], 16, 16, self.mario) == 'abajo':
                self.mario.vectorY = 0
                self.mario.y = self.colider[1] + self.alto
                if self.listabloques[i][2] == '?' or self.listabloques[i][2] == '?_MONEDA':
                    # Si colisiona con un bloque ? dependiendo del poder de mario recibe un powerup u otro
                    if self.listabloques[i][2] == '?':
                        if self.mario.mario_power == 0:
                            self.powerup.seta(self.listabloques[i][0], self.listabloques[i][1] - 16, True,
                                              self.avance, [self.mario.x, self.mario.y, self.mario.mario_power])
                        elif self.mario.mario_power >= 1:
                            self.powerup.flor(self.listabloques[i][0], self.listabloques[i][1] - 16, True,
                                              self.avance)
                        #Cambia el tipo de Bloque
                        self.listabloques[i][2] = 'OFF'
                        self.gameengine.puntuacion(200, self.mario.x, self.mario.y, self.avance)
                    else:
                        # Si colisona con un ? y este es de monedas va restando y sumando a la cantidad de monedas de Mario
                        if self.listabloques[i][3] > 0:
                            self.monedas += 1
                            self.gameengine.puntuacion(50, self.mario.x, self.mario.y, self.avance)
                            #Resta 1 al numero de monedas que ocntiene ese bloque
                            self.listabloques[i][3] -= 1
                            self.gameengine.puntuacion(50, self.mario.x, self.mario.y, self.avance)
                            pyxel.play(0, 0)
                # Si Mario es Grande y choca con un LADRILLO lo puede romper
                elif self.listabloques[i][2] == 'LADRILLO' and self.mario.mario_power > 0:
                    del (self.listabloques[i])
                    self.gameengine.puntuacion(50, self.mario.x, self.mario.y, self.avance)
            elif self.colisiones2(self.listabloques[i], 16, 16, self.mario) == 'izquierda':
                self.mario.x = self.colider[0] + self.avance - 14
                self.mario.vectorX = 0
            elif self.colisiones2(self.listabloques[i], 16, 16, self.mario) == 'derecha':
                self.mario.x = self.colider[0] + self.avance + self.ancho - 2
                self.mario.vectorX = 0

    # Con el método "def bandera()" creamos este elemento y lo colocamos en el
    # frame según código interior.
    def bandera(self):
        # Coordenadas del banderin final
        self.__x = 1740 + self.avance
        self.__yp = 20
        #Dibujado de la bandera
        pyxel.blt(self.__x, self.__yp + self.__ybanderin, 0, 16, 32, 16, 16, colkey=0)
        #Dibujado de la linea
        pyxel.line(self.__x + 16, self.__yp, self.__x + 16, 186, 11)
        #Dibujado de la bola
        pyxel.blt(self.__x + 12, self.__yp - 7, 0, 32, 32, 8, 8, colkey=7)
        #Dibujado del Bloque
        pyxel.blt(self.__x + 8, 187, constantes.BLOQUE_INDESTRUCTIBLE[0],
                  constantes.BLOQUE_INDESTRUCTIBLE[1], constantes.BLOQUE_INDESTRUCTIBLE[2]
                  , constantes.BLOQUE_INDESTRUCTIBLE[3], constantes.BLOQUE_INDESTRUCTIBLE[4])
        # Colisiones entre Mario y la bandera
        if self.__x - self.mario.x <= 0.5:
            if not self.mario.suelo:
                # Animacion banderin
                self.__ybanderin += 1
                self.mario.y += 1
                self.mario.gravedad = 0
                self.mario.vectorX = 0
                self.mario.vectorY = 0
            else:
                # Movimiento de Mario si ha pasado la meta
                self.mario.vectorX += 2
            # Booleano que indica si se ha ganado o no
            self.win = True
        #Si Mario ha pasado una cierta posicion desde la bandera el juego se resetea
        if self.mario.x - self.__x >=500:
            self.gameengine.ingame = False
        else:
            self.mario.gravedad = constantes.GRAVEDAD
        if self.win:
            #Se reproduce una musica que indica que Mario ha ganado
            if pyxel.btnp(pyxel.KEY_RIGHT):
                pyxel.playm(1, loop=False)


    '''====== RESET DE TODO EL JUEGO ======='''
    def reset(self):
        #Se encarga de poner todos los valores conforme estaban antes de que el jugador comenzase
        self.koppa.lista_enemigos =[]
        self.mario = Mario(40, 170, self.vidas)
        self.win = False
        self.avance = 0
        self.gameengine.monedas = 0
        self.monedas = 0
        self.__ybanderin = 0
        constantes.tabla_puntuaciones.append(self.gameengine.score)
        self.gameengine.score = 0
        constantes.TIEMPO_MAX= 403
        self.listabloques = copy.deepcopy(constantes.BLOQUES)



    ''''====== COLISONES GENEREALES ENTRE UN OBJETO CON UNA ANCHURA Y ALTURA Y OTRO OBJETO ====='''
    def colisiones2(self, colider, ancho, alto, objeto):
        self.colider = colider
        self.objeto = objeto
        self.ancho = ancho
        self.alto = alto
        #Colisiones por arriba
        if self.ancho - 5 >= self.objeto.x - (self.colider[0] + self.avance) >= -11 and - self.objeto.sprite[
            4] <= self.objeto.y - self.colider[1] <= 2 and not self.objeto.muerto:
            return 'arriba'
        # Colisiones por abajo
        elif 11 >= self.objeto.x - (self.colider[0] + self.avance) >= -11 and -22 <= self.objeto.y - (
                self.colider[1] + self.alto) <= 0 and not self.objeto.muerto:
            return 'abajo'
        # Colisiones por izquierda
        elif 0 < self.objeto.x + 14 - (self.colider[0] + self.avance) < self.ancho - 5 and 1.1 < self.objeto.y - (
                self.colider[1] - self.alto) < self.alto * 2 and not self.objeto.muerto:
            return 'izquierda'
        # Colisiones por derecha
        elif -11 <= self.objeto.x - (self.colider[0] + self.avance + self.ancho - 2) < 0 and 1.1 <= self.objeto.y - (
                self.colider[1] - self.alto) < self.alto * 2 and not self.objeto.muerto:
            return 'derecha'

    '''Funcion que guarda las bolas de fuego de Mario'''
    def bolas(self):
        # Dibujado y animacion de las bolas de fuego almacenadas en una lista
        for i in range(len(self.mario.bolas)):
            self.mario.bolas[i][0] += 2
            if self.mario.bolas[i][0] > self.width:
                #Si las bolas no se ven en pantalla las borra
                del (self.mario.bolas[i])
            pyxel.blt(self.mario.bolas[i][0] + self.avance, self.mario.bolas[i][1], 0, 16, 80, 8, 8, colkey=7)

    # Utilizamos la función "def draw()" para dibujar la escena según sea
    # necesario y el código interior de la misma.
    def draw(self):
        # PANTALLA DE GAME OVER SI VIDAS < 1
        if self.mario.vida < 1:
            self.gameengine.game_over()
        # PANTALLA VIDAS Y NIVEL SI MARIO MUERE
        elif self.mario.y > 1000:
            if not self.mario.muerto:
                self.mario.vida -= 1
                self.mario.muerto = True
            #Tiempo que esta esta pantalla activa
            if pyxel.frame_count // 30 - self.ti <= 2:
                self.gameengine.pre_game(self.vidas)
            else:
                self.reset()
            self.avance = 0
        # PANTALLA DE TITULO
        elif not self.gameengine.ingame:
            self.gameengine.title_screen(self.avance)
            self.reset()
            self.t = pyxel.frame_count // 30
        # PANTALLA VIDAS Y NIVEL SI MARIO MUERE
        elif self.gameengine.ingame:
            if pyxel.frame_count // 30 - self.t <= 2:
                self.gameengine.pre_game(self.mario.vida)
                self.reset()
            # PANTALLA DEL JUEGO
            else:
                pyxel.cls(6)
                self.gameengine.datos(self.monedas)
                self.bloques.fondo(self.avance)
                self.bloques.pintarBloques(self.x, self.y, self.avance, self.listabloques)
                self.bloque(self.x, self.y)
                self.bolas()
                self.bandera()
                self.ti = pyxel.frame_count //30

                self.koppa.spawner(self.avance)
                if self.powerup.onseta:
                    self.powerup.seta(self.powerup.xseta, self.powerup.yseta, self.powerup.onseta, self.avance,
                                      [self.mario.x, self.mario.y, self.mario.mario_power])
                if self.powerup.onflor:
                    self.powerup.flor(self.powerup.xflor, self.powerup.yflor, self.powerup.onflor, self.avance)

                # Dibujado del tiempo
                pyxel.text(constantes.WIDTH - 26, 19, str(constantes.TIEMPO_MAX - pyxel.frame_count // 30), 7)
                #Animacion del coldown de Mario si recibe daño
                if not self.mario.coldown or self.mario.mario_power <0:
                    pyxel.blt(self.mario.x, self.mario.y, self.mario.sprite[0], self.mario.sprite[1],
                              self.mario.sprite[2], self.mario.animacion_derecha * self.mario.sprite[3],
                              self.mario.sprite[4], colkey=7)
                else:
                    if pyxel.frame_count // 8 % 2 == 0:
                        pyxel.blt(self.mario.x, self.mario.y, self.mario.sprite[0], self.mario.sprite[1],
                                  self.mario.sprite[2], self.mario.animacion_derecha * self.mario.sprite[3],
                                  self.mario.sprite[4], colkey=7)
                #Dibujado de los puntos que recoge Mario
                self.gameengine.puntuacion(self.gameengine.puntos, self.mario.x, self.mario.y, self.avance)
