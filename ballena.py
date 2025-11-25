import pygame
import random
import sys
import os
import time

pygame.init()
pygame.mixer.init()

# ======== FUNCION PARA ENCONTRAR ARCHIVOS ========
def get_file_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(os.path.dirname(script_dir))
    possible_paths = [
        os.path.join(workspace_root, filename),
        os.path.join(workspace_root, "delfin-version-frogge3r-main", filename),
        os.path.join(script_dir, filename),
        os.path.join(workspace_root, "delfin-version-frogger-main", filename),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

# ===========================
# CONFIGURACIÓN
# ===========================
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delfín Esquivador")
clock = pygame.time.Clock()

# COLORES
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
LIGHT_BLUE = (100, 200, 255)
GREEN = (0, 200, 100)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
BROWN = (160, 110, 50)
BLACK = (0, 0, 0)

# ===========================
# CARGA DE IMÁGENES
# ===========================
def load_img(name, size, color=RED):
    ruta = get_file_path(os.path.join("imagenes", name))

    if ruta and os.path.exists(ruta):
        try:
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            pass

    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

dolphin_img          = load_img("delfin-fotor.png",  (60, 40), LIGHT_BLUE)
dolphin_saved_img    = load_img("delfin-fotor.png",(60, 40), YELLOW)
barrel_img           = load_img("bote de basura acostado.png", (45, 45), RED)
log_img              = load_img("tronco.png", (80, 30), BROWN)
oil_img              = load_img("petroleo1.png", (70, 25), BLACK)
house_img            = load_img("Koral.png", (80, 60), GREEN)
house_done_img       = load_img("Koral en casa.png", (80, 60), YELLOW)
bg_img               = load_img("fondoDelfin.png", (WIDTH, HEIGHT), BLUE)

music_file = "Beetlejuice (NES) Music - Stage 01.mp3"
music_path = get_file_path(music_file)

if music_path:
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
        pygame.mixer.music.set_volume(0.7)  # Volumen al 70%
        print(f"Musica cargada correctamente desde: {music_path}")
    except Exception as e:
        print(f"Error al cargar la música: {e}")
else:
    print(f"No se pudo encontrar el archivo de música: {music_file}")

# ===========================
# BARRA DE VIDA
# ===========================
def draw_life_bar(lives, x, y):
    bar_width = 150
    bar_height = 30
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    life_width = (lives / 5) * bar_width

    if lives >= 4: color = GREEN
    elif lives >= 2: color = YELLOW
    else: color = RED

    pygame.draw.rect(screen, color, (x, y, life_width, bar_height))
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)

    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Vidas: {lives}/5", True, WHITE)
    screen.blit(text, (x + 5, y + 5))


