import pygame, sys, os, random, time
pygame.init()
pygame.display.set_caption("Nivel 3 — Buzo Rescatista")

# ======== CONFIGURACION ========
ANCHO, ALTO = 832, 640
FPS = 60
TILE = 64
TIEMPO_LIMITE = 90

# MODO VENTANA
screen = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
clock = pygame.time.Clock()

# ======== SONIDO ========
try:
    pygame.mixer.init()
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
NARANJA = (255, 150, 50)
MORADO = (180, 70, 200)
MARRON = (150, 100, 50)

# ======== CARGA DE IMAGENES ========
def cargar_imagen(nombre, ancho=TILE, alto=TILE, color_default=(150, 150, 150)):
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
    
    print(f"Imagen no encontrada: {nombre}")
    surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    surf.fill(color_default)
    font = pygame.font.SysFont(None, 16)
    texto = font.render(nombre.split('.')[0], True, BLANCO)
    texto_rect = texto.get_rect(center=(ancho//2, alto//2))
    surf.blit(texto, texto_rect)
    return surf

# ======== FONDO ========
def cargar_fondo():
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
    
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(AZUL_AGUA)
    for i in range(20):
        y = random.randint(0, ALTO)
        pygame.draw.line(fondo, (40, 150, 220), (0, y), (ANCHO, y), 1)
    return fondo

fondo = cargar_fondo()

# ======== CARGAR IMAGENES DE ANIMALES Y CUEVA ========
img_buzo = cargar_imagen("buzo_abajo.png", TILE, TILE, (50, 150, 255))
img_barco = cargar_imagen("barco.png", 120, 60, (100, 100, 100))

# Cargar imagenes de todos los animales
img_tortuga = cargar_imagen("tortuga atrapada.png", 45, 35, (100, 200, 100))
img_delfin = cargar_imagen("delfin atrapado.png", 50, 30, (150, 200, 255))
img_pez = cargar_imagen("pescado atrapado.png", 40, 25, (255, 200, 50))
img_manati = cargar_imagen("manati.png", 55, 30, (150, 150, 200))
img_cangrejo = cargar_imagen("cancrejo.png", 35, 30, (220, 100, 80))
img_cueva = cargar_imagen("cueva.jpeg", 160, 120, (100, 80, 60))

animales_data = [
    {"imagen": img_tortuga, "nombre": "Tortuga", "puntos": 100, "color": (100, 200, 100)},
    {"imagen": img_delfin, "nombre": "Delfin", "puntos": 150, "color": (150, 200, 255)},
    {"imagen": img_pez, "nombre": "Pez", "puntos": 80, "color": (255, 200, 50)},
    {"imagen": img_manati, "nombre": "Manati", "puntos": 120, "color": (150, 150, 200)},
    {"imagen": img_cangrejo, "nombre": "Cancrejo", "puntos": 70, "color": (220, 100, 80)}
]

# ======== CLASES ========
class Buzo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_buzo
        self.rect = self.image.get_rect(center=(ANCHO//2, 48))
        
        # HITBOX MÁS PEQUEÑO
        self.hitbox = pygame.Rect(0, 0, TILE * 0.7, TILE * 0.7)
        self.hitbox.center = self.rect.center
        
        self.vidas = 5
        self.lleva_animal = None
        self.puntaje = 0
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.animales_rescatados = {animal["nombre"]: 0 for animal in animales_data}
        self.total_rescatados = 0
        
    def move(self, dx, dy):
        step = TILE // 2
        new_x = self.rect.x + dx * step
        new_y = self.rect.y + dy * step
        
        # Limitar movimiento dentro de la pantalla
        new_x = max(0, min(new_x, ANCHO - self.rect.width))
        new_y = max(0, min(new_y, ALTO - self.rect.height))
        
        self.rect.x = new_x
        self.rect.y = new_y
        # Actualizar hitbox con el movimiento
        self.hitbox.center = self.rect.center
        
    def update(self):
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
        
        # HITBOX MAS PEQUEÑO para barcos
        self.hitbox = pygame.Rect(0, 0, 120 * 0.6, 60 * 0.6)
        self.hitbox.center = self.rect.center
        
        self.vel = vel
        
    def update(self):
        self.rect.x += self.vel
        if self.rect.right < -50: 
            self.rect.left = ANCHO + 50
        elif self.rect.left > ANCHO + 50: 
            self.rect.right = -50
        
        self.hitbox.center = self.rect.center

class Animal(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo_animal):
        super().__init__()
        self.tipo = tipo_animal
        self.image = tipo_animal["imagen"]
        self.nombre = tipo_animal["nombre"]
        self.puntos = tipo_animal["puntos"]
        self.color = tipo_animal["color"]
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Hitbox para animales - tamaño segun el animal
        if self.nombre == "Manatí":
            self.hitbox = pygame.Rect(0, 0, 55 * 0.8, 30 * 0.8)
        elif self.nombre == "Delfín":
            self.hitbox = pygame.Rect(0, 0, 50 * 0.8, 30 * 0.8)
        elif self.nombre == "Tortuga":
            self.hitbox = pygame.Rect(0, 0, 45 * 0.8, 35 * 0.8)
        else:
            self.hitbox = pygame.Rect(0, 0, 40 * 0.8, 30 * 0.8)
            
        self.hitbox.center = self.rect.center

class Cueva(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_cueva
        self.rect = self.image.get_rect(midbottom=(x, y))
        
        # Hitbox para la entrada de la cueva
        self.hitbox = pygame.Rect(0, 0, 100, 60)
        self.hitbox.midbottom = (self.rect.centerx, self.rect.bottom - 10)

# ======== VARIABLES GLOBALES ========
buzo = None
buzo_g = None
barcos = None
animales = None
cueva = None
animales_requeridos = 8
inicio = 0
tiempo_restante = TIEMPO_LIMITE

# ======== CREAR NIVEL ========
def crear_nivel():
    global buzo, buzo_g, barcos, animales, cueva, inicio, tiempo_restante
    
    # Reiniciar grupos de sprites
    if buzo_g:
        buzo_g.empty()
    if barcos:
        barcos.empty()
    if animales:
        animales.empty()
    
    buzo = Buzo()
    buzo_g = pygame.sprite.Group(buzo)
    barcos = pygame.sprite.Group()
    animales = pygame.sprite.Group()

    alturas_barcos = [260, 320, 380]
    for y in alturas_barcos:
        for _ in range(2):
            x = random.randint(0, ANCHO)
            vel = random.choice([-3, 3])
            barcos.add(Barco(x, y, vel))

    # Crear animales de diferentes tipos
    posiciones_animales = []
    
    for _ in range(animales_requeridos):
        while True:
            x = random.randint(100, ANCHO-100)
            y = random.randint(ALTO-180, ALTO-60)
            
            if all(abs(x - px) > 70 or abs(y - py) > 70 for px, py in posiciones_animales):
                posiciones_animales.append((x, y))
                
                # Elegir un tipo de animal aleatorio
                tipo_animal = random.choice(animales_data)
                animales.add(Animal(x, y, tipo_animal))
                break

    cueva = Cueva(ANCHO - 120, ALTO - 30)

    inicio = time.time()
    tiempo_restante = TIEMPO_LIMITE

crear_nivel()

# ======== FUNCIONES DE DIBUJO ========
def dibujar_fondo():
    screen.blit(fondo, (0, 0))
    # Dibujar la cueva sin efectos adicionales
    screen.blit(cueva.image, cueva.rect)

def dibujar_hud(tiempo_restante):
    font = pygame.font.SysFont(None, 24)
    
    # Fondo semitransparente para el HUD
    hud_rect = pygame.Rect(5, 5, 220, 160)
    s = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 160))
    screen.blit(s, hud_rect)
    
    textos = [
        f"Vidas: {buzo.vidas}",
        f"Rescatados: {buzo.total_rescatados}/{animales_requeridos}",
        f"Puntaje: {buzo.puntaje}",
        f"Tiempo: {tiempo_restante}s"
    ]
    
    for i, texto in enumerate(textos):
        color = AMARILLO if i == 3 and tiempo_restante < 15 else BLANCO
        text_surf = font.render(texto, True, color)
        screen.blit(text_surf, (15, 15 + i * 25))
    
    # Indicador de animal que lleva
    if buzo.lleva_animal:
        animal = buzo.lleva_animal
        indicador = font.render(f"Llevando: {animal['nombre']} (+{animal['puntos']})", True, AMARILLO)
        screen.blit(indicador, (ANCHO - 250, 15))
    
    # Contador de animales rescatados por tipo (en la parte inferior)
    y_pos = ALTO - 120
    for i, (nombre, cantidad) in enumerate(buzo.animales_rescatados.items()):
        if cantidad > 0:
            color = next((a["color"] for a in animales_data if a["nombre"] == nombre), BLANCO)
            texto_animal = font.render(f"{nombre}: {cantidad}", True, color)
            screen.blit(texto_animal, (ANCHO - 150, y_pos + i * 20))

# ======== DETECCIÓN DE COLISIONES ========
def verificar_colision_barcos():
    for barco in barcos:
        if buzo.hitbox.colliderect(barco.hitbox):
            return True
    return False

def verificar_colision_animales():
    for animal in animales:
        if buzo.hitbox.colliderect(animal.hitbox):
            return animal
    return None

def verificar_colision_cueva():
    return buzo.hitbox.colliderect(cueva.hitbox)

def mostrar_mensaje(mensaje, subtitulo, color=BLANCO):
    font_titulo = pygame.font.SysFont(None, 64)
    font_sub = pygame.font.SysFont(None, 36)
    
    pantalla_actual = screen.copy()
    
    # Dibujar overlay
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    texto_titulo = font_titulo.render(mensaje, True, color)
    texto_sub = font_sub.render(subtitulo, True, BLANCO)
    
    screen.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, ALTO//2 - 50))
    screen.blit(texto_sub, (ANCHO//2 - texto_sub.get_width()//2, ALTO//2 + 20))
    
    pygame.display.flip()
    
    inicio_espera = time.time()
    esperando = True
    
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    esperando = False
        
        if time.time() - inicio_espera > 3:
            esperando = False
            
        clock.tick(30)
    
    # Restaurar la pantalla anterior
    screen.blit(pantalla_actual, (0, 0))
    pygame.display.flip()

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
                    if seleccion == 0:
                        pausa_activa = False
                    elif seleccion == 1:
                        crear_nivel()
                        pausa_activa = False
                    elif seleccion == 2:
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_ESCAPE:
                    pausa_activa = False

        # Dibujar overlay de pausa
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        titulo = font.render("PAUSA", True, BLANCO)
        screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//3))
        
        # Opciones
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            texto = font.render(opcion, True, color)
            screen.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 + i * 60))
        
        pygame.display.flip()
        clock.tick(30)

# ======== BUCLE PRINCIPAL CORREGIDO ========
ejecutando = True
game_over = False
victoria = False

while ejecutando:

    tiempo_transcurrido = time.time() - inicio
    tiempo_restante = max(0, TIEMPO_LIMITE - int(tiempo_transcurrido))
    
    # Verificar fin del tiempo
    if tiempo_restante <= 0 and buzo.total_rescatados < animales_requeridos and not game_over:
        mostrar_mensaje("TIEMPO AGOTADO", 
                       f"Rescataste: {buzo.total_rescatados}/{animales_requeridos} animales", 
                       ROJO)
        crear_nivel()
        continue

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

    barcos.update()
    buzo.update()

    # COLISIONES CON BARCOS
    if not buzo.invulnerable and verificar_colision_barcos():
        buzo.vidas -= 1
        buzo.hacer_invulnerable(60)
        buzo.puntaje = max(0, buzo.puntaje - 100)
        
        if buzo.vidas <= 0:
            mostrar_mensaje("Vuelve a intentarlo", 
                           f"Rescataste {buzo.total_rescatados} animales", ROJO)
            crear_nivel()
        else:
            buzo.rect.center = (ANCHO//2, 48)
            buzo.hitbox.center = buzo.rect.center
            buzo.lleva_animal = None

    if not buzo.lleva_animal:
        animal_colisionado = verificar_colision_animales()
        if animal_colisionado:
            # Crear un diccionario con la información del animal
            animal_info = {
                "imagen": animal_colisionado.image,
                "nombre": animal_colisionado.nombre,
                "puntos": animal_colisionado.puntos,
                "color": animal_colisionado.color
            }
            buzo.lleva_animal = animal_info
            animales.remove(animal_colisionado)
            buzo.puntaje += animal_colisionado.puntos // 2

    # ENTREGA EN LA CUEVA - CORREGIDO
    if buzo.lleva_animal and verificar_colision_cueva():
        animal = buzo.lleva_animal
        buzo.puntaje += animal["puntos"]  # Mitad restante al entregar
        buzo.animales_rescatados[animal["nombre"]] += 1
        buzo.total_rescatados += 1
        buzo.lleva_animal = None
        
        if buzo.total_rescatados < animales_requeridos:
            buzo.rect.center = (ANCHO//2, 48)
            buzo.hitbox.center = buzo.rect.center
        else:
            resumen = ", ".join([f"{cant} {nombre}" for nombre, cant in buzo.animales_rescatados.items() if cant > 0])
            mostrar_mensaje("¡MISIÓN CUMPLIDA! 🌊", 
                           f"Rescataste: {resumen}", 
                           VERDE)
            crear_nivel()

    # DIBUJADO
    dibujar_fondo()
    animales.draw(screen)
    barcos.draw(screen)
    buzo_g.draw(screen)
    
    if buzo.lleva_animal:
        animal_pos = (buzo.rect.centerx - buzo.lleva_animal["imagen"].get_width()//2, 
                     buzo.rect.top - buzo.lleva_animal["imagen"].get_height())
        screen.blit(buzo.lleva_animal["imagen"], animal_pos)
    
    dibujar_hud(tiempo_restante)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()