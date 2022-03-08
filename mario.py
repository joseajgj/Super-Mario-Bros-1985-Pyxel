"""
    Created by JOSE ANTONIO 
    in 10:50 and 03/12/2021
    UNIVERSIDAD CARLOS III DE MADRID
    ==== MARIO BROSS GAME ====
"""

# Importamos la libreria "pyxel", imprescindible para el proyecto (contiene
# todas las fucnciones, métodos, ... necesarios).
import pyxel

# Importamos todoel contenido del archivo "constante.py".
import constantes


class Mario():
    def __init__(self, x: int, y: int, vidas):
        # Este metodo crea el objeto de Mario.
        # @param x inicializa la posicion x de Mario.
        # @param y inicializa la posicion y de Mario.
        # @param vidas inicializa con un numero de vidas
        # Coordenadas x, y en la pantalla.
        self.x = x
        self.y = y
        # Int que indica el PowerUp de Mario, si es negativo, significa que esta muerto
        self.mario_power = 0
        # Vectores X, Y que indican hacia donde se mueve Mario
        self.vectorX = 0
        self.vectorY = 0
        # Gravedad que va a tener Mario
        self.gravedad = constantes.GRAVEDAD
        # Bool que indica si Mario esta tocando el suelo
        self.suelo = True
        # Bool que indica si Mario esta Muerto o no
        self.muerto = False
        # Sprite de Mario
        self.sprite = constantes.MARIO_SPRITE
        # Int que alterna entre 1 y -1 para rotar verticalmente el sprite de Mario
        self.animacion_derecha = 1
        # Vidas de Mario
        self.vida = vidas
        #Incicializamos una lista vacía con todas las bolas de fuego de Mario
        self.bolas = []
        #Booleano que indica si Mario a recibido daño hace poco y puede volver a recibir daño
        self.coldown = False
        #Int que sirve como contador para contar el coldown de Mario
        self.t = 0

    # ====== Movimiento de Mario ======
    def move(self, size: int, win):
        # Tamaño de Mario
        mario_x_size = self.sprite[3]

        # Velocidad de Mario
        if pyxel.btn(pyxel.KEY_Z) and (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT)):
            if self.velocidad <= 3:
                self.velocidad += 0.2
            else:
                self.velocidad = 3
        else:
            self.velocidad = 0.001

        if self.mario_power >=0 and not win:
            # Movimiento de Mario Derecha
            if pyxel.btn(pyxel.KEY_RIGHT) and self.x < size - mario_x_size and self.x < constantes.WIDTH / 2 - 8:
                self.animacion_derecha = 1
                self.vectorX += 1.3 + self.velocidad
            #Animacion de Mario cuando anda
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.animacion()

            # Movimiento de Mario Izquierda
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                self.animacion_derecha = -1
                self.vectorX -= 1.3 + self.velocidad
                # Animacion de Mario cuando anda
                self.animacion()

            # Salto de Mario cuando se presiona el boton
            if pyxel.btnp(pyxel.KEY_UP):
                if self.suelo:
                    self.vectorY = -13.2
                    self.suelo = False
            # Salto de Mario cuando se suelta el boton
            elif pyxel.btnr(pyxel.KEY_UP):
                if self.vectorY < -6:
                    self.vectorY = -6

     # ====== Animacion de Mario ======
    def animacion(self):
        #Nos ayudamos de la funcion Pyxel.frame_count para cambiar el sprite cada intervalo de tiempo definido
        #siempre y cuando el jugador se este moviendo en horizontal
        if (pyxel.frame_count //(3)) % 2 == 0:
            self.sprite = (constantes.MARIO_SPRITE_1[0], constantes.MARIO_SPRITE_1[1], constantes.MARIO_SPRITE_1[2], constantes.MARIO_SPRITE_1[3], constantes.MARIO_SPRITE_1[4])
        elif (pyxel.frame_count //(3)) % 3 == 0:
            self.sprite = (constantes.MARIO_SPRITE_2[0], constantes.MARIO_SPRITE_2[1], constantes.MARIO_SPRITE_2[2], constantes.MARIO_SPRITE_2[3], constantes.MARIO_SPRITE_2[4])

        else:
            self.sprite = (constantes.MARIO_SPRITE_3[0], constantes.MARIO_SPRITE_3[1], constantes.MARIO_SPRITE_3[2], constantes.MARIO_SPRITE_3[3], constantes.MARIO_SPRITE_3[4])

    # ====== Muerte de Mario ======
    def muerte(self):

        # Si la variable es negativa Mario ha muerto
        if self.mario_power < 0:
            #Cambio de Sprite a Mario muerto
            self.sprite = (0, 96, 0, 16, 16)
            # Animación de Mario muriendo si esta en el suelo
            if self.suelo:
                self.vectorY = -10
                self.suelo = False
            #Booleano que indica si esta muerto o no
            self.muerto = True

    # ====== Coldown de Mario ======
    def daño(self):

        #Comprobamos que Mario no haya recibido daño hace poco
        if not self.coldown:
            #Reducimos 1 su poder
            self.mario_power -=1
            #Si queda negativo le quitamos una vida
            if self.mario_power <0:
                self.vida -=1
            #Definimos el instante de tiempo en el ha pasado esto
            self.t = pyxel.frame_count
            #Activamos el coldown para que no se siga ejecutando si Mario sigue en contacto con un enemigo
            self.coldown = True

    # ====== Bolas de fuego de Mario ======
    def bola_fuego(self):
        #Lista con todas las bolas de fuego
        self.bolas.append([self.x + 8, self.y + self.sprite[4]/2])

    def update(self):
        # Según Mario tenga un champiñon o la flor, cambiara su sprite
        if self.mario_power ==1:
            self.sprite = (constantes.MARIO_GRANDE_SPRITE[0], constantes.MARIO_GRANDE_SPRITE[1], constantes.MARIO_GRANDE_SPRITE[2],constantes.MARIO_GRANDE_SPRITE[3], constantes.MARIO_GRANDE_SPRITE[4])
        elif self.mario_power ==2:
            if pyxel.btnp(pyxel.KEY_Z):
                self.bola_fuego()
            self.sprite = (constantes.MARIO_FLOR_SPRITE[0], constantes.MARIO_FLOR_SPRITE[1], constantes.MARIO_FLOR_SPRITE[2],constantes.MARIO_FLOR_SPRITE[3], constantes.MARIO_FLOR_SPRITE[4])
        #Si Mario esta en el suelo y no se está moviendo su sprite será el default
        elif self.mario_power == 0 and self.suelo and not pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_LEFT):
            if self.suelo and not pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_LEFT):
                self.sprite = (0, 0, 0, 16, 16)
        #Si Mario está saltando su sprite será el siguiente
        elif not self.suelo:
            self.sprite = (0, 16, 0, 16, 16)

        #Si ha pasado un intervalo de 2 segundos desde que Mario recibió daño
        #Este puede volver a recibir daño
        if (pyxel.frame_count - self.t)//30 >= 2:
            self.coldown = False

        # Llamo a la funcion muerte para que compruebe si se muere
        Mario.muerte(self)

        # Sumo al vector Y la gravedad del juego
        self.vectorY += self.gravedad

        # Sumo a las coordenadas X, Y sus respectivos vectores
        self.x += self.vectorX
        self.y += self.vectorY
        # El vector X será 0 para que Mario no se deslica por la pantalla
        self.vectorX = 0
