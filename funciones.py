import pygame
import pygame_gui
import sys
import sqlite3
from random import randrange
from Nave import Nave
from Scout import Scout
from Fragata import Fragata
from Dreadnaught import Dreadnaught
from Boton import Boton
import colores

def generar_musica_de_fondo():

    pygame.mixer.init()
    pygame.mixer.music.set_volume(1)
    sonido_fondo1 = pygame.mixer.Sound("assets/sonidos/fondo full vida.mp3")
    sonido_fondo1.set_volume(0.3)
    sonido_fondo2 = pygame.mixer.Sound("assets/sonidos/fondo poco dañado.mp3")
    sonido_fondo2.set_volume(0.3)
    sonido_fondo3 = pygame.mixer.Sound("assets/sonidos/fondo dañado.mp3")
    sonido_fondo3.set_volume(0.3)
    sonido_fondo4 = pygame.mixer.Sound("assets/sonidos/fondo muy dañado.mp3")
    sonido_fondo4.set_volume(0.3)
    musica_fondo = [sonido_fondo1, sonido_fondo2, sonido_fondo3, sonido_fondo4]

    return musica_fondo

def generar_scouts(cantidad):
    lista_scouts = []
    posx = 100
    posy = -90
    for i in range(cantidad):
        limite = randrange(400,1250,200)
        ciclos = randrange(1,2)
        scout = Scout(posx,posy,ciclos,limite)
        lista_scouts.append(scout)
        posx += 130
        if (i + 1) % 5 == 0: #Cada 5 enemigos los genera en una linea mas arriba
            posy -= 90
            posx = 100
    
    return lista_scouts

def generar_fragatas(cantidad):
    lista_fragatas = []
    posx = 250
    posy = -130
    for i in range(cantidad):
        limite = randrange(400,1250,400)
        ciclos = randrange(1,2)
        lado = True if i % 2 == 0 else False # Cambia el lado de descenso de la fragata
        fragata = Fragata(posx,posy,ciclos,lado,limite)
        lista_fragatas.append(fragata)
        posy -= 130

    return lista_fragatas

def dibujar_scouts(scouts,pantalla,nave,musica):
    if len(scouts) > 0:
        for scout in scouts:
            if scout.muerte == False:
                scout.movimiento()
                scout.dibujar(pantalla)
                if len(scout.lista_disparos) > 0:
                    scout.dibujar_disparo(pantalla,nave,musica)
            elif scout.muerte and len(scout.lista_disparos) > 0:
                scout.dibujar_disparo(pantalla,nave,musica)
            else:
                scouts.remove(scout)

def dibujar_fragatas(fragatas,pantalla,nave,musica):
    if len(fragatas) > 0:
        for fragata in fragatas:
            if fragata.muerte == False:
                fragata.movimiento()
                fragata.dibujar(pantalla)
                if len(fragata.lista_disparos) > 0:
                    fragata.dibujar_disparo(pantalla,nave,musica)
            elif fragata.muerte and len(fragata.lista_disparos) > 0:
                fragata.dibujar_disparo(pantalla,nave,musica)
            else:
                fragatas.remove(fragata)

def dibujar_dreadnaught(dreadnaught,pantalla,nave,musica,grupo):
    if dreadnaught.explosion == False:
        if dreadnaught.descendio == False:
            dreadnaught.descenso()
        dreadnaught.actualizar()
        dreadnaught.movimiento_lateral()
        dreadnaught.dibujar(pantalla)
        if len(dreadnaught.lista_disparos) > 0:
            dreadnaught.dibujar_disparo(pantalla,nave,musica)
            for disparo in dreadnaught.lista_disparos:
                disparo.actualizar_proyectil()
    else:
        dreadnaught.explotar(grupo)

def actualizar_grupos_sprites(grupo_nave,grupo_scout,grupo_fragata,grupo_dreadnaught,pantalla):
    if bool(grupo_scout):
        grupo_scout.draw(pantalla)
        grupo_scout.update()
    if bool(grupo_fragata):
        grupo_fragata.draw(pantalla)
        grupo_fragata.update()
    if bool(grupo_dreadnaught):
        grupo_dreadnaught.draw(pantalla)
        grupo_dreadnaught.update()
    if bool(grupo_nave):
        grupo_nave.draw(pantalla)
        grupo_nave.update()

