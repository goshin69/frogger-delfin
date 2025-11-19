import pygame, sys, os, random
pygame.init()
pygame.display.set_caption("Cangrejo Recolector — Dolpher")

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

# ======== MUSICA ========
try:
    pygame.mixer.init()
    musica_path = get_file_path(os.path.join("musica", "musica_level_2.mp3"))
    if musica_path:
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
except Exception as e:
    print(f"No se pudo cargar la musica: {e}")

# ======== CONFIGURACION ========
ANCHO, ALTO = 1220, 740
TILE = 64
FPS = 60
screen = pygame.display.set_mode((ANCHO, ALTO), 0)
clock = pygame.time.Clock()

# ======== COLORES ========
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (70, 200, 90)
AZUL = (50, 120, 255)
ROJO = (200, 60, 60)

# ======== FUNCION PARA CARGAR IMAGENES ========
def cargar_imagen(nombre_archivo, ancho=TILE, alto=TILE, color_placeholder=(150,150,150)):
    ruta = get_file_path(os.path.join("imagenes", nombre_archivo))
    
    if ruta and os.path.exists(ruta):
        try:
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, (ancho, alto))
        except Exception as e:
            print(f"Error cargando {ruta}: {e}")
    
    superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    superficie.fill(color_placeholder)
    return superficie

# ======== CARGAR IMAGENES ========
img_cangrejo = cargar_imagen("cancrejo.png", 50, 50, (220, 60, 60))
img_basura = cargar_imagen("bolsa de basura.png", 48, 48, (120, 120, 120))
img_peligro = cargar_imagen("gaviota_der.png", 64, 64, (120, 60, 160))
img_meta = cargar_imagen("coral.png", 64, 64, (200, 100, 50))

# ======== FONDO ========
def cargar_fondo():
    archivos_fondo = ["fondocancrejo.png"]
    for archivo in archivos_fondo:
        ruta = get_file_path(os.path.join("imagenes", archivo))
        if ruta and os.path.exists(ruta):
            try:
                fondo = pygame.image.load(ruta).convert()
                return pygame.transform.scale(fondo, (ANCHO, ALTO))
            except:
                continue
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((50, 120, 200))
    return fondo

fondo = cargar_fondo()

