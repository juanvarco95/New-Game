import pygame
import random
from pygame.locals import *

pygame.init()
 
#CONSTANTES 
ANCHO = 800 
ALTO = 600 
X0 = ANCHO/2 
Y0 = ALTO/2 
CX = (X0,Y0) 
Xmin = 0 
Xmax = ANCHO 
Ymin = 0 
Ymax = ALTO 
x = 0 
y = 0 
xb = 0 
yb = 0 
 
#COLORES 
Blanco = (255,255,255) 
Gris = (224,224,224) 
Rojo = (255,0,0) 
Azul = (0,0,255) 
Negro = (0,0,0) 
Verde = (0,255,0) 
Azul_Claro = (35,169,149)
Negro_Fondo = (48,53,77)
fondo = pygame.image.load('Kame_House1.png')
reloj = pygame.time.Clock()
fuente2 = pygame.font.Font('dejavu.ttf',50)
 
# Dimensiones de la pantalla
LARGO_PANTALLA = 800
ALTO_PANTALLA = 600
 
class Jugador(pygame.sprite.Sprite): 
    cambio_x = 0
    cambio_y = 0
    def __init__(self, image):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect() 
    def update(self): 
        self.calc_grav()
        self.rect.x += self.cambio_x
        ls_choque = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        for bloque in ls_choque:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                self.rect.left = bloque.rect.right
        self.rect.y += self.cambio_y
        ls_choque = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False) 
        for bloque in ls_choque:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top 
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom
            self.cambio_y = 0
 
    def calc_grav(self):
        if self.cambio_y == 0:
            self.cambio_y = 1
        else:
            self.cambio_y += .4 
        if self.rect.y >= ALTO_PANTALLA - self.rect.height and self.cambio_y >= 0:
            self.cambio_y = 0
            self.rect.y = ALTO_PANTALLA - self.rect.height
 
    def saltar(self):
        self.rect.y += 2
        lista_impactos_plataforma = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        self.rect.y -= 2

        if len(lista_impactos_plataforma) > 0 or self.rect.bottom >= ALTO_PANTALLA:
            self.cambio_y = -10
             
    
    def ir_izquierda(self):
        self.cambio_x = -10
 
    def ir_derecha(self):
        self.cambio_x = 10
 
    def stop(self):
        self.cambio_x = 0
        
class Bala(pygame.sprite.Sprite): 
    def __init__(self, image): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect()
        self.jugador = 1
 
    def update(self):
        if self.jugador == 1:
            self.rect.y -= 5
        else:
            self.rect.y -= 10

class Luz_Camara(pygame.sprite.Sprite): 
    def __init__(self, image): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect()
        self.disparar = random.randrange(100) 
        self.direccion = 0 
 
    def update(self): 
        if self.rect.y >= (ALTO - 20): 
            self.direccion = 1 
        if self.rect.y <= 10: 
            self.direccion = 0 
 
        if self.direccion == 0: 
            self.rect.y += 5 
        else: 
            self.rect.y -= 5
        self.disparar -= 1
        if self.disparar < 0:
            self.disparar = random.randrange(100)
                    
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect()
  
class Fondo(pygame.sprite.Sprite):    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect()
   
        #self.paredes = pygame.sprite.Group()
        
class Nivel(object):     
    def __init__(self, Jugador):
        """ Constructor. Requerido para cuando las plataformas moviles colisionan con el protagonista. """
        self.listade_plataformas = pygame.sprite.Group()
        self.listade_enemigos = pygame.sprite.Group()
        self.Jugador = Jugador
        self.listade_imagenes = pygame.sprite.Group()
        self.list_bonus = pygame.sprite.Group()
        
    
    
    mov_fondo = 0 
    # Actualizamos todo en este nivel
    def update(self):
        self.listade_plataformas.update()
        self.listade_enemigos.update()
        self.listade_imagenes.update()
     
    def draw(self, pantalla):
        pantalla.fill(Negro_Fondo)
        self.listade_plataformas.draw(pantalla)
        self.listade_enemigos.draw(pantalla)
        self.listade_imagenes.draw(pantalla)
        self.list_bonus.draw(pantalla)
 
    def Mover_fondo(self, mov_x):
        self.mov_fondo += mov_x
        for plataforma in self.listade_plataformas:
            plataforma.rect.x += mov_x
        for enemigo in self.listade_enemigos:
            enemigo.rect.x += mov_x
        for imagenes in self.listade_imagenes:
            imagenes.rect.x += mov_x
        for bonus in self.list_bonus:
            bonus.rect.x += mov_x    
        
