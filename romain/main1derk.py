import pygame, random, time
from pygame import mixer
import sys
import niveaux as n
import json
from datetime import datetime

mixer.init()  # initialise les fonctions pour la musique
pygame.init()  # intialise les fonctions de pygame
screen = pygame.display.set_mode((1280, 720))  # initialise la fenêtre ainsi que sa taille(X,Y)

# load images
fond_menu = pygame.image.load('images/im2mainmenudekal.jpg')  # charge une image(pas obligée .png)
fond_menu = fond_menu.convert()  # la convertie dans le bon format de pixel
fond_menu = pygame.transform.scale(fond_menu, (1280, 720))  # change sa taille

fond_bouton = pygame.image.load('images/FOND BOUTON.png')
fond_bouton = fond_bouton.convert()

fond_bouton2 = pygame.image.load('images/fond_bouton2.png')  # bouton orange+rouge
fond_bouton2 = fond_bouton2.convert()

fond_bouton3 = pygame.image.load('images/FOND BOUTON2.png')  # bouton marron
fond_bouton3 = fond_bouton3.convert()

fond_bouton4 = pygame.image.load('images/FOND BOUTON3.jpg')  # bouton marron+rouge
fond_bouton4 = fond_bouton4.convert()

music_plus_button_image = pygame.image.load('images/plus-removebg-preview.png').convert_alpha()

music_moins_button_image = pygame.image.load('images/moins-removebg-preview.png').convert_alpha()

music_on_button_image = pygame.image.load(
    'images/soundOnBtn.png').convert_alpha()  # charge et convertie une image et permet une sorte de transparence(mieux pour image non rectangle)

music_off_button_image = pygame.image.load('images/soundOffBtn.png').convert_alpha()

option_back = pygame.image.load('images/écranoption.png').convert_alpha()
option_jeu_back = pygame.image.load('images/back_for_option_jeu.png').convert_alpha()

option_jeu_button_image = pygame.image.load('images/option_jeu.png').convert_alpha()
option_jeu_button_image = pygame.transform.scale(option_jeu_button_image, (100, 80))  # change sa taille  X, Y

quit_button_image = pygame.image.load('images/croixbienbien.png').convert_alpha()

fond_jeu = pygame.image.load('images/grim.png')  # charge une image(pas obligée .png
fond_jeu = fond_jeu.convert()  # la convertie dans une version meilleur pour pygame
fond_jeu = pygame.transform.scale(fond_jeu, (1280, 720))  # chage sa taille

# Scale images(change la taille des images)
music_plus_button_image = pygame.transform.scale(music_plus_button_image, (60, 60))
music_moins_button_image = pygame.transform.scale(music_moins_button_image, (80, 80))
music_on_button_image = pygame.transform.scale(music_on_button_image, (150, 60))
music_off_button_image = pygame.transform.scale(music_off_button_image, (150, 60))
option_back = pygame.transform.scale(option_back, (370, 570))
option_jeu_back = pygame.transform.scale(option_jeu_back, (1100, 600))
quit_button_image = pygame.transform.scale(quit_button_image, (90, 90))
#quit_button_image = pygame.transform.rotate(quit_button_image,45)

# load music
pygame.mixer.music.load('images/Le_Donjon_Qutan.mp3')  # charge une piste audio(pas obligée le .wav)
gameplay_music = pygame.mixer.music.play(-1, 0.0,
                                         5000)  # lance la musique, -1=loop infini, 0.0 moment du debut de la musique,5000=5seconde de fade pour lancer la musique en douceur
volume = 0.3# max = 1
pygame.mixer.music.set_volume(volume)  # set volume to 30%

#load les sound effects
win_sound = pygame.mixer.Sound('images/you won audio.mp3')
win_sound.set_volume(0.3)
max_sound = pygame.mixer.Sound('images/Metal_Gear_Solid_Alert__.mp3')
max_sound.set_volume((0.2))

#initialise les listes
piece_place = []
boxes = []
all_l_objects = []
board = []
level = 0