def jugar(ancho,alto,pantalla,cant_scouts,cant_fragatas,vidas_dreadnaught):

    imagen_fondo = pygame.image.load("assets/Space Background.png")
    imagen_fondo = pygame.transform.scale(imagen_fondo,(ancho, alto))
    pygame.display.set_caption("Naves Locas")
    #Reloj
    reloj = pygame.time.Clock()
    #Timers
    timer_disparo_scout = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_disparo_scout, 3000)
    timer_disparo_fragata = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_disparo_fragata, 2000)
    timer_disparo_dreadnaught = pygame.USEREVENT + 3
    pygame.time.set_timer(timer_disparo_dreadnaught, 1000)
    timer_partida = pygame.USEREVENT + 4
    pygame.time.set_timer(timer_partida, 1000)
    
    #Musica
    musica = generar_musica_de_fondo()
    #Nave
    nave = Nave(ancho)
    grupo_explosion_nave = pygame.sprite.Group()
    #Scouts
    scouts = generar_scouts(cant_scouts)
    grupo_explosion_scout = pygame.sprite.Group()

    #Fragatas
    fragatas = generar_fragatas(cant_fragatas)
    grupo_explosion_fragata= pygame.sprite.Group()

    #Dreadnaught
    dreadnaught = Dreadnaught(ancho/2,-300,vidas_dreadnaught)
    grupo_explosion_dreadnaught= pygame.sprite.Group()
    #Score
    score = 0
    tiempo_partida = 0
    fuente = get_fuente(14)

    running = True

    musica[0].play(-1)
    
    tiempo_disparo = 300
    ultimo_disparo = 0
    while running:
        reloj.tick(60)
        
        tiempo = int(pygame.time.get_ticks()/1000)
        

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                running = False
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                
                ahora = pygame.time.get_ticks()
                if ahora - ultimo_disparo > tiempo_disparo:
                    x = nave.rect_imagen.x
                    y = nave.rect_imagen.y
                    nave.disparar(x,y)
                    ultimo_disparo = ahora
            if evento.type == timer_partida:
                tiempo_partida += 1
            if scouts:
                if evento.type == timer_disparo_scout:
                    for scout in scouts:
                        if scout.hitbox.bottom > 0 and scout.muerte == False:
                            scout.actualizar()
                            if scout.aparecio == False:
                                scout.sonido_aparicion.play()
                                scout.aparecio = True
                                scout.sonido_aparicion.set_volume(0.05)
            if fragatas and scouts == []:
                if evento.type == timer_disparo_fragata:
                    for fragata in fragatas:
                        if fragata.hitbox.bottom > 0 and fragata.muerte == False:
                            if fragata.aparecio == False:
                                fragata.sonido_aparicion.play()
                                fragata.aparecio = True
                            fragata.disparar()
            if fragatas == [] and scouts == [] and dreadnaught.muerte == False:
                if evento.type == timer_disparo_dreadnaught :
                    if dreadnaught.hitbox.bottom > 0:
                        if dreadnaught.aparecio == False:
                                dreadnaught.sonido_aparicion.play()
                                dreadnaught.aparecio = True
                        dreadnaught.disparar()
                    

        lista_teclas = pygame.key.get_pressed()
        if True in lista_teclas:
            if lista_teclas[pygame.K_d] and nave.rect_imagen.x < ancho - 100:
                nave.en_movimiento = True
                nave.rect_imagen.x = nave.rect_imagen.x + 15
            if lista_teclas[pygame.K_a] and nave.rect_imagen.x > 0:
                nave.rect_imagen.x = nave.rect_imagen.x - 15
                nave.en_movimiento = True

        if lista_teclas[pygame.K_d] == False and lista_teclas[pygame.K_a] == False:
            nave.en_movimiento = False

        if nave.en_movimiento == False:
            nave.actualizar_motor_idle(tiempo)
        else:
            nave.actualizar_motor_encendido(tiempo)
        
        for scout in scouts:
            for disparo in scout.lista_disparos:
                disparo.actualizar_proyectil()
            if scout.explosion:
                scout.explotar(grupo_explosion_scout)
       
        for fragata in fragatas:
            for disparo in fragata.lista_disparos:
                disparo.actualizar_proyectil()
            if fragata.explosion:
                fragata.explotar(grupo_explosion_fragata)

        for misil in nave.lista_misiles:
            misil.actualizar_misil()
                
        if nave.explosion:  
            nave.explotar(grupo_explosion_nave)

        if nave.muerte and grupo_explosion_nave.sprites() == []:    
            mostrar_pantalla_de_puntuacion(ancho,alto,pantalla,score,True,musica,tiempo_partida)
        
        pantalla.blit(imagen_fondo, imagen_fondo.get_rect())
        # Dibujo personaje
        nave.dibujar(pantalla)
        #Dibujo misiles
        score = nave.dibujar_misiles(pantalla,scouts,fragatas,dreadnaught,score)
        # Dibujo enemigos
        if scouts:
            dibujar_scouts(scouts,pantalla,nave,musica)
        if scouts == [] and fragatas:
            dibujar_fragatas(fragatas,pantalla,nave,musica)
        if scouts == [] and fragatas == []:
            dibujar_dreadnaught(dreadnaught,pantalla,nave,musica,grupo_explosion_dreadnaught)
        if scouts == [] and fragatas == [] and dreadnaught.muerte and grupo_explosion_dreadnaught.sprites() == []:
            mostrar_pantalla_de_puntuacion(ancho,alto,pantalla,score,False,musica,tiempo_partida)

        actualizar_grupos_sprites(grupo_explosion_nave,grupo_explosion_scout,grupo_explosion_fragata,grupo_explosion_dreadnaught,pantalla)

        texto = f"SCORE:{score}"
        puntos = fuente.render(texto,True,colores.GOLD1)
        tiempo = f"TIEMPO:{tiempo_partida}"
        timer = fuente.render(tiempo,True,colores.GOLD1)
        pantalla.blit(puntos,[10,10])
        pantalla.blit(timer,[10,27])

        pygame.display.flip()

