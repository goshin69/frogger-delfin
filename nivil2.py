import pygame, sys, os, random
pygame.init()
pygame.display.set_caption("Cangrejo Recolector — Frogger Ecológico")

# ======== CONFIGURACIÓN ========
ANCHO, ALTO = 832, 640
TILE = 64
FPS = 60
screen = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()

LANE_LAYOUT = [
    'META',
    'AGUA','AGUA','AGUA',
    'ORILLA',
    'ARENA','ARENA','ARENA',
    'INICIO'
]
COLS = 13
ROWS = len(LANE_LAYOUT)

# ======== COLORES ========
AGUA = (60,130,200)
ARENA = (240,220,160)
ORILLA = (230,240,200)
META = (50,100,150)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

# ======== IMÁGENES ========
def load_img(name, w=TILE, h=TILE, color=(150,150,150)):
    path = os.path.join("imagenes", name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w,h))
    s = pygame.Surface((w,h)); s.fill(color)
    pygame.draw.rect(s, (255,255,255), s.get_rect(), 2)
    return s

img_cangrejo = load_img("cangrejo.png", 50, 50, (200,50,50))
img_basura   = load_img("basura.png", 48, 48, (100,100,100))
img_peligro  = load_img("medusa.png", 64, 64, (120,60,160))
img_meta     = load_img("coral.png", 64, 64, (200,100,50))

# ======== CLASES ========
class Cangrejo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_cangrejo
        self.rect = self.image.get_rect(center=(ANCHO//2, ALTO-60))
        self.vidas = 3
        self.tiene_basura = False
    def move(self, dx, dy):
        self.rect.x += dx*TILE
        self.rect.y += dy*TILE
        self.rect.clamp_ip(screen.get_rect())

class Basura(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_basura
        self.rect = self.image.get_rect(center=(x,y))

class Peligro(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        self.image = img_peligro
        self.rect = self.image.get_rect(center=(x,y))
        self.vel = vel
    def update(self):
        self.rect.x += self.vel
        if self.rect.right < 0:
            self.rect.left = ANCHO
        elif self.rect.left > ANCHO:
            self.rect.right = 0

# ======== GRUPOS ========
jugador = Cangrejo()
player_group = pygame.sprite.Group(jugador)
basura_group = pygame.sprite.Group()
peligro_group = pygame.sprite.Group()

# Crear basura en carriles de agua
for i in range(5):
    x = random.randint(50, ANCHO-50)
    y = random.choice([TILE*1, TILE*2, TILE*3])
    basura_group.add(Basura(x,y))

# Crear peligros
for y in [TILE*5, TILE*6, TILE*2]:
    for _ in range(3):
        x = random.randint(0, ANCHO)
        vel = random.choice([-3,3])
        peligro_group.add(Peligro(x,y,vel))

# Metas (5 huecos)
meta_rects = []
ocupadas = [False]*5
espacio = ANCHO//5
for i in range(5):
    rect = pygame.Rect(i*espacio+30, 0, TILE, TILE)
    meta_rects.append(rect)

# ======== FUNCIONES ========
def draw_background():
    for i, zona in enumerate(LANE_LAYOUT):
        rect = pygame.Rect(0, i*TILE, ANCHO, TILE)
        color = {'AGUA':AGUA, 'ARENA':ARENA, 'ORILLA':ORILLA, 'META':META, 'INICIO':ARENA}.get(zona, BLANCO)
        pygame.draw.rect(screen, color, rect)
    # metas
    for i, rect in enumerate(meta_rects):
        if ocupadas[i]:
            pygame.draw.rect(screen, (60,180,80), rect)
        else:
            screen.blit(img_meta, rect)

def draw_hud():
    font = pygame.font.SysFont(None, 28)
    t1 = font.render(f"Vidas: {jugador.vidas}", True, NEGRO)
    t2 = font.render(f"Basura: {'✅' if jugador.tiene_basura else '❌'}", True, NEGRO)
    screen.blit(t1, (10,10))
    screen.blit(t2, (10,35))

def reset_player():
    jugador.rect.center = (ANCHO//2, ALTO-60)
    jugador.tiene_basura = False

# ======== BUCLE PRINCIPAL ========
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP: jugador.move(0,-1)
            if e.key == pygame.K_DOWN: jugador.move(0,1)
            if e.key == pygame.K_LEFT: jugador.move(-1,0)
            if e.key == pygame.K_RIGHT: jugador.move(1,0)

    peligro_group.update()

    # Colisiones con basura
    if not jugador.tiene_basura:
        hit = pygame.sprite.spritecollideany(jugador, basura_group)
        if hit:
            jugador.tiene_basura = True
            basura_group.remove(hit)

    # Colisiones con peligros
    if pygame.sprite.spritecollideany(jugador, peligro_group):
        jugador.vidas -= 1
        reset_player()
        if jugador.vidas <= 0:
            pygame.quit(); sys.exit()

    # Llegar a meta con basura
    for i, rect in enumerate(meta_rects):
        if jugador.tiene_basura and not ocupadas[i] and jugador.rect.colliderect(rect):
            ocupadas[i] = True
            jugador.tiene_basura = False
            reset_player()

    # Verificar victoria
    if all(ocupadas):
        screen.fill((0,0,0))
        font = pygame.font.SysFont(None, 64)
        text = font.render("¡Mar Limpio! 🌊🦀", True, BLANCO)
        screen.blit(text, (ANCHO//3, ALTO//2))
        pygame.display.flip()
        pygame.time.wait(4000)
        pygame.quit(); sys.exit()

    # ======== DIBUJO ========
    draw_background()
    basura_group.draw(screen)
    peligro_group.draw(screen)
    player_group.draw(screen)
    draw_hud()

    pygame.display.flip()
    clock.tick(FPS)
