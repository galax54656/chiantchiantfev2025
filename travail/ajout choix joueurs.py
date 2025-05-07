import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur = 1200  # Augmenté pour accueillir plus de joueurs
hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu Dékal")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (100, 100, 100)

# Taille des cartes et espacement
carte_largeur = 50
carte_hauteur = 70
espacement = 10


# Classe pour une carte
class Carte:
    def __init__(self, valeur):
        self.valeur = valeur
        self.revelee = False


# Classe pour un joueur
class Joueur:
    def __init__(self, nom, est_ia=False):
        self.nom = nom
        self.est_ia = est_ia
        self.tableau = [[Carte(random.randint(1, 10)) for _ in range(4)] for _ in range(4)]
        for ligne in self.tableau:
            for carte in ligne:
                carte.revelee = False
        self.position_vide = None
        self.score = 0
        self.carte_recuperee = None


# Classe pour l'IA
class IA(Joueur):
    def __init__(self, nom):
        super().__init__(nom, est_ia=True)

    def choisir_carte(self):
        cartes_face_cachee = [(i, j) for i in range(4) for j in range(4) if
                              self.tableau[i][j] and not self.tableau[i][j].revelee]
        return random.choice(cartes_face_cachee)

    def choisir_carte_centre(self, cartes_choisies):
        return min(cartes_choisies, key=lambda c: c.valeur)

    def choisir_direction(self, position_vide):
        i, j = position_vide
        directions_possibles = []
        if j > 0:
            directions_possibles.append("gauche")
        if j < 3:
            directions_possibles.append("droite")
        if i > 0:
            directions_possibles.append("haut")
        if i < 3:
            directions_possibles.append("bas")
        return random.choice(directions_possibles)


# Classe pour un bouton
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, NOIR, self.rect, 2)
        font = pygame.font.Font(None, 36)
        texte_surface = font.render(self.texte, True, NOIR)
        fenetre.blit(texte_surface, (self.rect.x + 10, self.rect.y + 10))

    def est_clique(self, x, y):
        return self.rect.collidepoint(x, y)


# Écran de sélection du nombre de joueurs et d'IA
def choisir_nombre_joueurs():
    fenetre.fill(BLANC)
    font = pygame.font.Font(None, 36)
    texte = font.render("Choisissez le nombre total de joueurs (2-6) :", True, NOIR)
    fenetre.blit(texte, (50, 50))

    boutons = []
    for i in range(2, 7):
        boutons.append(Bouton(50 + (i - 2) * 100, 100, 80, 50, str(i)))

    for bouton in boutons:
        bouton.afficher(fenetre)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for bouton in boutons:
                    if bouton.est_clique(x, y):
                        return int(bouton.texte)


def choisir_nombre_ia(nb_joueurs):
    fenetre.fill(BLANC)
    font = pygame.font.Font(None, 36)
    texte = font.render(f"Choisissez le nombre d'IA (0-{nb_joueurs - 1}) :", True, NOIR)
    fenetre.blit(texte, (50, 50))

    boutons = []
    for i in range(nb_joueurs):
        boutons.append(Bouton(50 + i * 100, 100, 80, 50, str(i)))

    for bouton in boutons:
        bouton.afficher(fenetre)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for bouton in boutons:
                    if bouton.est_clique(x, y):
                        return int(bouton.texte)


