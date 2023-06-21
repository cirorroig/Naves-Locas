import pygame
from pygame.locals import *
from get_superficies import get_superficies

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,ruta,alto,ancho,velocidad,columnas):
        pygame.sprite.Sprite.__init__(self)
        self.animacion_explosion = get_superficies(ruta,1,columnas,alto,ancho)
        self.pos_explosion = 0
        self.image =  self.animacion_explosion[self.pos_explosion]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.contador = 0
        self.velocidad = velocidad
        
    def update(self):

        self.contador += 1

        if self.contador >= self.velocidad and self.pos_explosion < len(self.animacion_explosion) - 1:
            self.contador = 0
            self.pos_explosion += 1
            self.image = self.animacion_explosion[self.pos_explosion]

        if self.pos_explosion >= len(self.animacion_explosion) - 1 and self.contador >= self.velocidad:
            self.explosion_terminada = True
            self.kill() #Elimina la instancia
    
            
        