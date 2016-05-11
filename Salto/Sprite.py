import pygame

echo "# Platform-Game" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/juanvarco95/Platform-Game.git
git push -u origin master
 
#CONSTANTES 
ANCHO=800 
ALTO=600 
X0=ANCHO/2 
Y0=ALTO/2 
CX=(X0,Y0) 
Xmin=0 
Xmax=ANCHO 
Ymin=0 
Ymax=ALTO 
x = 0 
y = 0 
xb = 0 
yb = 0 
 
#COLORES 
Blanco=(255,255,255) 
Gris=(224,224,224) 
Rojo=(255,0,0) 
Azul=(0,0,255) 
Negro=(0,0,0) 
Verde=(0,255,0) 
Azul_Claro=(35,169,149)
 
# Dimensiones de la pantalla
LARGO_PANTALLA = 800
ALTO_PANTALLA = 600
 
class Jugador(pygame.sprite.Sprite): 
    cambio_x = 0
    cambio_y = 0
    def __init__(self):  
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([20, 20])
        self.image.fill(Rojo)        
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
                    
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, largo, alto ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([largo, alto])
        self.image.fill(Verde)             
        self.rect = self.image.get_rect()
  
class Muro(pygame.sprite.Sprite):    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,40])
        self.image.fill(Verde)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.paredes = pygame.sprite.Group()
class Nivel(object):
    """ Esta es una super clase generica usada para definir un nivel.
        Crea una clase hija especifica para cada nivel con una info especifica. """
         
    def __init__(self, Jugador):
        """ Constructor. Requerido para cuando las plataformas moviles colisionan con el protagonista. """
        self.listade_plataformas = pygame.sprite.Group()
        self.listade_enemigos = pygame.sprite.Group()
        self.Jugador = Jugador
         
        # Imagen de fondo
    imagende_fondo = None
     
    # Actualizamos todo en este nivel
    def update(self):
        self.listade_plataformas.update()
        self.listade_enemigos.update()
     
    def draw(self, pantalla):
        pantalla.fill(Blanco)
        self.listade_plataformas.draw(pantalla)
        self.listade_enemigos.draw(pantalla)
 
''     
# Creamos las plataformas para el nivel
class Nivel_01(Nivel):
    """ Definicion para el nivel 1. """
 
    def __init__(self, Jugador):
        """ Creamos el nivel 1. """
         
        # llamamos al constructor padre
        Nivel.__init__(self, Jugador)
         
        # Array con la informacion sobre el largo, alto, x, e y
        nivel = [ [70, 50, 500, 500],
                  [70, 50, 500, 500],
                  [70, 50, 500, 500],
                  [70, 50, 500, 500],
                  [70, 50, 500, 500],
                  [70, 50, 500, 500]
                  ]
 
        # Iteramos sobre el array anterior y anadimos plataformas
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)
            
class Nivel_02(Nivel):
    """ Definicion para el nivel 1. """
 
    def __init__(self, Jugador):
        """ Creamos el nivel 1. """
         
        # llamamos al constructor padre
        Nivel.__init__(self, Jugador)
         
        # Array con la informacion sobre el largo, alto, x, e y
        nivel = [ [70, 50, 500, 500],
                  [70, 50, 600, 500]
                  ]
 
        # Iteramos sobre el array anterior y anadimos plataformas
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.Jugador = self.Jugador
            self.listade_plataformas.add(bloque)                      
 
def main():
    """ Programa Principal """
    pygame.init() 
        
    # Definimos el alto y largo de la pantalla 
    dimensiones = [LARGO_PANTALLA, ALTO_PANTALLA] 
    pantalla = pygame.display.set_mode(dimensiones) 
       
    pygame.display.set_caption("Saltador de Plataformas") 
     
    # Creamos al protagonista
    jugador = Jugador()
 
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
       
    
    while not Terminar: 
        for evento in pygame.event.get():  
            if evento.type == pygame.QUIT:
                Terminar = True 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador.ir_izquierda()
                if evento.key == pygame.K_RIGHT:
                    jugador.ir_derecha()
                if evento.key == pygame.K_UP:
                    jugador.saltar()
                     
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
              
        nivel_actual.draw(pantalla)
        ls_todos.draw(pantalla) 
        reloj.tick(60) 
        pygame.display.flip() 
           
    pygame.quit()
 
if __name__ == "__main__":
    main()