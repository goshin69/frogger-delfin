import pygame
import os
<<<<<<< Updated upstream
=======
import json
import os
>>>>>>> Stashed changes
import sys
import subprocess

ANCHO, ALTO = 1366, 768
FPS = 60
pygame.init()
<<<<<<< Updated upstream
=======
def cargar_volumen():
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'volumen.json'), 'r') as f:
            data = json.load(f)
            return float(data.get('volumen', 0.5))
    except Exception:
        return 0.5
pygame.mixer.init()
pygame.mixer.music.set_volume(cargar_volumen())
>>>>>>> Stashed changes
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dolpher")
font = pygame.font.Font("freesansbold.ttf", 30)

<<<<<<< Updated upstream
Ruta_Imagen_Fondo = os.path.join(os.path.dirname(__file__), "..", "Imgs", "MenuFondogrande.png")
background_image = None
try:
    _img = pygame.image.load(Ruta_Imagen_Fondo).convert_alpha()
<<<<<<< Updated upstream:Main Menu/mainmenu.py
    background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))    
except Exception as e:
    # No detener la ejecución si no se encuentra la imagen; se usará un color de fondo
    print(f"No se pudo cargar la imagen de fondo '{Ruta_Imagen_Fondo}': {e}")
=======
    background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))
except Exception:
    pass
>>>>>>> Stashed changes:MainGame/mainmenu.py


class Button:
    def __init__(self, txt, pos, image_path=None, hover_image_path=None):
        self.txt = txt
        self.pos = pos
        self.size = (500, 39)
=======

# --- Selección de idioma para fondo ---
IDIOMA_FILE = os.path.join(os.path.dirname(__file__), '..', 'idioma.json')
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
if idioma_actual == 'en':
    fondo_file = "MenuFondoIngles.png"
else:
    fondo_file = "MenuFondogrande.png"
Ruta_Imagen_Fondo = os.path.join(os.path.dirname(__file__), "..", "Imgs", fondo_file)
background_image = None
try:
    _img = pygame.image.load(Ruta_Imagen_Fondo).convert_alpha()
    background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))
except Exception:
    pass


class Button:
    def __init__(self, txt, pos, image_path=None, hover_image_path=None, size=None):
        self.txt = txt
        self.pos = pos
        if size is not None:
            self.size = size
        else:
            self.size = (500, 39)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
            # centrar la imagen hover sobre el área del botón
            img_rect = self.hover_image.get_rect()
            img_rect.center = self.button.center
            screen.blit(self.hover_image, img_rect.topleft)
            return
        if self.image:
            # dibujar la imagen del botón centrada sobre el área del botón (sin escalar)
            img_rect = self.image.get_rect()
            img_rect.center = self.button.center
            screen.blit(self.image, img_rect.topleft)
<<<<<<< Updated upstream:Main Menu/mainmenu.py
        else:
            # No dibujar imágenes de botones (el fondo ya contiene los botones).
            # Solo mostrar un sutil overlay y borde cuando se hace hover para dar feedback.
            if hovered:
                # overlay semitransparente
                overlay = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 40))  # blanco muy translúcido
                screen.blit(overlay, (self.pos[0], self.pos[1]))
                # borde de destaque
                pygame.draw.rect(screen, (255, 215, 0), self.button, 3, 5)
=======
        elif hovered:
            overlay = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 40))
            screen.blit(overlay, (self.pos[0], self.pos[1]))
            pygame.draw.rect(screen, (255, 215, 0), self.button, 3, 5)
>>>>>>> Stashed changes:MainGame/mainmenu.py
    def is_clicked(self, event):
        """Detecta si el botón fue pulsado usando un evento MOUSEBUTTONDOWN."""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button.collidepoint(event.pos)