# ===========================
# DELFÍN
# ===========================
class Dolphin:
    def __init__(self):
        self.image = dolphin_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-60))
        self.speed = 5
        self.lives = 5
        self.invincible = 0
        self.change_timer = 0   # <- tiempo para sprite especial

    def move(self, keys):
        if keys[pygame.K_LEFT]  and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed
        if keys[pygame.K_UP]    and self.rect.top > 0: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]  and self.rect.bottom < HEIGHT: self.rect.y += self.speed

    def hit(self):
        self.lives -= 1
        self.invincible = 90
        self.rect.center = (WIDTH//2, HEIGHT-60)

    def draw(self):
        if self.invincible % 10 < 5:
            screen.blit(self.image, self.rect)

    def update(self):
        if self.invincible > 0:
            self.invincible -= 1

        # Regresar sprite normal si termina el tiempo especial
        if self.change_timer > 0:
            self.change_timer -= 1
            if self.change_timer == 0:
                self.image = dolphin_img


# ===========================
# OBSTÁCULOS
# ===========================
class Obstacle:
    def __init__(self, type_name):
        self.type = type_name
        self.speed = random.choice([-3, -2, 2, 3])

        if type_name == "barrel": self.image = barrel_img
        if type_name == "log":    self.image = log_img
        if type_name == "oil":    self.image = oil_img

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(150, HEIGHT - 150)

    def move(self):
        self.rect.x += self.speed

        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = random.randint(150, HEIGHT - 150)

        elif self.rect.left > WIDTH:
            self.rect.right = 0
            self.rect.y = random.randint(150, HEIGHT - 150)

    def draw(self):
        screen.blit(self.image, self.rect)


# ===========================
# CASAS / CORALES
# ===========================
class House:
    def __init__(self, x):
        self.image = house_img
        self.done_image = house_done_img
        self.reached = False
        self.rect = self.image.get_rect(midtop=(x, 20))

    def draw(self):
        if self.reached:
            screen.blit(self.done_image, self.rect)
        else:
            screen.blit(self.image, self.rect)


# ===========================
# PAUSA
# ===========================
def pause_menu():
    while True:
        font = pygame.font.SysFont(None, 50)
        screen.fill((0, 0, 0))

        text = font.render("PAUSA (P para continuar)", True, WHITE)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                return


# ===========================
# JUEGO PRINCIPAL
# ===========================
def main():
    dolphin = Dolphin()

    obstacles = [Obstacle(random.choice(["barrel","log","oil"])) for _ in range(10)]

    houses = []
    spacing = WIDTH // 6
    for i in range(5):
        houses.append(House(spacing*(i+1)))

    score = 0
    reached = 0
    game_over = False
    win = False

    time_limit = 100
    start_time = time.time()

    # Burbujas
    bubbles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(3, 7)] for _ in range(20)]

    while True:
        keys = pygame.key.get_pressed()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p and not game_over:
                    pause_menu()
                if e.key == pygame.K_r:
                    main()
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        if not game_over and not win:

            elapsed = int(time.time() - start_time)
            remaining = time_limit - elapsed
            if remaining <= 0:
                game_over = True

            dolphin.move(keys)
            dolphin.update()

            # Colisiones con obstáculos
            for obs in obstacles:
                obs.move()
                if dolphin.invincible == 0 and dolphin.rect.colliderect(obs.rect):
                    dolphin.hit()
                    score -= 5
                    if score < 0: score = 0
                    if dolphin.lives <= 0:
                        game_over = True

            # Colisiones con casas/corales
            for h in houses:
                if not h.reached and dolphin.rect.colliderect(h.rect):
                    h.reached = True
                    reached += 1
                    score += 20

                    # Cambiar sprite del delfín
                    dolphin.image = dolphin_saved_img
                    dolphin.change_timer = 40  

                    # Reset posición
                    dolphin.rect.center = (WIDTH//2, HEIGHT-60)

                    if reached == 5:
                        win = True

        # ===========================
        # DIBUJAR
        # ===========================
        screen.blit(bg_img, (0, 0))

        # Burbujas
        for b in bubbles:
            pygame.draw.circle(screen, LIGHT_BLUE, (b[0], b[1]), b[2])
            b[1] -= 1
            if b[1] <= 0:
                b[1] = HEIGHT

        for obs in obstacles: obs.draw()
        for h in houses: h.draw()

        dolphin.draw()

        font = pygame.font.SysFont(None, 32)

        draw_life_bar(dolphin.lives, 10, 10)
        screen.blit(font.render(f"Puntaje: {score}", True, WHITE), (10, 50))
        screen.blit(font.render(f"Casas: {reached}/5", True, WHITE), (10, 80))

        if not game_over and not win:
            screen.blit(font.render(f"Tiempo: {remaining}", True, YELLOW), (10, 110))

        if game_over:
            screen.fill((0,0,0))
            screen.blit(font.render("GAME OVER (Tiempo agotado o sin vidas) - R para reiniciar", True, RED),
                        (WIDTH//2 - 350, HEIGHT//2))

        if win:
            screen.fill((0,0,0))
            screen.blit(font.render("¡GANASTE! - R para reiniciar", True, GREEN),
                        (WIDTH//2 - 150, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

main()