#initialise des couleurs (facilite suite)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)

FPS = 60#frame par secondes
clock = pygame.time.Clock()  # initialise une horloge interne au jeu

# initialise la fenêtre ainsi que sa taille(X,Y)
WINDOWWIDTH = 1280  # X
WINDOWHEIGHT = 720  # Y
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

# State de la music
music = 'on'

menu_mouse_pos = pygame.mouse.get_pos()  # facilite la recuperation de la position de la souris/ en faite nul



#classe pour les animaux
class Image():
    def __init__(self, nom, image, image2=None, taille=None, taille2=None, position_debut=(0, 0), position_debut2=None,
                 type=None, bougeable=None):
        self.type = type #savoir si L ou I
        if type == "simple":
            self.nom = nom
            self.image = pygame.image.load(image).convert_alpha()#load et change nb de pixels
            self.image = pygame.transform.scale(self.image, taille)#change taille
            self.rect = self.image.get_rect(topleft=position_debut)#utile pour clic
            self.dep_pos = position_debut
            self.bougeable = bougeable  # 1 = oui;  2 = non /si non piece déjà sur le bateau
            if self.bougeable == 1:
                boxes.append(self)
                self.place = 0
            elif self.bougeable == 0:
                self.place = 1
                piece_place.append(self)#pour le lancement du jeu place occupe et couleur
            self.case = None
            self.case_num = None
            self.row = None
            self.row_num = None
            #donne couleur pour les conditions de victoires
            if self.nom == "hippopotame1" or self.nom == "hippopotame2":
                self.couleur = "bleu"
                print("fait")
            elif self.nom == "lion1":
                self.couleur = "jaune"
            elif self.nom == "girafe1":
                self.couleur = "vert"
            elif self.nom == "elephant1":
                self.couleur = "violet"
            elif self.nom == "zebre1" or self.nom == "zebre2":
                self.couleur = "rouge"

        if type == "el":
            self.nom = nom
            #pareil que l'autre mais piece de droite
            self.imaged = pygame.image.load(image).convert_alpha()
            self.imaged = pygame.transform.scale(self.imaged, taille)
            self.rectd = self.imaged.get_rect(topleft=position_debut)
            #piece de gauche
            self.imageg = pygame.image.load(image2).convert_alpha()
            self.imageg = pygame.transform.scale(self.imageg, taille2)
            self.rectg = self.imageg.get_rect(topleft=position_debut2)
            self.bougeable = bougeable
            self.pos_deb1 = position_debut
            self.pos_deb2 = position_debut2

            if self.bougeable == 1:
                all_l_objects.append(self)
                self.place = 0
            elif self.bougeable == 0:
                self.place = 1
                piece_place.append(self)
            self.case = None
            self.case_num = None
            self.row = None
            self.row_num = None
            if self.nom == "lion2":
                self.couleur = "jaune"
            if self.nom == "girafe2":
                self.couleur = "vert"
            if self.nom == "elephant2":
                self.couleur = "violet"

#Bouton avec du texte, fait tôt dans le projet et donc pas la plus éfficace
class Button:  # classe pour les bouttons avec un texte
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, image_scale, hov_image=fond_bouton2):
        # change la taille de l'image
        self.image_scale = image_scale#pour changer taille
        self.image = pygame.transform.scale(image,
                                            (self.image_scale[0], self.image_scale[1]))  # change la taille de l'image
        self.image_base = pygame.transform.scale(image,
                                                 (self.image_scale[0], self.image_scale[1]))
        self.hov_image = pygame.transform.scale(hov_image,
                                                (self.image_scale[0], self.image_scale[1]))
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font  # taille du texte
        self.base_color = base_color  # couleur du texte
        self.hovering_color = hovering_color  # couleur du texte quand la souris survole
        self.text_input = text_input  # recupere le texte
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos))  # crée un rectangle autour de l'image pour initialiser sa position
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # crée celui autour du texte

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)  # permet au boutton de s'afficher

    #écrit avant de découvrir collidepoint
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):  # vérifie si la sourie est sur le bouton(collidepoint est mieux mais flemme)
            return True
        return False

    def changeColor(self, position):  # change la couleur du bouton et texte quand la souris est dessus
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.image = pygame.transform.scale(self.hov_image, (self.image_scale[0], self.image_scale[1]))
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.image = pygame.transform.scale(self.image_base, (self.image_scale[0], self.image_scale[1]))

