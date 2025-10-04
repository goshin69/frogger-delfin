import sys, random, math, pygame

# =========================
# Configuración general
# =========================
pygame.init()
pygame.display.set_caption("Frogger — Pygame")

TILE = 48
COLS = 13
LANE_LAYOUT = [
    'HOMES',  # fila 0: hogares
    'RIVER',
    'RIVER',
    'RIVER',
    'RIVER',
    'RIVER',
    'SAFE',   # franja segura central
    'ROAD',
    'ROAD',
    'ROAD',
    'ROAD',
    'ROAD',
    'SAFE',   # zona de inicio (abajo)
]
ROWS = len(LANE_LAYOUT)

WIDTH  = COLS * TILE  # 13 * 48 = 624
HEIGHT = ROWS * TILE  # 13 * 48 = 624
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()

# Colores
BG_DARK     = (18, 22, 28)
SAFE_GRASS  = (34, 139, 34)
ROAD_GRAY   = (60, 60, 70)
WATER_BLUE  = (30, 90, 140)
HOME_GREEN  = (20, 120, 60)
WHITE       = (235, 235, 235)
YELLOW      = (240, 220, 60)
RED         = (220, 50, 50)
BROWN       = (139, 90, 43)
TURTLE_GREEN= (80, 170, 120)
ORANGE      = (245, 160, 60)
BLACK       = (0, 0, 0)

FONT  = pygame.font.SysFont("arial", 20)
FONT2 = pygame.font.SysFont("arial", 36, bold=True)

# Puntuación
POINT_PER_NEW_ROW = 10
POINT_PER_HOME    = 200

# Temporizador por intento (segundos)
TIME_PER_ATTEMPT = 60.0

# Ranuras de Hogar (5)
HOME_COLS = [1, 4, 6, 8, 11]  # columnas válidas para los hogares (1 tile de ancho cada uno)

# Cargar sonido de victoria
try:
    win_sound = pygame.mixer.Sound("win.mp3")
except:
    print("No se pudo cargar el sonido de victoria. Continuando sin sonido.")
    win_sound = None

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
    def __init__(self, rect, vx, color):
        self.rect = rect
        self.vx   = vx
        self.color= color
        self.alive = True

    def update(self, dt):
        self.rect.x += self.vx * dt
        # Fuera de pantalla + margen de 2 tiles -> eliminar
        if self.rect.right < -2*TILE or self.rect.left > WIDTH + 2*TILE:
            self.alive = False

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=6)

class Vehicle(MovingEntity):
    pass

class Log(MovingEntity):
    pass

class Turtle(MovingEntity):
    """
    Tortuga sumergible: ciclo visible -> parpadeo -> sumergida
    """
    def __init__(self, rect, vx, color=TURTLE_GREEN):
        super().__init__(rect, vx, color)
        # parámetros del ciclo (segundos)
        self.period_total   = 6.0
        self.blink_duration = 0.8
        self.submerge_time  = 1.4
        # desfase aleatorio para no sincronizarlas
        self.phase = random.uniform(0, self.period_total)
        self.t = 0.0

    def update(self, dt):
        super().update(dt)
        self.t = (self.t + dt) % self.period_total

    @property
    def is_blinking(self):
        # último tramo antes de sumergirse
        return (self.period_total - self.blink_duration - self.submerge_time) <= self.t < (self.period_total - self.submerge_time)

    @property
    def is_submerged(self):
        # tramo final del ciclo
        return self.t >= (self.period_total - self.submerge_time)

    def draw(self, surf):
        if self.is_submerged:
            return  # no se dibuja
        color = ORANGE if self.is_blinking else self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=10)