def mostrar_menu_dificultades(ancho,alto,pantalla):
    fondo_menu = pygame.image.load("assets/menu/fondo2.png")
    fondo_menu = pygame.transform.scale(fondo_menu,(ancho,alto))
    
    fuente = get_fuente(60)
    texto_menu = fuente.render("SELECCIONE DIFICULTAD",True,colores.ANTIQUEWHITE)
    rect_menu = texto_menu.get_rect(center = (650,150))
    pygame.display.set_caption("Naves Locas")
    lista_botones = crear_botones_menu("FACIL","NORMAL","DIFICIL",40)
    
    running = True

    while running:
    
        pantalla.blit(fondo_menu,fondo_menu.get_rect())
        pos_mouse = pygame.mouse.get_pos()

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                running = False
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if lista_botones[0].verificar_input(pos_mouse):
                    jugar(ancho,alto,pantalla,5,4,5)
                elif lista_botones[1].verificar_input(pos_mouse):
                    jugar(ancho,alto,pantalla,10,6,10)
                elif lista_botones[2].verificar_input(pos_mouse):
                    jugar(ancho,alto,pantalla,15,8,15)

        pantalla.blit(texto_menu,rect_menu)

        for boton in lista_botones:
            boton.cambiar_color(pos_mouse)
            boton.actualizar(pantalla)
    
        pygame.display.flip()

def armar_texto_ranking(jugadores):
    texto = ""
    for jugador in jugadores:
        cadena =f'{jugador["posicion"]}. {jugador["nombre"]} - {jugador["puntuacion"]}\n' 
        texto += cadena
    
    texto_ranking = texto

    return texto_ranking

