import pygame, random, time
from pygame import mixer
import sys
import niveaux as n
import json
from datetime import datetime

mixer.init()  # initialise les fonctions pour la musique
pygame.init()  # intialise les fonctions de pygame
screen = pygame.display.set_mode((1280, 720))  # initialise la fenêtre ainsi que sa taille(X,Y)

# load image
fond_menu = pygame.image.load('../images/mer.PNG')  # charge une image(pas obligée .png
fond_menu = fond_menu.convert()  # la convertie dans le bon format de pixel
fond_menu = pygame.transform.scale(fond_menu, (1280, 720))  # chage sa taille

fond_bouton = pygame.image.load('../images/FOND BOUTON.png')
fond_bouton = fond_bouton.convert()

fond_bouton2 = pygame.image.load('../images/fond_bouton2.png')  # bouton orange+rouge
fond_bouton2 = fond_bouton2.convert()

fond_bouton3 = pygame.image.load('../images/FOND BOUTON2.png')  # bouton marron
fond_bouton3 = fond_bouton3.convert()

fond_bouton4 = pygame.image.load('../images/FOND BOUTON3.jpg')  # bouton marron+rouge
fond_bouton4 = fond_bouton4.convert()

music_plus_button_image = pygame.image.load('../images/plus-removebg-preview.png').convert_alpha()

music_moins_button_image = pygame.image.load('../images/moins-removebg-preview.png').convert_alpha()

music_on_button_image = pygame.image.load(
    '../images/soundOnBtn.png').convert_alpha()  # charge et convertie une image et permet une sorte de transparence(mieux pour image non rectangle)

music_off_button_image = pygame.image.load('../images/soundOffBtn.png').convert_alpha()

option_back = pygame.image.load('../images/bois option.jpg').convert_alpha()
option_jeu_back = pygame.image.load('../images/back_for_option_jeu.png').convert_alpha()

option_jeu_button_image = pygame.image.load('../images/option_jeu.png').convert_alpha()
option_jeu_button_image = pygame.transform.scale(option_jeu_button_image, (100, 80))  # change sa taille  X, Y

quit_button_image = pygame.image.load('../images/quit.png').convert_alpha()

fond_jeu = pygame.image.load('../images/grim.png')  # charge une image(pas obligée .png
fond_jeu = fond_jeu.convert()  # la convertie dans une version meilleur pour pygame
fond_jeu = pygame.transform.scale(fond_jeu, (1280, 720))  # chage sa taille

# Scale images(change la taille des images)
music_plus_button_image = pygame.transform.scale(music_plus_button_image, (60, 60))
music_moins_button_image = pygame.transform.scale(music_moins_button_image, (80, 80))
music_on_button_image = pygame.transform.scale(music_on_button_image, (200, 80))
music_off_button_image = pygame.transform.scale(music_off_button_image, (200, 80))
option_back = pygame.transform.scale(option_back, (550, 800))
option_jeu_back = pygame.transform.scale(option_jeu_back, (1100, 600))
quit_button_image = pygame.transform.scale(quit_button_image, (180, 110))

# load music
pygame.mixer.music.load('../images/Le_Donjon_Qutan.mp3')  # charge une piste audio(pas obligée le .wav)
gameplay_music = pygame.mixer.music.play(-1, 0.0,
                                         5000)  # lance la musique, -1=loop infini, 0.0 moment du debut de la musique,5000=5seconde de fade pour lancer la musique en douceur
volume = 0.3# max = 1
pygame.mixer.music.set_volume(volume)  # set volume to 30%

#load les sound effects
win_sound = pygame.mixer.Sound('../images/you won audio.mp3')
win_sound.set_volume(0.3)
max_sound = pygame.mixer.Sound('../images/Metal_Gear_Solid_Alert__.mp3')
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



