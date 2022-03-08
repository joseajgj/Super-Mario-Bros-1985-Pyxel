"""
    Created by JOSE ANTONIO 
    in 10:50 and 03/12/2021
    UNIVERSIDAD CARLOS III DE MADRID
    ==== MARIO BROSS GAME ====
"""

# Importamos la libreria "pyxel", imprescindible para el proyecto (contiene
# todas las fucnciones, métodos, ... necesarios).
import pyxel
import constantes

# Creamos la clase "PowerUp" y dentro generamos código necesario.
class PowerUp:
    def __init__(self):
        #Booleano que indica si se ha activado el powerup
        self.onseta = False
        self.onflor = False
        #Coordenadas del objeto en pantalla
        self.xseta = 0
        self.yseta = 0
        self.xflor = 0
        self.yflor = 0
        #Indica si la seta esta en el aire o no
        self.enaire = False

    '''SETA'''
    def seta(self, x, y, on, avance, mario):
        self.xseta = x
        self.yseta = y
        #Cambio las coordenas de la seta segun la y
        if self.yseta >=171:
            self.xseta += 1.1
        else:
            self.yseta +=constantes.GRAVEDAD
        self.onseta = on
        #Dibujado de la seta en el juego
        pyxel.blt(self.xseta + avance, self.yseta, constantes.SETA_SPRITE[0],
                  constantes.SETA_SPRITE[1],
                  constantes.SETA_SPRITE[2], constantes.SETA_SPRITE[3], constantes.SETA_SPRITE[4], colkey=0)

    '''FLOR'''
    def flor(self, x,y, on, avance):
        self.xflor = x
        self.yflor = y
        self.onflor = on
        #Dibujado de la flor en el juego
        pyxel.blt(self.xflor + avance, self.yflor, constantes.SETA_SPRITE[0], 16,
                  48, 16, 16, colkey=4)

