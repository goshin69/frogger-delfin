import pygame
import os
import sys
import subprocess
pygame.init()


ALTO = 600
ANCHO = 800
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dolpher")
fps = 60
timer = pygame.time.Clock()
main_menu = True
font = pygame.font.Font("freesansbold.ttf", 30)
command = 0

# Cargar imagen de fondo
# Ruta relativa desde este archivo hacia la carpeta Imgs
Ruta_Imagen_Fondo = os.path.join(os.path.dirname(__file__), "..", "Imgs", "bkgrmar.png")
background_image = None
try:
    _img = pygame.image.load(Ruta_Imagen_Fondo).convert_alpha()
    background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))
except Exception as e:
    # No detener la ejecución si no se encuentra la imagen; se usará un color de fondo
    print(f"No se pudo cargar la imagen de fondo '{Ruta_Imagen_Fondo}': {e}")


class Button:
    def __init__(self, txt, pos, image_path=None):
        self.txt = txt
        self.pos = pos
        self.size = (260, 60)
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.image = None
        if image_path:
            try:
                img = pygame.image.load(image_path).convert_alpha()
                # escalar la imagen al tamaño del botón
                self.image = pygame.transform.smoothscale(img, self.size)
            except Exception as e:
                print(f"No se pudo cargar la imagen del botón '{image_path}': {e}")

    def draw(self):
        if self.image:
            # dibujar texto del botón en caso de que no cargue la imagen
            screen.blit(self.image, (self.pos[0], self.pos[1]))
        else:
            pygame.draw.rect(screen, 'light blue', self.button, 0, 5)
            pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], self.size[0], self.size[1]], 5, 5)
            text = font.render(self.txt, True, 'black')
            screen.blit(text, (self.pos[0]+15, self.pos[1]+7))
    def is_clicked(self, event):
        """Detecta si el botón fue pulsado usando un evento MOUSEBUTTONDOWN."""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button.collidepoint(event.pos)



def draw_menu():
    # rutas a las imágenes de los botones (si no existen, Button usará el texto)
    base_imgs = os.path.join(os.path.dirname(__file__), "..", "Imgs")

    def pick_image(*names):
        """Devuelve la primera ruta existente dentro de base_imgs o None si ninguna existe."""
        for name in names:
            p = os.path.join(base_imgs, name)
            if os.path.isfile(p):
                return p
        return None

    btn_play_path = pick_image("jugarboton.png", "TemplateBoton.png")
    btn_levels_path = pick_image("niveles.png", "TemplateBoton.png")
    btn_sound_path = pick_image("sonido.png", "TemplateBoton.png")
    btn_happy_path = pick_image("bonk3.png", "TemplateBoton.png")
    btn_exit_path = pick_image("salir.png", "TemplateBoton.png")

    btn1 = Button('JUGAR', (260, 250), image_path=btn_play_path)
    btn2 = Button('NIVELES', (260, 310), image_path=btn_levels_path)
    btn3 = Button('SONIDO', (260, 370), image_path=btn_sound_path)
    btn4 = Button('FELICIDAD', (260, 430), image_path=btn_happy_path)
    btn5 = Button('SALIR', (260, 490), image_path=btn_exit_path)

    btn1.draw()
    btn2.draw()
    btn3.draw()
    btn4.draw()
    btn5.draw()

    # retornar la lista de botones para que el bucle principal los use con eventos
    return [btn1, btn2, btn3, btn4, btn5]

run = True
game_proc = None
while run:
    # Dibujar fondo: imagen si está disponible, si no usar color
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill('lightblue')
    timer.tick(fps)
    buttons = []
    if main_menu:
        buttons = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # detección por evento para evitar múltiples activaciones mientras se mantiene pulsado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                            print("El juego ya se está ejecutando.")
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

    pygame.display.flip()
pygame.quit()