def draw_menu():
    # No cargar PNGs para los botones; el fondo ya tiene los gráficos.
    # Crear hitboxes en las posiciones definidas y usar feedback de hover.
    btn1 = Button('JUGAR', (435, 365))
    btn2 = Button('NIVELES', (435, 428))
    btn3 = Button('OPCIONES', (435, 491))
    btn4 = Button('FELICIDAD', (580, 620))
    btn5 = Button('SALIR', (435, 553))

    btn1.draw()
    btn2.draw()
    btn3.draw()
    btn4.draw()
    btn5.draw()
=======
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

def draw_menu():
    SIZE_BTN_CREDITOS = (60, 50)

    btn1 = Button('JUGAR', (435, 365))
    btn2 = Button('NIVELES', (435, 428))
    btn3 = Button('OPCIONES', (435, 491))
    btn4 = Button('CRÉDITOS', (865, 615), size=SIZE_BTN_CREDITOS)
    btn5 = Button('SALIR', (435, 553))

    for btn in [btn1, btn2, btn3, btn4, btn5]:
        btn.draw()
>>>>>>> Stashed changes

    return [btn1, btn2, btn3, btn4, btn5]

run = True
game_proc = None
clock = pygame.time.Clock()
while run:
<<<<<<< Updated upstream
    # Dibujar fondo: imagen si está disponible, si no usar color
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream:Main Menu/mainmenu.py
            # comprobar cada botón
            if buttons:
                if buttons[0].is_clicked(event):
                    # Lanzar el juego principal en un proceso separado y mantener el menú abierto
                    try:
                        if game_proc is None or game_proc.poll() is not None:
                            dolpher_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "dolpher.py")
                            dolpher_path = os.path.abspath(dolpher_path)
                            dolpher_cwd = os.path.dirname(dolpher_path)
                            game_proc = subprocess.Popen([sys.executable, dolpher_path], cwd=dolpher_cwd)
                        else:
                            print("El juego se está ejecutando.")
                    except Exception as e:
                        print(f"No se pudo lanzar dolpher.py: {e}")
                elif buttons[1].is_clicked(event):
                    command = 2
                elif buttons[2].is_clicked(event):
                    command = 3
                elif buttons[3].is_clicked(event):
                    command = 4
                elif buttons[4].is_clicked(event):
                    command = 5
        if command == 5: # Salir
            run = False
=======
=======
>>>>>>> Stashed changes
            if buttons[0].is_clicked(event):
                try:
                    if game_proc is None or game_proc.poll() is not None:
                        dolpher_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "dolpher.py")
                        dolpher_path = os.path.abspath(dolpher_path)
                        dolpher_cwd = os.path.dirname(dolpher_path)
                        game_proc = subprocess.Popen([sys.executable, dolpher_path], cwd=dolpher_cwd)
                except Exception:
                    pass
            elif buttons[1].is_clicked(event):
                try:
<<<<<<< Updated upstream
                    niveles_path = os.path.join(os.path.dirname(__file__), "Niveles.py")
=======
                    niveles_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "Niveles.py")
>>>>>>> Stashed changes
                    niveles_path = os.path.abspath(niveles_path)
                    pygame.quit()
                    subprocess.run([sys.executable, niveles_path])
                    run = False
<<<<<<< Updated upstream
                    sys.exit()
                except Exception:
                    pass
            elif buttons[2].is_clicked(event):
                pass
=======
                except Exception:
                    pass
            elif buttons[2].is_clicked(event):
                try:
                    config_path = os.path.join(os.path.dirname(__file__), "..", "Config.py")
                    config_path = os.path.abspath(config_path)
                    pygame.quit()
                    subprocess.run([sys.executable, config_path])
                    run = False
                except Exception:
                    pass
>>>>>>> Stashed changes
            elif buttons[3].is_clicked(event):
                pass
            elif buttons[4].is_clicked(event):
                run = False
<<<<<<< Updated upstream
>>>>>>> Stashed changes:MainGame/mainmenu.py

    pygame.display.flip()
pygame.quit()

=======

    pygame.display.flip()
pygame.quit()
>>>>>>> Stashed changes
