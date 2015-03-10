# -*- coding: utf-8 -*-


import os
import pygame
from pygame.locals import *
import random
from time import sleep

ANCHO = 700
ALTO = 650
BLANCO = (255,255,255)
NEGRO = (0,0,0)

def cargar_imagen(archivo, usarTransparencia = False):
    '''
    cargar_imagen(archivo) --> imagen
    Carga una imagen desde un archivo, devolviendo el objeto apropiado)
    '''
    lugar = os.path.join("data", archivo)
    try:
        imagen = pygame.image.load(lugar)
    except pygame.error, mensaje:
        print 'No puedo cargar la imagen:', lugar
        raise SystemExit, mensaje
    imagen = imagen.convert()
    if usarTransparencia:
        colorTransparente = imagen.get_at((0,0))
        imagen.set_colorkey(colorTransparente)
    return imagen

def cargar_sonido(archivo):
    '''
    cargar_sonido(archivo) --> devuelve objeto Sound
    '''
    class SinSonido:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return SinSonido()
    lugar = os.path.join("data", archivo)
    try:
        sound = pygame.mixer.Sound(lugar)
    except pygame.error, message:
        print "No puedo cargar el sonido:", lugar
        raise SystemExit, message
    return sound


class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializar la clase Sprite original
        pygame.sprite.Sprite.__init__(self)
        # Almacenar en el sprite la imagen de la pelota
        self.image = cargar_imagen( 'pelota.png', True )
        # Definir el rect del sprite y la posición
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO/2,ALTO/2 - 50)
        # Definir las velocidad
        direccion = [-5, 5]
        self.dx = random.choice(direccion)
        self.dy = 4
        # Cargar el sonido de la pelota
        self.rebote = cargar_sonido('pelota_sound.wav')
        self.vidas = 3
        self.puntos = 0
        
    def update(self):
        # Modificar la posición del sprite
        self.rect.move_ip(self.dx,self.dy)
        # Comprobar si hay que cambiar el movimiento
        if self.rect.left <= 110 or self.rect.right >= 590:
            self.dx = -self.dx
            self.rect.move_ip(self.dx,self.dy)
            self.rebote.play()
        '''Si toca la margen superior de la pantalla'''
        if self.rect.top <= 0:
            self.dy = -self.dy
            self.rect.move_ip(self.dx,self.dy)
            self.rebote.play()
        '''Cambiar la velocidad de la bola según los puntos'''
            
        if self.puntos == 5:
            if self.dy  < 0:
                self.dy = -6
            else:
                self.dy = 6
        
        if self.puntos == 10:
            if self.dy  < 0:
                self.dy = -8.5
            else:
                self.dy = 8.5
        
        if self.puntos == 15:
            if self.dy  < 0:
                self.dy = -10
            else:
                self.dy = 10    
    
    def perder_vida(self):
        '''Si toca margen inferior de la pantalla'''
        if self.rect.bottom >= 650:
            self.rect.center = (ANCHO/2,ALTO/2 - 50)
            self.vidas -= 1
            return True
            
    def dibujar_puntos(self,screen,tipoLetra,tipoLetra2,puntos):
        '''
        Método para pintar el marcador
        '''
        marcadorpuntos = tipoLetra.render(str('PUNTOS'), True, BLANCO)
        marcadorpuntos2 = tipoLetra2.render(str(puntos), True, BLANCO)
        anchura_m = marcadorpuntos2.get_width()
        screen.blit(marcadorpuntos, (23,20,50,50))
        screen.blit(marcadorpuntos2, (50-anchura_m/2,43,50,50))
        
    def dibujar_puntos_cerrar(self,screen,tipoLetra3,puntos):
        '''
        Método para pintar el marcador al terminar la partida
        '''
        marcadorpuntos = tipoLetra3.render(str(puntos), True, BLANCO)
        if self.puntos < 10:
            x = 330
        else:
            x = 323 
        screen.blit(marcadorpuntos, (x,400,50,50))
        
    def leer_puntos(self, fichero):
        '''
        Método para leer de un fichero (puntos.txt) las puntuaciones
        '''
        fr = open('puntos.txt', 'rb')
        contenido = fr.read()
        return contenido
    
    def guardar_puntos(self,puntos):
        '''
        Método para guardar en un fichero (puntos.txt) las puntuaciones
        '''
        if os.path.exists('puntos.txt'):
            f = open('puntos.txt', 'rb')
            contenido = f.read()
            f.close()
            f = open('puntos.txt', 'w')
            f.write(contenido + "\n") # Hay que arreglar esto -> No debería repetirse tantas veces cada ronda.
            f.write(str(puntos)) # Hay que arreglar esto -> No debería repetirse tantas veces cada ronda.
            f.close()
        else:
            f = open('puntos.txt', 'w')
            f.write(str(puntos))
            f.close()
        
        
class Pala(pygame.sprite.Sprite):
    '''
    Pala del jugador
    '''
    def __init__(self):
        '''
        Carga la imagen de la Pala en la posición x = 250, y = 600
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("raqueta.png", True)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO/2,600)
        self.dx = 0
        self.dy = 0 
        
    def update(self):
        '''
        Comprueba los limites de movimiento de la pala.
        '''               
        self.rect.move_ip((self.dx, self.dy))
        if self.rect.left < 110:
            self.rect.left = 110
        elif self.rect.right > 590:
            self.rect.right = 590
        
class Bloque(pygame.sprite.Sprite):
    '''
    Bloques destruibles
    '''
    def __init__(self, posx, posy): 
        '''
        Cargar la imagen del bloque en las posiciones 'posx' y 'posy' las cuales las generaremos para cada bloque
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("bloque.jpg", True)
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        self.dx = 0
        self.dy = 0
            
class Marcador(pygame.sprite.Sprite):
    
    def __init__(self):
        pass

    def dibuja(self, vidas, screen):
        '''
        Cargar las imagenes de las vidas del jugador posicionandolas correctamente.
        '''
        if vidas == 3:
            imagen = cargar_imagen("pelota3vidas.gif",True)
        elif vidas == 2:
            imagen = cargar_imagen("pelota2vidas.gif",True)
        else:
            imagen = cargar_imagen("pelota1vidas.gif",True)
        screen.blit(imagen,(607.5,10,(25), 42))


class Menu(pygame.sprite.Sprite):
    
    def __init__(self):
        self.posicion = 1

    def dibuja(self, screen):
        #Cargar las secciones del menú.
        if self.posicion == 1:
            self.imagen = cargar_imagen("m_comenzar_ON.jpg",True)
        elif self.posicion == 2:
            self.imagen = cargar_imagen("m_puntuaciones_ON.jpg",True)
            proximamente = cargar_imagen("prox_version.jpg",True)
            screen.blit(proximamente,(495,465,(25), 42))
        else:
            self.imagen = cargar_imagen("m_salir_ON.jpg",True)
        # Depende como lo hagamos hay que meterlo en cada condición.
        screen.blit(self.imagen,(200,360,(25), 42))
