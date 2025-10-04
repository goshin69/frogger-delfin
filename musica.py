import pygame

# Inicializar mixer (módulo de audio)
pygame.mixer.init()

# =====================
# Cargar sonidos
# =====================
victoria = pygame.mixer.Sound("delfin-version-frogger-main\delfin-version-frogger-main\ballena.py")
gameover = pygame.mixer.Sound("delfin-version-frogger-main/sonidos/gameover.wav")
salto    = pygame.mixer.Sound("delfin-version-frogger-main/sonidos/salto.wav")

# Ajustar volúmenes (0.0 a 1.0)
victoria.set_volume(0.7)
gameover.set_volume(0.7)
salto.set_volume(0.5)

# =====================
# Musica de fondo
# =====================
def reproducir_musica():
    pygame.mixer.music.load("delfin-version-frogger-main/sonidos/fondo.mp3")
    pygame.mixer.music.set_volume(0.4)   # volumen de música
    pygame.mixer.music.play(-1)         # -1 = bucle infinito

def parar_musica():
    pygame.mixer.music.stop()