# Creamos las plataformas para el nivel
class Nivel_01(Nivel):
 
    def __init__(self, Jugador):
        
        Nivel.__init__(self, Jugador)
        self.limite = -2000
         
        
        columnas = [[0,0],
                    [1000,-200],
                    [2000,-200],
                    [2500,-300],
                ]
        
        cajones = [[400,470]]
        
        rcamara =[[20,0],
                  [1360,0]
                  ]
        lcamara =[[930,0],
                  [1300,0],
                  ]
        
        rLuz =[[80,25],
               [1420,25]
                  ]
        
        lLuz =[[550,25],
               [915,25]
                  ]
        Luz =[[2115,-500],
               
                  ]
        
        nivel = [ [ 1025, 100],
                  [ 1150, 500],
                  [ 1250, 370],
                  [ 1250, 170],
                  [ 1025, 300],
                  [ 1900, 400],
                  [ 1700, 500],
                  [ 2300, 500],
                  [ 2100, 400],
                  [ 2025, 300]
                  ]
        
        bonus = [[440,410],
                 [460,410],
                 [480,410],
                 [1025,40],
                 [1900,340],
                 [1920,340],
                 [2025, 240]
                 ]
        
        bombillo = [[2190,-80]]
        for plataforma in bombillo:
            bloque = Plataforma("Stickman/Bombillo.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)                      

        
        # Iteramos sobre el array anterior y anadimos plataformas
        for plataforma in nivel:
            bloque = Plataforma("Cuadrado.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)                      
        
        for plataforma in bonus:
            bloque = Plataforma("Fondo/dinero.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.list_bonus.add(bloque)                      
 
        
        for camara in rcamara:
            bloque = Plataforma("Fondo/camara.png")
            bloque.rect.x = camara[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)
            
        for luz in Luz:
            bloque = Plataforma("Fondo/LuzBomibillo.png")
            bloque.rect.x = luz[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)
            
        for camara in lcamara:
            bloque = Plataforma("Fondo/camara1.png")
            bloque.rect.x = camara[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)
            
        for luz in rLuz:
            bloque = Plataforma("Fondo/LuzCamara.png")
            bloque.rect.x = luz[0]
            bloque.rect.y = luz[1]
            self.listade_enemigos.add(bloque)
            
        for luz in lLuz:
            bloque = Plataforma("Fondo/LuzCamara1.png")
            bloque.rect.x = luz[0]
            bloque.rect.y = luz[1]
            self.listade_enemigos.add(bloque)
        
        # Iteramos sobre el array anterior y anadimos plataformas
        for cuadro in columnas:
            bloque = Plataforma("Fondo/columna.png")
            bloque.rect.x = cuadro[0]
            bloque.rect.y = cuadro[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)
            
        for cuadro in cajones:
            bloque = Plataforma("Fondo/Cajon.png")
            bloque.rect.x = cuadro[0]
            bloque.rect.y = cuadro[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)
            
            
            
class Nivel_02(Nivel):
    """ Definicion para el nivel 1. """
 
    def __init__(self, Jugador):
        """ Creamos el nivel 1. """
         
        # llamamos al constructor padre
        Nivel.__init__(self, Jugador)
        self.limite=-2000 
        # Array con la informacion sobre el largo, alto, x, e y
        columnas = [[0,0],
                    [1000,-200],
                    [2000,-200],
                    [2500,-300],
                ]
        
        cajones = [[400,470],
                   [1500,470]]
        
        rcamara =[[20,0],
                  [1360,0],
                  [1500,0],
                  ]
        lcamara =[[930,0],
                  [1300,0],
                  
                  ]
        
        rLuz =[[80,25],
               [1420,25],
               [1580,25]
                  ]
        
        lLuz =[[550,25],
               [900,25]
                  ]
        Luz =[[2115,-300],
              [350,0]
               
                  ]
        
        nivel = [ [ 1025, 100],
                  [ 1025, 300],
                  [ 1250, 370],
                  [ 1250, 170],
                  [ 1025, 300],
                  [ 1900, 400],
                  [ 1700, 500],
                  [ 2300, 500],
                  [ 2100, 400],
                  [ 2025, 300]
                  ]
        
        bonus = [[420,410],
                 [440,410],
                 [460,410],
                 [480,410],
                 [500,410],
                 [1025,40],
                 [1900,340],
                 [1920,340],
                 [2025, 240]
                 ]
        bombillo = [[450,-80],
                    [2190,-80]]
        for plataforma in bombillo:
            bloque = Plataforma("Stickman/Bombillo.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)                      

        # Iteramos sobre el array anterior y anadimos plataformas
        for plataforma in nivel:
            bloque = Plataforma("Cuadrado1.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)                      
        
        for plataforma in bonus:
            bloque = Plataforma("Fondo/dinero.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.list_bonus.add(bloque)                      
 
        
        for camara in rcamara:
            bloque = Plataforma("Fondo/camara.png")
            bloque.rect.x = camara[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)
            
        for luz in Luz:
            bloque = Plataforma("Fondo/LuzBomibillo.png")
            bloque.rect.x = luz[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)
            
        for camara in lcamara:
            bloque = Plataforma("Fondo/camara1.png")
            bloque.rect.x = camara[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_enemigos.add(bloque)
            
        for luz in rLuz:
            bloque = Plataforma("Fondo/LuzCamara.png")
            bloque.rect.x = luz[0]
            bloque.rect.y = luz[1]
            self.listade_enemigos.add(bloque)
            
        for luz in lLuz:
            bloque = Plataforma("Fondo/LuzCamara1.png")
            bloque.rect.x = luz[0]
            bloque.rect.y = luz[1]
            self.listade_enemigos.add(bloque)
        
        # Iteramos sobre el array anterior y anadimos plataformas
        for cuadro in columnas:
            bloque = Plataforma("Fondo/Pared.png")
            bloque.rect.x = cuadro[0]
            bloque.rect.y = cuadro[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)
            
        for cuadro in cajones:
            bloque = Plataforma("Fondo/Cajon2.png")
            bloque.rect.x = cuadro[0]
            bloque.rect.y = cuadro[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque) 
            
        cajaFuerte = Plataforma("Stickman/CajaFuerte.png")
        cajaFuerte.rect.x = 2700
        cajaFuerte.rect.y = 400              
        self.list_bonus.add(cajaFuerte)       
        
def cargar_jugador(archivo, ancho, alto):
        imagen = pygame.image.load(archivo).convert_alpha()
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

class Menu:
    def __init__(self, opciones):
        self.opciones = []
        fuente = pygame.font.Font('dejavu.ttf', 20)
        x = 105
        y = 105
        paridad = 1

        self.cursor = Cursor(x - 30, y, 30)

        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
        #sonido.play()
            elif k[K_DOWN]:
                self.seleccionado += 1
        #sonido.play()
            elif k[K_RETURN]:
                # Invoca a la funcion asociada a la opcion.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor este entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()
     
        for o in self.opciones:
            o.actualizar()

    def imprimir(self, screen):
        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)

class Cursor:

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('kamehameha.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x - 20
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

class Opcion:

    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, (0, 0, 0))
        self.imagen_destacada = fuente.render(titulo, 1, (200, 0, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def actualizar(self):
        destino_x = 105
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()

def salir_del_programa():
    print " Gracias por utilizar este programa."
    sys.exit(0)
 
def main():
    """ Programa Principal """
    pygame.init() 
        
    # Definimos el alto y largo de la pantalla 
    dimensiones = [LARGO_PANTALLA, ALTO_PANTALLA] 
    pantalla = pygame.display.set_mode(dimensiones) 
       
    pygame.display.set_caption("The good theif") 
     
    # Creamos al protagonista
    jugador = Jugador("Stickman/StickdePieNoche.png")
    jugadorRight = cargar_jugador("Stickman/StickmanNoche.png",98,100)
    jugadorLeft = cargar_jugador("Stickman/StickmanNocheIzq.png",98,100)
    ls_balas = pygame.sprite.Group()
    
    # Creamos todos los niveles
    listade_niveles = []
    listade_niveles.append(Nivel_01(jugador))
    listade_niveles.append(Nivel_02(jugador))
     
    # Establecemos el nivel actual
    nivel_actual_no = 0
    nivel_actual = listade_niveles[nivel_actual_no]
     
    ls_todos = pygame.sprite.Group()
    ls_jugador = pygame.sprite.Group()

    ls_jugador.add(jugador)
    
    jugador.nivel = nivel_actual
     
    jugador.rect.x = 340
    jugador.rect.y = ALTO_PANTALLA - jugador.rect.height
    ls_todos.add(jugador)
    
    
         
     
    Terminar = False
       
    reloj = pygame.time.Clock() 
    pos = 0  
    posj = [jugador.rect.x,jugador.rect.y]
    pygame.key.set_repeat(1,25)
    puntos = 10
    while not Terminar: 
        for evento in pygame.event.get():
            keys = pygame.key.get_pressed()  
            if evento.type == pygame.QUIT:
                Terminar = True 
            if evento.type == pygame.KEYDOWN:
                if keys[K_LEFT]:
                    jugador.ir_izquierda()
                    #ls_jugador.remove(jugador)
                    pantalla.blit(jugadorLeft[pos][0],(jugador.rect.x-30,jugador.rect.y-33))
                    pos += 1
                    if pos == 7:
                        pos = 0
                    pygame.display.flip()
                    reloj.tick(30)
                    
                
                if keys[K_RIGHT]:
                    jugador.ir_derecha()
                    pantalla.blit(jugadorRight[pos][0],(jugador.rect.x-30,jugador.rect.y-33))
                    pos += 1
                    if pos == 7:
                        pos = 0
                    pygame.display.flip()
                    reloj.tick(30)
                if evento.key == pygame.K_UP:
                    jugador.saltar()
                if evento.key == pygame.K_SPACE:
                    bala = Bala('Fondo/piedra.png') 
                    bala.rect.x = jugador.rect.x + 20
                    bala.rect.y = jugador.rect.y + 50
                    ls_balas.add(bala) 
                    ls_todos.add(bala)
                    puntos -= 1
                    print puntos
                    if(puntos == 0):
                        ls_balas.remove(bala)
                        ls_todos.remove(bala)

                for a in ls_jugador:
                    ls_bonus = pygame.sprite.spritecollide(a,listade_niveles[0].list_bonus,True)
                    for c in ls_bonus:
                        listade_niveles[0].list_bonus.remove(c)
                        
                for a in ls_jugador:
                    ls_bonus = pygame.sprite.spritecollide(a,listade_niveles[0].listade_enemigos,True)
                    for c in ls_bonus:
                        print "Perdio Marica"        
                    
                for b in ls_balas:
                    ls_impacto = pygame.sprite.spritecollide(b,listade_niveles[0].listade_enemigos,True)
                    for impacto in ls_impacto:
                        ls_balas.remove(b)
                        ls_todos.remove(b)

                for a in ls_jugador:
                    ls_bonus = pygame.sprite.spritecollide(a,listade_niveles[1].list_bonus,True)
                    for c in ls_bonus:
                        listade_niveles[0].list_bonus.remove(c)
                        
                for a in ls_jugador:
                    ls_bonus = pygame.sprite.spritecollide(a,listade_niveles[1].listade_enemigos,True)
                    for c in ls_bonus:
                        print "Perdio Marica"        
                    
                for b in ls_balas:
                    ls_impacto = pygame.sprite.spritecollide(b,listade_niveles[0].listade_enemigos,True)
                    for impacto in ls_impacto:
                        ls_balas.remove(b)
                        ls_todos.remove(b)
                
                for b in ls_balas:
                    ls_impacto = pygame.sprite.spritecollide(b,listade_niveles[1].listade_enemigos,True)
                    for impacto in ls_impacto:
                        ls_balas.remove(b)
                        ls_todos.remove(b)
                                   
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT and jugador.cambio_x < 0: 
                    jugador.stop()
                if evento.key == pygame.K_RIGHT and jugador.cambio_x > 0:
                    jugador.stop()

 
        ls_todos.update()
        ls_balas.update()
        #ls_enemigos.update()
        #nivel_actual.update()
       
     #  Si el jugador se aproxima al limite derecho de la pantalla (-x)
        if jugador.rect.x >= 500:
            dif = jugador.rect.x - 500
            jugador.rect.x = 500
            nivel_actual.Mover_fondo(-dif)

        # Si el jugador se aproxima al limite izquierdo de la pantalla (+x)
        if jugador.rect.x <= 120:
           dif = 120 - jugador.rect.x
           jugador.rect.x = 120
           nivel_actual.Mover_fondo(dif)
           
        #Si llegamos al final del nivel
        pos_actual=jugador.rect.x + nivel_actual.mov_fondo
        if pos_actual < nivel_actual.limite:
           jugador.rect.x=120
           if nivel_actual_no < len(listade_niveles)-1:
              nivel_actual_no += 1
              nivel_actual = listade_niveles[nivel_actual_no]
              jugador.nivel=nivel_actual

              
        nivel_actual.draw(pantalla)
        ls_todos.draw(pantalla) 
        reloj.tick(60) 
        pygame.display.flip() 
           
    pygame.quit()
 
if __name__ == "__main__":

    salir = False
    opciones = [
                ("Jugar", main),
                #("Creditos",creditos),
                ("Salir", salir_del_programa)
               ]

    pygame.font.init()
    pantalla=pygame.display.set_mode([ANCHO,ALTO])
    pygame.display.set_caption("STICKMAN")
    menu = Menu(opciones)

    while not salir:

        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        pantalla.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(pantalla)

        pygame.display.flip()
        reloj.tick(60)
