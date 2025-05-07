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


class Carte:
    def __init__(self, valeur, position=(200, 200), scale=(50, 70)):
        self.valeur = valeur
        self.position = position
        self.cote = 'dos'
        self.scale = scale
        self.image_back = pygame.transform.scale(card_back_img, scale)
        self.image_face = pygame.transform.scale(card_face_img, scale)
        self.image = self.image_back
        self.rect = self.image.get_rect(topleft=position)
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render(str(self.valeur), True, BLANC)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.cote == 'face':
            text_rect = self.text.get_rect(center=self.rect.center)
            screen.blit(self.text, text_rect)

    def flip(self):
        if self.cote == 'dos':
            self.cote = 'face'
            self.image = self.image_face
        else:
            self.cote = 'dos'
            self.image = self.image_back


class Joueur:
    def __init__(self, nom, ordi=False):
        self.nom = nom
        self.ordi = ordi
        self.tableau = [[Carte(random.randint(1, 10)) for _ in range(4)] for _ in range(4)]
        for ligne in self.tableau:
            for carte in ligne:
                carte.cote = "dos"
        self.pos_vide = None
        self.carte_prise = None
        self.score = 0
        self.nb_cartes = 16


class OrdiNiv1(Joueur):
    def __init__(self, nom):
        super().__init__(nom, ordi=True)

    def choisir_carte(self):
        cartes_pas_retourne = [(i, j) for i in range(4) for j in range(4) if self.tableau[i][j].cote == "dos"]
        return random.choice(cartes_pas_retourne)

    def choisir_carte_centre(self, cartes_choisies):
        return random.choice(cartes_choisies)

    def choisir_direction(self, position_vide):
        i, j = position_vide
        direction_possible = []
        if i == 0: direction_possible.append("bas")
        if i == 3: direction_possible.append("haut")
        if j == 0: direction_possible.append("droite")
        if j == 3: direction_possible.append("gauche")
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
    texte = font.render("Choisissez le nombre total de joueurs", True, NOIR)
    screen.blit(texte, (50, 50))

    boutons = [Bouton((300 + i * 150, 300), str(i), font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)) for i
               in range(2, 7)]
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
    font = pygame.font.Font(None, 36)
    texte = font.render(f"Choisissez le nombre d'ordis :", True, NOIR)
    screen.blit(texte, (50, 50))

    boutons = [Bouton((300 + i * 150, 300), str(i), font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)) for i
               in range(nb_joueurs)]
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


def bouge_carte(joueur, direction, carte):
    i, j = joueur.pos_vide
    tableau = joueur.tableau

    if direction == "haut" and i == 3:
        for k in range(3, 0, -1):
            tableau[k][j] = tableau[k - 1][j]
        tableau[0][j] = carte
        joueur.pos_vide = (0, j)
    elif direction == "bas" and i == 0:
        for k in range(0, 3):
            tableau[k][j] = tableau[k + 1][j]
        tableau[3][j] = carte
        joueur.pos_vide = (3, j)
    elif direction == "gauche" and j == 3:
        for k in range(3, 0, -1):
            tableau[i][k] = tableau[i][k - 1]
        tableau[i][0] = carte
        joueur.pos_vide = (i, 0)
    elif direction == "droite" and j == 0:
        for k in range(0, 3):
            tableau[i][k] = tableau[i][k + 1]
        tableau[i][3] = carte
        joueur.pos_vide = (i, 3)


def calculer_scores(joueurs):
    for joueur in joueurs:
        tableau = joueur.tableau
        a_supprimer = set()
        for i in range(4):
            for j in range(4):
                if (i, j) in a_supprimer:
                    continue
                valeur = tableau[i][j].valeur
                if j < 3 and tableau[i][j + 1].valeur == valeur:
                    a_supprimer.add((i, j))
                    a_supprimer.add((i, j + 1))
                if i < 3 and tableau[i + 1][j].valeur == valeur:
                    a_supprimer.add((i, j))
                    a_supprimer.add((i + 1, j))

        for i, j in a_supprimer:
            tableau[i][j] = None

        score = 0
        nb_cartes = 0
        for i in range(4):
            for j in range(4):
                if tableau[i][j] is not None:
                    score += tableau[i][j].valeur
                    nb_cartes += 1
        joueur.score = score
        joueur.nb_cartes = nb_cartes

    min_score = min(joueur.score for joueur in joueurs)
    candidats = [joueur for joueur in joueurs if joueur.score == min_score]
    if len(candidats) == 1:
        return f"Vainqueur : {candidats[0].nom} avec {min_score} points"
    else:
        min_cartes = min(joueur.nb_cartes for joueur in candidats)
        gagnants = [joueur for joueur in candidats if joueur.nb_cartes == min_cartes]
        if len(gagnants) == 1:
            return f"Vainqueur : {gagnants[0].nom} avec {min_score} points et {min_cartes} cartes"
        else:
            return f"Victoire partagée : {[joueur.nom for joueur in gagnants]} avec {min_score} points et {min_cartes} cartes"