# Classe principale du jeu
class JeuPygame:
    def __init__(self, nb_joueurs, nb_ia):
        if not 2 <= nb_joueurs <= 6 or nb_ia > nb_joueurs - 1:
            raise ValueError("Nombre de joueurs ou d'IA invalide.")

        # Créer les joueurs humains
        self.joueurs = [Joueur(f"Joueur {i + 1}") for i in range(nb_joueurs - nb_ia)]
        # Ajouter les IA
        for i in range(nb_ia):
            self.joueurs.append(IA(f"IA {i + 1}"))
        # Mélanger l'ordre des joueurs pour le premier tour
        random.shuffle(self.joueurs)
        self.ordre_joueurs = self.joueurs.copy()  # Conserver l'ordre pour toute la partie

        self.joueur_actuel_index = 0
        self.cartes_choisies = []
        self.etat = "CHOIX_CARTE"
        self.boutons_direction = []
        self.positions_tableaux = [(50 + i * 250, 50) for i in range(nb_joueurs)]  # Espacement réduit pour 6 joueurs
        self.position_centre = (50, 400)

    def afficher(self):
        fenetre.fill(BLANC)

        # Afficher les tableaux des joueurs
        for i, joueur in enumerate(self.joueurs):
            x, y = self.positions_tableaux[i]
            for m in range(4):
                for n in range(4):
                    carte = joueur.tableau[m][n]
                    carte_x = x + n * (carte_largeur + espacement)
                    carte_y = y + m * (carte_hauteur + espacement)
                    if carte is None:
                        pygame.draw.rect(fenetre, NOIR, (carte_x, carte_y, carte_largeur, carte_hauteur))
                    elif not carte.revelee:
                        pygame.draw.rect(fenetre, GRIS, (carte_x, carte_y, carte_largeur, carte_hauteur))
                    else:
                        pygame.draw.rect(fenetre, BLANC, (carte_x, carte_y, carte_largeur, carte_hauteur))
                        font = pygame.font.Font(None, 36)
                        texte = font.render(str(carte.valeur), True, NOIR)
                        fenetre.blit(texte, (carte_x + 20, carte_y + 20))

        # Afficher les cartes du centre
        if self.etat == "CHOIX_CARTE_CENTRE":
            for k, carte in enumerate(self.cartes_choisies):
                carte_x = self.position_centre[0] + k * (carte_largeur + espacement)
                carte_y = self.position_centre[1]
                pygame.draw.rect(fenetre, BLANC, (carte_x, carte_y, carte_largeur, carte_hauteur))
                font = pygame.font.Font(None, 36)
                texte = font.render(str(carte.valeur), True, NOIR)
                fenetre.blit(texte, (carte_x + 20, carte_y + 20))

        # Afficher les boutons de direction
        if self.etat == "CHOIX_DIRECTION":
            for bouton in self.boutons_direction:
                bouton.afficher(fenetre)

        # Afficher le message
        if self.etat == "CHOIX_CARTE":
            message = f"{self.ordre_joueurs[self.joueur_actuel_index].nom}, choisissez une carte face cachée"
        elif self.etat == "CHOIX_CARTE_CENTRE":
            message = f"{self.ordre_joueurs[self.joueur_actuel_index].nom}, choisissez une carte du centre"
        elif self.etat == "CHOIX_DIRECTION":
            message = f"{self.ordre_joueurs[self.joueur_actuel_index].nom}, choisissez une direction"
        font = pygame.font.Font(None, 36)
        texte = font.render(message, True, NOIR)
        fenetre.blit(texte, (50, 20))

        pygame.display.flip()

    def get_position_cliquee(self, x, y, tableau_x, tableau_y):
        for i in range(4):
            for j in range(4):
                carte_x = tableau_x + j * (carte_largeur + espacement)
                carte_y = tableau_y + i * (carte_hauteur + espacement)
                if carte_x <= x < carte_x + carte_largeur and carte_y <= y < carte_y + carte_hauteur:
                    return (i, j)
        return None

    def calculer_score(self, tableau):
        visite = [[False for _ in range(4)] for _ in range(4)]
        somme = 0
        for i in range(4):
            for j in range(4):
                if not visite[i][j] and tableau[i][j]:
                    groupe = self.dfs(tableau, i, j, visite, tableau[i][j].valeur)
                    if len(groupe) == 1:
                        somme += tableau[i][j].valeur
        return somme

    def dfs(self, tableau, i, j, visite, valeur):
        if (i < 0 or i >= 4 or j < 0 or j >= 4 or visite[i][j] or
                tableau[i][j] is None or tableau[i][j].valeur != valeur):
            return []
        visite[i][j] = True
        groupe = [(i, j)]
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            groupe += self.dfs(tableau, i + di, j + dj, visite, valeur)
        return groupe

    def main(self):
        running = True
        while running:
            self.afficher()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.etat != "FIN":
                    x, y = event.pos
                    joueur = self.ordre_joueurs[self.joueur_actuel_index]

                    if self.etat == "CHOIX_CARTE" and not joueur.est_ia:
                        idx = self.joueurs.index(joueur)
                        tableau_x, tableau_y = self.positions_tableaux[idx]
                        pos = self.get_position_cliquee(x, y, tableau_x, tableau_y)
                        if pos:
                            i, j = pos
                            if joueur.tableau[i][j] and not joueur.tableau[i][j].revelee:
                                carte = joueur.tableau[i][j]
                                joueur.tableau[i][j] = None
                                joueur.position_vide = (i, j)
                                self.cartes_choisies.append(carte)
                                self.joueur_actuel_index += 1
                                if self.joueur_actuel_index >= len(self.joueurs):
                                    for carte in self.cartes_choisies:
                                        carte.revelee = True
                                    self.etat = "CHOIX_CARTE_CENTRE"
                                    self.joueur_actuel_index = 0

                    elif self.etat == "CHOIX_CARTE_CENTRE" and not joueur.est_ia:
                        for k, carte in enumerate(self.cartes_choisies):
                            carte_x = self.position_centre[0] + k * (carte_largeur + espacement)
                            carte_y = self.position_centre[1]
                            if (carte_x <= x < carte_x + carte_largeur and
                                    carte_y <= y < carte_y + carte_hauteur):
                                joueur.carte_recuperee = carte
                                self.cartes_choisies.remove(carte)
                                self.etat = "CHOIX_DIRECTION"
                                i, j = joueur.position_vide
                                idx = self.joueurs.index(joueur)
                                tableau_x, tableau_y = self.positions_tableaux[idx]
                                bouton_y = tableau_y + 4 * (carte_hauteur + espacement) + 20
                                self.boutons_direction = []
                                if j > 0:
                                    self.boutons_direction.append(Bouton(tableau_x, bouton_y, 60, 30, "Gauche"))
                                if j < 3:
                                    self.boutons_direction.append(Bouton(tableau_x + 70, bouton_y, 60, 30, "Droite"))
                                if i > 0:
                                    self.boutons_direction.append(Bouton(tableau_x + 140, bouton_y, 60, 30, "Haut"))
                                if i < 3:
                                    self.boutons_direction.append(Bouton(tableau_x + 210, bouton_y, 60, 30, "Bas"))
                                break

                    elif self.etat == "CHOIX_DIRECTION" and not joueur.est_ia:
                        for bouton in self.boutons_direction:
                            if bouton.est_clique(x, y):
                                direction = bouton.texte.lower()
                                i, j = joueur.position_vide
                                if direction == "gauche":
                                    for k in range(j, 0, -1):
                                        joueur.tableau[i][k] = joueur.tableau[i][k - 1]
                                    joueur.tableau[i][0] = None
                                    joueur.position_vide = (i, 0)
                                elif direction == "droite":
                                    for k in range(j, 3):
                                        joueur.tableau[i][k] = joueur.tableau[i][k + 1]
                                    joueur.tableau[i][3] = None
                                    joueur.position_vide = (i, 3)
                                elif direction == "haut":
                                    for k in range(i, 0, -1):
                                        joueur.tableau[k][j] = joueur.tableau[k - 1][j]
                                    joueur.tableau[0][j] = None
                                    joueur.position_vide = (0, j)
                                elif direction == "bas":
                                    for k in range(i, 3):
                                        joueur.tableau[k][j] = joueur.tableau[k + 1][j]
                                    joueur.tableau[3][j] = None
                                    joueur.position_vide = (3, j)

                                i, j = joueur.position_vide
                                joueur.tableau[i][j] = joueur.carte_recuperee
                                joueur.carte_recuperee.revelee = True
                                joueur.position_vide = None
                                self.boutons_direction = []
                                self.joueur_actuel_index += 1
                                if self.joueur_actuel_index >= len(self.joueurs):
                                    self.etat = "CHOIX_CARTE"
                                    self.joueur_actuel_index = 0
                                else:
                                    self.etat = "CHOIX_CARTE_CENTRE"
                                break

            # Gestion des actions de l'IA
            joueur = self.ordre_joueurs[self.joueur_actuel_index]
            if joueur.est_ia:
                if self.etat == "CHOIX_CARTE":
                    i, j = joueur.choisir_carte()
                    carte = joueur.tableau[i][j]
                    joueur.tableau[i][j] = None
                    joueur.position_vide = (i, j)
                    self.cartes_choisies.append(carte)
                    self.joueur_actuel_index += 1
                    if self.joueur_actuel_index >= len(self.joueurs):
                        for carte in self.cartes_choisies:
                            carte.revelee = True
                        self.etat = "CHOIX_CARTE_CENTRE"
                        self.joueur_actuel_index = 0

                elif self.etat == "CHOIX_CARTE_CENTRE":
                    carte = joueur.choisir_carte_centre(self.cartes_choisies)
                    joueur.carte_recuperee = carte
                    self.cartes_choisies.remove(carte)
                    self.etat = "CHOIX_DIRECTION"

                elif self.etat == "CHOIX_DIRECTION":
                    direction = joueur.choisir_direction(joueur.position_vide)
                    i, j = joueur.position_vide
                    if direction == "gauche":
                        for k in range(j, 0, -1):
                            joueur.tableau[i][k] = joueur.tableau[i][k - 1]
                        joueur.tableau[i][0] = None
                        joueur.position_vide = (i, 0)
                    elif direction == "droite":
                        for k in range(j, 3):
                            joueur.tableau[i][k] = joueur.tableau[i][k + 1]
                        joueur.tableau[i][3] = None
                        joueur.position_vide = (i, 3)
                    elif direction == "haut":
                        for k in range(i, 0, -1):
                            joueur.tableau[k][j] = joueur.tableau[k - 1][j]
                        joueur.tableau[0][j] = None
                        joueur.position_vide = (0, j)
                    elif direction == "bas":
                        for k in range(i, 3):
                            joueur.tableau[k][j] = joueur.tableau[k + 1][j]
                        joueur.tableau[3][j] = None
                        joueur.position_vide = (3, j)

                    i, j = joueur.position_vide
                    joueur.tableau[i][j] = joueur.carte_recuperee
                    joueur.carte_recuperee.revelee = True
                    joueur.position_vide = None
                    self.joueur_actuel_index += 1
                    if self.joueur_actuel_index >= len(self.joueurs):
                        self.etat = "CHOIX_CARTE"
                        self.joueur_actuel_index = 0
                    else:
                        self.etat = "CHOIX_CARTE_CENTRE"

            # Vérifier la fin du jeu
            if all(all(carte and carte.revelee for carte in ligne) for joueur in self.joueurs for ligne in
                   joueur.tableau):
                running = False

        # Afficher les scores
        for joueur in self.joueurs:
            joueur.score = self.calculer_score(joueur.tableau)
            print(f"{joueur.nom} a un score de {joueur.score}")
        gagnant = min(self.joueurs, key=lambda j: j.score)
        print(f"Le gagnant est {gagnant.nom} avec un score de {gagnant.score}")
        pygame.quit()


if __name__ == "__main__":
    nb_joueurs = choisir_nombre_joueurs()
    nb_ia = choisir_nombre_ia(nb_joueurs)
    jeu = JeuPygame(nb_joueurs, nb_ia)
    jeu.main()