def mostrar_ranking(ancho,alto,pantalla):
    running = True
    pygame.display.set_caption("Naves Locas")
    fondo_menu = pygame.image.load("assets/menu/fondo2.png")
    fondo_menu = pygame.transform.scale(fondo_menu,(ancho,alto))

    fuente_boton  = get_fuente (40)
    boton_volver = Boton(None,(650,600),"VOLVER",fuente_boton,colores.ANTIQUEWHITE,colores.GOLD4)

    jugadores = leer_base_de_datos()

    texto = armar_texto_ranking(jugadores)

    fuente_titulo = get_fuente(60)
    texto_titulo = fuente_titulo.render("RANKING TOP 10:\n",True,colores.ANTIQUEWHITE)
    rect_titulo = texto_titulo.get_rect(center = (700,150))

    fuente_ranking = get_fuente(24)
    texto_ranking= fuente_ranking.render(texto,True,colores.ANTIQUEWHITE)
    rect_ranking = texto_ranking.get_rect(center = (650,350))

    while running:
        
        pos_mouse = pygame.mouse.get_pos()

        eventos  = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                running = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.verificar_input(pos_mouse):
                    menu(ancho,alto,pantalla)

        pantalla.blit(fondo_menu,fondo_menu.get_rect())
        pantalla.blit(texto_titulo,rect_titulo)
        pantalla.blit(texto_ranking,rect_ranking)
        boton_volver.cambiar_color(pos_mouse)
        boton_volver.actualizar(pantalla)

        pygame.display.flip()

def get_fuente(pixeles):
    return pygame.font.Font("assets/menu/fuente.ttf", pixeles)

def crear_botones_menu(texto_1,texto_2,texto_3,fuente):

    fuente = get_fuente(fuente)

    imagen_1 =  pygame.image.load("assets/menu/rectangulo jugar.png")
    boton_1 = Boton(imagen_1,(650,300),texto_1,fuente,colores.ANTIQUEWHITE,colores.GOLD4)

    if texto_2 == "NORMAL":
        imagen_2 =  pygame.image.load("assets/menu/rectangulo jugar.png")
        boton_2 = Boton(imagen_2,(650,450),texto_2,fuente,colores.ANTIQUEWHITE,colores.GOLD4)
    else:
        imagen_2 =  pygame.image.load("assets/menu/rectangulo ranking.png")
        boton_2 = Boton(imagen_2,(650,450),texto_2,fuente,colores.ANTIQUEWHITE,colores.GOLD4)

    if texto_2 == "DIFICIL":
        imagen_3 =  pygame.image.load("assets/menu/rectangulo jugar.png")
        boton_3 = Boton(imagen_3,(650,600),texto_3,fuente,colores.ANTIQUEWHITE,colores.GOLD4)
    else:         
        imagen_3 =  pygame.image.load("assets/menu/rectangulo salir.png")
        boton_3 = Boton(imagen_3,(650,600),texto_3,fuente,colores.ANTIQUEWHITE,colores.GOLD4)


    lista_botones = [boton_1,boton_2,boton_3]

    return lista_botones

def menu(ancho,alto,pantalla):
    
    fondo_menu = pygame.image.load("assets/menu/fondo2.png")
    fondo_menu = pygame.transform.scale(fondo_menu,(ancho,alto))
    
    fuente = get_fuente(80)
    texto_menu = fuente.render("NAVES LOCAS",True,colores.ANTIQUEWHITE)
    rect_menu = texto_menu.get_rect(center = (650,150))
    pygame.display.set_caption("Naves Locas")
    lista_botones = crear_botones_menu("JUGAR","RANKING","SALIR",50)
    
    running = True

    while running:
    

        pantalla.blit(fondo_menu,fondo_menu.get_rect())
        pos_mouse = pygame.mouse.get_pos()

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                running = False
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if lista_botones[0].verificar_input(pos_mouse):
                    mostrar_menu_dificultades(ancho,alto,pantalla)
                elif lista_botones[1].verificar_input(pos_mouse):
                    mostrar_ranking(ancho,alto,pantalla)
                elif lista_botones[2].verificar_input(pos_mouse):
                    running = False
                    sys.exit()

        pantalla.blit(texto_menu,rect_menu)

        for boton in lista_botones:
            boton.cambiar_color(pos_mouse)
            boton.actualizar(pantalla)
    
        pygame.display.flip()

