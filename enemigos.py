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
import random


# Creamos la clase "Enemigos" y dentro generamos código necesario.
class Enemigos():
    def __init__(self, x, y):
        #Lista con todos los enemigos activos
        self.lista_enemigos = []
        #Direccion en la que van los enemigos
        self.direccion = 1
        #Indica si los enemigos estñan muertos o no
        self.muerto = False
        #Sprite del Goomba
        self.goombasprite = (
        constantes.GOOMBA_SPRITE_1[0], constantes.GOOMBA_SPRITE_1[1], constantes.GOOMBA_SPRITE_1[2],
        constantes.GOOMBA_SPRITE_1[3], constantes.GOOMBA_SPRITE_1[4])
        #Sprite del Koopa
        self.koppasprite = (0, 48, 64, 16, 24)

    '''Funcion goomba'''
    def goomba(self, direccion, avance):
        if not self.muerto:
            #Animacion del Goomba
            if (pyxel.frame_count //8) % 2 == 0:
                self.goombasprite = (constantes.GOOMBA_SPRITE_1[0], constantes.GOOMBA_SPRITE_1[1], constantes.GOOMBA_SPRITE_1[2], constantes.GOOMBA_SPRITE_1[3], constantes.GOOMBA_SPRITE_1[4])
            else:
                self.goombasprite = (constantes.GOOMBA_SPRITE_2[0], constantes.GOOMBA_SPRITE_2[1], constantes.GOOMBA_SPRITE_2[2], constantes.GOOMBA_SPRITE_2[3], constantes.GOOMBA_SPRITE_2[4])
        else:
            self.goombasprite = (constantes.GOOMBA_MUERTO[0], constantes.GOOMBA_MUERTO[1], constantes.GOOMBA_MUERTO[2], constantes.GOOMBA_MUERTO[3], constantes.GOOMBA_MUERTO[4])

    '''Funcion Koopa'''
    def koppa(self, direccion):
        #Animacion del Koopa
        if (pyxel.frame_count // 5) % 2 == 0:
            self.koppasprite = (0, 48, 64, 16, 24)
        else:
            self.koppasprite = (0, 64, 64, 16, 24)

    '''Generador de enemigos'''
    def spawner(self, avance):
        p = pyxel.frame_count %100
        n = random.randint(0,100)
        self.goomba(1, avance)
        self.koppa(1)
        self.avance = avance
        #Comprueba si no hay más de 4 enemigos en pantalla y su el numero random coincide con el nuemero de frames
        if len(self.lista_enemigos) <4 and p == n and self.avance > -1500:
            #Si n <= añade un Koopa
            if n <=25:
                self.lista_enemigos.append([constantes.WIDTH - self.avance + 16, 163, 'KOOPA', -1, 0])
            #Sino añade un Goomba
            else:
                self.lista_enemigos.append([constantes.WIDTH -self.avance +16, 171, 'GOOMBA', -1])
        for i in range(len(self.lista_enemigos)):
            #Borro de la lista a los enemigos que no estén en pantalla
            if self.lista_enemigos[i][0] + self.avance <= -16:
                del(self.lista_enemigos[i])
            #Dibujo un Koopa y lo muevo en el eje X
            if self.lista_enemigos[i][2] == 'KOOPA':
                self.lista_enemigos[i][0] +=1 * self.lista_enemigos[i][3]
                pyxel.blt(self.lista_enemigos[i][0] + self.avance - 16, self.lista_enemigos[i][1], self.koppasprite[0],
                          self.koppasprite[1],
                          self.koppasprite[2],
                          self.lista_enemigos[i][3] * self.koppasprite[3], self.koppasprite[4], colkey=0)
            # Dibujo un Goomba y lo muevo en el eje X
            else:
                self.lista_enemigos[i][0] += 1 * self.lista_enemigos[i][3]
                pyxel.blt(self.lista_enemigos[i][0] + self.avance -16, self.lista_enemigos[i][1], self.goombasprite[0], self.goombasprite[1],
                          self.goombasprite[2],
                          self.goombasprite[3], self.goombasprite[4], colkey=7)

    '''Colisiones entre enemigos y escenario'''
    def colisiones(self, ancho, alto, objeto, avance, bloques):
        for i in range(len(self.lista_enemigos)):
            self.colider = self.lista_enemigos[i]
            self.objeto = objeto
            self.ancho = ancho
            self.alto = alto
            self.avance = avance
            self.bloques = bloques
            #Colisiones entre los enemigos y los bloques, si estos chocan devuelven un valor
            if self.ancho - 5 >= self.objeto.x - (self.colider[0] -8 + self.avance) >= -11 and - self.objeto.sprite[
                4] <= self.objeto.y - self.colider[1] + 1 <= 2 and not self.objeto.muerto:
                self.lista_enemigos[i][3]=0
                del(self.lista_enemigos[i])
                return 'arriba'
            elif 0 < self.objeto.x + 14 - (
                    self.colider[0] - 10 + self.avance) < self.ancho - 5 and 1.1 < self.objeto.y - (
                    self.colider[1] - self.alto) < self.alto * 2 and not self.objeto.muerto:
                return 'izquierda'
            elif -7 <= self.objeto.x - (
                    self.colider[0] + self.avance + self.ancho -18) < 0 and 1.1 <= self.objeto.y - (
                    self.colider[1] - self.alto) < self.alto * 2 and not self.objeto.muerto:
                return 'derecha'

            # Colisiones entre los enemigos y las tuberias, si estos chocan con una cambian su dirección
            for j in range(len(self.bloques)):
                if self.bloques[j][2] == 'TUBERIA':
                    if self.lista_enemigos[i][1] + 16  >= self.bloques[j][1] and -7 < (self.bloques[j][0] + self.avance) - (self.lista_enemigos[i][0] + self.avance) < 0:
                        self.lista_enemigos[i][3] = -1
                    elif (self.lista_enemigos[i][1] + 16 >= self.bloques[j][1] and -40 <= (self.bloques[j][0] + self.avance) - (self.lista_enemigos[i][0] + self.avance) < 0):
                        self.lista_enemigos[i][3] = 1

            if 1056<=self.lista_enemigos[i][0] <=1088:
                self.lista_enemigos[i][1]+=2


