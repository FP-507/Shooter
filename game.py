import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Shooter Pygame")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Crear la imagen del jugador (un rectángulo simple)
        self.image = pygame.Surface([50, 50])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        # Posición inicial (centro en la parte inferior)
        self.rect.x = ANCHO // 2
        self.rect.y = ALTO - 70
        # Velocidad del jugador
        self.velocidad = 5
        # Salud del jugador
        self.salud = 100
        
    def update(self):
        # Obtener las teclas presionadas
        teclas = pygame.key.get_pressed()
        
        # Movimiento izquierda/derecha
        if teclas[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.x < ANCHO - 50:
            self.rect.x += self.velocidad
            
        # Movimiento arriba/abajo
        if teclas[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.y < ALTO - 50:
            self.rect.y += self.velocidad
    
    def disparar(self):
        # Crear una bala en la posición actual del jugador
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_sprites.add(bala)
        balas.add(bala)

# Clase para las balas del jugador
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Crear la imagen de la bala (un rectángulo pequeño)
        self.image = pygame.Surface([5, 10])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        # Posición inicial (centrada en x, arriba del jugador)
        self.rect.centerx = x
        self.rect.bottom = y
        # Velocidad de la bala (hacia arriba)
        self.velocidad = -10
        
    def update(self):
        # Mover la bala
        self.rect.y += self.velocidad
        
        # Eliminar la bala si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

# Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Crear la imagen del enemigo (un rectángulo simple)
        self.image = pygame.Surface([30, 30])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        # Posición inicial (aleatoria en la parte superior)
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        # Velocidad del enemigo (aleatoria)
        self.velocidad_y = random.randrange(1, 4)
        self.velocidad_x = random.randrange(-2, 2)
        
    def update(self):
        # Mover el enemigo
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        
        # Rebotar en los bordes de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.velocidad_x *= -1
            
        # Si el enemigo sale por abajo, reaparece arriba
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(1, 4)

# Clase para las explosiones
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        # Crear animación de explosión (simplificada)
        self.image = pygame.Surface([30, 30])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.tiempo_vida = 10  # Fotogramas que dura la explosión
        
    def update(self):
        # Reducir el tiempo de vida
        self.tiempo_vida -= 1
        if self.tiempo_vida <= 0:
            self.kill()

# Crear grupos de sprites
todas_las_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()

# Crear jugador
jugador = Jugador()
todas_las_sprites.add(jugador)

# Crear enemigos iniciales
for i in range(8):
    enemigo = Enemigo()
    todas_las_sprites.add(enemigo)
    enemigos.add(enemigo)

# Puntuación
puntuacion = 0
fuente = pygame.font.SysFont('Arial', 30)

# Bucle principal del juego
ejecutando = True
game_over = False

while ejecutando:
    # Mantener el bucle funcionando a la velocidad correcta
    reloj.tick(60)
    
    # Procesar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not game_over:
                jugador.disparar()
            if evento.key == pygame.K_r and game_over:
                # Reiniciar el juego
                game_over = False
                jugador.salud = 100
                puntuacion = 0
                # Limpiar todos los sprites
                for sprite in todas_las_sprites:
                    sprite.kill()
                # Crear nuevos sprites
                jugador = Jugador()
                todas_las_sprites.add(jugador)
                for i in range(8):
                    enemigo = Enemigo()
                    todas_las_sprites.add(enemigo)
                    enemigos.add(enemigo)
    
    if not game_over:
        # Actualizar
        todas_las_sprites.update()
        
        # Colisiones entre balas y enemigos
        hits = pygame.sprite.groupcollide(enemigos, balas, True, True)
        for hit in hits:
            # Aumentar puntuación
            puntuacion += 10
            # Crear explosión
            explosion = Explosion(hit.rect.center)
            todas_las_sprites.add(explosion)
            # Crear nuevo enemigo
            enemigo = Enemigo()
            todas_las_sprites.add(enemigo)
            enemigos.add(enemigo)
        
        # Colisiones entre jugador y enemigos
        hits = pygame.sprite.spritecollide(jugador, enemigos, True)
        for hit in hits:
            jugador.salud -= 20
            enemigo = Enemigo()
            todas_las_sprites.add(enemigo)
            enemigos.add(enemigo)
            if jugador.salud <= 0:
                game_over = True
    
    # Dibujar / renderizar
    pantalla.fill(NEGRO)
    todas_las_sprites.draw(pantalla)
    
    # Mostrar puntuación
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))
    
    # Mostrar salud
    texto_salud = fuente.render(f"Salud: {jugador.salud}", True, BLANCO)
    pantalla.blit(texto_salud, (10, 50))
    
    # Mostrar mensaje de game over
    if game_over:
        texto_game_over = fuente.render("GAME OVER - Presiona R para reiniciar", True, ROJO)
        pantalla.blit(texto_game_over, (ANCHO//2 - 200, ALTO//2))
    
    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()