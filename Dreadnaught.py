import pygame
import colores
from Proyectil import Proyectil
from Explosion import Explosion
from get_superficies import get_superficies

class Dreadnaught(pygame.sprite.Sprite):
    def __init__(self,posx,posy,vidas) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = get_superficies("assets/enemigos/dreadnaught/animacion.png",1,60,250,250)
        self.pos = 0
        self.imagen = self.imagenes[self.pos]
        self.rect = self.imagen.get_rect()
        self.hitbox = pygame.Rect(posx+52,posy+26,145,200)

        self.lista_disparos = []
        self.velocidad =  6
        self.rect.top = posy
        self.rect.left = posx

        self.derecha = True
        self.max_descenso = self.rect.top + 100
        self.tiempo_cambio = pygame.time.get_ticks() + 100

        self.sonido_aparicion = pygame.mixer.Sound("assets/sonidos/aparicion dreadnaught.mp3")
        self.sonido_aparicion.set_volume(0.3)
        self.aparecio = False 

        self.vidas = vidas
        self.sonido_disparo = pygame.mixer.Sound("assets/sonidos/onda.mp3")
        self.sonido_impacto = pygame.mixer.Sound("assets/sonidos/impacto fragata.wav")
        self.sonido_impacto.set_volume(0.25)
        self.sonido_disparo.set_volume(0.05)
        self.muerte = False
        self.explosion = False
        self.sonido_muerte = pygame.mixer.Sound("assets/sonidos/explosion dreadnaught.mp3")
        self.sonido_muerte.set_volume(1)
        self.puntos = 1000
        self.damage = 3

        self.tiempo_cambio = pygame.time.get_ticks() + 100
        self.descendio = False
        self.acumulador = 0

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual >= self.tiempo_cambio:
            self.tiempo_cambio = tiempo_actual + 100  
            self.pos = (self.pos + 1) % len(self.imagenes)
            self.imagen = self.imagenes[self.pos]


    def movimiento_lateral(self):
        if self.derecha:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > 1100:
                self.derecha = False
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < 0:
                self.derecha = True
    
    def descenso(self):
        if self.acumulador < 300:
            self.rect.top += 5
            self.acumulador +=5
        else:
            self.descendio = True

    def disparar(self):
        ruta = "assets/enemigos/dreadnaught/onda.png"
        x,y = self.rect.center
        proyectil = Proyectil(x,y+40,ruta,6,100,100,(60,20),(20,37))
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

    def explotar(self,grupo_explosion_dreadnaught):
        self.explosion = False
        self.muerte = True
        ruta = "assets/enemigos/dreadnaught/explosion.png"
        x, y = self.hitbox.center
        explosion = Explosion(x, y, ruta, 250, 250, 5, 12)
        grupo_explosion_dreadnaught.add(explosion)
        self.sonido_muerte.set_volume(0.1)
        self.sonido_muerte.play()

    def dibujar(self,superficie):
        """ pygame.draw.rect(superficie,colores.GREEN,self.rect)    
        pygame.draw.rect(superficie,colores.RED1,self.hitbox)  """ 
        if self.muerte == False and self.explosion == False:
            self.hitbox.x = self.rect.x+ 52
            self.hitbox.y = self.rect.y + 26
            superficie.blit(self.imagen,self.rect)
        
          
