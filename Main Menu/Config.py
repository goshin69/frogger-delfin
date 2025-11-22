
import os
import pygame
import sys
import json

ANCHO, ALTO = 800, 600
VOLUMEN_FILE = os.path.join(os.path.dirname(__file__), 'volumen.json')

pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Configuración del Juego")
clock = pygame.time.Clock()

def get_file_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(os.path.dirname(script_dir))
    possible_paths = [
        os.path.join(workspace_root, filename),
        os.path.join(script_dir, filename),
        os.path.join(workspace_root, "Imgs", filename),
        os.path.join(script_dir, "Imgs", filename),
        os.path.join(workspace_root, "Main Menu", "Imgs", filename),
        os.path.join(script_dir, "Main Menu", "Imgs", filename),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

# --- Volumen global ---
def cargar_volumen():
    if os.path.exists(VOLUMEN_FILE):
        try:
            with open(VOLUMEN_FILE, 'r') as f:
                data = json.load(f)
                return float(data.get('volumen', 0.5))
        except Exception:
            return 0.5
    return 0.5

def guardar_volumen(vol):
    with open(VOLUMEN_FILE, 'w') as f:
        json.dump({'volumen': vol}, f)

volumen = cargar_volumen()
pygame.mixer.init()
pygame.mixer.music.set_volume(volumen)

# --- Botones ---

import subprocess

class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse)
        # Fondo transparente (no se dibuja nada si no hay hover)
        if is_hover:
            # Dibujar fondo semitransparente al hacer hover
            hover_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            hover_surf.fill((70, 130, 180, 120))  # RGBA, alpha=120
            surface.blit(hover_surf, self.rect.topleft)
        # Texto siempre visible
        txt = self.font.render(self.text, True, (255,255,255))
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# --- Acciones de volumen ---
def subir_volumen():
    global volumen
    volumen = min(1.0, volumen + 0.1)
    pygame.mixer.music.set_volume(volumen)
    guardar_volumen(volumen)

def bajar_volumen():
    global volumen
    volumen = max(0.0, volumen - 0.1)
    pygame.mixer.music.set_volume(volumen)
    guardar_volumen(volumen)

def apagar_volumen():
    global volumen
    volumen = 0.0
    pygame.mixer.music.set_volume(volumen)
    guardar_volumen(volumen)

# --- Cargar fondo ---
ruta_fondo = get_file_path("MenuConfig.png")
if ruta_fondo:
    fondo = pygame.image.load(ruta_fondo).convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
else:
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((50, 50, 100))


# --- Posiciones de los botones (modificables) ---
POS_BTN_SUBIR = (150, 110)
POS_BTN_BAJAR = (335, 110)
POS_BTN_APAGAR = (520, 110)
BTN_WIDTH = 135
BTN_HEIGHT = 90



# --- Idioma ---
IDIOMA_FILE = os.path.join(os.path.dirname(__file__), 'idioma.json')
def guardar_idioma(idioma):
    with open(IDIOMA_FILE, 'w') as f:
        json.dump({'idioma': idioma}, f)
def cargar_idioma():
    if os.path.exists(IDIOMA_FILE):
        try:
            with open(IDIOMA_FILE, 'r') as f:
                data = json.load(f)
                return data.get('idioma', 'es')
        except Exception:
            return 'es'
    return 'es'

idioma_actual = cargar_idioma()

def set_espanol():
    global idioma_actual
    idioma_actual = 'es'
    guardar_idioma('es')

def set_ingles():
    global idioma_actual
    idioma_actual = 'en'
    guardar_idioma('en')

# --- Posiciones y tamaños de los botones de idioma (modificables) ---
POS_BTN_ES = (140, 330)
POS_BTN_EN = (418, 330)
BTN_IDIOMA_W = 255
BTN_IDIOMA_H = 150
POS_TEXTO_IDIOMA = (ANCHO//2, POS_BTN_ES[1] + BTN_IDIOMA_H + 10)  # (x_centro, debajo de los botones)

btn_es = Button("Español", POS_BTN_ES[0], POS_BTN_ES[1], BTN_IDIOMA_W, BTN_IDIOMA_H, set_espanol)
btn_en = Button("Inglés", POS_BTN_EN[0], POS_BTN_EN[1], BTN_IDIOMA_W, BTN_IDIOMA_H, set_ingles)

btn_subir = Button(" ", POS_BTN_SUBIR[0], POS_BTN_SUBIR[1], BTN_WIDTH, BTN_HEIGHT, subir_volumen)
btn_bajar = Button(" ", POS_BTN_BAJAR[0], POS_BTN_BAJAR[1], BTN_WIDTH, BTN_HEIGHT, bajar_volumen)
btn_apagar = Button(" ", POS_BTN_APAGAR[0], POS_BTN_APAGAR[1], BTN_WIDTH, BTN_HEIGHT, apagar_volumen)

# Botón Atrás
def volver_menu():
    mainmenu_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Main Menu', 'mainmenu.py'))
    if os.path.exists(mainmenu_path):
        # Usar subprocess.Popen en todos los sistemas para evitar cierre inmediato
        subprocess.Popen([sys.executable, mainmenu_path], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    global running
    running = False

BTN_ATRAS_X = 55
BTN_ATRAS_Y = ALTO - 55
BTN_ATRAS_W = 275
BTN_ATRAS_H = 30
btn_atras = Button("", BTN_ATRAS_X, BTN_ATRAS_Y, BTN_ATRAS_W, BTN_ATRAS_H, volver_menu)

botones = [btn_subir, btn_bajar, btn_apagar, btn_es, btn_en, btn_atras]

# --- Bucle principal ---
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        for btn in botones:
            btn.handle_event(event)
        # Si running se puso en False por el botón Atrás, salir del bucle inmediatamente
        if not running:
            break

    if not running:
        break


    screen.blit(fondo, (0, 0))

    # Dibujar botones
    for btn in botones:
        btn.draw(screen)


    # Mostrar valor de volumen
    font = pygame.font.SysFont(None, 40)
    txt = font.render(f"Volumen: {int(volumen*100)}%", True, (255,255,255))
    screen.blit(txt, (ANCHO//2 - txt.get_width()//2, 220))

    # Mostrar idioma actual
    font_idioma = pygame.font.SysFont(None, 32)
    idioma_txt = "Idioma actual: Español" if idioma_actual == 'es' else "Idioma actual: Inglés"

    idioma_surf = font_idioma.render(idioma_txt, True, (255,255,255))
    screen.blit(idioma_surf, (POS_TEXTO_IDIOMA[0] - idioma_surf.get_width()//2, POS_TEXTO_IDIOMA[1]))

    pygame.display.flip()
    clock.tick(60)

# Cerrar pygame y salir solo al final del script
pygame.quit()
sys.exit()