def jeu(screen, nb_joueurs, nb_ordis):
    joueurs = []
    for i in range(nb_joueurs - nb_ordis):
        joueurs.append(Joueur(f"Joueur {i + 1}"))
    for i in range(nb_ordis):
        joueurs.append(OrdiNiv1(f"Ordi {i + 1}"))
    random.shuffle(joueurs)

    joueur_actuel_index = 0
    premier_joueur_index = 0
    cartes_choisies = []  # Cartes au centre après sélection de tous les joueurs
    cartes_prises = []   # Cartes temporairement stockées pendant la sélection
    etat = "CHOIX_CARTE"
    tour = 1
    positions_tableaux = [
        (50, 50),    # Joueur 1
        (500, 50),   # Joueur 2
        (950, 50),   # Joueur 3
        (50, 400),   # Joueur 4
        (500, 400),  # Joueur 5
        (950, 400)   # Joueur 6
    ]
    positions_tableaux = positions_tableaux[:nb_joueurs]
    position_centre = [(500 + i * 60, 300) for i in range(nb_joueurs)]
    boutons_direction = []
    font = pygame.font.Font(None, 36)

    while True:
        screen.blit(game_background, (0, 0))

        # Afficher les grilles
        for i, joueur in enumerate(joueurs):
            x, y = positions_tableaux[i]
            texte_joueur = font.render(joueur.nom, True, BLANC)
            screen.blit(texte_joueur, (x, y - 30))
            pygame.draw.rect(screen, GRIS, (x - 10, y - 10, 240, 320), 2)
            for a in range(4):
                for b in range(4):
                    carte = joueur.tableau[a][b]
                    # Si la carte est prise, afficher un rectangle vide ou la face arrière
                    if (i, a, b) in cartes_prises:
                        pygame.draw.rect(screen, NOIR, (x + b * 60, y + a * 80, 60, 80), 2)  # Bordure vide
                    else:
                        carte.rect.topleft = (x + b * 60, y + a * 80)
                        carte.draw(screen)

        # Afficher les cartes au centre
        for i, carte in enumerate(cartes_choisies):
            carte.rect.topleft = position_centre[i]
            carte.draw(screen)

        texte = font.render(f"Tour {tour}/16 - Joueur : {joueurs[joueur_actuel_index].nom}", True, BLANC)
        screen.blit(texte, (50, 650))

        mouse_pos = pygame.mouse.get_pos()

        if etat == "CHOIX_CARTE":
            if joueurs[joueur_actuel_index].ordi:
                i, j = joueurs[joueur_actuel_index].choisir_carte()
                carte = joueurs[joueur_actuel_index].tableau[i][j]
                carte.flip()
                joueurs[joueur_actuel_index].carte_prise = carte
                joueurs[joueur_actuel_index].pos_vide = (i, j)
                cartes_prises.append((joueur_actuel_index, i, j))  # Stocker la position prise
                joueur_actuel_index = (joueur_actuel_index + 1) % len(joueurs)
                if len(cartes_prises) == len(joueurs):
                    # Tous les joueurs ont choisi, déplacer les cartes au centre
                    for idx, i, j in cartes_prises:
                        carte = joueurs[idx].carte_prise
                        carte.rect.topleft = position_centre[len(cartes_choisies)]
                        cartes_choisies.append(carte)
                    if tour == 1:
                        min_valeur = min(carte.valeur for carte in cartes_choisies)
                        premiers = [i for i, joueur in enumerate(joueurs) if cartes_choisies[i].valeur == min_valeur]
                        premier_joueur_index = random.choice(premiers)
                        joueur_actuel_index = premier_joueur_index
                    etat = "CHOIX_CARTE_CENTRE"
                    cartes_prises = []  # Réinitialiser après déplacement
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit"
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for i in range(4):
                            for j in range(4):
                                carte = joueurs[joueur_actuel_index].tableau[i][j]
                                if carte.rect.collidepoint(mouse_pos) and carte.cote == "dos":
                                    carte.flip()
                                    joueurs[joueur_actuel_index].carte_prise = carte
                                    joueurs[joueur_actuel_index].pos_vide = (i, j)
                                    cartes_prises.append((joueur_actuel_index, i, j))
                                    joueur_actuel_index = (joueur_actuel_index + 1) % len(joueurs)
                                    if len(cartes_prises) == len(joueurs):
                                        for idx, i, j in cartes_prises:
                                            carte = joueurs[idx].carte_prise
                                            carte.rect.topleft = position_centre[len(cartes_choisies)]
                                            cartes_choisies.append(carte)
                                        if tour == 1:
                                            min_valeur = min(carte.valeur for carte in cartes_choisies)
                                            premiers = [i for i, joueur in enumerate(joueurs) if cartes_choisies[i].valeur == min_valeur]
                                            premier_joueur_index = random.choice(premiers)
                                            joueur_actuel_index = premier_joueur_index
                                        etat = "CHOIX_CARTE_CENTRE"
                                        cartes_prises = []

        # (Les autres états "CHOIX_CARTE_CENTRE" et "CHOIX_INSERTION" restent inchangés)

        pygame.display.flip()

def main():
    nb_joueurs = choix_nombre_joueurs()
    nb_ordis = choisir_nombre_ia(nb_joueurs)
    jeu(screen, nb_joueurs, nb_ordis)
    pygame.quit()


if __name__ == "__main__":
    main()