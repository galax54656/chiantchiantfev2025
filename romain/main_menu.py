# main_menu.py
import pygame
from pygame import mixer

mixer.init()
pygame.init()  # Initialise Pygame une seule fois
screen = pygame.display.set_mode((1280, 720))  # Définissez la taille réelle de la fenêtre

# Chargement et transformation des images
background_img = pygame.image.load('images/im2mainmenudekal.jpg').convert()
background_img = pygame.transform.scale(background_img, (1280, 720))

bouton_img = pygame.image.load('images/FOND BOUTON.png').convert_alpha()
bouton_img = pygame.transform.scale(bouton_img, (380, 100))
bouton_hover_img = pygame.image.load('images/fond_bouton2.png').convert_alpha()
bouton_hover_img = pygame.transform.scale(bouton_hover_img, (380, 100))

pygame.mixer.music.load('images/Le_Donjon_Qutan.mp3')  # charge une piste audio(pas obligée le .wav)
gameplay_music = pygame.mixer.music.play(-1, 0.0,
                                         5000)  # lance la musique, -1=loop infini, 0.0 moment du debut de la musique,5000=5seconde de fade pour lancer la musique en douceur
volume = 0# max = 1
pygame.mixer.music.set_volume(volume)


# Classe Bouton pour le menu principal (bouton avec texte)
class Bouton:
    def __init__(self, pos, text, font, base_color, hover_color, image, hover_image, scale):
        self.pos = pos
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.image = pygame.transform.scale(image, scale)
        self.hover_image = pygame.transform.scale(hover_image, scale)
        self.current_image = self.image
        self.rect = self.current_image.get_rect(center=pos)
        self.text_surf = self.font.render(self.text, True, self.base_color)
        self.text_rect = self.text_surf.get_rect(center=pos)

    def update(self, screen):
        screen.blit(self.current_image, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def au_dessus(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text_surf = self.font.render(self.text, True, self.hover_color)
            self.current_image = self.hover_image
        else:
            self.text_surf = self.font.render(self.text, True, self.base_color)
            self.current_image = self.image

def main_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)

    # Définition des boutons avec leur position, texte et images
    game_bouton = Bouton(pos=(640, 220), text="GAME MODE", font=font, base_color="White", hover_color="Red",
                         image=bouton_img, hover_image=bouton_hover_img, scale=(380, 100))
    options_bouton = Bouton(pos=(640, 340), text="OPTIONS", font=font, base_color="White", hover_color="Red",
                            image=bouton_img, hover_image=bouton_hover_img, scale=(290, 100))
    quit_bouton = Bouton(pos=(640, 460), text="QUIT", font=font, base_color="White", hover_color="Red",
                         image=bouton_img, hover_image=bouton_hover_img, scale=(250, 100))

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Mise à jour et affichage des boutons
        for bouton in [game_bouton, options_bouton, quit_bouton]:
            bouton.change_color(mouse_pos)
            bouton.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_bouton.au_dessus(mouse_pos):
                    return "game"
                if options_bouton.au_dessus(mouse_pos):
                    return "options"
                if quit_bouton.au_dessus(mouse_pos):
                    return "quit"

        pygame.display.update()
        clock.tick(60)
