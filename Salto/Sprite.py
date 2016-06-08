import pygame
import random
 
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
        self.cambio_x = -6
 
    def ir_derecha(self):
        self.cambio_x = 6
 
    def stop(self):
        self.cambio_x = 0

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
 
    def Mover_fondo(self, mov_x):
        self.mov_fondo += mov_x
        for plataforma in self.listade_plataformas:
            plataforma.rect.x += mov_x
        for enemigo in self.listade_enemigos:
            enemigo.rect.x += mov_x
        for imagenes in self.listade_imagenes:
            plataforma.rect.x += mov_x
        
# Creamos las plataformas para el nivel
class Nivel_01(Nivel):
 
    def __init__(self, Jugador):
        
        Nivel.__init__(self, Jugador)
        self.limite = -1000
         
        
        nivel = [[0,0],[0,20],[0,40],
                 [0,60],[0,80],[0,100],
                 [0,120],[0,140],[0,160],
                 [0,180],[0,200],[0,220],
                 [0,240],[0,260],[0,280],
                 [0,300],[0,320],[0,340],
                 [0,360],[0,380],[0,400],
                 [0,420],[0,440],[0,460],
                 [0,480],[0,500],[0,520],
                 [0,540],
                                
                ]
        ncamara =[[1400,0]
                  ]
        
        for camara in ncamara:
            bloque = Plataforma("Fondo/camara1.png")
            bloque.rect.x = camara[0]
            bloque.rect.y = camara[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)
        
        # Iteramos sobre el array anterior y anadimos plataformas
        for cuadro in nivel:
            bloque = Plataforma("Cuadrado.png")
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
        self.limite=-1000 
        # Array con la informacion sobre el largo, alto, x, e y
        nivel = [ [ 500, 500],
                  [ 600, 500]
                  ]
 
        # Iteramos sobre el array anterior y anadimos plataformas
        for plataforma in nivel:
            bloque = Plataforma("Cuadrado.png")
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)                      
 
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
 
def main():
    """ Programa Principal """
    pygame.init() 
        
    # Definimos el alto y largo de la pantalla 
    dimensiones = [LARGO_PANTALLA, ALTO_PANTALLA] 
    pantalla = pygame.display.set_mode(dimensiones) 
       
    pygame.display.set_caption("Saltador de Plataformas") 
     
    # Creamos al protagonista
    jugador = Jugador("Stickman/StickdePie.png")
    jugS = pygame.image.load('Stickman/StickS.png')
    
 
    # Creamos todos los niveles
    listade_niveles = []
    listade_niveles.append(Nivel_01(jugador))
    listade_niveles.append(Nivel_02(jugador))
     
    # Establecemos el nivel actual
    nivel_actual_no = 0
    nivel_actual = listade_niveles[nivel_actual_no]
     
    ls_todos = pygame.sprite.Group()
    jugador.nivel = nivel_actual
     
    jugador.rect.x = 340
    jugador.rect.y = ALTO_PANTALLA - jugador.rect.height
    ls_todos.add(jugador)
         
     
    Terminar = False
       
    reloj = pygame.time.Clock() 
       
    i = 0
    while not Terminar: 
        jug = cargar_fondo("Stickman/Stickman.png",98,120)
        
        for evento in pygame.event.get():  
            if evento.type == pygame.QUIT:
                Terminar = True 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador.ir_izquierda()
                if evento.key == pygame.K_RIGHT:
                    jugador.ir_derecha()        
                if evento.key == pygame.K_UP:
                    pantalla.blit(jugS,(jugador.rect.x,jugador.rect.y))
                    jugador.saltar()
                if evento.key == pygame.K_ESCAPE:
                    pass
                
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT and jugador.cambio_x < 0: 
                    jugador.stop()
                if evento.key == pygame.K_RIGHT and jugador.cambio_x > 0:
                    jugador.stop()
 
 
        ls_todos.update()
        nivel_actual.update()
       
        if jugador.rect.right > LARGO_PANTALLA:
            jugador.rect.right = LARGO_PANTALLA
     
        
        if jugador.rect.left < 0:
            jugador.rect.left = 0
        
        ls_todos.update()
    
        # Actualizamos elementos en el nivel
        nivel_actual.update()
        
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

        # Dibujamos y refrescamos
        pantalla.fill(Negro_Fondo)
        nivel_actual.draw(pantalla)
        ls_todos.draw(pantalla)     
        nivel_actual.draw(pantalla)
        ls_todos.draw(pantalla) 
        
        reloj.tick(30) 
        pygame.display.flip() 
           
    pygame.quit()
 
if __name__ == "__main__":
    main()