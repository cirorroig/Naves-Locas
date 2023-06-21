import pygame
import colores 
from Misil import Misil
from Explosion import Explosion
from get_superficies import get_superficies
class Nave:
    def __init__(self,ancho) -> None:
        self.animacion_vida = get_superficies("assets/nave/nave_spritesheet.png",1,4,100,100)
        self.pos_vida = 0
        self.imagen = self.animacion_vida[self.pos_vida]
        self.rect_imagen = self.imagen.get_rect()
        self.rect_imagen.x = ancho/2
        self.rect_imagen.y = 590
        self.hitbox_horizontal = pygame.Rect(20,640,60,20)
        self.hitbox_vertical = pygame.Rect(20,615,20,20)

        self.en_movimiento = False
        self.animacion_motor_idle = get_superficies("assets/nave/motor_idle_spritesheet.png",1,4,100,100)
        self.pos_motor_idle = 0
        self.imagen_motor_idle = self.animacion_motor_idle[self.pos_motor_idle]
        self.rect_imagen_motor_idle = self.imagen_motor_idle.get_rect()
        self.rect_imagen_motor_idle.y = 597

        self.animacion_motor_encendido = get_superficies("assets/nave/motor_encendido_spritesheet.png",1,4,100,100)
        self.pos_motor_encendido = 0
        self.imagen_motor_encendido = self.animacion_motor_encendido[self.pos_motor_encendido]
        self.rect_imagen_motor_encendido = self.imagen_motor_encendido.get_rect()
        self.rect_imagen_motor_encendido.y = 597

        
        self.golpes = 0
        self.sonido_golpe = pygame.mixer.Sound("assets/sonidos/impacto nave.wav")
        self.sonido_golpe.set_volume(0.3) 
        self.muerte = False
        self.explosion = False
        self.sonido_muerte = pygame.mixer.Sound("assets/sonidos/muerte.mp3") 
        self.sonido_muerte.set_volume(0.5)

        self.municion = 6


        self.lista_misiles = []
        self.tiempo_cambio_motor = 1
        self.tiempo_cambio_muerte = 1
        self.sonido_misil = pygame.mixer.Sound("assets/sonidos/MissileLaunchFast.mp3")
        self.sonido_misil.set_volume(0.05)

    
    def actualizar_daño(self,musica,damage):
        if(self.pos_vida < len(self.animacion_vida)-1):
            self.golpes += damage
            self.pos_vida += damage 
           
        else:
            self.golpes = 4
            self.pos_vida = 0
        
        if self.golpes == 1:
            musica[0].stop()
            musica[1].play(-1)
            self.sonido_golpe.play()   
        elif self.golpes == 2:
            musica[0].stop()                 
            musica[1].fadeout(50)
            musica[2].play(-1)
            self.sonido_golpe.play()
        elif self.golpes == 3:
            musica[0].stop()
            musica[1].stop() 
            musica[2].fadeout(50)
            musica[3].play(-1)     
            self.sonido_golpe.play()  
        elif self.golpes >= 4:
            musica[0].stop()
            musica[1].stop() 
            musica[2].stop() 
            musica[3].stop()
            self.explosion = True

    def actualizar_motor_idle(self,tiempo):
        if self.tiempo_cambio_motor == tiempo:
            self.pos_motor_idle += 1 
            self.tiempo_cambio_motor += 1
            if(self.pos_motor_idle > len(self.animacion_motor_idle)-1):
                self.pos_motor_idle = 0

    def actualizar_motor_encendido(self,tiempo):
        if self.tiempo_cambio_motor == tiempo:
            self.pos_motor_encendido += 1 
            self.tiempo_cambio_motor += 1
            if(self.pos_motor_encendido > len(self.animacion_motor_encendido)-1):
                self.pos_motor_encendido = 0
        
    def disparar(self,x,y):
        misil = Misil(x,y)
        self.lista_misiles.append(misil)
        self.sonido_misil.play()

    def dibujar_misiles(self,pantalla,scouts,fragatas,dreadnaught,score):
        if len(self.lista_misiles) > 0:
            for misil in self.lista_misiles:
                misil.dibujar(pantalla)
                misil.trayectoria()
                for scout in scouts:
                    if misil.hitbox.colliderect(scout.hitbox) and scout.muerte == False:
                        scout.explosion = True
                        if misil in self.lista_misiles:
                            self.lista_misiles.remove(misil)
                        score += scout.puntos
                for fragata in fragatas:
                    if misil.hitbox.colliderect(fragata.hitbox) and fragata.muerte == False:
                        if fragata.vidas > 0:
                            if misil in self.lista_misiles:
                                self.lista_misiles.remove(misil)
                            fragata.vidas -= 1
                            fragata.sonido_impacto.play()
                        if fragata.vidas == 0:
                            fragata.explosion = True
                            if misil in self.lista_misiles:
                                self.lista_misiles.remove(misil)
                            score += fragata.puntos
                if misil.hitbox.colliderect(dreadnaught.hitbox) and dreadnaught.muerte == False:
                        if dreadnaught.vidas > 0:
                            if misil in self.lista_misiles:
                                self.lista_misiles.remove(misil)
                            dreadnaught.vidas -= 1
                            dreadnaught.sonido_impacto.play()
                        if dreadnaught.vidas == 0:
                            dreadnaught.explosion = True
                            if misil in self.lista_misiles:
                                self.lista_misiles.remove(misil)
                            score += dreadnaught.puntos            
                if misil.hitbox.top < 0 and misil in self.lista_misiles:
                    self.lista_misiles.remove(misil)
        
        return score

    def explotar(self,grupo_explosion_nave):
        self.sonido_muerte.play()
        self.explosion = False
        self.muerte = True
        ruta = "assets/nave/Explosion.png"
        explosion = Explosion(self.rect_imagen.x+50,self.rect_imagen.y+50, ruta, 100, 100, 5, 8)
        grupo_explosion_nave.add(explosion)
        
    def dibujar(self,pantalla):
        if self.muerte == False and self.explosion == False:
            self.hitbox_horizontal.x = self.rect_imagen.x + 20
            self.hitbox_vertical.x = self.rect_imagen.x + 40
            self.rect_imagen_motor_idle.x = self.rect_imagen.x
            self.rect_imagen_motor_encendido.x = self.rect_imagen.x
            self.imagen = self.animacion_vida[self.pos_vida]
            self.imagen_motor_idle = self.animacion_motor_idle[self.pos_motor_idle]
            
            #pygame.draw.rect(pantalla,colores.RED1,self.rect_imagen)
            """ pygame.draw.rect(pantalla,colores.BLUE,self.hitbox_horizontal)
            pygame.draw.rect(pantalla,colores.GREEN,self.hitbox_vertical) """
            

            pantalla.blit(self.imagen, self.rect_imagen)
            if self.en_movimiento:
                pantalla.blit(self.imagen_motor_encendido,self.rect_imagen_motor_encendido)
            else:
                pantalla.blit(self.imagen_motor_idle,self.rect_imagen_motor_idle)
             

