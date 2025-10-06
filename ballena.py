import sys, random, math, pygame
import os

# =========================
# Configuración general
# =========================
pygame.init()
pygame.display.set_caption("DEFIN — Pygame")

# Inicializar el mezclador de sonido
pygame.mixer.init()

TILE = 48
COLS = 13
LANE_LAYOUT = [
    'HOMES',
    'RIVER','RIVER','RIVER','RIVER','RIVER',
    'SAFE',
    'ROAD','ROAD','ROAD','ROAD','ROAD',
    'SAFE',
]
ROWS = len(LANE_LAYOUT)

WIDTH  = COLS * TILE
HEIGHT = ROWS * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

# =========================
# Manejo de rutas de archivos
# =========================
def get_file_path(filename):
    """Busca el archivo en diferentes ubicaciones posibles"""
    # Posibles ubicaciones donde podrían estar los archivos
    possible_paths = [
        filename,  # En el directorio actual
        os.path.join("delfin-version-frogge3r-main", filename),
        os.path.join("delfin-version-frogger-main", filename),
        os.path.join("..", filename),
        os.path.join(".", filename)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

# Cargar y reproducir música de fondo
music_file = "MusicaBackgruand.mp3"
music_path = get_file_path(music_file)

if music_path:
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
        pygame.mixer.music.set_volume(0.7)  # Volumen al 70%
        print(f"Música cargada correctamente desde: {music_path}")
    except Exception as e:
        print(f"Error al cargar la música: {e}")
else:
    print(f"No se pudo encontrar el archivo de música: {music_file}")

# También cargar sonido de victoria si existe
win_sound = None
win_sound_path = get_file_path("win.mp3")
if win_sound_path:
    try:
        win_sound = pygame.mixer.Sound(win_sound_path)
        print(f"Sonido de victoria cargado desde: {win_sound_path}")
    except Exception as e:
        print(f"Error al cargar el sonido de victoria: {e}")
else:
    print("No se pudo encontrar el archivo win.mp3")

# Colores (para fondos y HUD)
BG_DARK    = (18, 22, 28)
SAFE_GRASS = (236, 226, 198)
ROAD_GRAY  = (30, 90, 140)
WATER_BLUE = (30, 90, 140)
HOME_GREEN = (236, 226, 198)
WHITE      = (235, 235, 235)
RED        = (220, 50, 50)

FONT  = pygame.font.SysFont("arial", 20)
FONT2 = pygame.font.SysFont("arial", 36, bold=True)

# Puntuación
POINT_PER_NEW_ROW = 10
POINT_PER_HOME    = 200

# Temporizador
TIME_PER_ATTEMPT = 60.0

# Ranuras de Hogar
HOME_COLS = [1, 4, 6, 8, 11]

# =========================
# Cargar imágenes (con manejo de errores)
# =========================
def load_image(path, alpha=True):
    # Primero verificar si la ruta existe
    if not os.path.exists(path):
        # Intentar encontrar el archivo en ubicaciones alternativas
        filename = os.path.basename(path)
        alt_path = get_file_path(filename)
        if alt_path:
            path = alt_path
        else:
            print(f"Archivo de imagen no encontrado: {path}")
    
    try:
        if alpha:
            return pygame.image.load(path).convert_alpha()
        else:
            return pygame.image.load(path).convert()
    except Exception as e:
        print(f"Error cargando imagen {path}: {e}")
        # Crear una imagen de placeholder si hay error
        surf = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        if alpha:
            surf.fill((255, 0, 255, 128))  # Magenta transparente para imágenes alpha
        else:
            surf.fill((255, 0, 255))  # Magenta para imágenes normales
        return surf

# Cargar todas las imágenes
frog_img = load_image("delfin-version-frogge3r-main/imagenes/Delfin2o.png")
car_img = load_image("delfin-version-frogge3r-main/imagenes/BARCO.png")
contenedor_img = load_image("delfin-version-frogge3r-main/imagenes/CONTENEDOR.png")
log_img = load_image("delfin-version-frogge3r-main/imagenes/TRONCO.png")
turtle_img = load_image("delfin-version-frogge3r-main/imagenes/CONTENEDOR.png")
home_frog_img = load_image("delfin-version-frogge3r-main/imagenes/MAR.png")
background_img = load_image("delfin-version-frogge3r-main/imagenes/oceano.png", alpha=False)

# Redimensionar background si es necesario
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Utilidades
def grid_to_px(col, row):
    return col * TILE, row * TILE

def lane_type(row):
    return LANE_LAYOUT[row]

def in_bounds_rect(r):
    return 0 <= r.left and r.right <= WIDTH and 0 <= r.top and r.bottom <= HEIGHT

# =========================
# Entidades en movimiento
# =========================
class MovingEntity:
    def __init__(self, rect, vx, img):
        self.rect = rect
        self.vx   = vx
        self.img  = img
        self.alive = True

    def update(self, dt):
        self.rect.x += self.vx * dt
        if self.rect.right < -2*TILE or self.rect.left > WIDTH + 2*TILE:
            self.alive = False

    def draw(self, surf):
        img_scaled = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
        surf.blit(img_scaled, self.rect.topleft)

class Vehicle(MovingEntity):
    pass

class Log(MovingEntity):
    pass

class Turtle(MovingEntity):
    def __init__(self, rect, vx, img=turtle_img):
        super().__init__(rect, vx, img)
        self.period_total   = 6.0
        self.blink_duration = 0.8
        self.submerge_time  = 1.4
        self.phase = random.uniform(0, self.period_total)
        self.t = 0.0

    def update(self, dt):
        super().update(dt)
        self.t = (self.t + dt) % self.period_total

    @property
    def is_submerged(self):
        return self.t >= (self.period_total - self.submerge_time)

    def draw(self, surf):
        if self.is_submerged:
            return
        img_scaled = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
        surf.blit(img_scaled, self.rect.topleft)

# =========================
# Spawner
# =========================
class Spawner:
    def __init__(self, row, entity_kind, direction, speed_range, size_range_tiles, gap_range, level_scale=1.0):
        self.row = row
        self.entity_kind = entity_kind
        self.direction = direction
        self.speed_range = speed_range
        self.size_range_tiles = size_range_tiles
        self.gap_range = gap_range
        self.level_scale = level_scale
        self.timer = random.uniform(*self.gap_range)

    def spawn_one(self):
        y = self.row * TILE
        h = int(TILE * 0.9)
        w_tiles = random.randint(*self.size_range_tiles)
        w = int(w_tiles * TILE)
        if self.direction > 0:
            x = -w - TILE
        else:
            x = WIDTH + TILE
        vx = random.uniform(*self.speed_range) * self.direction * self.level_scale
        rect = pygame.Rect(x, y + (TILE - h)//2, w, h)

        if self.entity_kind == 'VEHICLE':
            img = car_img
            return Vehicle(rect, vx, img)
        elif self.entity_kind == 'LOG':
            return Log(rect, vx, log_img)
        else:
            return Turtle(rect, vx, turtle_img)

    def update(self, dt, container_list):
        self.timer -= dt
        if self.timer <= 0:
            container_list.append(self.spawn_one())
            self.timer = random.uniform(*self.gap_range)

# =========================
# delfin/frog
# =========================
class Frog:
    def __init__(self, spawn_col, spawn_row):
        self.w = int(TILE * 0.9)
        self.h = int(TILE * 0.9)
        self.spawn_col = spawn_col
        self.spawn_row = spawn_row
        self.input_cooldown = 0.0
        self.cooldown_time = 0.12
        self.reset()

    def reset(self):
        x, y = grid_to_px(self.spawn_col, self.spawn_row)
        self.rect = pygame.Rect(x+(TILE-self.w)//2, y+(TILE-self.h)//2, self.w, self.h)
        self.on_platform = None
        self.furthest_row = self.spawn_row
        self.alive = True

    def row(self):
        return max(0, min(ROWS-1, self.rect.centery // TILE))

    def move(self, dx_tiles, dy_tiles):
        self.rect.x += dx_tiles * TILE
        self.rect.y += dy_tiles * TILE

    def update(self, dt):
        if self.input_cooldown > 0:
            self.input_cooldown -= dt

    def draw(self, surf):
        img_scaled = pygame.transform.scale(frog_img, (self.rect.w, self.rect.h))
        surf.blit(img_scaled, self.rect.topleft)

# =========================
# Juego
# =========================
class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 5
        self.home_occupied = [False]*5
        self.state = 'PLAYING'
        self.time_left = TIME_PER_ATTEMPT
        spawn_row = max(i for i,t in enumerate(LANE_LAYOUT) if t == 'SAFE')
        spawn_col = COLS // 2
        self.frog = Frog(spawn_col, spawn_row)
        self.vehicles = []
        self.platforms = []
        self.spawners = []
        self.build_spawners()
        self.home_rects = []
        for idx, c in enumerate(HOME_COLS):
            x, y = grid_to_px(c, 0)
            self.home_rects.append(pygame.Rect(x+4, y+4, TILE-8, TILE-8))

    def build_spawners(self):
        self.vehicles.clear()
        self.platforms.clear()
        self.spawners.clear()
        level_scale = 1.0 + (self.level-1)*0.12
        for r, kind in enumerate(LANE_LAYOUT):
            if kind == 'ROAD':
                direction = -1 if (r % 2 == 0) else 1
                speed_range = (50, 120)
                size_tiles  = (2, 3)
                gap_range   = (5, 2.2)
                self.spawners.append(Spawner(r, 'VEHICLE', direction, speed_range, size_tiles, gap_range, level_scale))
            elif kind == 'RIVER':
                direction = 1 if (r % 2 == 0) else -1
                speed_range = (80, 150)
                gap_range   = (1.3, 2.5)
                if r % 3 == 0:
                    size_tiles = (1, 2)
                    self.spawners.append(Spawner(r, 'TURTLE', direction, speed_range, size_tiles, gap_range, level_scale))
                else:
                    size_tiles = (2, 3)
                    self.spawners.append(Spawner(r, 'LOG', direction, speed_range, size_tiles, gap_range, level_scale))

    def reset_attempt(self, lose_life=True):
        if lose_life:
            self.lives -= 1
            if self.lives <= 0:
                self.state = 'GAMEOVER'
                # Detener la música cuando el juego termina
                pygame.mixer.music.stop()
                return
        self.time_left = TIME_PER_ATTEMPT
        self.frog.reset()

    def all_homes_filled(self):
        return all(self.home_occupied)

    def next_level(self):
        self.level += 1
        self.home_occupied = [False]*5
        self.build_spawners()
        self.reset_attempt(lose_life=False)
        self.state = 'PLAYING'
        # Reproducir sonido de victoria si está disponible
        if win_sound:
            win_sound.play()

    def handle_input(self, key):
        if self.state != 'PLAYING':
            return
        if self.frog.input_cooldown > 0:
            return
        dx = dy = 0
        if key == pygame.K_UP: dy = -1
        elif key == pygame.K_DOWN: dy = 1
        elif key == pygame.K_LEFT: dx = -1
        elif key == pygame.K_RIGHT: dx = 1
        else: return
        prev_row = self.frog.row()
        self.frog.move(dx, dy)
        if not in_bounds_rect(self.frog.rect):
            self.reset_attempt(lose_life=True)
            return
        new_row = self.frog.row()
        if new_row < self.frog.furthest_row:
            self.score += POINT_PER_NEW_ROW
            self.frog.furthest_row = new_row
        self.frog.input_cooldown = self.frog.cooldown_time

    def update(self, dt):
        if self.state != 'PLAYING':
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.reset_attempt(lose_life=True)
            return
        for sp in self.spawners:
            if LANE_LAYOUT[sp.row] == 'ROAD':
                sp.update(dt, self.vehicles)
            elif LANE_LAYOUT[sp.row] == 'RIVER':
                sp.update(dt, self.platforms)
        for v in self.vehicles: v.update(dt)
        for p in self.platforms: p.update(dt)
        self.vehicles = [v for v in self.vehicles if v.alive]
        self.platforms= [p for p in self.platforms if p.alive]
        self.frog.update(dt)
        r = self.frog.row()
        kind = lane_type(r)
        if r == 0:
            on_empty_home = False
            for i, rect in enumerate(self.home_rects):
                if self.frog.rect.colliderect(rect):
                    if not self.home_occupied[i]:
                        self.home_occupied[i] = True
                        self.score += POINT_PER_HOME
                        self.reset_attempt(lose_life=False)
                        if self.all_homes_filled():
                            self.state = 'LEVEL_CLEARED'
                    else:
                        self.reset_attempt(lose_life=True)
                    on_empty_home = True
                    break
            if not on_empty_home and self.state == 'PLAYING':
                self.reset_attempt(lose_life=True)
            return
        if kind == 'ROAD':
            for v in self.vehicles:
                if self.frog.rect.colliderect(v.rect):
                    self.reset_attempt(lose_life=True)
                    return
        elif kind == 'RIVER':
            supported = False
            carry_vx = 0.0
            for p in self.platforms:
                if self.frog.rect.colliderect(p.rect):
                    if isinstance(p, Turtle):
                        if not p.is_submerged:
                            supported = True
                            carry_vx = p.vx
                    else:
                        supported = True
                        carry_vx = p.vx
            if supported:
                self.frog.rect.x += int(carry_vx * dt)
                if not in_bounds_rect(self.frog.rect):
                    self.reset_attempt(lose_life=True)
                    return
            else:
                self.reset_attempt(lose_life=True)
                return

    def draw_grid_bg(self, surf):
        # Dibujar la imagen de fondo
        surf.blit(background_img, (0, 0))
        
        # Dibujar áreas semitransparentes para mejorar la visibilidad
        for row in range(ROWS):
            kind = lane_type(row)
            rect = pygame.Rect(0, row*TILE, WIDTH, TILE)
            if kind == 'SAFE':
                # Área segura con transparencia
                s = pygame.Surface((WIDTH, TILE), pygame.SRCALPHA)
                s.fill((236, 226, 198, 100))  # Transparencia
                surf.blit(s, (0, row*TILE))
            elif kind == 'ROAD':
                # Carretera con transparencia
                s = pygame.Surface((WIDTH, TILE), pygame.SRCALPHA)
                s.fill((30, 90, 140, 100))  # Transparencia
                surf.blit(s, (0, row*TILE))
            elif kind == 'RIVER':
                # Río con transparencia
                s = pygame.Surface((WIDTH, TILE), pygame.SRCALPHA)
                s.fill((30, 90, 140, 100))  # Transparencia
                surf.blit(s, (0, row*TILE))
        
        # Dibujar las ranuras de hogar
        for i, r in enumerate(self.home_rects):
            color = (236, 226, 198, 150) if not self.home_occupied[i] else (90, 190, 110, 200)
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill(color)
            surf.blit(s, r.topleft)
            if self.home_occupied[i]:
                img_scaled = pygame.transform.scale(home_frog_img, (r.w, r.h))
                surf.blit(img_scaled, r.topleft)

    def draw_hud(self, surf):
        hud_text = f"Puntos: {self.score}   Vidas: {self.lives}   Nivel: {self.level}   Tiempo: {int(self.time_left)}s"
        txt = FONT.render(hud_text, True, WHITE)
        # Fondo semitransparente para el HUD
        s = pygame.Surface((WIDTH, 30), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        surf.blit(s, (0, 0))
        surf.blit(txt, (8, 6))

    def draw(self, surf):
        self.draw_grid_bg(surf)
        for v in self.vehicles: v.draw(surf)
        for p in self.platforms: p.draw(surf)
        if self.state == 'PLAYING':
            self.frog.draw(surf)
        self.draw_hud(surf)

        if self.state == 'LEVEL_CLEARED':
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0,0,0,160))
            surf.blit(shade,(0,0))
            txt1 = FONT2.render("¡Nivel completado!", True, WHITE)
            txt2 = FONT.render("Pulsa ENTER para continuar", True, WHITE)
            surf.blit(txt1, (WIDTH//2-txt1.get_width()//2, HEIGHT//2-40))
            surf.blit(txt2, (WIDTH//2-txt2.get_width()//2, HEIGHT//2+8))

        if self.state == 'GAMEOVER':
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0,0,0,180))
            surf.blit(shade,(0,0))
            txt1 = FONT2.render("GAME OVER", True, RED)
            txt2 = FONT.render("Pulsa R para reiniciar", True, WHITE)
            txt3 = FONT.render(f"Puntuación final: {self.score}", True, WHITE)
            surf.blit(txt1, (WIDTH//2-txt1.get_width()//2, HEIGHT//2-60))
            surf.blit(txt3, (WIDTH//2-txt3.get_width()//2, HEIGHT//2-16))
            surf.blit(txt2, (WIDTH//2-txt2.get_width()//2, HEIGHT//2+24))

        if self.state == 'PAUSED':
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0,0,0,180))
            surf.blit(shade,(0,0))
            txt1 = FONT2.render("PAUSA", True, WHITE)
            txt2 = FONT.render("Pulsa P para continuar", True, WHITE)
            surf.blit(txt1, (WIDTH//2 - txt1.get_width()//2, HEIGHT//2 - 40))
            surf.blit(txt2, (WIDTH//2 - txt2.get_width()//2, HEIGHT//2 + 10))

# =========================
# Bucle principal
# =========================
def main():
    game = Game()
    running = True
    while running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.KEYDOWN:
                # --- tecla P para pausar ---
                if event.key == pygame.K_p:
                    if game.state == 'PLAYING':
                        game.state = 'PAUSED'
                        pygame.mixer.music.pause()  # Pausar música cuando el juego se pausa
                    elif game.state == 'PAUSED':
                        game.state = 'PLAYING'
                        pygame.mixer.music.unpause()  # Reanudar música cuando el juego continúa

                if game.state == 'PLAYING':
                    game.handle_input(event.key)
                elif game.state == 'LEVEL_CLEARED':
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game.next_level()
                elif game.state == 'GAMEOVER':
                    if event.key == pygame.K_r:
                        # Reiniciar el juego y la música
                        game = Game()
                        pygame.mixer.music.play(-1)  # Volver a reproducir la música

        if game.state == 'PLAYING':
            game.update(dt)

        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()