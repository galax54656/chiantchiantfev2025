import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu Dékal")

game_background = pygame.image.load("../../images/fonjeumtn.png").convert()
game_background = pygame.transform.scale(game_background, (1280, 720))

bouton_img = pygame.image.load('../../images/FOND BOUTON.png').convert_alpha()
bouton_img = pygame.transform.scale(bouton_img, (380, 100))
bouton_hover_img = pygame.image.load('../../images/fond_bouton2.png').convert_alpha()
bouton_hover_img = pygame.transform.scale(bouton_hover_img, (380, 100))

card_back_img = pygame.image.load('../../images/tigre.webp').convert()
card_face_img = pygame.image.load('../../images/avantvraicarterouge.png').convert()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (100, 100, 100)

'''
dimension des cartes largeur = 50, hauteur = 70'''

class Carte:
    #def __init__(self, valeur):
    #    self.valeur = valeur
    #    self.cote = "dos"
    def __init__(self, valeur, position=(200, 200), scale=(50, 70)):
        self.valeur = valeur
        self.position = position
        self.cote = 'dos'  # 'back' = face cachée, 'face' = face visible
        self.scale = scale


        self.image_back = pygame.transform.scale(card_back_img, scale)
        self.image_face = pygame.transform.scale(card_face_img, scale)

        self.image = self.image_back
        self.rect = self.image.get_rect(topleft=position)

        self.font = pygame.font.Font(None, 75)
        self.text = self.font.render(str(self.value), True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.cote == 'face':
            text_rect = self.text.get_rect(center=self.rect.center)
            screen.blit(self.text, text_rect)

    def flip(self):
        if self.cote == 'dos':
            self.cote = 'face'
            self.image = self.image_face
            #self.rect.center = (640, 360)#ajout d'un endroit selon nombre de joueurs
        else:
            self.cote = 'dos'
            self.image = self.image_back
            self.rect.topleft = self.position

    def choisi(self, nb_joueurs, joueur_actuel_index):
        self.rect.center = (640, 360)




class Joueur:
    def __init__(self, nom, ordi=False, num_joueur=None):
        self.nom = nom
        self.ordi = ordi
        self.tableau = []  # On crée une liste vide pour stocker les lignes
        for i in range(4):  # On veut 4 lignes
            ligne = []  # Une nouvelle ligne vide
            for j in range(4):  # Chaque ligne contient 4 cartes
                carte = Carte(random.randint(1, 10))  # Crée une carte avec une valeur aléatoire
                ligne.append(carte)  # Ajoute la carte à la ligne
            self.tableau.append(ligne)  # Ajoute la ligne au tableau

        for ligne in self.tableau:
            for carte in ligne:
                carte.cote = "dos"

        self.pos_vide = None
        self.score = 0
        self.care_prise = None


class OrdiNiv1(Joueur):
    def __init__(self, nom):
        super().__init__(nom, ordi=True)

    def choisir_carte(self):
        cartes_pas_retourne = []
        for i in range(4):
            for j in range(4):  # Chaque ligne contient 4 cartes
                if self.tableau[i][j].cote == "dos":  # Crée une carte avec une valeur aléatoire
                    cartes_pas_retourne.append((i, j))  # Ajoute la carte à la ligne
        return random.choice(cartes_pas_retourne)

    def choisir_carte_centre(selfself, cartes_choisies):
        carte_min = cartes_choisies[0]  # On suppose que la première carte est la plus petite

        # Parcourt toutes les cartes pour trouver la plus petite
        for carte in cartes_choisies:
            if carte.valeur < carte_min.valeur:  # Si on trouve une carte plus petite
                carte_min = carte  # On met à jour la carte minimale

        return carte_min  # Retourne la carte avec la plus petite valeur

    def choisir_direction(self, position_vide):
        i, j = position_vide
        direction_possible = []
        if j > 0: direction_possible.append("gauche")#si pas tout à gauche
        if j < 3: direction_possible.append("droite")
        if i > 0: direction_possible.append("haut")
        if i < 3: direction_possible.append("bas")

        return random.choice(direction_possible)

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

def choix_nombre_joueurs():
    screen.blit(game_background, (0, 0))
    font = pygame.font.Font(None, 36)
    texte = font.render("choisissez le nombre total de joueurs", True, NOIR)
    screen.blit(texte, (50, 50))

    boutons = []
    for i in range(2, 7):
        boutons.append(Bouton(((50+i)*100, 100), text=str(i), font=font, base_color="White", hover_color="Red",
                         image=bouton_img, hover_image=bouton_hover_img, scale=(380, 100)))
    for bouton in boutons:
        bouton.update(screen)
    pygame.display.flip()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    if bouton.au_dessus(mouse_pos):
                        return int(bouton.text)

def choisir_nombre_ia(nb_joueurs):
    screen.blit(game_background, (0, 0))
    font = pygame.font.Font(None, 36)  # Crée une police de taille 36
    # Affiche un message demandant le nombre d'IA
    texte = font.render(f"Choisissez le nombre d'Ordis :", True, NOIR)
    screen.blit(texte, (50, 50))  # Positionne le texte à (50, 50)

    # Crée une liste de boutons pour les choix possibles (0 à nb_joueurs-1)
    boutons = []
    for i in range(nb_joueurs):  # Boucle de 0 à nb_joueurs-1
        boutons.append(Bouton(((50+i)*100, 100), text=str(i), font=font, base_color="White", hover_color="Red",
                         image=bouton_img, hover_image=bouton_hover_img, scale=(380, 100) ))

    # Affiche tous les boutons
    for bouton in boutons:
        bouton.update(screen)
    pygame.display.flip()  # Met à jour l'écran

    # Boucle pour attendre un clic sur un bouton
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():  # Récupère tous les événements
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()  # Ferme Pygame
                exit()  # Quitte le programme
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si clic de souris
                for bouton in boutons:
                    if bouton.au_dessus(mouse_pos):  # Si un bouton est cliqué
                        return int(bouton.text)  # Retourne le nombre d'IA choisi

'''
class Jeu:
    def __init__(self, nb_joueurs, nb_ordis):
        self.joueurs = []
        for i in range(nb_joueurs - nb_ordis):
            self.joueurs.append(Joueur("Joueur "+i+1))
        for i in range(nb_ordis):
            self.joueurs.append(OrdiNiv1)
        random.shuffle(self.joueurs)
        self.ordre_joueurs = self.joueurs.copy()

        self.joueur_actuel_index = 0  # Index du joueur actuel dans l'ordre
        self.cartes_choisies = []  # Liste des cartes mises au centre
        self.etat = "CHOIX_CARTE"  # État du jeu : commence par choisir une carte
        self.boutons_direction = []  # Liste des boutons de direction (vide au départ)
        # Positions des tableaux des joueurs à l'écran (espacés de 250 pixels)
        self.positions_tableaux = [(50 + i * 250, 50) for i in range(nb_joueurs)]
        self.position_centre = (50, 400)  # Position des cartes au centre


    def afficher(self):
        screen.blit(game_background, (0, 0))

        for i, joueur in enumerate(self.joueur):
            x, y = self.position_tableaux[i]
            for a in range(4):
                for b in range(4):
                    carte = joueur.tableau[a][b]
'''


def bouge_carte(self, ):
    pass

def jeu(screen, nb_joueurs, nb_ordis):
    joueurs = []
    for i in range(nb_joueurs - nb_ordis):
        joueurs.append(Joueur("Joueur " + i + 1))
    for i in range(nb_ordis):
        joueurs.append(OrdiNiv1)
    random.shuffle(joueurs)
    #ordre_joueurs = joueurs.copy()

    joueur_actuel_index = 0  # Index du joueur actuel dans l'ordre
    cartes_choisies = []  # Liste des cartes mises au centre
    etat = "CHOIX_CARTE"  # État du jeu : commence par choisir une carte
    boutons_direction = []  # Liste des boutons de direction (vide au départ)
    # Positions des tableaux des joueurs à l'écran (espacés de 250 pixels)
    positions_tableaux = [(50 + i * 250, 50) for i in range(nb_joueurs)]
    position_centre = (640, 360)  # Position des cartes au centre

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for joueur in joueurs:
            for a in range(4):
                for b in range(4):
                    joueur.tableau[a][b].draw
        if etat == "CHOIX_CARTE" and joueurs[joueur_actuel_index].ordi == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"  # Retour vers le main pour quitter
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for ligne in joueurs[joueur_actuel_index].tableau:
                            j=0
                            for carte in joueurs[joueur_actuel_index].tableau[i]:
                                j+=1
                                if carte.rect.collidepoint(mouse_pos):
                                    if carte.cote == "dos":
                                        carte.choisi()
                                        joueur.carte_prise = carte
                                        joueur.pos_vide = (i, j)
                                        if joueur_actuel_index == len(joueurs):
                                            joueur_actuel_index = 0
                                            etat == "CHOIX_CARTE_CENTRE"
                                        else :
                                            joueur_actuel_index += 1
        elif etat == "CHOIX_CARTE" and joueurs[joueur_actuel_index].ordi == True:
            pass




