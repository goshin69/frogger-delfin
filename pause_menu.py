import pygame
import sys

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.options = ["C - Continuar", "R - Reiniciar", "Q - Salir"]

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fondo negro
        title = self.font.render("Juego en Pausa", True, (255, 255, 255))
        self.screen.blit(title, (200, 100))

        for i, text in enumerate(self.options):
            option = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(option, (200, 200 + i * 60))

        pygame.display.flip()

    def run(self):
        """Bucle del menú de pausa"""
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_r:  # Reiniciar
                        return "restart"
                    elif event.key == pygame.K_q:  # Salir
                        pygame.quit()
                        sys.exit()

            self.draw()
            self.clock.tick(30)

        return "continue"
