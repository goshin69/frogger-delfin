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
AZUL_CLARO = (100, 150, 255)
ROJO_CLARO = (255, 100, 100)

# ======== FUNCION PARA CARGAR IMAGENES ========
def cargar_imagen(nombre_archivo, ancho=TILE, alto=TILE, color_placeholder=(150,150,150)):
    ruta = get_file_path(os.path.join("imagenes", nombre_archivo))
    
    if ruta and os.path.exists(ruta):
        try:
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, (ancho, alto))
        except Exception as e:
            print(f"Error cargando {ruta}: {e}")
    
    # Si no encuentra la imagen, crea una de reemplazo con el color
    superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    superficie.fill(color_placeholder)
    
    # Dibujar texto con el nombre del archivo para identificarlo
    font = pygame.font.SysFont(None, 20)
    texto = font.render(nombre_archivo.split('.')[0], True, BLANCO)
    texto_rect = texto.get_rect(center=(ancho//2, alto//2))
    superficie.blit(texto, texto_rect)
    
    return superficie

# ======== CARGAR IMAGENES DEL CÓMIC ========
def cargar_pagina_comic(num_pagina):
    return cargar_imagen(f"Intro2.jpeg", ANCHO, ALTO, (50, 120, 200))

# ======== SECUENCIA DE CÓMIC ========
def mostrar_comic():
    num_paginas = 1 
    
    # Cargar páginas del cómic
    paginas_comic = []
    for i in range(1, num_paginas + 1):
        pagina = cargar_pagina_comic(i)
        paginas_comic.append(pagina)
    
    # Crear botón de skip
    fuente_skip = pygame.font.SysFont(None, 36)
    texto_skip = fuente_skip.render("Saltar (ESC)", True, BLANCO)
    rect_skip = texto_skip.get_rect(topright=(ANCHO - 20, 20))
    
    # Mostrar cada página del cómic
    pagina_actual = 0
    duracion_pagina = 4000  # 4 segundos por página
    tiempo_inicio_pagina = pygame.time.get_ticks()
    
    ejecutando = True
    while ejecutando and pagina_actual < num_paginas:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en el botón de skip
                if rect_skip.collidepoint(evento.pos):
                    ejecutando = False
                # Avanzar página al hacer clic en cualquier parte
                else:
                    pagina_actual += 1
                    tiempo_inicio_pagina = pygame.time.get_ticks()
        
        # Avanzar página automáticamente después del tiempo establecido
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_inicio_pagina > duracion_pagina:
            pagina_actual += 1
            tiempo_inicio_pagina = tiempo_actual
        
        # Dibujar página actual
        if pagina_actual < num_paginas:
            screen.blit(paginas_comic[pagina_actual], (0, 0))
            
            pygame.draw.rect(screen, (0, 0, 0, 150), rect_skip.inflate(20, 10), border_radius=5)
            screen.blit(texto_skip, rect_skip)
            
            # Dibujar indicador de pagina
            indicador_pagina = fuente_skip.render(f"{pagina_actual + 1}/{num_paginas}", True, BLANCO)
            screen.blit(indicador_pagina, (ANCHO // 2 - indicador_pagina.get_width() // 2, ALTO - 50))
        
        pygame.display.flip()
        clock.tick(60)

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

# ======== CARGAR IMAGENES DEL JUEGO ========
img_cangrejo = cargar_imagen("cancrejo.png", 50, 50, (220, 60, 60))
img_basura = cargar_imagen("bolsa de basura.png", 48, 48, (120, 120, 120))
img_lata_azul = cargar_imagen("lata azul.png", 35, 45, AZUL_CLARO)
img_lata_roja = cargar_imagen("lata roja.png", 35, 45, ROJO_CLARO)
img_peligro = cargar_imagen("gaviota_der.png", 64, 64, (120, 60, 160))

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
        self.vidas = 5
        self.tiene_basura = False
        self.tipo_basura = None  # Para saber qué tipo de basura lleva
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        
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
    def __init__(self, x, y, tipo="bolsa"):
        super().__init__()
        self.tipo = tipo
        # Asignar imagen según el tipo
        if tipo == "bolsa":
            self.image = img_basura
            self.puntos = 3  # 3 puntos para bolsas
        elif tipo == "lata_azul":
            self.image = img_lata_azul
            self.puntos = 2  # 2 puntos para latas
        elif tipo == "lata_roja":
            self.image = img_lata_roja
            self.puntos = 2  # 2 puntos para latas
            
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
    tipos_basura = ["bolsa", "lata_azul", "lata_roja"]
    
    # Solo 5 basuras en total
    for _ in range(5):
        while True:
            x = random.randint(50, ANCHO-50)
            y = random.choice([TILE*1, TILE*2, TILE*3])
            if all(abs(x - px) > 40 or abs(y - py) > 40 for px, py in posiciones_basura):
                posiciones_basura.append((x, y))
                # Elegir tipo aleatorio de basura
                tipo = random.choice(tipos_basura)
                basura_group.add(Basura(x, y, tipo))
                break
    
    for y in [TILE*4, TILE*5]:
        for _ in range(2):
            x = random.randint(0, ANCHO)
            vel = random.choice([-5, 5])
            peligro_group.add(Peligro(x, y, vel))

def draw_background():
    screen.blit(fondo, (0, 0))

def draw_hud():
    font = pygame.font.SysFont(None, 28)
    screen.blit(font.render(f"Vidas: {jugador.vidas}", True, BLANCO), (10, 10))
    
    if jugador.tiene_basura:
        color_basura = AZUL_CLARO if jugador.tipo_basura == "lata_azul" else ROJO_CLARO if jugador.tipo_basura == "lata_roja" else BLANCO
        tipo_texto = jugador.tipo_basura.replace("_", " ").title()
        screen.blit(font.render(f"Basura: {tipo_texto}", True, color_basura), (10, 35))
    else:
        screen.blit(font.render(f"Basura: NO", True, BLANCO), (10, 35))
        
    screen.blit(font.render(f"Limpiezas: {sum(ocupadas)}/5", True, BLANCO), (10, 60))
    screen.blit(font.render(f"Puntaje: {puntaje}", True, BLANCO), (10, 85))

def reset_player():
    jugador.rect.center = (ANCHO//2, ALTO-60)
    jugador.tiene_basura = False
    jugador.tipo_basura = None

def reiniciar_nivel():
    global puntaje
    reset_player()
    jugador.vidas = 5
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
# Los corales son invisibles - solo definimos sus rectangulos para la detección de colisiones
meta_rects = [pygame.Rect(i*(ANCHO//5)+30, 0, TILE, TILE) for i in range(5)]
ocupadas = [False]*5
puntaje = 0

# ======== MOSTRAR CÓMIC AL INICIO ========
mostrar_comic()
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
            jugador.tipo_basura = hit.tipo
            puntaje += hit.puntos  
            basura_group.remove(hit)

    # ======== COLISION CON PELIGROS ========
    if not jugador.invulnerable and pygame.sprite.spritecollideany(jugador, peligro_group):
        # REAPARECER BASURA EN EL CENTRO SI LA LLEVABA
        if jugador.tiene_basura:
            # Regenerar basura del mismo tipo en el centro
            basura_group.add(Basura(ANCHO//2, ALTO//2, jugador.tipo_basura))
            jugador.tiene_basura = False
            jugador.tipo_basura = None

        jugador.vidas -= 1
        puntaje = max(0, puntaje - 5)  # Penalización reducida

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
            jugador.tipo_basura = None
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