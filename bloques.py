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

# Creamos la clase "Bloques" y dentro generamos código necesario.
class Bloques:
    # ====== DIBUJADO DE BLOQUES DEL NIVEL ======
    def pintarBloques(self, x, y, avance, bloques):
        self.x = x
        self.y = y
        self.avance = avance
        self.bloques = bloques
        #Recorre toda la lista de constantes y según el tipo que sea dibuja una textura u otra
        for i in range(len(self.bloques)):
            if self.bloques[i][2] =='TUBERIA':
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1], 0, 0, 96, 26, 60, colkey=7)
            elif self.bloques[i][2] =='MONEDA':
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1],constantes.MONEDA_SPRITE[0],constantes.MONEDA_SPRITE[1],constantes.MONEDA_SPRITE[2]
                          ,constantes.MONEDA_SPRITE[3], constantes.MONEDA_SPRITE[4], colkey=7)
            elif self.bloques[i][2] =='INDESTRUCTIBLE':
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1],constantes.BLOQUE_INDESTRUCTIBLE[0],constantes.BLOQUE_INDESTRUCTIBLE[1],constantes.BLOQUE_INDESTRUCTIBLE[2]
                          ,constantes.BLOQUE_INDESTRUCTIBLE[3], constantes.BLOQUE_INDESTRUCTIBLE[4])
            elif self.bloques[i][2] =='LADRILLO':
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1],constantes.BLOQUE_LADRILLO[0],constantes.BLOQUE_LADRILLO[1],constantes.BLOQUE_LADRILLO[2]
                          ,constantes.BLOQUE_LADRILLO[3], constantes.BLOQUE_LADRILLO[4])
            elif self.bloques[i][2] =='SUELO':
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1], constantes.BLOQUE_SPRITE[0], constantes.BLOQUE_SPRITE[1],
                      constantes.BLOQUE_SPRITE[2], constantes.BLOQUE_SPRITE[3], constantes.BLOQUE_SPRITE[4])
            elif self.bloques[i][2] =='OFF' or (self.bloques[i][2] =='?_MONEDA' and self.bloques[i][3] == 0):
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1], constantes.BLOQUE_LADRILLO[0]
                , 0,
                32, 16, 16, colkey = 4)
            elif self.bloques[i][2] == '?' or self.bloques[i][2] == '?_MONEDA':
                pyxel.blt(self.bloques[i][0] + self.avance, self.bloques[i][1],
                          constantes.BLOQUE_INTERROGACION[0],
                          constantes.BLOQUE_INTERROGACION[1], constantes.BLOQUE_INTERROGACION[2]
                          , constantes.BLOQUE_INTERROGACION[3], constantes.BLOQUE_INTERROGACION[4])

    # ====== DIBUJADO DEL FONDO DEL NIVEL ======
    def fondo(self, avance):
        pyxel.blt(0 + avance, 158, constantes.COLINA[0], constantes.COLINA[1],constantes.COLINA[2],constantes.COLINA[3],constantes.COLINA[4], colkey=7)
        pyxel.blt(256 + avance, 168, constantes.COLINA[0], constantes.COLINA[1], constantes.COLINA[2],
                  constantes.COLINA[3], constantes.COLINA[4], colkey=7)
