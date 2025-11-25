
import pygame
import os
import sys
import subprocess
import argparse

ANCHO, ALTO = 1366, 768
FPS = 60
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dolpher")
font = pygame.font.Font("freesansbold.ttf", 30)




# --- Argumentos de línea de comandos para idioma ---

def obtener_idioma():
    parser = argparse.ArgumentParser()
    parser.add_argument('--idioma', default='es', choices=['es', 'en'])
    args, _ = parser.parse_known_args()
    return args.idioma

global idioma_actual
idioma_actual = obtener_idioma()

def cargar_fondo_idioma():
    if idioma_actual == 'en':
        fondo_file = "MenuFondoIngles.png"
    else:
        fondo_file = "MenuFondogrande.png"
    ruta = os.path.join(os.path.dirname(__file__), "..", "Imgs", fondo_file)
    try:
        _img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.smoothscale(_img, (ANCHO, ALTO))
    except Exception:
        return None

background_image = cargar_fondo_idioma()

class Button:
    def __init__(self, txt, pos, image_path=None, hover_image_path=None, size=None):
        self.txt = txt
        self.pos = pos
        if size is not None:
            self.size = size
        else:
            self.size = (500, 39)
        self.button = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.image = None
        self.hover_image = None
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
            except Exception:
                pass
        if hover_image_path:
            try:
                self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
            except Exception:
                pass


    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.button.collidepoint(mouse_pos)
        if hovered and self.hover_image:
            img_rect = self.hover_image.get_rect()
            img_rect.center = self.button.center
            screen.blit(self.hover_image, img_rect.topleft)
        elif self.image:
            img_rect = self.image.get_rect()
            img_rect.center = self.button.center
            screen.blit(self.image, img_rect.topleft)
        else:
            color = (0, 0, 0, 0)
            base = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
            base.fill(color)
            screen.blit(base, (self.pos[0], self.pos[1]))
            if hovered:
                overlay = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 40))
                screen.blit(overlay, (self.pos[0], self.pos[1]))
                pygame.draw.rect(screen, (255, 215, 0), self.button, 3, 5)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button.collidepoint(event.pos)

def mostrar_intro():
    posibles = [
        os.path.join(os.path.dirname(__file__), 'Intro.jpeg'),
        os.path.join(os.path.dirname(__file__), '..', 'Imgs', 'Intro.jpeg'),
        os.path.join(os.path.dirname(__file__), '..', 'Intro.jpeg'),
    ]
    intro_path = None
    for path in posibles:
        if os.path.exists(path):
            intro_path = path
            break
    if not intro_path:
        screen.fill((0,0,0))
        font_big = pygame.font.SysFont(None, 60)
        txt = font_big.render("No se encontró Intro.jpeg", True, (255,0,0))
        screen.blit(txt, (ANCHO//2-txt.get_width()//2, ALTO//2-txt.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(1500)
        return
    img = pygame.image.load(intro_path).convert()
    img = pygame.transform.scale(img, (ANCHO, ALTO))
    screen.fill((0,0,0))
    screen.blit(img, (0, 0))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
        pygame.time.wait(10)

def draw_menu():
    SIZE_BTN_CREDITOS = (60, 50)

    btn1 = Button('JUGAR', (435, 365))
    btn2 = Button('NIVELES', (435, 428))
    btn3 = Button('OPCIONES', (435, 491))
    btn4 = Button('INTRO', (865, 615), size=SIZE_BTN_CREDITOS)
    btn5 = Button('SALIR', (435, 553))

    for btn in [btn1, btn2, btn3, btn4, btn5]:
        btn.draw()

    return [btn1, btn2, btn3, btn4, btn5]

run = True
game_proc = None
clock = pygame.time.Clock()
while run:
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill('lightblue')
    clock.tick(FPS)
    buttons = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons[0].is_clicked(event):
                try:
                    if game_proc is None or game_proc.poll() is not None:
                        dolpher_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "dolpher.py")
                        dolpher_path = os.path.abspath(dolpher_path)
                        dolpher_cwd = os.path.dirname(dolpher_path)
                        game_proc = subprocess.Popen([sys.executable, dolpher_path, '--idioma', idioma_actual], cwd=dolpher_cwd)
                except Exception:
                    pass
            elif buttons[1].is_clicked(event):
                try:
                    niveles_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "Niveles.py")
                    niveles_path = os.path.abspath(niveles_path)
                    # Pasa el idioma actual como argumento
                    pygame.quit()
                    run = False
                    subprocess.run([sys.executable, niveles_path, '--idioma', idioma_actual])
                except Exception:
                    pass
            elif buttons[2].is_clicked(event):
                try:
                    config_path = os.path.join(os.path.dirname(__file__), "Config.py")
                    config_path = os.path.abspath(config_path)
                    # Pausar la música y el menú principal mientras se abre la configuración
                    pygame.mixer.music.pause()
                    subprocess.run([sys.executable, config_path])
                    pygame.mixer.music.unpause()
                    # Recargar idioma y fondo si cambió
                    nuevo_idioma = obtener_idioma()
                    if os.path.exists(os.path.join(os.path.dirname(__file__), 'idioma.json')):
                        import json
                        with open(os.path.join(os.path.dirname(__file__), 'idioma.json'), 'r') as f:
                            data = json.load(f)
                            if 'idioma' in data and data['idioma'] != idioma_actual:
                                idioma_actual = data['idioma']
                                background_image = cargar_fondo_idioma()
                except Exception:
                    pass
            elif buttons[3].is_clicked(event):
                mostrar_intro()
            elif buttons[4].is_clicked(event):
                run = False


    if run:
        pygame.display.flip()
pygame.quit()