#même fonction qu'au dessus mais sans texte /pas besoin de changer de couleur
class Button2:  # Button with a simple image
    def __init__(self, image, pos, hovering_image):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.hovering_image = hovering_image

    def update2(self, screen):  # pour afficher l'image
        screen.blit(self.image, self.rect)

    #propre à l'image enceinte
    def on_off_music(self, position, event):  # pour arrêter et lancer la musique
        global music  # recupere le statue de la musique
        if self.rect.collidepoint(position) and event.type == pygame.MOUSEBUTTONDOWN:  # souris sur le bouton et clique
            if music == 'on':
                pygame.mixer.music.pause()  # pause la musique
                music = 'off'  # change le statue de la musique
                self.image = self.hovering_image  # change l'image
            elif music == 'off':#inverse de au dessus
                pygame.mixer.music.unpause()
                music = 'on'
                self.image = music_on_button_image

    #propre au plus et moins
    def change_volume(self, position, event):
        global volume
        if self.rect.collidepoint(position) and event.type == pygame.MOUSEBUTTONDOWN:  # souris sur le bouton et clique
            if self.image == music_plus_button_image:
                if volume + 0.05 <= 1.05:#vérifie de pas aller au dessus du max
                    volume = volume + 0.05
                    pygame.mixer.music.set_volume(volume)

                else:
                    max_sound.play(loops=0)#son indiquant le max

            elif self.image == music_moins_button_image:
                if volume - 0.05 >= 0:
                    volume = volume - 0.05
                    pygame.mixer.music.set_volume(volume)

                else:
                    max_sound.play(loops=0)

#fonction pour texte ne nécessitant pas d'input
class Text:  # pour le texte simple
    def __init__(self, pos, text_input, font, base_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.text_input = text_input
        self.rendered_text = self.font.render(self.text_input, True,
                                              self.base_color)  # True=pour rendre smooth les lettre dans le decor
        self.text_rect = self.rendered_text.get_rect(topleft=(self.x_pos, self.y_pos))

    def update3(self, screen):
        screen.blit(self.rendered_text, self.text_rect)


#classe pour les cases du bateau
class Board_box(pygame.Rect):
    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)
        pygame.draw.rect(screen, LIGHT_GRAY, self, width=1)
        self.occupe = 0
        self.couleur = None
#esquisse pour montrer où la pièce sera placé mais trop demandant pour l'ordinateur
'''
    def changeColor(self):
        self.color = RED  # Update the color attribute
        pygame.draw.rect(screen, self.color, self)
        pygame.display.flip()

    def backtonormal(self):
        self.color = LIGHT_GRAY  # Reset color attribute to LIGHT_GRAY
        pygame.draw.rect(screen, self.color, self)
'''
#fonction déssinant les cases du bateau grâce à la classe
def draw_board():
    row_sizes = [5, 7, 7, 5]
    posi = -1

    for row_size in row_sizes:
        posi += 1
        if row_size == 5:
            row = []
            for column in range(row_size):
                x = 676 + column * 84
                y = 216 + posi * 105
                case = Board_box(x, y, 84, 105)
                row.append(case)
            board.append(row)
        else:
            row = []
            for column in range(row_size):
                x = 592 + column * 84
                y = 216 + posi * 105
                case = Board_box(x, y, 84, 105)
                row.append(case)
            board.append(row)


niv = None
# on donnera le choix au mec
gagné = 0
win_time = 0


