import pygame
import colores
from get_superficies import get_superficies

pygame.mixer.init()

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ruta,columnas,alto,ancho,coordenadas_hitbox,ajuste_hitbox) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.animacion = get_superficies(ruta,1,columnas,alto,ancho)
        self.pos = 0
        self.imagen = self.animacion[self.pos]
        self.rect = self.imagen.get_rect()
        self.hitbox= pygame.Rect(posx,posy,coordenadas_hitbox[0],coordenadas_hitbox[1]) 
        self.ajuste = ajuste_hitbox
        self.velocidad = 3
        self.tiempo_cambio = pygame.time.get_ticks() + 100

        self.rect.top = posy
        self.rect.left = posx
        
    def actualizar_proyectil(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual >= self.tiempo_cambio:
            self.tiempo_cambio = tiempo_actual + 100  
            self.pos = (self.pos + 1) % len(self.animacion)
            self.imagen = self.animacion[self.pos]

    def trayectoria(self):
        self.rect.top += self.velocidad
    
    def dibujar(self,superficie):
        self.hitbox.x = self.rect.x + self.ajuste[0]
        self.hitbox.y = self.rect.y + self.ajuste[1]

        #pygame.draw.rect(superficie,colores.GREEN,self.hitbox)
        superficie.blit(self.imagen,self.rect)
        