import pygame
import os
import sys
import subprocess
pygame.init()


ALTO = 768
ANCHO = 1366
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dolpher")
fps = 60
timer = pygame.time.Clock()
main_menu = True
font = pygame.font.Font("freesansbold.ttf", 30)
command = 0

# Cargar imagen de fondo
# Ruta relativa desde este archivo hacia la carpeta Imgs
Ruta_Imagen_Fondo = os.path.join(os.path.dirname(__file__), "..", "Imgs", "MenuFondogrande.png")
background_image = None
try:
    _img = pygame.image.load(Ruta_Imagen_Fondo).convert_alpha()
    background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))    
except Exception as e:
    # No detener la ejecución si no se encuentra la imagen; se usará un color de fondo
    print(f"No se pudo cargar la imagen de fondo '{Ruta_Imagen_Fondo}': {e}")


class Button:
    def __init__(self, txt, pos, image_path=None, hover_image_path=None):
        self.txt = txt
        self.pos = pos
        self.size = (500, 39)
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.image = None
        self.hover_image = None
        if image_path:
            try:
                # cargar la imagen y mantener su tamaño original (NO escalar)
                img = pygame.image.load(image_path).convert_alpha()
                self.image = img
            except Exception as e:
                print(f"No se pudo cargar la imagen del botón '{image_path}': {e}")
        if hover_image_path:
            try:
                # cargar la imagen seleccionada y mantener su tamaño original (NO escalar)
                img_h = pygame.image.load(hover_image_path).convert_alpha()
                self.hover_image = img_h
            except Exception as e:
                print(f"No se pudo cargar la imagen seleccionada del botón '{hover_image_path}': {e}")

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

    pygame.display.flip()
pygame.quit()