def option():
    pygame.display.set_caption("Options")

    menu_mouse_pos = pygame.mouse.get_pos()
    quit_button = Button2(image=quit_button_image, pos=(780, 65), hovering_image=quit_button_image)
    music_plus_button = Button2(image=music_plus_button_image, pos=(785, 410), hovering_image=music_plus_button_image)
    music_moins_button = Button2(image=music_moins_button_image, pos=(480, 407),
                                 hovering_image=music_moins_button_image)
    music_button = Button2(image=music_on_button_image, pos=(720, 220), hovering_image=music_off_button_image)
    option_text = Text(pos=(485, 70), text_input='OPTION', font=pygame.font.Font(None, 75), base_color='White')
    sound_text = Text(pos=(470, 200), text_input='Music :', font=pygame.font.Font(None, 60), base_color='White')
    volume_text = Text(pos=(460, 320), text_input='Volume :', font=pygame.font.Font(None, 60), base_color='White')
    if music == 'off':
        music_button.image = music_off_button_image

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                if quit_button.rect.collidepoint(menu_mouse_pos):  # lance le menu options si appuie sur options
                    main_menu()
                    break
            music_button.on_off_music(menu_mouse_pos, event)
            music_plus_button.change_volume(menu_mouse_pos, event)
            music_moins_button.change_volume(menu_mouse_pos, event)
        # Clear the screen
        screen.blit(fond_menu, (0, 0))
        screen.blit(option_back, (450, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        # Create and render the button
        quit_button.update2(screen)
        option_text.update3(screen)
        sound_text.update3(screen)
        volume_text.update3(screen)
        music_button.update2(screen)
        music_plus_button.update2(screen)
        music_moins_button.update2(screen)
        pygame.draw.rect(screen, WHITE, (515, 380, 235, 60), width=5, border_radius=20)#480, 420, 300 , 60
        volume_bar_width = int(235 * volume)  # Calculate the width of the volume bar based on the volume level
        if volume_bar_width == 235:
            pygame.draw.rect(screen, WHITE, (516, 380, volume_bar_width, 60), border_radius=20)
        else:
            pygame.draw.rect(screen, WHITE, (513, 380, volume_bar_width, 60), border_top_left_radius=20,
                             border_bottom_left_radius=20)

        clock.tick(FPS)

        # Update the display
        pygame.display.update()


def main_menu():  # menu principale
    pygame.display.set_caption("Menu")  # donne le nom à la fenêtre

    while True:
        screen.blit(fond_menu, (0, 0))  # met l'image de font(mer)
        menu_mouse_pos = pygame.mouse.get_pos()  # facilite la recuperation de la position de la souris
        menu_text = pygame.font.Font(None, 150).render(" ", True,
                                                       (0, 0, 0))  # texte main menu en marron clair
        menu_rect = menu_text.get_rect(center=(640, 100))

        # crée le bouton select
        select_button = Button(image=fond_bouton, pos=(640, 240-20),
                               text_input="GAME MODE", font=pygame.font.Font(None, 75), base_color="White",
                               hovering_color="Red", image_scale=[380, 100], hov_image=fond_bouton2)

        options_button = Button(image=fond_bouton, pos=(640, 365-20),
                                text_input="OPTIONS", font=pygame.font.Font(None, 75), base_color="White",
                                hovering_color="Red", image_scale=[290, 100], hov_image=fond_bouton2)

        quit_button = Button(image=fond_bouton, pos=(640, 495-20),
                             text_input="QUIT", font=pygame.font.Font(None, 75), base_color="White",
                             hovering_color="Red", image_scale=[250, 100], hov_image=fond_bouton2)

        screen.blit(menu_text, menu_rect)

        for button in [select_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # si appui sur la croix
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                if select_button.checkForInput(menu_mouse_pos):  # lance le menu select si appuie sur select
                    pass#menu nombre joueurs
                elif options_button.checkForInput(menu_mouse_pos):  # lance le menu options si appuie sur options
                    option()
                elif quit_button.checkForInput(menu_mouse_pos):  # quitte le jeu
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

pygame.quit()

