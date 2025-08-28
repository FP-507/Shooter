import pygame
import random
import math
import time

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
        self.disparo_doble = False
        
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
        if self.disparo_doble:
            bala2 = Bala(self.rect.centerx - 15, self.rect.top)
            todas_las_sprites.add(bala2)
            balas.add(bala2)
            bala3 = Bala(self.rect.centerx + 15, self.rect.top)
            todas_las_sprites.add(bala3)
            balas.add(bala3)

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
        tamaño = random.randint(20, 60)
        self.image = pygame.Surface([tamaño, tamaño])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 4)
        self.velocidad_x = random.randrange(-2, 2)
        # Vida: 1 para el mínimo tamaño, hasta 3 para el máximo
        self.vida = 1 + ((tamaño - 20) * 2) // 40  # 20-60 → 1-3

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

# Clase para los potenciadores
class Potenciador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tipo = random.choice(['velocidad', 'doble'])
        self.image = pygame.Surface([30, 30])
        if self.tipo == 'velocidad':
            self.image.fill(AZUL)
        else:
            self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = 3

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.kill()

# Crear grupos de sprites
todas_las_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
potenciadores = pygame.sprite.Group()

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
potenciador_activo = None
potenciador_tiempo = 0

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
    
    # Aparición aleatoria de potenciadores
    if not game_over and random.random() < 0.005:
        potenciador = Potenciador()
        todas_las_sprites.add(potenciador)
        potenciadores.add(potenciador)

    if not game_over:
        # Actualizar
        todas_las_sprites.update()
        
        # Colisión con potenciadores
        hits = pygame.sprite.spritecollide(jugador, potenciadores, True)
        for hit in hits:
            potenciador_activo = hit.tipo
            potenciador_tiempo = pygame.time.get_ticks()

            if potenciador_activo == 'velocidad':
                jugador.velocidad = 10
            elif potenciador_activo == 'doble':
                jugador.disparo_doble = True

        # Desactivar potenciador tras 5 segundos
        if potenciador_activo:
            if pygame.time.get_ticks() - potenciador_tiempo > 5000:
                potenciador_activo = None
                jugador.velocidad = 5
                jugador.disparo_doble = False

        # Colisiones entre balas y enemigos
        hits = pygame.sprite.groupcollide(enemigos, balas, False, True)
        for enemigo, balas_impacto in hits.items():
            enemigo.vida -= len(balas_impacto)
            if enemigo.vida <= 0:
                puntuacion += 10
                explosion = Explosion(enemigo.rect.center)
                todas_las_sprites.add(explosion)
                enemigo.kill()
                # Crear nuevo enemigo
                nuevo_enemigo = Enemigo()
                todas_las_sprites.add(nuevo_enemigo)
                enemigos.add(nuevo_enemigo)

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