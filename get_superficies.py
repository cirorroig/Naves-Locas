import pygame

def get_superficies(path,filas,columnas,alto,ancho):
    lista = []
    superficie_imagen = pygame.image.load(path)
    fotograma_ancho = int(superficie_imagen.get_width()/columnas)
    fotograma_alto = int(superficie_imagen.get_height()/filas)

    for fila in range(filas):
        for columna in range(columnas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            #un pedacito de la imagen del sprite
            superficie_fotograma = superficie_imagen.subsurface(x,y,fotograma_ancho, fotograma_alto)
            superficie_fotograma = pygame.transform.scale(superficie_fotograma,(alto,ancho))
            lista.append(superficie_fotograma)

    return lista