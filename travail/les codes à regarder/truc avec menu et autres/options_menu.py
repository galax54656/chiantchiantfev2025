# options_menu.py
import pygame

# Chargement et transformation des images pour le menu options
background_img = pygame.image.load('../../images/im2mainmenudekal.jpg').convert()
background_img = pygame.transform.scale(background_img, (1280, 720))
option_panel_img = pygame.image.load('../../images/écranoption.png').convert_alpha()
option_panel_img = pygame.transform.scale(option_panel_img, (370, 570))

music_on_img = pygame.image.load('../../images/soundOnBtn.png').convert_alpha()
music_off_img = pygame.image.load('../../images/soundOffBtn.png').convert_alpha()
music_on_img = pygame.transform.scale(music_on_img, (150, 60))
music_off_img = pygame.transform.scale(music_off_img, (150, 60))

volume_plus_img = pygame.image.load('../../images/plus-removebg-preview.png').convert_alpha()
volume_minus_img = pygame.image.load('../../images/moins-removebg-preview.png').convert_alpha()
volume_plus_img = pygame.transform.scale(volume_plus_img, (60, 60))
volume_minus_img = pygame.transform.scale(volume_minus_img, (80, 80))

quit_img = pygame.image.load('../../images/croixbienbien.png').convert_alpha()
quit_img = pygame.transform.scale(quit_img, (90, 90))

# Variables globales pour l'état de la musique et le volume
music_state = "on"
volume = 0


# Classe simple pour les boutons utilisant uniquement une image
class Bouton_simple:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def au_dessus(self, pos):
        return self.rect.collidepoint(pos)


def options_menu(screen):
    global music_state, volume
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)
    small_font = pygame.font.Font(None, 60)

    # Bouton pour revenir au menu principal
    quit_button = Bouton_simple(quit_img, (780, 65))

    # Bouton pour activer/désactiver la musique
    music_button = Bouton_simple(music_on_img if music_state == "on" else music_off_img, (720, 220))

    # Boutons pour augmenter ou diminuer le volume
    plus_button = Bouton_simple(volume_plus_img, (785, 410))
    minus_button = Bouton_simple(volume_minus_img, (480, 407))

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        screen.blit(option_panel_img, (450, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.au_dessus(mouse_pos):
                    return "main_menu"
                if music_button.au_dessus(mouse_pos):
                    # Bascule de l'état de la musique
                    if music_state == "on":
                        pygame.mixer.music.pause()
                        music_state = "off"
                        music_button.image = music_off_img
                    else:
                        pygame.mixer.music.unpause()
                        music_state = "on"
                        music_button.image = music_on_img
                if plus_button.rect.collidepoint(mouse_pos):
                    if volume + 0.05 <= 1.05:
                        volume += 0.05
                        pygame.mixer.music.set_volume(volume)
                if minus_button.rect.collidepoint(mouse_pos):
                    if volume - 0.05 >= 0:
                        volume -= 0.05
                        pygame.mixer.music.set_volume(volume)

        # Affichage des boutons
        quit_button.draw(screen)
        music_button.draw(screen)
        plus_button.draw(screen)
        minus_button.draw(screen)

        # Dessin de la barre de volume
        bar_x, bar_y = 515, 380
        bar_width, bar_height = 235, 60
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), width=5, border_radius=20)
        volume_bar_width = int(235 * volume)
        # Dessin de la barre de volume seulement si volume > 0
        if volume_bar_width > 0:
            if volume_bar_width == 235:
                pygame.draw.rect(screen, (255, 255, 255), (516, 385, volume_bar_width, 50), border_radius=20)
            else:
                pygame.draw.rect(screen, (255, 255, 255), (516, 385, volume_bar_width, 50), border_top_left_radius=20,
                                 border_bottom_left_radius=20)

        title_text = font.render("Options", True, (255, 255, 255))
        music_text = small_font.render("Music :", True, (255, 255, 255))
        volume_text = small_font.render("Volume", True, (255, 255, 255))

        screen.blit(title_text, (485, 70))  # Titre "Options"
        screen.blit(music_text, (470, 200))  # Texte "Music"
        screen.blit(volume_text, (460, 320))  # Texte "Volume"

        pygame.display.update()
        clock.tick(60)
