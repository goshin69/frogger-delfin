import pygame
import sys
import os
import subprocess

# Configuración básica
ANCHO = 1366
ALTO = 768
BG_COLOR = (30, 30, 30)
BTN_COLOR = (70, 130, 180)
BTN_HOVER = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)
FPS = 60
# Highlight config: muestra un área amarilla semitransparente sobre cada hitbox
HIGHLIGHT_YELLOW = True
HIGHLIGHT_COLOR = (255, 255, 0, 120)  # RGBA (alpha 0-255)

try:
    pygame.mixer.init()
    musica_path = os.path.join("delfin-version-frogge3r-main","musica","Fountains Of Wayne, Too Cool For School (With Lyrics).mp3")
    if os.path.exists(musica_path):
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
except Exception as e:
    print(f"No se pudo cargar la musica: {e}")


# Inicializar pygame y configurar la pantalla
pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Seleccionar Nivel")

# Cargar imagen de fondo
# Ruta relativa desde este archivo hacia la carpeta Imgs
Ruta_Imagen_Fondo = os.path.join(os.path.dirname(__file__), "..", "Imgs", "MenuNivelesBotones.png")
background_image = None

if os.path.exists(Ruta_Imagen_Fondo):
    try:
        _img = pygame.image.load(Ruta_Imagen_Fondo)
        if _img:
            _img = _img.convert_alpha()
            background_image = pygame.transform.smoothscale(_img, (ANCHO, ALTO))
            print(f"Imagen de fondo cargada exitosamente: {Ruta_Imagen_Fondo}")
    except Exception as e:
        print(f"Error al cargar la imagen de fondo '{Ruta_Imagen_Fondo}': {e}")
else:
    print(f"No se encontró el archivo de imagen: {Ruta_Imagen_Fondo}")

class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

def _run_mainmenu():
    # intenta importar mainmenu y llamar mainmenu.main()
    # si falla, intenta ejecutar mainmenu.py como script usando runpy o subprocess
    pygame.quit()
    try:
        import mainmenu
        if hasattr(mainmenu, "main"):
            mainmenu.main()
            return
    except Exception:
        pass



    # último recurso: lanzar un nuevo proceso
    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "mainmenu.py")])
    except Exception:
        pass

def _run_dolpher():
    # Ejecuta dolpher.py. Intenta importar y llamar main(), luego runpy, y por último subprocess.
    pygame.quit()
    try:
        import dolpher
        if hasattr(dolpher, "main"):
            dolpher.main()
            return
    except Exception:
        pass



    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "ballena.py")])
    except Exception:
        pass

def _run_mainmenu():
    pygame.quit()
    try:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "mainmenu.py")])
    except Exception:
        pass
        
def _run_nivel2():
    pygame.quit()
    try:
        import nivil2
        if hasattr(nivil2, "main"):
            nivil2.main()
            return
    except Exception:
        pass
    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "nivel2.py")])
    except Exception:
        pass

def _run_nivil3():
    pygame.quit()
    try:
        import nivil3
        if hasattr(nivil3, "main"):
            nivil3.main()
            return
    except Exception:
        pass
    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "nivel3.py")])
    except Exception:
        pass



def seleccionar_nivel():

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)

    # Coordenadas de hitboxes: AJUSTA MANUALMENTE
    HITBOXES = {
        "nivel1": (415, 260, 550, 40),  #415=Pos X, 260=Pos Y, 550=Ancho, 40=Alto.
        "nivel2": (415, 360, 550, 40),
        "nivel3": (415, 440, 550, 40),
        "atras":  (415, 530, 550, 40),
    }

    botones = [Button(HITBOXES[f"nivel{i+1}"], f"Nivel {i+1}", font) for i in range(3)]
    btn_atras = Button(HITBOXES["atras"], "Atrás", font)

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            for idx, b in enumerate(botones):
                if b.is_clicked(event):
                    print(f"Clicked {b.text} rect={b.rect}")
                    if idx == 0:
                        _run_dolpher()
                        return None
                    if idx == 1:
                        _run_nivel2()
                        return None
                    if idx == 2:
                        _run_nivil3()
                        return None
                    return idx + 1
            if btn_atras.is_clicked(event):
                print(f"Clicked {btn_atras.text} rect={btn_atras.rect}")
                _run_mainmenu()
                return None

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BG_COLOR)

        title = title_font.render("Selecciona un nivel", True, TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(ANCHO // 2, 80)))

        # Efecto hover: ilumina el botón solo si el mouse está encima
        hover_color = (255, 255, 0, 120)
        for b in botones + [btn_atras]:
            if b.rect.collidepoint(mouse_pos):
                s = pygame.Surface((b.rect.width, b.rect.height), pygame.SRCALPHA)
                s.fill(hover_color)
                screen.blit(s, b.rect.topleft)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    nivel_seleccionado = seleccionar_nivel()
    print(f"Nivel seleccionado: {nivel_seleccionado}")
    pygame.quit()
    sys.exit()
    