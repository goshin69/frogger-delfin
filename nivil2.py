import pygame, sys, os, random
pygame.init()
pygame.display.set_caption("Dopher — Frogger Ecológico")

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
AGUA = (198,166,100)
ARENA = (119,197,214)
ORILLA = (230,240,200)
META = (198,166,100)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
VERDE = (70,200,90)
ROJO = (200,60,60)
AZUL = (119,197,214)

# ======== IMÁGENES ========
def load_img(name, w=TILE, h=TILE, color=(150,150,150)):
    path = os.path.join("imagenes", name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w,h))
    s = pygame.Surface((w,h)); s.fill(color)
    pygame.draw.rect(s, (255,255,255), s.get_rect(), 2)
    return s

img_cangrejo = load_img("cancrejo.png", 50, 50, (200,50,50))
img_basura   = load_img("basura.png", 48, 48, (100,100,100))
img_peligro  = load_img("medusa.png", 64, 64, (120,60,160))
img_meta     = load_img("basura.png", 64, 64, (200,100,50))

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

# ======== FUNCIONES ========
def crear_basura_y_peligros():
    basura_group.empty()
    peligro_group.empty()
    for i in range(5):
        x = random.randint(50, ANCHO-50)
        y = random.choice([TILE*1, TILE*2, TILE*3])
        basura_group.add(Basura(x,y))
    for y in [TILE*5, TILE*6, TILE*2]:
        for _ in range(3):
            x = random.randint(0, ANCHO)
            vel = random.choice([-3,3])
            peligro_group.add(Peligro(x,y,vel))

def draw_background():
    for i, zona in enumerate(LANE_LAYOUT):
        rect = pygame.Rect(0, i*TILE, ANCHO, TILE)
        color = {'AGUA':AGUA, 'ARENA':ARENA, 'ORILLA':ORILLA, 'META':META, 'INICIO':ARENA}.get(zona, BLANCO)
        pygame.draw.rect(screen, color, rect)
    for i, rect in enumerate(meta_rects):
        if ocupadas[i]:
            pygame.draw.rect(screen, VERDE, rect)
        else:
            screen.blit(img_meta, rect)

def draw_hud():
    font = pygame.font.SysFont(None, 28)
    t1 = font.render(f"Vidas: {jugador.vidas}", True, NEGRO)
    t2 = font.render(f"Basura: {'✅' if jugador.tiene_basura else '❌'}", True, NEGRO)
    t3 = font.render(f"Limpiezas: {sum(ocupadas)}/5", True, NEGRO)
    screen.blit(t1, (10,10))
    screen.blit(t2, (10,35))
    screen.blit(t3, (10,60))

def reset_player():
    jugador.rect.center = (ANCHO//2, ALTO-60)
    jugador.tiene_basura = False

def reiniciar_nivel():
    reset_player()
    jugador.vidas = 3
    for i in range(5): ocupadas[i] = False
    crear_basura_y_peligros()

# ======== Menu de pausa ========
def menu_pausa():
    opciones = ["Continuar", "Reiniciar", "Salir"]
    seleccion = 0
    font = pygame.font.SysFont(None, 48)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: seleccion = (seleccion - 1) % len(opciones)
                if e.key == pygame.K_DOWN: seleccion = (seleccion + 1) % len(opciones)
                if e.key == pygame.K_RETURN:
                    if opciones[seleccion] == "Continuar":
                        return
                    elif opciones[seleccion] == "Reiniciar":
                        reiniciar_nivel()
                        return
                    elif opciones[seleccion] == "Salir":
                        pygame.quit(); sys.exit()

        # Fondo semitransparente
        s = pygame.Surface((ANCHO, ALTO)); s.set_alpha(180); s.fill((0,0,0))
        screen.blit(s, (0,0))
        title = font.render("PAUSA", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, ALTO//3))
        for i, texto in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            t = font.render(texto, True, color)
            screen.blit(t, (ANCHO//2 - t.get_width()//2, ALTO//2 + i*60))
        pygame.display.flip()
        clock.tick(30)

# ======== OBJETOS INICIALES ========
jugador = Cangrejo()
player_group = pygame.sprite.Group(jugador)
basura_group = pygame.sprite.Group()
peligro_group = pygame.sprite.Group()

meta_rects = [pygame.Rect(i*(ANCHO//5)+30, 0, TILE, TILE) for i in range(5)]
ocupadas = [False]*5
crear_basura_y_peligros()

# ======== BUCLE PRINCIPAL ========
pausado = False
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP: jugador.move(0,-1)
            if e.key == pygame.K_DOWN: jugador.move(0,1)
            if e.key == pygame.K_LEFT: jugador.move(-1,0)
            if e.key == pygame.K_RIGHT: jugador.move(1,0)
            if e.key == pygame.K_p:  # PAUSA
                menu_pausa()

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
            reiniciar_nivel()

    # Llegar a meta con basura
    for i, rect in enumerate(meta_rects):
        if jugador.tiene_basura and not ocupadas[i] and jugador.rect.colliderect(rect):
            ocupadas[i] = True
            jugador.tiene_basura = False
            reset_player()

    # Verificar victoria
    if all(ocupadas):
        font = pygame.font.SysFont(None, 64)
        screen.fill(NEGRO)
        text = font.render("¡Mar Limpio!" \
        " siguiente nivel!", True, BLANCO)
        screen.blit(text, (ANCHO//3, ALTO//2))
        pygame.display.flip()
        pygame.time.wait(4000)
        reiniciar_nivel()

    # ======== DIBUJO ========
    draw_background()
    basura_group.draw(screen)
    peligro_group.draw(screen)
    player_group.draw(screen)
    draw_hud()

    pygame.display.flip()
    clock.tick(FPS)
