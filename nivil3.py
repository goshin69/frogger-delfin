import pygame, sys, os, random, time
pygame.init()
pygame.display.set_caption("Nivel 3 — Buzo")

# ======== CONFIGURACIÓN MEJORADA ========
ANCHO, ALTO = 832, 640
FPS = 60
TILE = 64
TIEMPO_LIMITE = 75

# MODO VENTANA
screen = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
clock = pygame.time.Clock()

# ======== SONIDO MEJORADO ========
try:
    pygame.mixer.init()
    # Usar path multiplataforma
    musica_path = os.path.join("delfin-version-frogge3r-main", "musica", "level 3.mp3")
    if os.path.exists(musica_path):
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
except Exception as e:
    print(f"No se pudo cargar la música: {e}")

# ======== COLORES ========
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_OSCURO = (10, 40, 90)
AZUL_AGUA = (30, 130, 200)
ROJO = (220, 70, 70)
VERDE = (60, 200, 120)
AZUL = (50, 100, 255)
AMARILLO = (255, 255, 0)

# ======== CARGA DE IMÁGENES MEJORADA ========
def cargar_imagen(nombre, ancho=TILE, alto=TILE, color_default=(150, 150, 150)):
    """Carga imágenes de forma robusta con múltiples rutas posibles"""
    rutas_posibles = [
        os.path.join("imagenes", nombre),
        os.path.join("delfin-version-frogge3r-main", "imagenes", nombre),
        nombre
    ]
    
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            try:
                img = pygame.image.load(ruta).convert_alpha()
                return pygame.transform.scale(img, (ancho, alto))
            except Exception as e:
                print(f"Error cargando {ruta}: {e}")
                continue
    
    # Placeholder si no se encuentra
    print(f"Imagen no encontrada: {nombre}")
    surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    surf.fill(color_default)
    # Añadir texto identificador
    font = pygame.font.SysFont(None, 20)
    texto = font.render(nombre.split('.')[0], True, BLANCO)
    texto_rect = texto.get_rect(center=(ancho//2, alto//2))
    surf.blit(texto, texto_rect)
    return surf

# ======== FONDO MEJORADO ========
def cargar_fondo():
    """Carga el fondo con múltiples opciones"""
    fondos_posibles = ["fondobuzo.png"]
    
    for fondo_nombre in fondos_posibles:
        rutas = [
            os.path.join("imagenes", fondo_nombre),
            os.path.join("delfin-version-frogge3r-main", "imagenes", fondo_nombre),
            fondo_nombre
        ]
        
        for ruta in rutas:
            if os.path.exists(ruta):
                try:
                    fondo_img = pygame.image.load(ruta).convert()
                    return pygame.transform.scale(fondo_img, (ANCHO, ALTO))
                except Exception as e:
                    print(f"Error cargando fondo {ruta}: {e}")
                    continue
    
    # Fondo por defecto
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(AZUL_AGUA)
    # Añadir efecto de olas simples
    for i in range(20):
        y = random.randint(0, ALTO)
        pygame.draw.line(fondo, (40, 150, 220), (0, y), (ANCHO, y), 1)
    return fondo

fondo = cargar_fondo()

# ======== CARGAR IMÁGENES ========
img_buzo = cargar_imagen("buzo_abajo.png", TILE, TILE, (50, 150, 255))
img_barco = cargar_imagen("barco.png", 120, 60, (100, 100, 100))
img_animal = cargar_imagen("tortuga.png", 40, 40, (200, 120, 50))

# ======== CLASES MEJORADAS ========
class Buzo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_buzo
        self.rect = self.image.get_rect(center=(ANCHO//2, 48))
        self.vidas = 3
        self.lleva = False
        self.puntaje = 0
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        
    def move(self, dx, dy):
        step = TILE // 2
        new_x = self.rect.x + dx * step
        new_y = self.rect.y + dy * step
        
        # Limitar movimiento dentro de la pantalla
        new_x = max(0, min(new_x, ANCHO - self.rect.width))
        new_y = max(0, min(new_y, ALTO - self.rect.height))
        
        self.rect.x = new_x
        self.rect.y = new_y
        
    def update(self):
        # Actualizar tiempo de invulnerabilidad
        if self.invulnerable:
            self.tiempo_invulnerable -= 1
            if self.tiempo_invulnerable <= 0:
                self.invulnerable = False
                
    def hacer_invulnerable(self, tiempo=30):
        self.invulnerable = True
        self.tiempo_invulnerable = tiempo

class Barco(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        self.image = img_barco
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = vel
        
    def update(self):
        self.rect.x += self.vel
        if self.rect.right < -50: 
            self.rect.left = ANCHO + 50
        elif self.rect.left > ANCHO + 50: 
            self.rect.right = -50

class Animal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_animal
        self.rect = self.image.get_rect(center=(x, y))

# ======== CREAR NIVEL MEJORADO ========
def crear_nivel():
    global buzo, buzo_g, barcos, animales, zona_segura, entregados, inicio, tiempo_restante
    
    buzo = Buzo()
    buzo_g = pygame.sprite.Group(buzo)
    barcos = pygame.sprite.Group()
    animales = pygame.sprite.Group()

    # Barcos en diferentes alturas con velocidades variadas
    alturas_barcos = [260, 300, 340, 380, 420]
    for y in alturas_barcos:
        x = random.randint(0, ANCHO)
        vel = random.choice([-4, -3, 3, 4])
        barcos.add(Barco(x, y, vel))

    # Animales distribuidos en el fondo marino
    posiciones_animales = []
    for _ in range(5):
        while True:
            x = random.randint(100, ANCHO-100)
            y = random.randint(ALTO-150, ALTO-60)
            # Verificar que no estén muy cerca unos de otros
            if all(abs(x - px) > 60 or abs(y - py) > 60 for px, py in posiciones_animales):
                posiciones_animales.append((x, y))
                animales.add(Animal(x, y))
                break

    zona_segura = pygame.Rect(ANCHO-140, ALTO-100, 120, 80)
    entregados = 0
    inicio = time.time()
    tiempo_restante = TIEMPO_LIMITE

crear_nivel()

# ======== FUNCIONES MEJORADAS ========
def dibujar_fondo():
    screen.blit(fondo, (0, 0))
    # Dibujar zona segura con efecto visual
    pygame.draw.rect(screen, VERDE, zona_segura, 0, 10)  # Relleno
    pygame.draw.rect(screen, BLANCO, zona_segura, 4, 10)  # Borde
    
    # Añadir texto a la zona segura
    font = pygame.font.SysFont(None, 24)
    texto = font.render("ZONA SEGURA", True, BLANCO)
    texto_rect = texto.get_rect(center=zona_segura.center)
    screen.blit(texto, texto_rect)

def dibujar_hud(tiempo_restante):
    font = pygame.font.SysFont(None, 28)
    
    # Fondo semitransparente para el HUD
    hud_rect = pygame.Rect(5, 5, 200, 110)
    s = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))  # Negro semitransparente
    screen.blit(s, hud_rect)
    
    # Textos del HUD
    textos = [
        f"Vidas: {buzo.vidas}",
        f"Animales: {entregados}/5",
        f"Puntaje: {buzo.puntaje}",
        f"Tiempo: {tiempo_restante}s"
    ]
    
    for i, texto in enumerate(textos):
        color = AMARILLO if i == 3 and tiempo_restante < 10 else BLANCO
        text_surf = font.render(texto, True, color)
        screen.blit(text_surf, (15, 15 + i * 25))
    
    # Indicador de si lleva animal
    if buzo.lleva:
        indicador = font.render("🐢 LLEVANDO ANIMAL", True, AMARILLO)
        screen.blit(indicador, (ANCHO - 200, 15))

def mostrar_mensaje(mensaje, subtitulo, color=BLANCO):
    """Muestra un mensaje en pantalla de forma no bloqueante"""
    font_titulo = pygame.font.SysFont(None, 64)
    font_sub = pygame.font.SysFont(None, 36)
    
    # Fondo semitransparente
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Renderizar textos
    texto_titulo = font_titulo.render(mensaje, True, color)
    texto_sub = font_sub.render(subtitulo, True, BLANCO)
    
    # Centrar textos
    screen.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, ALTO//2 - 50))
    screen.blit(texto_sub, (ANCHO//2 - texto_sub.get_width()//2, ALTO//2 + 20))
    
    pygame.display.flip()
    
    # Espera con posibilidad de salir
    inicio_espera = time.time()
    while time.time() - inicio_espera < 2.5:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
        clock.tick(30)

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
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:  # Continuar
                        pausa_activa = False
                    elif seleccion == 1:  # Reiniciar
                        crear_nivel()
                        pausa_activa = False
                    elif seleccion == 2:  # Salir
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_ESCAPE:
                    pausa_activa = False

        # Dibujar overlay de pausa
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Título
        titulo = font.render("PAUSA", True, BLANCO)
        screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//3))
        
        # Opciones
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            texto = font.render(opcion, True, color)
            screen.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 + i * 60))
        
        pygame.display.flip()
        clock.tick(30)

# ======== BUCLE PRINCIPAL MEJORADO ========
ejecutando = True
while ejecutando:
    # Calcular tiempo restante
    tiempo_transcurrido = time.time() - inicio
    tiempo_restante = max(0, TIEMPO_LIMITE - int(tiempo_transcurrido))
    
    # Verificar si se acabó el tiempo
    if tiempo_restante <= 0 and entregados < 5:
        mostrar_mensaje("⏰ TIEMPO AGOTADO", f"Rescates: {entregados}/5", ROJO)
        crear_nivel()
        continue

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP: buzo.move(0, -1)
            if evento.key == pygame.K_DOWN: buzo.move(0, 1)
            if evento.key == pygame.K_LEFT: buzo.move(-1, 0)
            if evento.key == pygame.K_RIGHT: buzo.move(1, 0)
            if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE: 
                menu_pausa()

    # Actualizaciones
    barcos.update()
    buzo.update()

    # Colisiones con barcos (con invulnerabilidad)
    if not buzo.invulnerable and pygame.sprite.spritecollideany(buzo, barcos):
        buzo.vidas -= 1
        buzo.hacer_invulnerable(60)  # 1 segundo de invulnerabilidad
        buzo.puntaje = max(0, buzo.puntaje - 100)
        
        if buzo.vidas <= 0:
            mostrar_mensaje("GAME OVER ☠️", f"Puntaje: {buzo.puntaje}", ROJO)
            crear_nivel()
        else:
            # Respawn seguro
            buzo.rect.center = (ANCHO//2, 48)
            buzo.lleva = False

    # Rescate de animales
    if not buzo.lleva:
        animal_colisionado = pygame.sprite.spritecollideany(buzo, animales)
        if animal_colisionado:
            buzo.lleva = True
            animales.remove(animal_colisionado)
            buzo.puntaje += 100

    # Entrega en zona segura
    if buzo.lleva and buzo.rect.colliderect(zona_segura):
        buzo.lleva = False
        buzo.puntaje += 200
        entregados += 1
        
        # Feedback visual y de sonido podría ir aquí
        if entregados < 5:
            buzo.rect.center = (ANCHO//2, 48)  # Volver al inicio

    # Victoria
    if entregados >= 5:
        mostrar_mensaje("¡RESCATE COMPLETO! 🌊🐢", f"Puntaje: {buzo.puntaje}", VERDE)
        crear_nivel()

    # Dibujado
    dibujar_fondo()
    animales.draw(screen)
    barcos.draw(screen)
    buzo_g.draw(screen)
    
    # Mostrar animal si el buzo lo lleva
    if buzo.lleva:
        animal_pos = (buzo.rect.centerx - 20, buzo.rect.top - 25)
        screen.blit(img_animal, animal_pos)
    
    dibujar_hud(tiempo_restante)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()