def jeu():
    global board
    global boxes
    global all_l_objects
    global piece_place
    bien_joué = 0


    start_time = time.time()  # prend le temps de début du jeu
    mouse_pos = pygame.mouse.get_pos()
    running = 0
    temps_perdu = 0
    moment_appuie = 0
    niv
    #utilisation de la classe Image
    zebre1 = Image(nom="zebre1", image="images/zebre.png", taille=(84, 210), position_debut=n.niveau["position_zebre1"],
                   type="simple", bougeable=n.niveau["boug_zebre1"])
    zebre2 = Image(nom="zebre2", image="images/zebre2.png", taille=(168, 105),
                   position_debut=n.niveau["position_zebre2"],
                   type="simple", bougeable=n.niveau["boug_zebre2"])
    hippopotame1 = Image(nom="hippopotame1", image="images/hippopotame.png", taille=(252, 105),
                         position_debut=n.niveau["position_hippopotame1"],
                         type="simple", bougeable=n.niveau["boug_hippopotame1"])
    hippopotame2 = Image(nom="hippopotame2", image="images/hippopotame2.png", taille=(168, 105),
                         position_debut=n.niveau["position_hippopotame2"],
                         type="simple", bougeable=n.niveau["boug_hippopotame2"])
    lion1 = Image(nom="lion1", image="images/lion.png", taille=(168, 105), position_debut=n.niveau["position_lion1"],
                  type="simple", bougeable=n.niveau["boug_lion1"])
    elephant1 = Image(nom="elephant1", image="images/elephant.png", taille=(168, 105),
                      position_debut=n.niveau["position_elephant1"],
                      type="simple", bougeable=n.niveau["boug_elephant1"])
    girafe1 = Image(nom="girafe1", image="images/girafe2.png", taille=(84, 210),
                    position_debut=n.niveau["position_girafe1"],
                    type="simple", bougeable=n.niveau["boug_girafe1"])
    elephant2 = Image(nom="elephant2", image="images/elephantdt.png", image2="images/elephantg.png", taille=(84, 105),
                      taille2=(84, 210),
                      position_debut=n.niveau["position_elephant2d"], position_debut2=n.niveau["position_elephant2g"],
                      type="el", bougeable=n.niveau["boug_elephant2"])
    girafe2 = Image(nom="girafe2", image="images/girafedtest.png", image2="images/girafegt.png", taille=(84, 210),
                    taille2=(84, 105),
                    position_debut=n.niveau["position_girafe2d"], position_debut2=n.niveau["position_girafe2g"],
                    type="el", bougeable=n.niveau["boug_girafe2"])
    lion2 = Image(nom="lion2", image="images/lionnedt.png", image2="images/lionnegtest.png", taille=(84, 105),
                  taille2=(84, 210),
                  position_debut=n.niveau["position_lion2d"], position_debut2=n.niveau["position_lion2g"],
                  type="el", bougeable=n.niveau["boug_lion2"])
    active_box = None
    # Variable pour suivre la partie actuellement déplacée
    active_L = None  # Initialise la variable pour suivre la partie de l'objet L actuellement en cours de déplacement.
    draw_board()
    #dessin des limites autour du bateau
    limites = [
        pygame.draw.polygon(screen, RED,
                            ((666, 196), (666, 206), (666 + 5 * 84 + 20, 206), (666 + 5 * 84 + 20, 196))),
        pygame.draw.polygon(screen, RED, (
            (666 + 5 * 84 + 20, 196), (666 + 5 * 84 + 20 + 10, 196), (666 + 5 * 84 + 20 + 10, 196 + 105 + 10),
            (666 + 5 * 84 + 20, 196 + 105 + 10))),
        pygame.draw.polygon(screen, RED,
                            ((666 + 5 * 84 + 20 + 10, 196 + 105), (666 + 5 * 84 + 20 + 10 + 84, 196 + 105),
                             (666 + 5 * 84 + 20 + 10 + 84, 196 + 105 + 10),
                             (666 + 5 * 84 + 20 + 10, 196 + 105 + 10))),
        pygame.draw.polygon(screen, RED, (
            (666 + 5 * 84 + 20 + 84, 196 + 105 + 10), (666 + 5 * 84 + 20 + 10 + 84, 196 + 105 + 10),
            (666 + 5 * 84 + 20 + 10 + 84, 196 + 105 + 20 + 210 + 10),
            (666 + 5 * 84 + 20 + 84, 196 + 105 + 20 + 210 + 10))),
        pygame.draw.polygon(screen, RED, ((666, 206 + 10 + (4 * 105) + 10), (666, 206 + 20 + (4 * 105) + 10),
                                          (666 + 10 + 5 * 84 + 10, 206 + 10 + (4 * 105) + 20),
                                          (666 + 10 + 5 * 84 + 10, 206 + 10 + (4 * 105) + 10))),
        pygame.draw.polygon(screen, RED, (
            (666 - 84, 206 + 105), (666 - 84, 206 + 20 + (2 * 105) + 105),
            (666 - 84 - 10, 206 + 20 + (2 * 105) + 105),
            (666 - 84 - 10, 206 + 105))),
        pygame.draw.polygon(screen, RED, ((666, 196), (666 - 10, 196), (666 - 10, 196 + 105), (666, 196 + 105))),
        pygame.draw.polygon(screen, RED, (
            (666, 196 + 3 * 105 + 40), (666 - 10, 196 + 3 * 105 + 40), (666 - 10, 196 + 105 + 3 * 105 + 40),
            (666, 196 + 105 + 3 * 105 + 40))),
        pygame.draw.polygon(screen, RED, (
            (666, 196 + 3 * 105 + 40), (666, 196 + 3 * 105 + 30), (666 - 84 - 10, 196 + 3 * 105 + 30),
            (666 - 84 - 10, 196 + 3 * 105 + 40))),
        pygame.draw.polygon(screen, RED, (
            (666, 196 + 105), (666, 196 + 105 + 10), (666 - 84 - 10, 196 + 105 + 10), (666 - 84 - 10, 196 + 105))),
        pygame.draw.polygon(screen, RED, (
            (666 + 10 + 5 * 84 + 10, 196 + 20 + 3 * 105 + 20),
            (666 + 10 + 5 * 84 + 10 + 10, 196 + 20 + 3 * 105 + 20),
            (666 + 10 + 5 * 84 + 10 + 10, 196 + 20 + 4 * 105 + 20),
            (666 + 10 + 10 + 5 * 84, 196 + 20 + 4 * 105 + 20))),
        pygame.draw.polygon(screen, RED, (
            (666 + 10 + 5 * 84 + 10, 196 + 20 + 3 * 105 + 10), (666 + 10 + 5 * 84 + 10, 196 + 20 + 3 * 105 + 20),
            (666 + 10 + 5 * 84 + 84 + 20, 196 + 20 + 3 * 105 + 20),
            (666 + 10 + 5 * 84 + 84 + 20, 196 + 20 + 3 * 105 + 10)))]
    #fait en sorte de donner un état et une couleur aux cases celon les pieces deja placées
    for active_box in piece_place:
        if active_box.type == "simple":
            for row_num, row in enumerate(board):
                for case_num, case in enumerate(row):
                    if case.topleft == active_box.dep_pos:
                        if active_box.nom in ["zebre1", "girafe1"]:
                            if row_num == 0:
                                if case.occupe == 0 and board[row_num + 1][case_num + 1].occupe == 0:
                                    board[row_num + 1][case_num + 1].occupe = 1
                                    board[row_num + 1][case_num + 1].couleur = active_box.couleur
                                    case.occupe = 1
                                    case.couleur = active_box.couleur
                                    active_box.rect.topleft = case.topleft
                                    case.couleur = active_box.couleur
                                    active_box.case = case
                                    active_box.case_num = case_num
                                    active_box.row_num = row_num
                                    active_box.row = row
                                    active_box.place = 1
                                else:
                                    # Space is already occupied, reset the piece position
                                    active_box.rect.topleft = active_box.dep_pos
                            elif row_num == 1:
                                if case.occupe == 0 and board[row_num + 1][case_num].occupe == 0:
                                    board[row_num + 1][case_num].occupe = 1
                                    case.occupe = 1
                                    board[row_num + 1][case_num].couleur = active_box.couleur
                                    case.couleur = active_box.couleur
                                    active_box.rect.topleft = case.topleft
                                    active_box.case = case
                                    active_box.case_num = case_num
                                    active_box.row_num = row_num
                                    active_box.row = row
                                    active_box.place = 1
                                else:
                                    # Space is already occupied, reset the piece position
                                    active_box.rect.topleft = active_box.dep_pos
                            elif row_num == 2:
                                if case.occupe == 0 and board[row_num + 1][case_num - 1].occupe == 0:
                                    board[row_num + 1][case_num - 1].occupe = 1
                                    case.occupe = 1
                                    board[row_num + 1][case_num - 1].couleur = active_box.couleur
                                    case.couleur = active_box.couleur
                                    active_box.rect.topleft = case.topleft
                                    active_box.case = case
                                    active_box.case_num = case_num
                                    active_box.row_num = row_num
                                    active_box.row = row
                                    active_box.place = 1
                                else:
                                    # Space is already occupied, reset the piece position
                                    active_box.rect.topleft = active_box.dep_pos

                        elif active_box.nom in ["zebre2", "hippopotame2", "lion1", "elephant1"]:
                            if case.occupe == 0 and row[case_num + 1].occupe == 0:
                                active_box.rect.topleft = case.topleft
                                row[case_num + 1].occupe = 1
                                case.occupe = 1
                                row[case_num + 1].couleur = active_box.couleur
                                case.couleur = active_box.couleur
                                active_box.case = case
                                active_box.case_num = case_num
                                active_box.row_num = row_num
                                active_box.row = row
                                active_box.place = 1
                                active_box.case.couleur = active_box.couleur
                            else:
                                # Space is already occupied, reset the piece position
                                active_box.rect.topleft = active_box.dep_pos

                        elif active_box.nom == "hippopotame1":
                            if case.occupe == 0 and row[case_num + 1].occupe == 0 and row[
                                case_num + 2].occupe == 0:
                                row[case_num + 1].occupe = 1
                                case.occupe = 1
                                row[case_num + 2].occupe = 1
                                row[case_num + 1].couleur = active_box.couleur
                                case.couleur = active_box.couleur
                                row[case_num + 2].couleur = active_box.couleur
                                active_box.case = case
                                active_box.case_num = case_num
                                active_box.row_num = row_num
                                active_box.row = row
                                active_box.place = 1
                                active_box.case.couleur = active_box.couleur
    active_box = None
    for active_L in piece_place:
        if active_L.type == "el":
            for row_num, row in enumerate(board):
                for case_num, case in enumerate(row):
                    if case.topleft == active_L.pos_deb2:
                        if row_num == 0:
                            if active_L.nom == "lion2" and row[case_num + 1].occupe == 0 and board[row_num + 1][
                                case_num + 1].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectg.topleft = case.topleft
                                # active_L.rectd.topleft = (case.topleft[0] + 84, case.topleft[1])
                                case.occupe = 1
                                row[case_num + 1].occupe = 1
                                board[row_num + 1][case_num + 1].occupe = 1
                                case.couleur = active_L.couleur
                                row[case_num + 1].couleur = active_L.couleur
                                board[row_num + 1][case_num + 1].couleur = active_L.couleur

                            elif active_L.nom == "elephant2" and board[row_num + 1][
                                case_num + 1].occupe == 0 and board[row_num + 1][
                                case_num + 2].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectg.topleft = case.topleft
                                # active_L.rectd.topleft = (case.bottomright[0], case.bottomright[1])
                                case.occupe = 1
                                board[row_num + 1][case_num + 1].occupe = 1
                                board[row_num + 1][case_num + 2].occupe = 1
                                case.couleur = active_L.couleur
                                board[row_num + 1][case_num + 1].couleur = active_L.couleur
                                board[row_num + 1][case_num + 2].couleur = active_L.couleur

                        elif row_num == 1:
                            print(active_L.nom)

                            if active_L.nom == "lion2" and row[case_num + 1].occupe == 0 and \
                                    board[row_num + 1][case_num].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectg.topleft = case.topleft
                                # active_L.rectd.topleft = (case.topleft[0] + 84, case.topleft[1])
                                case.occupe = 1
                                row[case_num + 1].occupe = 1
                                board[row_num + 1][case_num].occupe = 1
                                case.couleur = active_L.couleur
                                row[case_num + 1].couleur = active_L.couleur
                                board[row_num + 1][case_num].couleur = active_L.couleur

                            elif active_L.nom == "elephant2":
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectg.topleft = case.topleft
                                # active_L.rectd.topleft = (case.bottomright[0], case.bottomright[1])
                                case.occupe = 1
                                board[row_num + 1][case_num].occupe = 1
                                board[row_num + 1][case_num + 1].occupe = 1
                                case.couleur = active_L.couleur
                                board[row_num + 1][case_num].couleur = active_L.couleur
                                board[row_num + 1][case_num + 1].couleur = active_L.couleur

                        elif row_num == 2:
                            if active_L.nom == "lion2" and row[case_num + 1].occupe == 0 and row[
                                case_num + 1].occupe == 0 and \
                                    board[row_num + 1][case_num - 1].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectg.topleft = case.topleft
                                # active_L.rectd.topleft = (case.topleft[0] + 84, case.topleft[1])
                                case.occupe = 1
                                row[case_num + 1].occupe = 1
                                board[row_num + 1][case_num - 1].occupe = 1
                                case.couleur = active_L.couleur
                                row[case_num + 1].couleur = active_L.couleur
                                board[row_num + 1][case_num - 1].couleur = active_L.couleur

                            elif active_L.nom == "elephant2" and board[row_num + 1][
                                case_num - 1].occupe == 0 and board[row_num + 1][case_num].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectg.topleft = case.topleft
                                # active_L.rectd.topleft = (case.bottomright[0], case.bottomright[1])
                                case.occupe = 1
                                board[row_num + 1][case_num - 1].occupe = 1
                                board[row_num + 1][case_num].occupe = 1
                                case.couleur = active_L.couleur
                                board[row_num + 1][case_num - 1].couleur = active_L.couleur
                                board[row_num + 1][case_num].couleur = active_L.couleur

                    elif active_L.nom == "girafe2" and case.topleft == active_L.pos_deb1:
                        if row_num == 0:

                            if active_L.nom == "girafe2" and board[row_num + 1][
                                case_num + 1].occupe == 0 and board[row_num + 1][case_num].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectd.topright = case.topright
                                # active_L.rectg.topleft = (case.bottomleft[0] - 84, case.bottomleft[1])
                                case.occupe = 1
                                board[row_num + 1][case_num + 1].occupe = 1
                                board[row_num + 1][case_num].occupe = 1
                                case.couleur = active_L.couleur
                                board[row_num + 1][case_num + 1].couleur = active_L.couleur
                                board[row_num + 1][case_num].couleur = active_L.couleur

                        elif row_num == 1:
                            if active_L.nom == "girafe2" and board[row_num + 1][
                                case_num].occupe == 0 and \
                                    board[row_num + 1][case_num - 1].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectd.topright = case.topright
                                # active_L.rectg.topleft = (case.bottomleft[0] - 84, case.bottomleft[1])
                                case.occupe = 1
                                board[row_num + 1][case_num].occupe = 1
                                board[row_num + 1][case_num - 1].occupe = 1
                                case.couleur = active_L.couleur
                                board[row_num + 1][case_num].couleur = active_L.couleur
                                board[row_num + 1][case_num - 1].couleur = active_L.couleur

                        elif row_num == 2:
                            if active_L.nom == "girafe2" and board[row_num + 1][
                                case_num - 1].occupe == 0 and \
                                    board[row_num + 1][case_num - 2].occupe == 0:
                                active_L.case = case
                                active_L.case_num = case_num
                                active_L.row_num = row_num
                                active_L.row = row
                                active_L.place = 1
                                # active_L.rectd.topright = case.topright
                                # active_L.rectg.topleft = (case.bottomleft[0] - 84, case.bottomleft[1])
                                case.occupe = 1
                                board[row_num + 1][case_num - 1].occupe = 1
                                board[row_num + 1][case_num - 2].occupe = 1
                                case.couleur = active_L.couleur
                                board[row_num + 1][case_num - 1].couleur = active_L.couleur
                                board[row_num + 1][case_num - 2].couleur = active_L.couleur
    active_L = None
    # for row in board:
    #    for case in row:
    #        print(case.couleur)
    #initialise les boutton dans le jeu et les options ingame
    restart_button = Button(image=fond_bouton3, pos=(1000, 60),
                            text_input="RESTART", font=pygame.font.Font(None, 48), base_color="White",
                            hovering_color="White", image_scale=[180, 70], hov_image=fond_bouton4)
    optionjeu_button = Button2(image=option_jeu_button_image, pos=(1185, 62), hovering_image=option_jeu_button_image)
    # appelle pour les options
    quit_button = Button2(image=quit_button_image, pos=(608, 555), hovering_image=quit_button_image)
    music_plus_button = Button2(image=music_plus_button_image, pos=(820 + 84, 470 - 138),
                                hovering_image=music_plus_button_image)
    music_moins_button = Button2(image=music_moins_button_image, pos=(440 + 84, 467 - 135),
                                 hovering_image=music_moins_button_image)
    music_button = Button2(image=music_on_button_image, pos=(750 - 165, 315 - 85),
                           hovering_image=music_off_button_image)
    sound_text = Text(pos=(265, 202), text_input='Music :', font=pygame.font.Font(None, 75), base_color='White')
    volume_text = Text(pos=(265, 295), text_input='Volume :', font=pygame.font.Font(None, 75), base_color='White')
    home_bouton = Button(image=fond_bouton3, pos=(345, 415),
                         text_input="HOME", font=pygame.font.Font(None, 48), base_color="White",
                         hovering_color="White", image_scale=[180, 70], hov_image=fond_bouton4)
    #victoire
    fondvictoire = pygame.image.load("../images/gagner.png").convert_alpha()
    homebtn = pygame.image.load("../images/homeBtn.png").convert_alpha()
    backarrow = pygame.image.load("../images/backarrow.png").convert_alpha()
    backarrowbtn = Button(image=backarrow, pos=(700, 430), text_input="", font=pygame.font.Font(None, 75),
                          base_color="White", hovering_color="Red", image_scale=[80, 80])
    homebtnn = Button(image=homebtn, pos=(550, 430), text_input="", font=pygame.font.Font(None, 75), base_color="White",
                      hovering_color="Red", image_scale=[80, 80])
    tablvictoire = Button(image=fondvictoire, pos=(640, 360), text_input="", font=pygame.font.Font(None, 75),
                          base_color="White", hovering_color="Red", image_scale=[545, 400])
    nom_text = Text(pos=(440, 323), text_input='Name :', font=pygame.font.Font(None, 50), base_color='White')



    gagner1 = pygame.font.Font(None, 40).render("YOU WON", True, (0, 0, 0))  # texte main menu en marron clair
    gagner_rect = gagner1.get_rect(center=(640, 200 + 10))


    box_saisie = pygame.Rect(555, 315, 200, 50)
    color_inactive = (0, 0, 0)
    color_active = (255, 128, 0)
    color = color_inactive
    active = False
    nom = ''



    if music == 'off':
        music_button.image = music_off_button_image
    jeu_cour = True

    while True:
        #permet d'afficher la fenetre appelé jeu
        pygame.display.set_caption("Jeu")
        #permet afficher les image
        screen.blit(fond_jeu, (0, 0))
        screen.blit(hippopotame1.image, hippopotame1.rect)
        screen.blit(hippopotame2.image, hippopotame2.rect)
        screen.blit(lion1.image, lion1.rect)
        screen.blit(elephant1.image, elephant1.rect)
        screen.blit(girafe1.image, girafe1.rect)
        screen.blit(zebre1.image, zebre1.rect)
        screen.blit(zebre2.image, zebre2.rect)

        optionjeu_button.update2(screen)

        restart_button.changeColor(pygame.mouse.get_pos())
        restart_button.update(screen)

        # Dessine les objets en forme de L
        for l_object in all_l_objects:  # Boucle à travers tous les objets L.
            screen.blit(l_object.imaged, l_object.rectd)
            screen.blit(l_object.imageg, l_object.rectg)

        for object in piece_place:  # Boucle à travers tous les objets L.
            if object.type == "el":
                screen.blit(object.imaged, object.rectd)
                screen.blit(object.imageg, object.rectg)

        #fonction ingame
        if running == 0:
            if jeu_cour:
                temps_écoulé = time.time() - start_time - temps_perdu
                minutes = int(temps_écoulé // 60)
                secondes = int(temps_écoulé % 60)
                timer_text = f"{minutes:02}:{secondes:02}"
                timer = pygame.font.Font(None, 50).render(timer_text, True,
                                                          WHITE)  # antialias = plus smooth c est same que convet alpha

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if restart_button.checkForInput(event.pos):  # restart le jeu
                            start_time = time.time()
                            temps_perdu = 0
                            for box in boxes:
                                active_box = box
                                active_box.rect.topleft = active_box.dep_pos
                                if active_box.nom in ["zebre1", "girafe1"] and active_box.place == 1:
                                    if active_box.row_num == 0:
                                        board[active_box.row_num + 1][active_box.case_num + 1].occupe = 0
                                        board[active_box.row_num + 1][active_box.case_num + 1].couleur = None
                                    elif active_box.row_num == 1:
                                        board[active_box.row_num + 1][active_box.case_num].occupe = 0
                                        board[active_box.row_num + 1][active_box.case_num].couleur = None
                                    elif active_box.row_num == 2:
                                        board[active_box.row_num + 1][active_box.case_num - 1].occupe = 0
                                        board[active_box.row_num + 1][active_box.case_num - 1].couleur = None
                                    active_box.case.occupe = 0
                                    active_box.case.couleur = None
                                    active_box.case = None
                                    active_box.case_num = None
                                    active_box.row_num = None
                                    active_box.row = None
                                    active_box.place = 0





                                elif active_box.nom in ["zebre2", "hippopotame2", "lion1",
                                                        "elephant1"] and active_box.place == 1:
                                    active_box.row[active_box.case_num + 1].occupe = 0
                                    active_box.row[active_box.case_num + 1].couleur = None
                                    active_box.case.occupe = 0
                                    active_box.case.couleur = None
                                    active_box.case = None
                                    active_box.case_num = None
                                    active_box.row_num = None
                                    active_box.row = None
                                    active_box.place = 0


                                elif active_box.nom == "hippopotame1" and active_box.place == 1:
                                    active_box.row[active_box.case_num + 1].occupe = 0
                                    active_box.row[active_box.case_num + 1].couleur = None
                                    active_box.row[active_box.case_num + 2].occupe = 0
                                    active_box.row[active_box.case_num + 2].couleur = None
                                    active_box.case.occupe = 0
                                    active_box.case.couleur = None
                                    active_box.case = None
                                    active_box.case_num = None
                                    active_box.row_num = None
                                    active_box.row = None
                                    active_box.place = 0

                            for l_object in all_l_objects:  # Boucle à travers tous les objets L et leurs parties.
                                if l_object.place == 1:
                                    # Vérifie si la position du clic est à l'intérieur de la partie de l'objet L.
                                    active_L = l_object  # Enregistre l'index de l'objet L et de sa partie.ex(0, 1)= (le L numero 0, la partie basse 1)
                                    active_L.rectg.topleft = active_L.pos_deb2
                                    active_L.rectd.topleft = active_L.pos_deb1

                                    if active_L.row_num == 0:
                                        if active_L.nom == "girafe2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None

                                        elif active_L.nom == "lion2":
                                            active_L.case.occupe = 0
                                            active_L.row[active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            active_L.case.couleur = None
                                            active_L.row[active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None

                                        elif active_L.nom == "elephant2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 2].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 2].couleur = None


                                    elif active_L.row_num == 1:
                                        if active_L.nom == "girafe2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None

                                        elif active_L.nom == "lion2":
                                            active_L.case.occupe = 0
                                            active_L.row[active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            active_L.case.couleur = None
                                            active_L.row[active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None

                                        elif active_L.nom == "elephant2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None


                                    elif active_L.row_num == 2:
                                        if active_L.nom == "girafe2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 2].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 2].couleur = None

                                        elif active_L.nom == "lion2":
                                            active_L.case.occupe = 0
                                            active_L.row[active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            active_L.case.couleur = None
                                            active_L.row[active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None

                                        elif active_L.nom == "elephant2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None
                                    active_L.case = None
                                    active_L.case_num = None
                                    active_L.row_num = None
                                    active_L.row = None
                                    active_L.place = 0

                            active_L = None
                        if optionjeu_button.rect.collidepoint(pygame.mouse.get_pos()):
                            print("option")
                            running = 1
                            moment_appuie = time.time()
                        for box in boxes:
                            if box.rect.collidepoint(event.pos):
                                active_box = box
                                active_box.rect.topleft = event.pos
                                if active_box.nom in ["zebre1", "girafe1"] and active_box.place == 1:
                                    if active_box.row_num == 0:
                                        board[active_box.row_num + 1][active_box.case_num + 1].occupe = 0
                                        board[active_box.row_num + 1][active_box.case_num + 1].couleur = None
                                    elif active_box.row_num == 1:
                                        board[active_box.row_num + 1][active_box.case_num].occupe = 0
                                        board[active_box.row_num + 1][active_box.case_num].couleur = None
                                    elif active_box.row_num == 2:
                                        board[active_box.row_num + 1][active_box.case_num - 1].occupe = 0
                                        board[active_box.row_num + 1][active_box.case_num - 1].couleur = None
                                    active_box.case.occupe = 0
                                    active_box.case.couleur = None
                                    active_box.case = None
                                    active_box.case_num = None
                                    active_box.row_num = None
                                    active_box.row = None
                                    active_box.place = 0





                                elif active_box.nom in ["zebre2", "hippopotame2", "lion1",
                                                        "elephant1"] and active_box.place == 1:
                                    active_box.row[active_box.case_num + 1].occupe = 0
                                    active_box.row[active_box.case_num + 1].couleur = None
                                    active_box.case.occupe = 0
                                    active_box.case.couleur = None
                                    active_box.case = None
                                    active_box.case_num = None
                                    active_box.row_num = None
                                    active_box.row = None
                                    active_box.place = 0


                                elif active_box.nom == "hippopotame1" and active_box.place == 1:
                                    active_box.row[active_box.case_num + 1].occupe = 0
                                    active_box.row[active_box.case_num + 1].couleur = None
                                    active_box.row[active_box.case_num + 2].occupe = 0
                                    active_box.row[active_box.case_num + 2].couleur = None
                                    active_box.case.occupe = 0
                                    active_box.case.couleur = None
                                    active_box.case = None
                                    active_box.case_num = None
                                    active_box.row_num = None
                                    active_box.row = None
                                    active_box.place = 0

                        if active_box == None:
                            for l_object in all_l_objects:  # Boucle à travers tous les objets L et leurs parties.
                                if l_object.rectd.collidepoint(event.pos) or l_object.rectg.collidepoint(
                                        event.pos):  # Vérifie si la position du clic est à l'intérieur de la partie de l'objet L.
                                    active_L = l_object  # Enregistre l'index de l'objet L et de sa partie.ex(0, 1)= (le L numero 0, la partie basse 1)
                                    if active_L.nom == "lion2":
                                        active_L.rectg.topleft = event.pos
                                        active_L.rectd.topleft = (event.pos[0] + 84, event.pos[1])
                                    elif active_L.nom == "elephant2":
                                        active_L.rectg.topleft = event.pos
                                        active_L.rectd.topleft = (event.pos[0] + 84, event.pos[1] + 105)
                                    elif active_L.nom == "girafe2":
                                        active_L.rectd.topright = event.pos
                                        active_L.rectg.topright = (event.pos[0] - 84, event.pos[1] + 105)

                                    if active_L.row_num == 0:
                                        if active_L.nom == "girafe2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None

                                        elif active_L.nom == "lion2":
                                            active_L.case.occupe = 0
                                            active_L.row[active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            active_L.case.couleur = None
                                            active_L.row[active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None

                                        elif active_L.nom == "elephant2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 2].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 2].couleur = None


                                    elif active_L.row_num == 1:
                                        if active_L.nom == "girafe2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None

                                        elif active_L.nom == "lion2":
                                            active_L.case.occupe = 0
                                            active_L.row[active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            active_L.case.couleur = None
                                            active_L.row[active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None

                                        elif active_L.nom == "elephant2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num + 1].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num + 1].couleur = None


                                    elif active_L.row_num == 2:
                                        if active_L.nom == "girafe2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 2].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 2].couleur = None

                                        elif active_L.nom == "lion2":
                                            active_L.case.occupe = 0
                                            active_L.row[active_L.case_num + 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            active_L.case.couleur = None
                                            active_L.row[active_L.case_num + 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None

                                        elif active_L.nom == "elephant2":
                                            active_L.case.occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num - 1].occupe = 0
                                            board[active_L.row_num + 1][active_L.case_num].occupe = 0
                                            active_L.case.couleur = None
                                            board[active_L.row_num + 1][active_L.case_num - 1].couleur = None
                                            board[active_L.row_num + 1][active_L.case_num].couleur = None
                                    active_L.case = None
                                    active_L.case_num = None
                                    active_L.row_num = None
                                    active_L.row = None
                                    active_L.place = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if active_box != None:  # Check if active_box is not None
                            for row_num, row in enumerate(board):
                                for case_num, case in enumerate(row):
                                    if case.collidepoint(event.pos):
                                        if active_box.nom in ["zebre1", "girafe1"]:
                                            active_box.rect.topleft = case.topleft
                                            for limite in limites:
                                                if active_box.rect.colliderect(limite):
                                                    active_box.rect.topleft = active_box.dep_pos
                                                    break
                                            if active_box.rect.topleft != active_box.dep_pos:
                                                if row_num == 0:
                                                    if case.occupe == 0 and board[row_num + 1][
                                                        case_num + 1].occupe == 0:
                                                        board[row_num + 1][case_num + 1].occupe = 1
                                                        board[row_num + 1][case_num + 1].couleur = active_box.couleur
                                                        case.occupe = 1
                                                        case.couleur = active_box.couleur
                                                        active_box.rect.topleft = case.topleft
                                                        case.couleur = active_box.couleur
                                                        active_box.case = case
                                                        active_box.case_num = case_num
                                                        active_box.row_num = row_num
                                                        active_box.row = row
                                                        active_box.place = 1
                                                    else:
                                                        # Space is already occupied, reset the piece position
                                                        active_box.rect.topleft = active_box.dep_pos
                                                elif row_num == 1:
                                                    if case.occupe == 0 and board[row_num + 1][case_num].occupe == 0:
                                                        board[row_num + 1][case_num].occupe = 1
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num].couleur = active_box.couleur
                                                        case.couleur = active_box.couleur
                                                        active_box.rect.topleft = case.topleft
                                                        active_box.case = case
                                                        active_box.case_num = case_num
                                                        active_box.row_num = row_num
                                                        active_box.row = row
                                                        active_box.place = 1
                                                    else:
                                                        # Space is already occupied, reset the piece position
                                                        active_box.rect.topleft = active_box.dep_pos
                                                elif row_num == 2:
                                                    if case.occupe == 0 and board[row_num + 1][
                                                        case_num - 1].occupe == 0:
                                                        board[row_num + 1][case_num - 1].occupe = 1
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num - 1].couleur = active_box.couleur
                                                        case.couleur = active_box.couleur
                                                        active_box.rect.topleft = case.topleft
                                                        active_box.case = case
                                                        active_box.case_num = case_num
                                                        active_box.row_num = row_num
                                                        active_box.row = row
                                                        active_box.place = 1
                                                    else:
                                                        # Space is already occupied, reset the piece position
                                                        active_box.rect.topleft = active_box.dep_pos

                                        elif active_box.nom in ["zebre2", "hippopotame2", "lion1", "elephant1"]:
                                            active_box.rect.topleft = case.topleft
                                            for limite in limites:
                                                if active_box.rect.colliderect(limite):
                                                    active_box.rect.topleft = active_box.dep_pos
                                                    break
                                            if active_box.rect.topleft != active_box.dep_pos:
                                                if case.occupe == 0 and row[case_num + 1].occupe == 0:
                                                    active_box.rect.topleft = case.topleft
                                                    row[case_num + 1].occupe = 1
                                                    case.occupe = 1
                                                    row[case_num + 1].couleur = active_box.couleur
                                                    case.couleur = active_box.couleur
                                                    active_box.case = case
                                                    active_box.case_num = case_num
                                                    active_box.row_num = row_num
                                                    active_box.row = row
                                                    active_box.place = 1
                                                    active_box.case.couleur = active_box.couleur
                                                else:
                                                    # Space is already occupied, reset the piece position
                                                    active_box.rect.topleft = active_box.dep_pos

                                        elif active_box.nom == "hippopotame1":
                                            active_box.rect.topleft = case.topleft
                                            for limite in limites:
                                                if active_box.rect.colliderect(limite):
                                                    active_box.rect.topleft = active_box.dep_pos
                                                    break
                                            if active_box.rect.topleft != active_box.dep_pos:
                                                if case.occupe == 0 and row[case_num + 1].occupe == 0 and row[
                                                    case_num + 2].occupe == 0:
                                                    row[case_num + 1].occupe = 1
                                                    case.occupe = 1
                                                    row[case_num + 2].occupe = 1
                                                    row[case_num + 1].couleur = active_box.couleur
                                                    case.couleur = active_box.couleur
                                                    row[case_num + 2].couleur = active_box.couleur
                                                    active_box.case = case
                                                    active_box.case_num = case_num
                                                    active_box.row_num = row_num
                                                    active_box.row = row
                                                    active_box.place = 1
                                                    active_box.case.couleur = active_box.couleur
                                                else:
                                                    # Space is already occupied, reset the piece position
                                                    active_box.rect.topleft = active_box.dep_pos

                                            # Mark the space as occupied
                                        else:
                                            # Space is already occupied, reset the piece position
                                            active_box.rect.topleft = active_box.dep_pos
                                            # Set active_box to None after updating
                                            break
                            if active_box.place == 0:
                                active_box.rect.topleft = active_box.dep_pos
                            active_box = None

                        elif active_L != None:
                            for row_num, row in enumerate(board):
                                for case_num, case in enumerate(row):
                                    if case.collidepoint(event.pos):
                                        if case.occupe != 1:
                                            if active_L.nom == "girafe2":
                                                active_L.rectd.topright = case.topright
                                                active_L.rectg.topright = case.bottomleft
                                            if active_L.nom == "lion2":
                                                active_L.rectg.topleft = case.topleft
                                                active_L.rectd.topleft = case.topright
                                            if active_L.nom == "elephant2":
                                                active_L.rectg.topleft = case.topleft
                                                active_L.rectd.topleft = case.bottomright
                                            for limite in limites:
                                                if active_L.rectd.colliderect(limite) or active_L.rectg.colliderect(
                                                        limite):
                                                    active_L.rectg.topleft = active_L.pos_deb2
                                                    active_L.rectd.topleft = active_L.pos_deb1
                                                    break
                                            if active_L.rectg.topleft != active_L.pos_deb2:
                                                if row_num == 0:
                                                    if active_L.nom == "girafe2" and board[row_num + 1][
                                                        case_num + 1].occupe == 0 and board[row_num + 1][
                                                        case_num].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectd.topright = case.topright
                                                        # active_L.rectg.topleft = (case.bottomleft[0] - 84, case.bottomleft[1])
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num + 1].occupe = 1
                                                        board[row_num + 1][case_num].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        board[row_num + 1][case_num + 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num].couleur = active_L.couleur

                                                    elif active_L.nom == "lion2" and row[case_num + 1].occupe == 0 and \
                                                            board[row_num + 1][case_num + 1].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectg.topleft = case.topleft
                                                        # active_L.rectd.topleft = (case.topleft[0] + 84, case.topleft[1])
                                                        case.occupe = 1
                                                        row[case_num + 1].occupe = 1
                                                        board[row_num + 1][case_num + 1].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        row[case_num + 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num + 1].couleur = active_L.couleur

                                                    elif active_L.nom == "elephant2" and board[row_num + 1][
                                                        case_num + 1].occupe == 0 and board[row_num + 1][
                                                        case_num + 2].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectg.topleft = case.topleft
                                                        # active_L.rectd.topleft = (case.bottomright[0], case.bottomright[1])
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num + 1].occupe = 1
                                                        board[row_num + 1][case_num + 2].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        board[row_num + 1][case_num + 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num + 2].couleur = active_L.couleur

                                                    else:
                                                        active_L.rectg.topleft = active_L.pos_deb2
                                                        active_L.rectd.topleft = active_L.pos_deb1
                                                        active_L.place = 0

                                                elif row_num == 1:
                                                    if active_L.nom == "girafe2" and board[row_num + 1][
                                                        case_num].occupe == 0 and \
                                                            board[row_num + 1][case_num - 1].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectd.topright = case.topright
                                                        # active_L.rectg.topleft = (case.bottomleft[0] - 84, case.bottomleft[1])
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num].occupe = 1
                                                        board[row_num + 1][case_num - 1].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        board[row_num + 1][case_num].couleur = active_L.couleur
                                                        board[row_num + 1][case_num - 1].couleur = active_L.couleur

                                                    elif active_L.nom == "lion2" and row[case_num + 1].occupe == 0 and \
                                                            board[row_num + 1][case_num].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectg.topleft = case.topleft
                                                        # active_L.rectd.topleft = (case.topleft[0] + 84, case.topleft[1])
                                                        case.occupe = 1
                                                        row[case_num + 1].occupe = 1
                                                        board[row_num + 1][case_num].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        row[case_num + 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num].couleur = active_L.couleur

                                                    elif active_L.nom == "elephant2" and board[row_num + 1][
                                                        case_num].occupe == 0 and board[row_num + 1][
                                                        case_num + 1].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectg.topleft = case.topleft
                                                        # active_L.rectd.topleft = (case.bottomright[0], case.bottomright[1])
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num].occupe = 1
                                                        board[row_num + 1][case_num + 1].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        board[row_num + 1][case_num].couleur = active_L.couleur
                                                        board[row_num + 1][case_num + 1].couleur = active_L.couleur

                                                    else:
                                                        active_L.rectg.topleft = active_L.pos_deb2
                                                        active_L.rectd.topleft = active_L.pos_deb1
                                                        active_L.place = 0

                                                elif row_num == 2:
                                                    if active_L.nom == "girafe2" and board[row_num + 1][
                                                        case_num - 1].occupe == 0 and \
                                                            board[row_num + 1][case_num - 2].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectd.topright = case.topright
                                                        # active_L.rectg.topleft = (case.bottomleft[0] - 84, case.bottomleft[1])
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num - 1].occupe = 1
                                                        board[row_num + 1][case_num - 2].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        board[row_num + 1][case_num - 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num - 2].couleur = active_L.couleur

                                                    elif active_L.nom == "lion2" and row[case_num + 1].occupe == 0 and \
                                                            row[
                                                                case_num + 1].occupe == 0 and \
                                                            board[row_num + 1][case_num - 1].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectg.topleft = case.topleft
                                                        # active_L.rectd.topleft = (case.topleft[0] + 84, case.topleft[1])
                                                        case.occupe = 1
                                                        row[case_num + 1].occupe = 1
                                                        board[row_num + 1][case_num - 1].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        row[case_num + 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num - 1].couleur = active_L.couleur

                                                    elif active_L.nom == "elephant2" and board[row_num + 1][
                                                        case_num - 1].occupe == 0 and board[row_num + 1][
                                                        case_num].occupe == 0:
                                                        active_L.case = case
                                                        active_L.case_num = case_num
                                                        active_L.row_num = row_num
                                                        active_L.row = row
                                                        active_L.place = 1
                                                        # active_L.rectg.topleft = case.topleft
                                                        # active_L.rectd.topleft = (case.bottomright[0], case.bottomright[1])
                                                        case.occupe = 1
                                                        board[row_num + 1][case_num - 1].occupe = 1
                                                        board[row_num + 1][case_num].occupe = 1
                                                        case.couleur = active_L.couleur
                                                        board[row_num + 1][case_num - 1].couleur = active_L.couleur
                                                        board[row_num + 1][case_num].couleur = active_L.couleur

                                                    else:
                                                        active_L.rectg.topleft = active_L.pos_deb2
                                                        active_L.rectd.topleft = active_L.pos_deb1
                                                        active_L.place = 0
                                                break
                            if active_L.place == 0:
                                active_L.rectg.topleft = active_L.pos_deb2
                                active_L.rectd.topleft = active_L.pos_deb1

                            active_L = None

                        # Réinitialise la partie active à None.

                if event.type == pygame.MOUSEMOTION:
                    if active_box != None:
                        active_box.rect.move_ip(event.rel)
                    if active_L is not None:  # Vérifie s'il y a une partie active en cours de déplacement.
                        active_L.rectg.move_ip(event.rel)
                        active_L.rectd.move_ip(event.rel)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        #Option ingame
        elif running == 1:

            temps_écoulé_pause = time.time() - moment_appuie
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                    if quit_button.rect.collidepoint(
                            pygame.mouse.get_pos()):  # lance le menu options si appuie sur options
                        running = 0
                        temps_perdu += temps_écoulé_pause
                    elif home_bouton.checkForInput(event.pos):
                        piece_place = []
                        boxes = []
                        all_l_objects = []
                        board = []

                        main_menu()
                music_button.on_off_music(pygame.mouse.get_pos(), event)
                music_plus_button.change_volume(pygame.mouse.get_pos(), event)
                music_moins_button.change_volume(pygame.mouse.get_pos(), event)
            # Clear the screen
            screen.blit(option_jeu_back, (40, 40))

            menu_mouse_pos = pygame.mouse.get_pos()

            # Create and render the button
            quit_button.update2(screen)
            sound_text.update3(screen)
            volume_text.update3(screen)
            music_button.update2(screen)
            music_plus_button.update2(screen)
            music_moins_button.update2(screen)
            restart_button.changeColor(pygame.mouse.get_pos())
            home_bouton.update(screen)
            home_bouton.changeColor(pygame.mouse.get_pos())
            pygame.draw.rect(screen, WHITE, (480 + 84, 440 - 135, 300, 60), width=5, border_radius=20)
            volume_bar_width = int(300 * volume)  # Calculate the width of the volume bar based on the volume level
            if volume_bar_width == 300:
                pygame.draw.rect(screen, WHITE, (480 + 84, 440 - 135, volume_bar_width, 60), border_radius=20)
            else:
                pygame.draw.rect(screen, WHITE, (480 + 84, 440 - 135, volume_bar_width, 60), border_top_left_radius=20,
                                 border_bottom_left_radius=20)

        #popup de victoire
        elif running == 2:
            minutes1 = int(win_time // 60)
            secondes1 = int(win_time % 60)
            timer_text = f"time= {minutes1:02}:{secondes1:02}"  # {}=variable 02=format 2 caractères
            timer1 = pygame.font.Font(None, 50).render(timer_text, True, WHITE)
            timer_rect = timer1.get_rect(center=(640, 275))

            tablvictoire.update(screen)
            homebtnn.update(screen)
            backarrowbtn.update(screen)
            screen.blit(timer1, timer_rect)
            screen.blit(gagner1, gagner_rect)
            nom_text.update3(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                    if box_saisie.collidepoint(event.pos):
                        active = True
                    color = color_active if active else color_inactive

                    if homebtnn.checkForInput(pygame.mouse.get_pos()):
                        piece_place = []
                        boxes = []
                        all_l_objects = []
                        board = []

                        date = datetime.today().strftime("%Y-%m-%d")
                        # creation enregistrement
                        jeu = {"joueur": nom,
                               "level": level,
                               "date": date,
                               "resolutionTime": timer_text

                               }
                        # charger données dans fichier
                        with open('../results.json', mode='a') as my_file:
                            json.dump(jeu, my_file)
                            my_file.write('\n')
                        main_menu()

                    if backarrowbtn.checkForInput(pygame.mouse.get_pos()):
                        piece_place = []
                        boxes = []
                        all_l_objects = []
                        board = []

                        date = datetime.today().strftime("%Y-%m-%d")  # formate date anné-mois-jour
                        # creation enregistrement
                        jeu = {"joueur": nom,
                               "level": level,
                               "date": date,
                               "resolutionTime": timer_text
                               }
                        # charger données dans fichier
                        with open('../results.json', mode='a') as my_file:
                            json.dump(jeu, my_file)
                            my_file.write('\n')
                        menu_niveaux()


                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            active = False
                        elif event.key == pygame.K_BACKSPACE:
                            nom = nom[:-1]
                        else:
                            nom += event.unicode

            color = color_active if active else color_inactive
            font = pygame.font.Font(None, 74)
            txt_surface = font.render(nom, True, (255, 255, 255))
            width = max(200, txt_surface.get_width() + 10)
            box_saisie.w = width
            screen.blit(txt_surface, (box_saisie.x + 5, box_saisie.y + 5))
            pygame.draw.rect(screen, color, box_saisie, 2)



        '''
        for row in board:
            for case in row:
                if case.couleur == "bleu":
                    print("marche")'''
        gagné = 0
        #vérification de la couleur des cases autour de 5 cases définies
        for p in boxes + piece_place:
            if p.nom == "hippopotame2" or p.nom == "zebre2" or p.nom == "lion1" or p.nom == "elephant1":
                if p.place == 1:
                    if p.row_num == 0:
                        if p.case_num == 0:
                            # droite et dessous
                            if p.row[p.case_num + 2].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 2].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 1 and p.case_num <= 2:
                            # droite gauche et dessous
                            if p.row[p.case_num - 1].couleur == p.couleur or p.row[
                                p.case_num + 2].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 2].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 3:
                            # gauche et dessous
                            if p.row[p.case_num - 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 2].couleur == p.couleur:
                                gagné += 1

                    elif p.row_num == 1:
                        if p.case_num == 0:
                            # droite et dessous et dessus-droite
                            if p.row[p.case_num + 2].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 1 and p.case_num <= 4:
                            # droite gauche et dessous et dessus same -1
                            if p.row[p.case_num - 1].couleur == p.couleur or p.row[
                                p.case_num + 2].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur \
                                    or board[p.row_num - 1][p.case_num].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num - 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 5:
                            # gauche et dessous et dessus gauche
                            if p.row[p.case_num - 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num - 1].couleur == p.couleur:
                                gagné += 1

                    elif p.row_num == 2:
                        if p.case_num == 0:
                            # droite et dessous droite et dessus
                            if p.row[p.case_num + 2].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num].couleur == p.couleur or \
                                    board[p.row_num - 1][p.case_num + 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 1 and p.case_num <= 4:
                            # droite gauche et dessous et dessus same -1
                            if p.row[p.case_num - 1].couleur == p.couleur or p.row[
                                p.case_num + 2].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num - 1].couleur == p.couleur \
                                    or board[p.row_num - 1][p.case_num].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 5:
                            # gauche et dessous et dessus gauche
                            if p.row[p.case_num - 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num - 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num].couleur == p.couleur:
                                gagné += 1

                    elif p.row_num == 3:
                        if p.case_num == 0:
                            # droite et dessous
                            if p.row[p.case_num + 2].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 2].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 1 and p.case_num <= 2:
                            # droite gauche et dessous
                            if p.row[p.case_num - 1].couleur == p.couleur or p.row[
                                p.case_num + 2].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 2].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 3:
                            # gauche et dessous
                            if p.row[p.case_num - 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num + 2].couleur == p.couleur:
                                gagné += 1

            elif p.nom == "girafe1":
                if p.place == 1:
                    if p.row_num == 0:
                        if p.case_num == 0:
                            # droite et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 2].couleur == p.couleur \
                                    or board[p.row_num + 2][p.case_num + 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 1 and p.case_num <= 3:
                            # droite gauche et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 2].couleur == p.couleur \
                                    or board[p.row_num + 2][p.case_num + 1].couleur == p.couleur or p.row[
                                p.case_num - 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 4:
                            # gauche et dessous
                            if board[p.row_num + 1][p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 2].couleur == p.couleur \
                                    or board[p.row_num + 2][p.case_num + 1].couleur == p.couleur or p.row[
                                p.case_num - 1].couleur == p.couleur:
                                gagné += 1

                    elif p.row_num == 1:
                        if p.case_num == 0:
                            # droite et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num + 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 1 and p.case_num <= 5:
                            # droite gauche et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or p.row[
                                p.case_num - 1].couleur == p.couleur or board[p.row_num - 1][
                                p.case_num - 1].couleur == p.couleur \
                                    or board[p.row_num + 2][p.case_num - 1].couleur == p.couleur or \
                                    board[p.row_num + 1][p.case_num - 1].couleur == p.couleur \
                                    or board[p.row_num + 1][p.case_num + 1].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 6:
                            # gauche et dessous
                            if p.row[p.case_num - 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num - 1].couleur == p.couleur:
                                gagné += 1

                    elif p.row_num == 2:
                        if p.case_num == 1:
                            # droite et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or p.row[p.case_num - 1].couleur == p.couleur \
                                    or board[p.row_num - 1][p.case_num].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num >= 2 and p.case_num <= 4:
                            # droite gauche et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num].couleur == p.couleur or p.row[p.case_num - 1].couleur == p.couleur \
                                    or board[p.row_num - 1][p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num - 2].couleur == p.couleur:
                                gagné += 1
                        elif p.case_num == 5:
                            # gauche et dessous
                            if p.row[p.case_num + 1].couleur == p.couleur or p.row[p.case_num - 1].couleur == p.couleur \
                                    or board[p.row_num - 1][p.case_num].couleur == p.couleur or board[p.row_num + 1][
                                p.case_num - 2].couleur == p.couleur:
                                gagné += 1

        # print (gagné)
        if gagné == 5:
            time.sleep(1)
            win_time = temps_écoulé
            jeu_cour = False
            if bien_joué == 0:
                win_sound.play(loops=0)
                bien_joué = 1
                running = 2



        screen.blit(timer, (1138, 660))
        clock.tick(60)
        pygame.display.update()


def menu_niveaux():
    pygame.display.set_caption("Niveaux")

    while True:
        screen.blit(fond_menu, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        facile = pygame.font.Font(None, 40).render("EASY", True, (0, 0, 0))  # texte main menu en marron clair
        facile_rect = facile.get_rect(center=(640, 50))
        moyen = pygame.font.Font(None, 40).render("MEDIUM", True, (0, 0, 0))  # texte main menu en marron clair
        moyen_rect = moyen.get_rect(center=(640, 220))
        difficile = pygame.font.Font(None, 40).render("HARD", True, (0, 0, 0))  # texte main menu en marron clair
        difficile_rect = difficile.get_rect(center=(640, 390))
        extreme = pygame.font.Font(None, 40).render("EXTREME", True, (0, 0, 0))  # texte main menu en marron clair
        extreme_rect = extreme.get_rect(center=(640, 560))
        screen.blit(extreme, extreme_rect)
        screen.blit(difficile, difficile_rect)
        screen.blit(moyen, moyen_rect)
        screen.blit(facile, facile_rect)
        _1b = Button(image=fond_bouton, pos=(100 + 35, 100), text_input="1", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _2b = Button(image=fond_bouton, pos=(300 + 35, 100), text_input="2", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _3b = Button(image=fond_bouton, pos=(500 + 35, 100), text_input="3", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _4b = Button(image=fond_bouton, pos=(700 + 35, 100), text_input="4", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _5b = Button(image=fond_bouton, pos=(900 + 35, 100), text_input="5", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _6b = Button(image=fond_bouton, pos=(1100 + 35, 100), text_input="6", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _7b = Button(image=fond_bouton, pos=(100 + 35, 170), text_input="7", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _8b = Button(image=fond_bouton, pos=(300 + 35, 170), text_input="8", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _9b = Button(image=fond_bouton, pos=(500 + 35, 170), text_input="9", font=pygame.font.Font(None, 75),
                     base_color="White", hovering_color="Red", image_scale=[145, 50])
        _10b = Button(image=fond_bouton, pos=(700 + 35, 170), text_input="10", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _11b = Button(image=fond_bouton, pos=(900 + 35, 170), text_input="11", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _12b = Button(image=fond_bouton, pos=(1100 + 35, 170), text_input="12", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _13b = Button(image=fond_bouton, pos=(100 + 35, 270), text_input="13", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _14b = Button(image=fond_bouton, pos=(300 + 35, 270), text_input="14", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _15b = Button(image=fond_bouton, pos=(500 + 35, 270), text_input="15", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _16b = Button(image=fond_bouton, pos=(700 + 35, 270), text_input="16", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _17b = Button(image=fond_bouton, pos=(900 + 35, 270), text_input="17", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _18b = Button(image=fond_bouton, pos=(1100 + 35, 270), text_input="18", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _19b = Button(image=fond_bouton, pos=(100 + 35, 340), text_input="19", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _20b = Button(image=fond_bouton, pos=(300 + 35, 340), text_input="20", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _21b = Button(image=fond_bouton, pos=(500 + 35, 340), text_input="21", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _22b = Button(image=fond_bouton, pos=(700 + 35, 340), text_input="22", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _23b = Button(image=fond_bouton, pos=(900 + 35, 340), text_input="23", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _24b = Button(image=fond_bouton, pos=(1100 + 35, 340), text_input="24", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _25b = Button(image=fond_bouton, pos=(100 + 35, 440), text_input="25", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _26b = Button(image=fond_bouton, pos=(300 + 35, 440), text_input="26", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _27b = Button(image=fond_bouton, pos=(500 + 35, 440), text_input="27", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _28b = Button(image=fond_bouton, pos=(700 + 35, 440), text_input="28", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _29b = Button(image=fond_bouton, pos=(900 + 35, 440), text_input="29", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _30b = Button(image=fond_bouton, pos=(1100 + 35, 440), text_input="30", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _31b = Button(image=fond_bouton, pos=(100 + 35, 510), text_input="31", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _32b = Button(image=fond_bouton, pos=(300 + 35, 510), text_input="32", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _33b = Button(image=fond_bouton, pos=(500 + 35, 510), text_input="33", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _34b = Button(image=fond_bouton, pos=(700 + 35, 510), text_input="34", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _35b = Button(image=fond_bouton, pos=(900 + 35, 510), text_input="35", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _36b = Button(image=fond_bouton, pos=(1100 + 35, 510), text_input="36", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _37b = Button(image=fond_bouton, pos=(100 + 35, 610), text_input="37", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _38b = Button(image=fond_bouton, pos=(300 + 35, 610), text_input="38", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _39b = Button(image=fond_bouton, pos=(500 + 35, 610), text_input="39", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _40b = Button(image=fond_bouton, pos=(700 + 35, 610), text_input="40", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _41b = Button(image=fond_bouton, pos=(900 + 35, 610), text_input="41", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _42b = Button(image=fond_bouton, pos=(1100 + 35, 610), text_input="42", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _43b = Button(image=fond_bouton, pos=(100 + 35, 680), text_input="43", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _44b = Button(image=fond_bouton, pos=(300 + 35, 680), text_input="44", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _45b = Button(image=fond_bouton, pos=(500 + 35, 680), text_input="45", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _46b = Button(image=fond_bouton, pos=(700 + 35, 680), text_input="46", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _47b = Button(image=fond_bouton, pos=(900 + 35, 680), text_input="47", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _48b = Button(image=fond_bouton, pos=(1100 + 35, 680), text_input="48", font=pygame.font.Font(None, 75),
                      base_color="White", hovering_color="Red", image_scale=[145, 50])
        _1b.changeColor(menu_mouse_pos)
        _1b.update(screen)
        _2b.changeColor(menu_mouse_pos)
        _2b.update(screen)
        _3b.changeColor(menu_mouse_pos)
        _3b.update(screen)
        _4b.changeColor(menu_mouse_pos)
        _4b.update(screen)
        _5b.changeColor(menu_mouse_pos)
        _5b.update(screen)
        _6b.changeColor(menu_mouse_pos)
        _6b.update(screen)
        _7b.changeColor(menu_mouse_pos)
        _7b.update(screen)
        _8b.changeColor(menu_mouse_pos)
        _8b.update(screen)
        _9b.changeColor(menu_mouse_pos)
        _9b.update(screen)
        _10b.changeColor(menu_mouse_pos)
        _10b.update(screen)
        _11b.changeColor(menu_mouse_pos)
        _12b.changeColor(menu_mouse_pos)
        _13b.changeColor(menu_mouse_pos)
        _14b.changeColor(menu_mouse_pos)
        _15b.changeColor(menu_mouse_pos)
        _16b.changeColor(menu_mouse_pos)
        _17b.changeColor(menu_mouse_pos)
        _18b.changeColor(menu_mouse_pos)
        _19b.changeColor(menu_mouse_pos)
        _20b.changeColor(menu_mouse_pos)
        _21b.changeColor(menu_mouse_pos)
        _22b.changeColor(menu_mouse_pos)
        _23b.changeColor(menu_mouse_pos)
        _24b.changeColor(menu_mouse_pos)
        _25b.changeColor(menu_mouse_pos)
        _26b.changeColor(menu_mouse_pos)
        _27b.changeColor(menu_mouse_pos)
        _28b.changeColor(menu_mouse_pos)
        _29b.changeColor(menu_mouse_pos)
        _30b.changeColor(menu_mouse_pos)
        _31b.changeColor(menu_mouse_pos)
        _32b.changeColor(menu_mouse_pos)
        _33b.changeColor(menu_mouse_pos)
        _34b.changeColor(menu_mouse_pos)
        _35b.changeColor(menu_mouse_pos)
        _36b.changeColor(menu_mouse_pos)
        _37b.changeColor(menu_mouse_pos)
        _38b.changeColor(menu_mouse_pos)
        _39b.changeColor(menu_mouse_pos)
        _40b.changeColor(menu_mouse_pos)
        _41b.changeColor(menu_mouse_pos)
        _42b.changeColor(menu_mouse_pos)
        _43b.changeColor(menu_mouse_pos)
        _44b.changeColor(menu_mouse_pos)
        _45b.changeColor(menu_mouse_pos)
        _46b.changeColor(menu_mouse_pos)
        _47b.changeColor(menu_mouse_pos)
        _48b.changeColor(menu_mouse_pos)
        _11b.update(screen)
        _12b.update(screen)
        _13b.update(screen)
        _14b.update(screen)
        _15b.update(screen)
        _16b.update(screen)
        _17b.update(screen)
        _18b.update(screen)
        _19b.update(screen)
        _20b.update(screen)
        _21b.update(screen)
        _22b.update(screen)
        _23b.update(screen)
        _24b.update(screen)
        _25b.update(screen)
        _26b.update(screen)
        _27b.update(screen)
        _28b.update(screen)
        _29b.update(screen)
        _30b.update(screen)
        _31b.update(screen)
        _32b.update(screen)
        _33b.update(screen)
        _34b.update(screen)
        _35b.update(screen)
        _36b.update(screen)
        _37b.update(screen)
        _38b.update(screen)
        _39b.update(screen)
        _40b.update(screen)
        _41b.update(screen)
        _42b.update(screen)
        _43b.update(screen)
        _44b.update(screen)
        _45b.update(screen)
        _46b.update(screen)
        _47b.update(screen)
        _48b.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # si appui sur la croix
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                if _1b.checkForInput(menu_mouse_pos):
                    global niv
                    global level
                    niv = n.niveau1()
                    level = 1
                    jeu()
                if _2b.checkForInput(menu_mouse_pos):
                    niv = n.niveau2()
                    level = 2
                    jeu()
                if _3b.checkForInput(menu_mouse_pos):
                    niv = n.niveau3()
                    level = 3
                    jeu()
                if _4b.checkForInput(menu_mouse_pos):
                    niv = n.niveau4()
                    level = 4
                    jeu()
                if _5b.checkForInput(menu_mouse_pos):
                    niv = n.niveau5()
                    level = 5
                    jeu()
                if _6b.checkForInput(menu_mouse_pos):
                    niv = n.niveau6()
                    level = 6
                    jeu()
                if _7b.checkForInput(menu_mouse_pos):
                    niv = n.niveau7()
                    level = 7
                    jeu()
                if _8b.checkForInput(menu_mouse_pos):
                    niv = n.niveau8()
                    level = 8
                    jeu()
                if _9b.checkForInput(menu_mouse_pos):
                    niv = n.niveau9()
                    level = 9
                    jeu()
                if _10b.checkForInput(menu_mouse_pos):
                    niv = n.niveau10()
                    level = 10
                    jeu()
                if _11b.checkForInput(menu_mouse_pos):
                    niv = n.niveau11()
                    level = 11
                    jeu()
                if _12b.checkForInput(menu_mouse_pos):
                    niv = n.niveau12()
                    level = 12
                    jeu()
                if _13b.checkForInput(menu_mouse_pos):
                    niv = n.niveau13()
                    level = 13
                    jeu()
                if _14b.checkForInput(menu_mouse_pos):
                    niv = n.niveau14()
                    level = 14
                    jeu()
                if _15b.checkForInput(menu_mouse_pos):
                    niv = n.niveau15()
                    level = 15
                    jeu()
                if _16b.checkForInput(menu_mouse_pos):
                    niv = n.niveau16()
                    level = 16
                    jeu()
                if _17b.checkForInput(menu_mouse_pos):
                    niv = n.niveau17()
                    level = 17
                    jeu()
                if _18b.checkForInput(menu_mouse_pos):
                    niv = n.niveau18()
                    level = 18
                    jeu()
                if _19b.checkForInput(menu_mouse_pos):
                    niv = n.niveau19()
                    level = 19
                    jeu()
                if _20b.checkForInput(menu_mouse_pos):
                    niv = n.niveau20()
                    level = 20
                    jeu()
                if _21b.checkForInput(menu_mouse_pos):
                    niv = n.niveau21()
                    level = 21
                    jeu()
                if _22b.checkForInput(menu_mouse_pos):
                    niv = n.niveau22()
                    level = 22
                    jeu()
                if _23b.checkForInput(menu_mouse_pos):
                    niv = n.niveau23()
                    level = 23
                    jeu()
                if _24b.checkForInput(menu_mouse_pos):
                    niv = n.niveau24()
                    level = 24
                    jeu()
                if _25b.checkForInput(menu_mouse_pos):
                    niv = n.niveau25()
                    level = 25
                    jeu()
                if _26b.checkForInput(menu_mouse_pos):
                    niv = n.niveau26()
                    level = 26
                    jeu()
                if _27b.checkForInput(menu_mouse_pos):
                    niv = n.niveau27()
                    level = 27
                    jeu()
                if _28b.checkForInput(menu_mouse_pos):
                    niv = n.niveau28()
                    level = 28
                    jeu()
                if _29b.checkForInput(menu_mouse_pos):
                    niv = n.niveau29()
                    level = 29
                    jeu()
                if _30b.checkForInput(menu_mouse_pos):
                    niv = n.niveau30()
                    level = 30
                    jeu()
                if _31b.checkForInput(menu_mouse_pos):
                    niv = n.niveau31()
                    level = 31
                    jeu()
                if _32b.checkForInput(menu_mouse_pos):
                    niv = n.niveau32()
                    level = 32
                    jeu()
                if _33b.checkForInput(menu_mouse_pos):
                    niv = n.niveau33()
                    level = 33
                    jeu()
                if _34b.checkForInput(menu_mouse_pos):
                    niv = n.niveau34()
                    level = 34
                    jeu()
                if _35b.checkForInput(menu_mouse_pos):
                    niv = n.niveau35()
                    level = 35
                    jeu()
                if _36b.checkForInput(menu_mouse_pos):
                    niv = n.niveau36()
                    level = 36
                    jeu()
                if _37b.checkForInput(menu_mouse_pos):
                    niv = n.niveau37()
                    level = 37
                    jeu()
                if _38b.checkForInput(menu_mouse_pos):
                    niv = n.niveau38()
                    level = 38
                    jeu()
                if _39b.checkForInput(menu_mouse_pos):
                    niv = n.niveau39()
                    level = 39
                    jeu()
                if _40b.checkForInput(menu_mouse_pos):
                    niv = n.niveau40()
                    level = 40
                    jeu()
                if _41b.checkForInput(menu_mouse_pos):
                    niv = n.niveau41()
                    level = 41
                    jeu()
                if _42b.checkForInput(menu_mouse_pos):
                    niv = n.niveau42()
                    level = 42
                    jeu()
                if _43b.checkForInput(menu_mouse_pos):
                    niv = n.niveau43()
                    level = 43
                    jeu()
                if _44b.checkForInput(menu_mouse_pos):
                    niv = n.niveau44()
                    level = 44
                    jeu()
                if _45b.checkForInput(menu_mouse_pos):
                    niv = n.niveau45()
                    level = 45
                    jeu()
                if _46b.checkForInput(menu_mouse_pos):
                    niv = n.niveau46()
                    level = 46
                    jeu()
                if _47b.checkForInput(menu_mouse_pos):
                    niv = n.niveau47()
                    level = 47
                    jeu()
                if _48b.checkForInput(menu_mouse_pos):
                    niv = n.niveau48()
                    level = 48
                    jeu()

        pygame.display.update()


def option():
    pygame.display.set_caption("Options")

    menu_mouse_pos = pygame.mouse.get_pos()
    quit_button = Button2(image=quit_button_image, pos=(638, 615), hovering_image=quit_button_image)
    music_plus_button = Button2(image=music_plus_button_image, pos=(820, 470), hovering_image=music_plus_button_image)
    music_moins_button = Button2(image=music_moins_button_image, pos=(440, 467),
                                 hovering_image=music_moins_button_image)
    music_button = Button2(image=music_on_button_image, pos=(750, 315), hovering_image=music_off_button_image)
    sound_text = Text(pos=(430, 287), text_input='Music :', font=pygame.font.Font(None, 75), base_color='White')
    volume_text = Text(pos=(430, 380), text_input='Volume :', font=pygame.font.Font(None, 75), base_color='White')
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
        screen.blit(option_back, (360, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        # Create and render the button
        quit_button.update2(screen)
        sound_text.update3(screen)
        volume_text.update3(screen)
        music_button.update2(screen)
        music_plus_button.update2(screen)
        music_moins_button.update2(screen)
        pygame.draw.rect(screen, WHITE, (480, 440, 300, 60), width=5, border_radius=20)
        volume_bar_width = int(300 * volume)  # Calculate the width of the volume bar based on the volume level
        if volume_bar_width == 300:
            pygame.draw.rect(screen, WHITE, (480, 440, volume_bar_width, 60), border_radius=20)
        else:
            pygame.draw.rect(screen, WHITE, (480, 440, volume_bar_width, 60), border_top_left_radius=20,
                             border_bottom_left_radius=20)

        clock.tick(FPS)

        # Update the display
        pygame.display.update()


def main_menu():  # menu principale
    pygame.display.set_caption("Menu")  # donne le nom à la fenêtre

    while True:
        screen.blit(fond_menu, (0, 0))  # met l'image de font(mer)
        menu_mouse_pos = pygame.mouse.get_pos()  # facilite la recuperation de la position de la souris
        menu_text = pygame.font.Font(None, 150).render("MAIN MENU", True,
                                                       (0, 0, 0))  # texte main menu en marron clair
        menu_rect = menu_text.get_rect(center=(640, 100))

        # crée le bouton select
        select_button = Button(image=fond_bouton, pos=(640, 240 + 40),
                               text_input="SELECT", font=pygame.font.Font(None, 75), base_color="White",
                               hovering_color="Red", image_scale=[250, 100], hov_image=fond_bouton2)

        options_button = Button(image=fond_bouton, pos=(640, 495 - 90 + 15),
                                text_input="OPTIONS", font=pygame.font.Font(None, 75), base_color="White",
                                hovering_color="Red", image_scale=[290, 100], hov_image=fond_bouton2)

        quit_button = Button(image=fond_bouton, pos=(640, 625 - 80 + 10),
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
                    menu_niveaux()
                elif options_button.checkForInput(menu_mouse_pos):  # lance le menu options si appuie sur options
                    option()
                elif quit_button.checkForInput(menu_mouse_pos):  # quitte le jeu
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

pygame.quit()

