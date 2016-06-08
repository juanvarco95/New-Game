import pygame
import random

ALTO = 300
ANCHO = 300

Blanco = (255,255,255)
Verde = (0,255,0)
Negro= (0,0,0)

def cargar_fondo(archivo, ancho, alto):
        imagen = pygame.image.load(archivo).convert()
        imagen_ancho, imagen_alto = imagen.get_size()
        #print 'ancho: ', imagen_ancho, ' xmax: ', imagen_ancho/ancho
        #print 'alto: ', imagen_alto, 'ymax: ', imagen_alto/alto
        tabla_fondos = []
        for fondo_x in range(0, imagen_ancho/ancho):
                linea = []
                tabla_fondos.append(linea)
                for fondo_y in range(0, imagen_alto/alto):
                        cuadro = (fondo_x * ancho, fondo_y * alto, ancho, alto)
                        linea.append(imagen.subsurface(cuadro))
        return tabla_fondos

if __name__ == '__main__':
        pygame.init()
        pantalla = pygame.display.set_mode([ANCHO,ALTO])
        #pantalla.fill(Blanco)
        terminar = False
        
        

        reloj = pygame.time.Clock()

        while (not terminar):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                terminar = True
                #pantalla.fill(Blanco)
                

                leo = cargar_fondo('Stickman/StickmanNocheLinterna.png',98,120)
                for i in range(0,7):
                        pantalla.blit(leo[i][0],(30,30))
                        pygame.display.flip()
                        reloj.tick(10) 

        
        
        
        
        
