import pygame
from funciones import *

ANCHO_VENTANA = 1300
ALTO_VENTANA = 700
PANTALLA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()
#Reloj
crear_base_de_datos()
menu(ANCHO_VENTANA, ALTO_VENTANA, PANTALLA)
pygame.quit()
