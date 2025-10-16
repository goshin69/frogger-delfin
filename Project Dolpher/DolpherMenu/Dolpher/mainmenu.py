import pygame
import os
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

    def check_clicked(self): # Detecta si se ha hecho click en el botón
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False



def draw_menu():
    # rutas a las imágenes de los botones (si no existen, Button usará el texto)
    base_imgs = os.path.join(os.path.dirname(__file__), "..", "Imgs")
    btn_play_path = os.path.join(base_imgs, "jugarboton.png")
    btn_levels_path = os.path.join(base_imgs, "niveles.png")
    btn_sound_path = os.path.join(base_imgs, "sonido.png")
    btn_happy_path = os.path.join(base_imgs, "bonk3.png")
    btn_exit_path = os.path.join(base_imgs, "salir.png")

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
    if btn1.check_clicked():
        command = 1
    if btn2.check_clicked():
        command = 2
    if btn3.check_clicked():
        command = 3
    if btn4.check_clicked():
        command = 4
    if btn5.check_clicked():
        command = 5        
    #return command

run = True
while run:
    # Dibujar fondo: imagen si está disponible, si no usar color
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill('lightblue')
    timer.tick(fps)
    if main_menu:
        draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.flip()
pygame.quit()

