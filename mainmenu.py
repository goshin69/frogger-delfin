import pygame
import os
import sys
import subprocess

ANCHO, ALTO = 1366, 768
FPS = 60
pygame.init()
command = 0
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dolpher")
font = pygame.font.Font("freesansbold.ttf", 30)

# ======== FUNCION PARA ENCONTRAR ARCHIVOS ========
def get_file_path(filename):
    """Busca el archivo en diferentes ubicaciones posibles"""
    # Obtener el directorio actual del script (Main Menu)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Subir tres niveles: Main Menu -> frogger-delfin-Menu-principal -> prueba (workspace)
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    
    # Posibles ubicaciones donde podrían estar los archivos
    possible_paths = [
        # En workspace root
        os.path.join(workspace_root, filename),
        # En la carpeta delfin-version-frogge3r-main
        os.path.join(workspace_root, "delfin-version-frogge3r-main", filename),
        # En el directorio actual del script
        os.path.join(script_dir, filename),
        # Alternativa con nombre similar
        os.path.join(workspace_root, "delfin-version-frogger-main", filename),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

try:
    pygame.mixer.init()
    musica_path = get_file_path("Fountains Of Wayne, Too Cool For School (With Lyrics).mp3")
    if musica_path:
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
        print(f"Música cargada: {musica_path}")
    else:
        print("No se encontró el archivo de música")
        
except Exception as e:
    print(f"No se pudo cargar la musica: {e}")

Ruta_Imagen_Fondo = os.path.join(os.path.dirname(__file__), "..", "Imgs", "MenuFondogrande.png")
background_image = None
try:
    _img = pygame.image.load(Ruta_Imagen_Fondo).convert_alpha()
    background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))
except Exception:
    pass


class Button:
    def __init__(self, txt, pos, image_path=None, hover_image_path=None):
        self.txt = txt
        self.pos = pos
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
        elif hovered:
            overlay = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 40))
            screen.blit(overlay, (self.pos[0], self.pos[1]))
            pygame.draw.rect(screen, (255, 215, 0), self.button, 3, 5)
    def is_clicked(self, event):
        """Detecta si el botón fue pulsado usando un evento MOUSEBUTTONDOWN."""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button.collidepoint(event.pos)



def draw_menu():
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

    return [btn1, btn2, btn3, btn4, btn5]

run = True
game_proc = None
clock = pygame.time.Clock()
while run:
    # Dibujar fondo: imagen si está disponible, si no usar color
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
            # comprobar cada botón
            if buttons:
                if buttons[0].is_clicked(event):
                    # Lanzar el juego principal en un proceso separado y mantener el menú abierto
                    try:
                        if game_proc is None or game_proc.poll() is not None:
                            dolpher_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "ballena.py")
                            dolpher_path = os.path.abspath(dolpher_path)
                            dolpher_cwd = os.path.dirname(dolpher_path)
                            game_proc = subprocess.Popen([sys.executable, dolpher_path], cwd=dolpher_cwd)
                        else:
                            print("El juego se está ejecutando.")
                    except Exception as e:
                        print(f"No se pudo lanzar ballena.py: {e}")
                elif buttons[1].is_clicked(event):
                    # Lanzar el módulo de niveles en un proceso separado
                    try:
                        if game_proc is None or game_proc.poll() is not None:
                            niveles_path = os.path.join(os.path.dirname(__file__), "..", "MainGame", "Niveles.py")
                            niveles_path = os.path.abspath(niveles_path)
                            niveles_cwd = os.path.dirname(niveles_path)
                            game_proc = subprocess.Popen([sys.executable, niveles_path], cwd=niveles_cwd)
                        else:
                            print("Ya hay un proceso del juego en ejecución.")
                    except Exception as e:
                        print(f"No se pudo lanzar Niveles.py: {e}")
                elif buttons[2].is_clicked(event):
                    command = 3
                elif buttons[3].is_clicked(event):
                    command = 4
                elif buttons[4].is_clicked(event):
                    command = 5
        if command == 5: # Salir
            run = False

    pygame.display.flip()
pygame.quit()

