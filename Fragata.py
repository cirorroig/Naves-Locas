import pygame
import colores
from Proyectil import Proyectil
from Explosion import Explosion

class Fragata(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ciclos,lado,limite) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("assets/enemigos/fragata/fragata.png")
        self.imagen = pygame.transform.scale(self.imagen,(130,130))
        self.rect = self.imagen.get_rect()
        self.hitbox = pygame.Rect(posx+28,posy+22,74,82)

        self.lista_disparos = []
        self.velocidad =  5
        self.rect.top = posy
        self.rect.left = posx
        self.limite = limite
        self.ciclos = ciclos
        self.contador = 0
        self.derecha = True
        self.max_descenso = self.rect.top + 130
        self.sonido_aparicion = pygame.mixer.Sound("assets/sonidos/aparicion fragata.wav")
        self.sonido_aparicion.set_volume(0.3)
        self.aparecio = False 

        self.vidas = 3
        self.sonido_disparo = pygame.mixer.Sound("assets/sonidos/bala fragata.wav")
        self.sonido_impacto = pygame.mixer.Sound("assets/sonidos/impacto fragata.wav")
        self.sonido_impacto.set_volume(0.25)
        self.sonido_disparo.set_volume(0.05)
        self.muerte = False
        self.explosion = False
        self.sonido_muerte = pygame.mixer.Sound("assets/sonidos/explosion fragata.wav")
        self.sonido_muerte.set_volume(2)
        self.puntos = 300
        self.damage = 2
        self.lado_descenso = lado

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
            self.max_descenso = self.rect.top + 130
        else:
            self.rect.top += 5

    def disparar(self):
        ruta = "assets/enemigos/fragata/bala.png"
        x,y = self.rect.center
        proyectil = Proyectil(x-9,y+4,ruta,4,40,40,(40,40),(0,0))
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

    def explotar(self,grupo_explosion_fragata):
        self.explosion = False
        self.muerte = True
        ruta = "assets/enemigos/fragata/fragata explosion.png"
        x, y = self.hitbox.center
        explosion = Explosion(x, y-1, ruta, 130, 130, 5, 9)
        grupo_explosion_fragata.add(explosion)
        self.sonido_muerte.set_volume(0.1)
        self.sonido_muerte.play()

    def dibujar(self,superficie):
        """ pygame.draw.rect(superficie,colores.GREEN,self.rect)    
        pygame.draw.rect(superficie,colores.RED1,self.hitbox) """  
        if self.muerte == False and self.explosion == False:
            self.hitbox.x = self.rect.x + 28
            self.hitbox.y = self.rect.y + 22
            superficie.blit(self.imagen,self.rect)
        
          
