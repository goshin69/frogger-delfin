import pygame
import sys
import os
import runpy
import subprocess

pygame.init()

# Configuración básica
WIDTH, HEIGHT = 640, 480
BG_COLOR = (30, 30, 30)
BTN_COLOR = (70, 130, 180)
BTN_HOVER = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)
FPS = 60

class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, surf, mouse_pos):
        color = BTN_HOVER if self.rect.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=6)
        txt = self.font.render(self.text, True, TEXT_COLOR)
        txt_r = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_r)

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

    # intenta ejecutar el archivo mainmenu.py en la misma carpeta
    try:
        mainmenu_path = os.path.join(os.path.dirname(__file__), "mainmenu.py")
        if os.path.isfile(mainmenu_path):
            runpy.run_path(mainmenu_path, run_name="__main__")
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
        dolpher_path = os.path.join(os.path.dirname(__file__), "dolpher.py")
        if os.path.isfile(dolpher_path):
            runpy.run_path(dolpher_path, run_name="__main__")
            return
    except Exception:
        pass

    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "dolpher.py")])
    except Exception:
        pass

def _run_mainmenu():
    # Ejecuta mainmenu.py usando subprocess y espera a que termine
    pygame.quit()
    try:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "mainmenu.py")])
    except Exception:
        pass
        
def _run_nivel2():
    # Ejecuta nivel2.py. Intenta importar y llamar main(), luego runpy, y por último subprocess.
    pygame.quit()
    try:
        import nivel2
        if hasattr(nivel2, "main"):
            nivel2.main()
            return
    except Exception:
        pass

    try:
        nivel2_path = os.path.join(os.path.dirname(__file__), "nivel2.py")
        if os.path.isfile(nivel2_path):
            runpy.run_path(nivel2_path, run_name="__main__")
            return
    except Exception:
        pass

    try:
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "nivel2.py")])
    except Exception:
        pass

def seleccionar_nivel():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Seleccionar Nivel")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)

    # Botones: ajustar cantidad/etiquetas según necesidad
    btn_w, btn_h = 220, 60
    spacing = 20
    start_y = (HEIGHT - (3 * btn_h + 2 * spacing + btn_h + spacing)) // 2

    botones = [
        Button(((WIDTH - btn_w)//2, start_y + i*(btn_h+spacing), btn_w, btn_h), f"Nivel {i+1}", font)
        for i in range(3)
    ]
    btn_atras = Button(((WIDTH - btn_w)//2, start_y + 3*(btn_h+spacing), btn_w, btn_h), "Atrás", font)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            for idx, b in enumerate(botones):
                if b.is_clicked(event):
                    # Si es Nivel 1 (idx == 0), ejecutar dolpher.py
                    if idx == 0:
                        _run_dolpher()
                        return None
                    # Si es Nivel 2 (idx == 1), ejecutar nivel2.py
                    if idx == 1:
                        _run_nivel2()
                        return None
                    # para otros niveles simplemente devolvemos el número
                    return idx + 1  # devuelve 1,2,3...
            if btn_atras.is_clicked(event):
                # vuelve al menú principal (mainmenu.py)
                _run_mainmenu()
                return None

        screen.fill(BG_COLOR)
        title = title_font.render("Selecciona un nivel", True, TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))

        for b in botones:
            b.draw(screen, mouse_pos)
        btn_atras.draw(screen, mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    seleccionado = seleccionar_nivel()
    print("Nivel seleccionado:", seleccionado)
    pygame.quit()
    sys.exit()