def mostrar_pantalla_de_puntuacion(ancho,alto,pantalla,score,murio,musica,tiempo_partida):
    manager = pygame_gui.UIManager((ancho,alto))
    pygame.display.set_caption("Naves Locas")
    fondo_menu = pygame.image.load("assets/menu/fondo2.png")
    fondo_menu = pygame.transform.scale(fondo_menu,(ancho,alto))

    fuente_principal = get_fuente(70)

    has_muerto = fuente_principal.render("HAS MUERTO" if murio else "VICTORIA",True,colores.RED4 if murio else colores.GREEN)
    rect_muerte = has_muerto.get_rect(center = (650,150))


    if tiempo_partida < 40:
        aumento = 1000
        score += 1000
    elif tiempo_partida >= 40 and tiempo_partida <=60:
        aumento = 500
        score += 500
    elif tiempo_partida >= 60 and tiempo_partida <=90:
        aumento = 250
        score += 250

    fuente_secundaria = get_fuente(20)
    puntaje = fuente_secundaria.render(f"Puntaje final:{score} | Tiempo final:{tiempo_partida} suma {aumento} puntos",True,colores.ANTIQUEWHITE)
    rect_puntaje = puntaje.get_rect(center = (650,250))

    explicacion = fuente_secundaria.render("Ingrese su nombre para poder registrar su puntaje.\nPresione enter para confirmar",True,colores.ANTIQUEWHITE)
    rect_explicacion = explicacion.get_rect(center = (650,300))

    pygame_gui.elements.UITextEntryLine(pygame.Rect((370, 400), (500, 50)),manager,object_id = '#input_nombre')

    running = True

    reloj = pygame.time.Clock()
    
    tasa_refresh = reloj.tick(60)/100000

    ruta = "assets/sonidos/gameover.mp3" if murio else "assets/sonidos/victoria.mp3"
    sonido_fondo = pygame.mixer.Sound(ruta)
    sonido_fondo.set_volume(0.3)
    
    for cancion in musica:
        cancion.stop()

    sonido_fondo.play()

    

    while running:
        reloj.tick(60)

        eventos  =  pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                running = False
                sys.exit()
            if evento.type  == pygame_gui.UI_TEXT_ENTRY_FINISHED and evento.ui_object_id == "#input_nombre":
                jugador  = {
                    "nombre": evento.text,
                    "puntuacion":score,
                }
                modificar_base_de_datos(jugador)
                menu(ancho,alto,pantalla)
            
            manager.process_events(evento)   
        
        manager.update(tasa_refresh)

        pantalla.blit(fondo_menu,fondo_menu.get_rect())
        pantalla.blit(has_muerto,rect_muerte)
        pantalla.blit(puntaje,rect_puntaje)
        pantalla.blit(explicacion,rect_explicacion)
        manager.draw_ui(pantalla)

        pygame.display.update()

def crear_base_de_datos():
    with sqlite3.connect("rankings.db") as conexion:
        try:
            sentencia = """ CREATE TABLE IF NOT EXISTS Jugadores
                            (
                                id integer primary key autoincrement,
                                nombre text,
                                puntuacion integer
                            ) 
                        """
            conexion.execute(sentencia)
        except sqlite3.OperationalError:
            print("Ya existe la base de datos")

def modificar_base_de_datos(jugador):
    with sqlite3.connect("rankings.db") as conexion:
        try:
            cursor = conexion.cursor()
            sentencia = "SELECT * FROM Jugadores WHERE nombre  = ?"
            cursor.execute(sentencia,(jugador["nombre"],))
            resultado = cursor.fetchone()

            if resultado and resultado[2] < jugador["puntuacion"]:
                modificacion = "UPDATE Jugadores SET puntuacion = ? WHERE nombre = ?"
                cursor.execute(modificacion,(jugador["puntuacion"],jugador["nombre"]))
            else:
                sentencia = "INSERT INTO Jugadores (nombre,puntuacion) VALUES (?,?)"
                cursor.execute(sentencia,(jugador["nombre"],jugador["puntuacion"]))
            
            conexion.commit()
        except sqlite3.OperationalError:
            print("Error al modificar datos")
    
def leer_base_de_datos():
    with sqlite3.connect("rankings.db") as conexion:
        try:
            cursor = conexion.cursor()
            sentencia = "SELECT * FROM Jugadores ORDER BY puntuacion DESC"
            cursor.execute(sentencia)
            jugadores = cursor.fetchmany(10)
            
            lista_jugadores = []
            posicion = 1
            for jugador in jugadores:
                dict = {
                    "posicion":posicion,
                    "nombre":jugador[1],
                    "puntuacion":jugador[2]
                }
                posicion += 1
                lista_jugadores.append(dict)
        except sqlite3.OperationalError:
            print("Error al leer datos")
    
    return lista_jugadores

