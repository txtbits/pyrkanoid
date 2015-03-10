# -*- coding: utf-8 -*-
'''
Pyrkanoid

Minijuego basado en el antiguo Arkanoid construido con Python utilizando la libreria Pygame.
'''

import pygame
from pygame.locals import *
from minijuegolib import *
from random import randint
import sys

pygame.init()

'''
Pantalla
'''
screen = pygame.display.set_mode((ANCHO, ALTO))

fondo_intro = cargar_imagen("intro.jpg")
fondo_puntuaciones = cargar_imagen( "screen_puntuaciones.jpg")
fondo_jugando = cargar_imagen("muro.jpg" )
fondo_perder = cargar_imagen("perder.jpg")
fondo_ganar = cargar_imagen("ganar.jpg")

fondo = fondo_intro

screen.blit(fondo, (0,0))

'''
Declaración de variables de estado del juego
'''
jugando = False
iniciando = True
cerrando = False
empezar = True

arribaa = False 
abajoa = False


'''
Creación de objetos
'''
menu = Menu()
marcadorvidas = Marcador()
pelota = Pelota()
pala = Pala()

tipoLetra = pygame.font.SysFont('arial', 17)
tipoLetra2 = pygame.font.SysFont('arial', 24)
tipoLetra3 = pygame.font.SysFont('arial', 72)

'''
Creación de los grupos de Sprites
'''
pelota_grupo = pygame.sprite.RenderUpdates(pelota)
pala_grupo = pygame.sprite.RenderUpdates(pala)
bloque_grupo = pygame.sprite.RenderUpdates()


def crear_bloques():
    posx = 150
    posy = 40
    for x in range(6):
        bloque = Bloque(posx, posy)
        bloque_grupo.add(bloque)
        posx += 80
    posx = 200
    posy = 90  
    for x in range(4):
        bloque = Bloque(posx, posy)
        bloque_grupo.add(bloque)
        posx += 100
    posx = 150
    posy = 140  
    for x in range(6):
        bloque = Bloque(posx, posy)
        bloque_grupo.add(bloque)
        posx += 80
crear_bloques()

reloj = pygame.time.Clock()

'''
Bucle principal del juego
'''
while True:
    '''
    Gestión de la velocidad del juego
    '''
    reloj.tick(60)  # FPS
    
    '''
    Eventos
    '''
    for event in pygame.event.get():
        if event.type == QUIT:  
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
                
        elif event.type == KEYUP: # Evento que REINICIA el movimiento de la pala a 0 al levantar las teclas.
            pala.dx = 0
            
    if pelota.vidas <= 0:
        fondo = fondo_perder
        jugando = False
        cerrando = True
        pelota.guardar_puntos(pelota.puntos)

    if len(bloque_grupo) == 0:
        fondo = fondo_ganar
        jugando = False
        cerrando = True
        pelota.guardar_puntos(pelota.puntos)

    if iniciando:
        teclasPulsadas = pygame.key.get_pressed()
        if teclasPulsadas[K_DOWN]:
            if abajoa ==  False:
                if menu.posicion < 3:
                    menu.posicion += 1
        elif teclasPulsadas[K_UP]:
            if arribaa == False:
                if menu.posicion > 1:
                    menu.posicion -= 1
        if teclasPulsadas[K_RETURN]:
            if menu.posicion == 1:
                jugando = True
                iniciando = False
                fondo = fondo_jugando
            elif menu.posicion == 2:
                print pelota.leer_puntos('puntos.txt') # FALTA IMPLEMENTARLO EN PANTALLA
            elif menu.posicion == 3:
                sys.exit()
                
        # guardo valor para siguiente iteración
        abajoa = teclasPulsadas[K_DOWN]
        arribaa = teclasPulsadas[K_UP]
        screen.blit(fondo, (0,0))
        menu.dibuja(screen)
        
    if jugando:
        teclasPulsadas = pygame.key.get_pressed()
        # Movimiento de la pala
        if teclasPulsadas[K_LEFT]:
            pala.dx = -4.5
        if teclasPulsadas[K_RIGHT]:
            pala.dx = 4.5
        
        '''
        Detectar colisión de la pelota con la pala
        '''
        if pygame.sprite.spritecollideany(pelota, pala_grupo):
            pelota.dy = -pelota.dy
    
        '''
        Detectar colisión de la pelota con un bloque
        '''
        if pygame.sprite.spritecollide(pelota, bloque_grupo, 1):
            pelota.dy = -pelota.dy
            pelota.puntos += 1
        
        screen.blit(fondo, (0,0))
        
        # Borra
        pelota_grupo.clear( screen, fondo )
        bloque_grupo.clear( screen, fondo )
        pala_grupo.clear( screen, fondo )
        
        # Dibuja
        pelota_grupo.draw(screen)
        bloque_grupo.draw(screen)
        pala_grupo.draw(screen)
        pelota.dibujar_puntos(screen,tipoLetra,tipoLetra2,pelota.puntos)
        marcadorvidas.dibuja(pelota.vidas,screen)
        
        #actualizar pala y pelota    
        pelota_grupo.update()
        if pelota.perder_vida():
            pala.rect.center = (ANCHO/2,600)
            screen.blit(fondo, (0,0))
            pelota_grupo.draw(screen)
            bloque_grupo.draw(screen)
            pala_grupo.draw(screen)
            pelota.dibujar_puntos(screen,tipoLetra,tipoLetra2,pelota.puntos)
            marcadorvidas.dibuja(pelota.vidas,screen)
            pygame.display.update()
            if pelota.vidas >= 1:
                sleep(2)   
        pala_grupo.update()
        pygame.display.update()
        if pelota.vidas == 3 and empezar == True:
                sleep(2)
                empezar = False
            
    if cerrando:
        screen.blit(fondo, (0,0))
        pelota.dibujar_puntos_cerrar(screen,tipoLetra3,pelota.puntos)
        teclasPulsadas = pygame.key.get_pressed()
        if teclasPulsadas[K_SPACE]:
            cerrando = False
            iniciando = True
            pelota.vidas = 3
            fondo = fondo_intro
            crear_bloques()
            pelota.puntos = 0
            pelota.dy = 4
            empezar = True
            
    # Actualiza
    pygame.display.update()