# =========================
# Spawner por carril
# =========================
class Spawner:
    """
    Genera vehículos / troncos / tortugas en una fila específica.
    """
    def __init__(self, row, entity_kind, direction, speed_range, size_range_tiles, gap_range, level_scale=1.0):
        self.row = row
        self.entity_kind = entity_kind  # 'VEHICLE', 'LOG', 'TURTLE'
        self.direction = direction      # -1 (izq), +1 (der)
        self.speed_range = speed_range  # (min, max) px/s
        self.size_range_tiles = size_range_tiles # (minTiles, maxTiles)
        self.gap_range = gap_range      # (min_s, max_s)
        self.level_scale = level_scale
        self.timer = random.uniform(*self.gap_range)

    def lane_yx(self):
        y = self.row * TILE
        return y

    def spawn_one(self):
        y = self.row * TILE
        # alto = casi 1 tile
        h = int(TILE * 0.9)
        w_tiles = random.randint(self.size_range_tiles[0], self.size_range_tiles[1])
        w = int(w_tiles * TILE * random.uniform(0.95, 1.05))

        if self.direction > 0:
            x = -w - TILE  # nace por la izquierda
        else:
            x = WIDTH + TILE  # nace por la derecha

        vx = random.uniform(*self.speed_range) * self.direction * self.level_scale

        # centrar verticalmente en la fila
        rect = pygame.Rect(x, y + (TILE - h)//2, w, h)

        if self.entity_kind == 'VEHICLE':
            color = random.choice([(200,80,60), (70,170,220), (240,200,70), (170,100,200)])
            return Vehicle(rect, vx, color)
        elif self.entity_kind == 'LOG':
            return Log(rect, vx, BROWN)
        else:
            return Turtle(rect, vx)

    def update(self, dt, container_list):
        self.timer -= dt
        if self.timer <= 0:
            container_list.append(self.spawn_one())
            self.timer = random.uniform(*self.gap_range)

# =========================
# Rana (Jugador)
# =========================
class Frog:
    def __init__(self, spawn_col, spawn_row):
        size = int(TILE * 0.9)
        self.w = size
        self.h = size
        self.spawn_col = spawn_col
        self.spawn_row = spawn_row
        self.input_cooldown = 0.0
        self.cooldown_time = 0.12  # segundos entre saltos
        self.reset()

    def reset(self):
        x, y = grid_to_px(self.spawn_col, self.spawn_row)
        self.rect = pygame.Rect(x + (TILE - self.w)//2, y + (TILE - self.h)//2, self.w, self.h)
        self.on_platform = None
        self.furthest_row = self.spawn_row  # para puntuación por avance
        self.alive = True

    def row(self):
        return max(0, min(ROWS-1, self.rect.centery // TILE))

    def move(self, dx_tiles, dy_tiles):
        # aplicar salto en tiles
        self.rect.x += dx_tiles * TILE
        self.rect.y += dy_tiles * TILE

    def update(self, dt):
        if self.input_cooldown > 0:
            self.input_cooldown -= dt

    def draw(self, surf):
        pygame.draw.rect(surf, YELLOW, self.rect, border_radius=10)
        # ojitos
        eye_w = max(2, self.w//10)
        eye_h = eye_w
        pygame.draw.rect(surf, BLACK, (self.rect.x+self.w*0.25, self.rect.y+self.h*0.25, eye_w, eye_h))
        pygame.draw.rect(surf, BLACK, (self.rect.x+self.w*0.65, self.rect.y+self.h*0.25, eye_w, eye_h))

# =========================
# Juego
# =========================
class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 5
        # hogar ocupado
        self.home_occupied = [False]*5
        self.state = 'PLAYING'  # PLAYING | LEVEL_CLEARED | GAMEOVER | PAUSED
        # temporizador por intento
        self.time_left = TIME_PER_ATTEMPT
        # Controlar si ya se reprodujo el sonido de victoria
        self.played_win_sound = False

        # Rana
        spawn_row = max(i for i,t in enumerate(LANE_LAYOUT) if t == 'SAFE')  # última SAFE
        spawn_col = COLS // 2
        self.frog = Frog(spawn_col, spawn_row)

        # entidades
        self.vehicles = []
        self.platforms = []
        self.spawners = []
        self.build_spawners()

        # precomputar rects de hogares
        self.home_rects = []
        y0 = 0
        for idx, c in enumerate(HOME_COLS):
            x, y = grid_to_px(c, 0)
            self.home_rects.append(pygame.Rect(x+4, y+4, TILE-8, TILE-8))

    def build_spawners(self):
        self.vehicles.clear()
        self.platforms.clear()
        self.spawners.clear()

        level_scale = 1.0 + (self.level-1)*0.12

        # Configurar spawners por fila
        for r, kind in enumerate(LANE_LAYOUT):
            if kind == 'ROAD':
                # dirección alterna por fila
                direction = -1 if (r % 2 == 0) else 1
                speed_range = (120, 210)  # px/s
                size_tiles  = (2, 3)
                gap_range   = (1.0, 2.2)
                self.spawners.append(Spawner(r, 'VEHICLE', direction, speed_range, size_tiles, gap_range, level_scale))

            elif kind == 'RIVER':
                direction = 1 if (r % 2 == 0) else -1
                speed_range = (80, 150)
                gap_range   = (1.3, 2.5)
                # alternar entre troncos y tortugas por fila
                if r % 3 == 0:
                    # tortugas un poco más cortas
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
        # Reiniciar la bandera de sonido de victoria
        self.played_win_sound = False

    def toggle_pause(self):
        if self.state == 'PLAYING':
            self.state = 'PAUSED'
        elif self.state == 'PAUSED':
            self.state = 'PLAYING'

    def play_win_sound(self):
        """Reproducir sonido de victoria si está disponible"""
        if win_sound and not self.played_win_sound:
            win_sound.play()
            self.played_win_sound = True

    def handle_input(self, key):
        if self.state == 'PAUSED':
            if key == pygame.K_p:
                self.toggle_pause()
            return
            
        if self.state != 'PLAYING':
            return
        if self.frog.input_cooldown > 0:
            return

        dx = dy = 0
        if key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_DOWN:
            dy = 1
        elif key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        elif key == pygame.K_p:
            self.toggle_pause()
            return
        else:
            return

        # mover
        prev_row = self.frog.row()
        self.frog.move(dx, dy)

        # morir si sale de límites por salto
        if not in_bounds_rect(self.frog.rect):
            self.reset_attempt(lose_life=True)
            return

        # puntuación por primer avance de fila (hacia arriba)
        new_row = self.frog.row()
        if new_row < self.frog.furthest_row:
            self.score += POINT_PER_NEW_ROW
            self.frog.furthest_row = new_row

        self.frog.input_cooldown = self.frog.cooldown_time

    def update(self, dt):
        if self.state != 'PLAYING':
            # Reproducir sonido de victoria cuando se complete un nivel
            if self.state == 'LEVEL_CLEARED':
                self.play_win_sound()
            return

        # temporizador
        self.time_left -= dt
        if self.time_left <= 0:
            self.reset_attempt(lose_life=True)
            return

        # actualizar spawners
        for sp in self.spawners:
            if LANE_LAYOUT[sp.row] == 'ROAD':
                sp.update(dt, self.vehicles)
            elif LANE_LAYOUT[sp.row] == 'RIVER':
                sp.update(dt, self.platforms)

        # actualizar entidades
        for v in self.vehicles:
            v.update(dt)
        for p in self.platforms:
            p.update(dt)

        # eliminar fuera de pantalla
        self.vehicles = [v for v in self.vehicles if v.alive]
        self.platforms= [p for p in self.platforms if p.alive]

        # actualizar rana (cooldown)
        self.frog.update(dt)

        # chequeos de colisión por tipo de fila
        r = self.frog.row()
        kind = lane_type(r)

        # HOGARES (fila 0)
        if r == 0:
            on_empty_home = False
            for i, rect in enumerate(self.home_rects):
                if self.frog.rect.colliderect(rect):
                    if not self.home_occupied[i]:
                        # ocupa hogar
                        self.home_occupied[i] = True
                        self.score += POINT_PER_HOME
                        # reintento sin perder vida (nueva rana)
                        self.reset_attempt(lose_life=False)
                        # nivel completo?
                        if self.all_homes_filled():
                            self.state = 'LEVEL_CLEARED'
                            # Reproducir sonido de victoria
                            self.play_win_sound()
                    else:
                        # hogar ocupado -> muerte (puedes cambiar a 'rebote' si prefieres)
                        self.reset_attempt(lose_life=True)
                    on_empty_home = True
                    break
            # si está en fila de hogares pero no está dentro de un slot, cae al agua
            if not on_empty_home and self.state == 'PLAYING':
                self.reset_attempt(lose_life=True)
            return  # ya resuelto el caso superior

        if kind == 'ROAD':
            # colisión con vehículos = muerte
            for v in self.vehicles:
                if self.frog.rect.colliderect(v.rect):
                    self.reset_attempt(lose_life=True)
                    return

        elif kind == 'RIVER':
            # verificar soporte en plataforma
            supported = False
            carry_vx = 0.0
            platform_submerged_under_frog = False

            for p in self.platforms:
                if self.frog.rect.colliderect(p.rect):
                    if isinstance(p, Turtle):
                        if not p.is_submerged:
                            supported = True
                            carry_vx = p.vx
                        else:
                            platform_submerged_under_frog = True
                    else:
                        # log
                        supported = True
                        carry_vx = p.vx
                    # no rompemos; podría haber múltiples
            if supported:
                # arrastre
                self.frog.rect.x += int(carry_vx * dt)
                # si nos saca de la pantalla -> muerte
                if not in_bounds_rect(self.frog.rect):
                    self.reset_attempt(lose_life=True)
                    return
            else:
                # agua!
                self.reset_attempt(lose_life=True)
                return

        # nada específico en SAFE

    def draw_grid_bg(self, surf):
        # fondo
        surf.fill(BG_DARK)
        # pintar franjas por tipo
        for row in range(ROWS):
            kind = lane_type(row)
            x, y = 0, row*TILE
            rect = pygame.Rect(x, y, WIDTH, TILE)

            if kind == 'SAFE':
                pygame.draw.rect(surf, SAFE_GRASS, rect)
            elif kind == 'ROAD':
                pygame.draw.rect(surf, ROAD_GRAY, rect)
            elif kind == 'RIVER':
                pygame.draw.rect(surf, WATER_BLUE, rect)
            elif kind == 'HOMES':
                pygame.draw.rect(surf, WATER_BLUE, rect)  # agua con hogares encima

        # dibujar hogares
        for i, r in enumerate(self.home_rects):
            color = HOME_GREEN if not self.home_occupied[i] else (90, 190, 110)
            pygame.draw.rect(surf, color, r, border_radius=8)
            if self.home_occupied[i]:
                # pequeña "rana" como sello
                stamp = r.inflate(-r.w*0.45, -r.h*0.45)
                pygame.draw.rect(surf, YELLOW, stamp, border_radius=6)

        # líneas de rejilla sutiles
        for c in range(COLS+1):
            x = c*TILE
            pygame.draw.line(surf, (0,0,0,40), (x,0), (x,HEIGHT))
        for r in range(ROWS+1):
            y = r*TILE
            pygame.draw.line(surf, (0,0,0,40), (0,y), (WIDTH,y))

    def draw_hud(self, surf):
        # HUD (arriba)
        hud_text = f"Puntos: {self.score}   Vidas: {self.lives}   Nivel: {self.level}   Tiempo: {int(self.time_left)}s"
        txt = FONT.render(hud_text, True, WHITE)
        surf.blit(txt, (8, 6))

    def draw(self, surf):
        self.draw_grid_bg(surf)

        # entidades
        for v in self.vehicles:
            v.draw(surf)
        for p in self.platforms:
            p.draw(surf)

        # rana
        if self.state == 'PLAYING' or self.state == 'PAUSED':
            self.frog.draw(surf)

        # HUD
        self.draw_hud(surf)

        # overlays
        if self.state == 'LEVEL_CLEARED':
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 160))
            surf.blit(shade, (0, 0))
            txt1 = FONT2.render("¡Nivel completado!", True, WHITE)
            txt2 = FONT.render("Pulsa ENTER para continuar", True, WHITE)
            surf.blit(txt1, (WIDTH//2 - txt1.get_width()//2, HEIGHT//2 - 40))
            surf.blit(txt2, (WIDTH//2 - txt2.get_width()//2, HEIGHT//2 + 8))

        elif self.state == 'GAMEOVER':
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 180))
            surf.blit(shade, (0, 0))
            txt1 = FONT2.render("GAME OVER", True, RED)
            txt2 = FONT.render("Pulsa R para reiniciar", True, WHITE)
            txt3 = FONT.render(f"Puntuación final: {self.score}", True, WHITE)
            surf.blit(txt1, (WIDTH//2 - txt1.get_width()//2, HEIGHT//2 - 60))
            surf.blit(txt3, (WIDTH//2 - txt3.get_width()//2, HEIGHT//2 - 16))
            surf.blit(txt2, (WIDTH//2 - txt2.get_width()//2, HEIGHT//2 + 24))
            
        elif self.state == 'PAUSED':
            # Oscurecer la pantalla
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 160))
            surf.blit(shade, (0, 0))
            
            # Dibujar menú de pausa
            txt1 = FONT2.render("PAUSA", True, WHITE)
            txt2 = FONT.render("Pulsa P para continuar", True, WHITE)
            txt3 = FONT.render("Pulsa R para reiniciar", True, WHITE)
            txt4 = FONT.render("Pulsa ESC para salir", True, WHITE)
            
            surf.blit(txt1, (WIDTH//2 - txt1.get_width()//2, HEIGHT//2 - 60))
            surf.blit(txt2, (WIDTH//2 - txt2.get_width()//2, HEIGHT//2 - 10))
            surf.blit(txt3, (WIDTH//2 - txt3.get_width()//2, HEIGHT//2 + 20))
            surf.blit(txt4, (WIDTH//2 - txt4.get_width()//2, HEIGHT//2 + 50))

# =========================
# Bucle principal
# =========================
def main():
    game = Game()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                # Manejar inputs según el estado del juego
                if game.state == 'PLAYING' or game.state == 'PAUSED':
                    game.handle_input(event.key)
                    
                elif game.state == 'LEVEL_CLEARED':
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game.next_level()
                        
                elif game.state == 'GAMEOVER':
                    if event.key == pygame.K_r:  # Solo pygame.K_r, no pygame.K_R
                        # Reiniciar el juego completo
                        game = Game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        # Actualizar el juego solo si está en estado PLAYING
        if game.state == 'PLAYING':
            game.update(dt)
        else:
            game.update(0)  # Pasar dt=0 para manejar sonidos en otros estados

        # Dibujo
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()