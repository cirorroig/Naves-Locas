import pygame
from random import randrange
from Proyectil import Proyectil
from Explosion import Explosion
import colores
from get_superficies import get_superficies

class Scout(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ciclos,limite) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.imagenes = get_superficies("assets/enemigos/scout/scout.png",1,6,130,130)
        self.pos = 0
        self.imagen = self.imagenes[self.pos]
        self.rect = self.imagen.get_rect()
        self.hitbox = pygame.Rect(posx+45,posy+45,40,40)
        self.limite = limite
        self.lista_disparos = []
        self.velocidad =  5
        self.rect.top = posy
        self.rect.left = posx

        self.ciclos = ciclos
        self.contador = 0
        self.derecha = True
        self.max_descenso = self.rect.top + 80

        self.sonido_aparicion = pygame.mixer.Sound("assets/sonidos/scout_aparicion.wav")
        self.aparecio = False 

        self.sonido_disparo = pygame.mixer.Sound("assets/sonidos/disparo scout.wav")
        self.sonido_disparo.set_volume(0.1)
        self.muerte = False
        self.explosion = False
        self.sonido_muerte = pygame.mixer.Sound("assets/sonidos/muerte scout.wav")
        
        self.puntos = 100
        self.damage = 1

    def actualizar(self):
        self.pos += 1
        if self.pos > len(self.imagenes) - 1:
            self.pos = 0 

    def movimiento(self):
        if self.contador < self.ciclos:
            self.movimiento_lateral()
        else:
            self.descenso()

    def movimiento_lateral(self):
        if self.derecha:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > self.limite:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < 0:
                self.derecha = True
    

    def descenso(self):
        if self.max_descenso  ==  self.rect.top:
            self.contador = 0
            self.max_descenso = self.rect.top + 80
        else:
            self.rect.top += 5


    def disparar(self):
        x,y = self.rect.center
        ruta = "assets/enemigos/scout/bala_scout.png"
        proyectil = Proyectil(x-9,y+4,ruta,4,20,20,(20,20),(0,0))
        self.lista_disparos.append(proyectil)
        self.sonido_disparo.play()

    def dibujar_disparo(self,pantalla,nave,musica):
        for disparo in self.lista_disparos:
            disparo.dibujar(pantalla)
            disparo.trayectoria()
            if disparo.rect.colliderect(nave.hitbox_horizontal) or disparo.rect.colliderect(nave.hitbox_vertical):
                nave.actualizar_daño(musica,self.damage)
                self.lista_disparos.remove(disparo)
            if disparo.rect.top > 700:
                self.lista_disparos.remove(disparo)

    def explotar(self,grupo_explosion_scout):
        self.explosion = False
        self.muerte = True
        ruta = "assets/enemigos/scout/explosion_scout.png"
        x,y = self.hitbox.center
        explosion = Explosion(x, y-1, ruta, 130, 130, 5, 10)
        grupo_explosion_scout.add(explosion)
        self.sonido_muerte.set_volume(0.1)
        self.sonido_muerte.play()

    def dibujar(self,superficie):
        if self.muerte == False and self.explosion == False:
            self.image = self.imagenes[self.pos]
            self.hitbox.x = self.rect.x + 45
            self.hitbox.y = self.rect.y + 45
            superficie.blit(self.image,self.rect)
        
        #pygame.draw.rect(superficie,colores.GREEN,self.rect)    
        #pygame.draw.rect(superficie,colores.RED1,self.hitbox)    

