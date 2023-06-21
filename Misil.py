import pygame
import colores
from get_superficies import get_superficies
pygame.mixer.init()

class Misil(pygame.sprite.Sprite):
    def __init__(self,posx,posy) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.animacion_misil = get_superficies("assets/nave/misil.png",1,3,100,100)
        self.pos_misil = 0
        self.imagen = self.animacion_misil[self.pos_misil]
        self.rect = self.imagen.get_rect()
        self.hitbox= pygame.Rect(693,607,14,34)
        self.velocidad = 6
        self.tiempo_cambio = pygame.time.get_ticks() + 100

        self.rect.top = posy
        self.rect.left = posx
        

    def actualizar_misil(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual >= self.tiempo_cambio:
            self.tiempo_cambio = tiempo_actual + 100  
            self.pos_misil = (self.pos_misil + 1) % len(self.animacion_misil)
            self.imagen = self.animacion_misil[self.pos_misil]

                
    def trayectoria(self):
        self.rect.top -= self.velocidad
    
    def dibujar(self,superficie):
        self.hitbox.y = self.rect.y + 40 
        self.hitbox.x = self.rect.x + 42 
        
        #pygame.draw.rect(superficie,colores.GREEN,self.hitbox)
        
        superficie.blit(self.imagen,self.rect)
        