# ======== CLASES ========
class Cangrejo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_cangrejo
        self.rect = self.image.get_rect(center=(ANCHO//2, ALTO-60))
        self.vidas = 3
        self.tiene_basura = False
        self.invulnerable = False
        self.tiempo_invulnerable = 0

        # para guardar basura recogida
        self.basura_x = None
        self.basura_y = None
        
    def move(self, dx, dy):
        new_x = self.rect.x + dx * TILE
        new_y = self.rect.y + dy * TILE
        new_x = max(0, min(new_x, ANCHO - self.rect.width))
        new_y = max(0, min(new_y, ALTO - self.rect.height))
        self.rect.x = new_x
        self.rect.y = new_y
        
    def update(self):
        if self.invulnerable:
            self.tiempo_invulnerable -= 1
            if self.tiempo_invulnerable <= 0:
                self.invulnerable = False
                
    def hacer_invulnerable(self, tiempo=60):
        self.invulnerable = True
        self.tiempo_invulnerable = tiempo

class Basura(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_basura
        self.rect = self.image.get_rect(center=(x, y))

class Peligro(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        self.image = img_peligro
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = vel
        
    def update(self):
        self.rect.x += self.vel
        if self.rect.right < 0:
            self.rect.left = ANCHO
        elif self.rect.left > ANCHO:
            self.rect.right = 0

# ======== FUNCIONES DEL JUEGO ========
def crear_basura_y_peligros():
    basura_group.empty()
    peligro_group.empty()
    
    posiciones_basura = []
    for _ in range(5):
        while True:
            x = random.randint(50, ANCHO-50)
            y = random.choice([TILE*1, TILE*2, TILE*3])
            if all(abs(x - px) > 40 or abs(y - py) > 40 for px, py in posiciones_basura):
                posiciones_basura.append((x, y))
                basura_group.add(Basura(x, y))
                break
    
    for y in [TILE*4, TILE*5]:
        for _ in range(2):
            x = random.randint(0, ANCHO)
            vel = random.choice([-2, 2])
            peligro_group.add(Peligro(x, y, vel))

def draw_background():
    screen.blit(fondo, (0, 0))

def draw_hud():
    font = pygame.font.SysFont(None, 28)
    screen.blit(font.render(f"Vidas: {jugador.vidas}", True, BLANCO), (10, 10))
    screen.blit(font.render(f"Basura: {'SÍ' if jugador.tiene_basura else 'NO'}", True, BLANCO), (10, 35))
    screen.blit(font.render(f"Limpiezas: {sum(ocupadas)}/5", True, BLANCO), (10, 60))
    screen.blit(font.render(f"Puntaje: {puntaje}", True, BLANCO), (10, 85))

def reset_player():
    jugador.rect.center = (ANCHO//2, ALTO-60)
    jugador.tiene_basura = False

def reiniciar_nivel():
    global puntaje
    reset_player()
    jugador.vidas = 3
    jugador.invulnerable = False
    puntaje = 0
    for i in range(5): 
        ocupadas[i] = False
    crear_basura_y_peligros()

# ======== MENU DE PAUSA ========
def menu_pausa():
    opciones = ["Continuar", "Reiniciar", "Salir"]
    seleccion = 0
    font = pygame.font.SysFont(None, 48)
    pausa_activa = True
    
    while pausa_activa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if seleccion == 0:
                        pausa_activa = False
                    elif seleccion == 1:
                        reiniciar_nivel()
                        pausa_activa = False
                    elif seleccion == 2:
                        pygame.quit()
                        sys.exit()
                elif evento.key in (pygame.K_ESCAPE, pygame.K_p):
                    pausa_activa = False

        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(180)
        overlay.fill(NEGRO)
        screen.blit(overlay, (0, 0))
        
        titulo = font.render("PAUSA", True, BLANCO)
        screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//3))
        
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            texto = font.render(opcion, True, color)
            screen.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 + i*60))
        
        pygame.display.flip()
        clock.tick(30)

# ======== PANTALLAS ========
def pantalla_mensaje(texto, subtexto, color=BLANCO):
    font1 = pygame.font.SysFont(None, 64)
    font2 = pygame.font.SysFont(None, 36)
    s = pygame.Surface((ANCHO, ALTO))
    s.fill(NEGRO)
    screen.blit(s, (0,0))
    t1 = font1.render(texto, True, color)
    t2 = font2.render(subtexto, True, BLANCO)
    screen.blit(t1, (ANCHO//2 - t1.get_width()//2, ALTO//2 - 40))
    screen.blit(t2, (ANCHO//2 - t2.get_width()//2, ALTO//2 + 20))
    pygame.display.flip()

# ======== INICIALIZACION ========
jugador = Cangrejo()
player_group = pygame.sprite.Group(jugador)
basura_group = pygame.sprite.Group()
peligro_group = pygame.sprite.Group()
meta_rects = [pygame.Rect(i*(ANCHO//5)+30, 0, TILE, TILE) for i in range(5)]
ocupadas = [False]*5
puntaje = 0
crear_basura_y_peligros()

# ======== BUCLE PRINCIPAL ========
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP: jugador.move(0, -1)
            if evento.key == pygame.K_DOWN: jugador.move(0, 1)
            if evento.key == pygame.K_LEFT: jugador.move(-1, 0)
            if evento.key == pygame.K_RIGHT: jugador.move(1, 0)
            if evento.key == pygame.K_p: menu_pausa()

    peligro_group.update()
    jugador.update()

    # ======== TOMAR BASURA ========
    if not jugador.tiene_basura:
        hit = pygame.sprite.spritecollideany(jugador, basura_group)
        if hit:
            jugador.tiene_basura = True
            basura_group.remove(hit)
            puntaje += 50

    # ======== COLISION CON PELIGROS ========
    if not jugador.invulnerable and pygame.sprite.spritecollideany(jugador, peligro_group):
        # REAPARECER BASURA EN EL CENTRO SI LA LLEVABA
        if jugador.tiene_basura:
            # Regenerar basura en el centro de la pantalla para que sea visible
            basura_group.add(Basura(ANCHO//2, ALTO//2))
            jugador.tiene_basura = False

        jugador.vidas -= 1
        puntaje = max(0, puntaje - 100)

        reset_player()
        jugador.hacer_invulnerable(60)

        if jugador.vidas <= 0:
            pantalla_mensaje("Vuelve Intentar", f"Puntaje final: {puntaje}", ROJO)
            pygame.time.wait(4000)
            reiniciar_nivel()

    # ======== ENTREGA DE BASURA ========
    for i, rect in enumerate(meta_rects):
        if jugador.tiene_basura and not ocupadas[i] and jugador.rect.colliderect(rect):
            ocupadas[i] = True
            jugador.tiene_basura = False
            puntaje += 200
            reset_player()

    # ======== NIVEL COMPLETADO ========
    if all(ocupadas):
        pantalla_mensaje("¡MAR LIMPIO!", f"Tu puntaje: {puntaje}", VERDE)
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
