# main.py
import pygame
from main_menu import main_menu
from options_menu import options_menu
from game import game_loop

def run():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Mon Jeu")

    # Écran de départ
    current_screen = "main_menu"

    # Boucle principale de navigation
    while True:
        if current_screen == "main_menu":
            current_screen = main_menu(screen)
        elif current_screen == "options":
            current_screen = options_menu(screen)
        elif current_screen == "game":
            current_screen = game_loop(screen)
        elif current_screen == "quit":
            break

    pygame.quit()

if __name__ == '__main__':
    run()
