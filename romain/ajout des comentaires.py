# Importation des bibliothèques nécessaires
import pygame  # Bibliothèque pour créer des jeux graphiques
import random  # Pour générer des nombres ou choix aléatoires

# Initialisation de Pygame (doit être fait avant toute utilisation de Pygame)
pygame.init()

# Définition des dimensions de la fenêtre de jeu
largeur = 1200  # Largeur de la fenêtre en pixels (assez grand pour 6 joueurs)
hauteur = 600   # Hauteur de la fenêtre en pixels
fenetre = pygame.display.set_mode((largeur, hauteur))  # Crée la fenêtre
pygame.display.set_caption("Jeu Dékal")  # Définit le titre de la fenêtre

# Définition des couleurs en RGB (Rouge, Vert, Bleu)
BLANC = (255, 255, 255)  # Couleur blanche pour l'arrière-plan
NOIR = (0, 0, 0)         # Couleur noire pour le texte et les contours
GRIS = (100, 100, 100)   # Couleur grise pour les cartes face cachée

# Dimensions des cartes et espacement entre elles
carte_largeur = 50   # Largeur d'une carte en pixels
carte_hauteur = 70   # Hauteur d'une carte en pixels
espacement = 10      # Espacement entre les cartes en pixels

# Classe pour représenter une carte dans le jeu
class Carte:
    def __init__(self, valeur):
        # Chaque carte a une valeur et un état (révélée ou non)
        self.valeur = valeur      # Valeur de la carte (entre 1 et 10)
        self.revelee = False      # False = face cachée, True = face visible

# Classe pour représenter un joueur (humain ou IA)
class Joueur:
    def __init__(self, nom, est_ia=False):
        # Initialisation des attributs du joueur
        self.nom = nom            # Nom du joueur (ex. "Joueur 1" ou "IA 1")
        self.est_ia = est_ia      # True si c'est une IA, False si humain
        # Crée un tableau 4x4 de cartes avec des valeurs aléatoires
        self.tableau = [[Carte(random.randint(1, 10)) for _ in range(4)] for _ in range(4)]
        # Toutes les cartes commencent face cachée
        for ligne in self.tableau:
            for carte in ligne:
                carte.revelee = False
        self.position_vide = None  # Position (i, j) de la case vide après avoir retiré une carte
        self.score = 0             # Score calculé à la fin (basé sur les cartes isolées)
        self.carte_recuperee = None  # Carte que le joueur a prise au centre

# Classe pour l'IA, qui hérite de la classe Joueur
class IA(Joueur):
    def __init__(self, nom):
        # Appelle le constructeur de la classe parent (Joueur) avec est_ia=True
        super().__init__(nom, est_ia=True)

    # Méthode pour que l'IA choisisse une carte face cachée au hasard
    def choisir_carte(self):
        # Liste des positions (i, j) des cartes face cachée dans le tableau
        cartes_face_cachee = [(i, j) for i in range(4) for j in range(4) if not self.tableau[i][j].revelee]
        # Retourne une position choisie aléatoirement dans cette liste
        return random.choice(cartes_face_cachee)

    # Méthode pour que l'IA choisisse la carte du centre avec la plus petite valeur
    def choisir_carte_centre(self, cartes_choisies):
        # Retourne la carte avec la valeur minimale parmi celles au centre
        return min(cartes_choisies, key=lambda c: c.valeur)

    # Méthode pour que l'IA choisisse une direction aléatoire
    def choisir_direction(self, position_vide):
        i, j = position_vide  # Récupère les coordonnées de la case vide
        directions_possibles = []  # Liste des directions possibles
        if j > 0: directions_possibles.append("gauche")  # Si pas tout à gauche
        if j < 3: directions_possibles.append("droite")  # Si pas tout à droite
        if i > 0: directions_possibles.append("haut")    # Si pas tout en haut
        if i < 3: directions_possibles.append("bas")     # Si pas tout en bas
        # Retourne une direction choisie au hasard
        return random.choice(directions_possibles)

# Classe pour créer des boutons cliquables dans l'interface
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        # Crée un rectangle pour le bouton avec ses coordonnées et dimensions
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte  # Texte affiché sur le bouton (ex. "2" ou "Gauche")

    # Méthode pour dessiner le bouton à l'écran
    def afficher(self, fenetre):
        # Dessine un rectangle noir (contour seulement, épaisseur 2)
        pygame.draw.rect(fenetre, NOIR, self.rect, 2)
        # Crée une police pour le texte (taille 36)
        font = pygame.font.Font(None, 36)
        # Rend le texte en noir
        texte_surface = font.render(self.texte, True, NOIR)
        # Affiche le texte au centre du bouton (décalé de 10 pixels)
        fenetre.blit(texte_surface, (self.rect.x + 10, self.rect.y + 10))

    # Méthode pour tester si le bouton a été cliqué
    def est_clique(self, x, y):
        # Vérifie si les coordonnées (x, y) du clic sont dans le rectangle
        return self.rect.collidepoint(x, y)

# Fonction pour demander à l'utilisateur de choisir le nombre total de joueurs
def choisir_nombre_joueurs():
    fenetre.fill(BLANC)  # Remplit l'écran avec du blanc
    font = pygame.font.Font(None, 36)  # Crée une police de taille 36
    # Affiche un message demandant de choisir le nombre de joueurs
    texte = font.render("Choisissez le nombre total de joueurs (2-6) :", True, NOIR)
    fenetre.blit(texte, (50, 50))  # Positionne le texte à (50, 50)

    # Crée une liste de boutons pour les choix possibles (2 à 6)
    boutons = []
    for i in range(2, 7):  # Boucle de 2 à 6 inclus
        boutons.append(Bouton(50 + (i-2) * 100, 100, 80, 50, str(i)))

    # Affiche tous les boutons
    for bouton in boutons:
        bouton.afficher(fenetre)
    pygame.display.flip()  # Met à jour l'écran pour afficher les changements

    # Boucle pour attendre un clic sur un bouton
    while True:
        for event in pygame.event.get():  # Récupère tous les événements
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()  # Ferme Pygame
                exit()  # Quitte le programme
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si clic de souris
                x, y = event.pos  # Récupère les coordonnées du clic
                for bouton in boutons:
                    if bouton.est_clique(x, y):  # Si un bouton est cliqué
                        return int(bouton.texte)  # Retourne le nombre choisi

# Fonction pour demander à l'utilisateur de choisir le nombre d'IA
def choisir_nombre_ia(nb_joueurs):
    fenetre.fill(BLANC)  # Remplit l'écran avec du blanc
    font = pygame.font.Font(None, 36)  # Crée une police de taille 36
    # Affiche un message demandant le nombre d'IA
    texte = font.render(f"Choisissez le nombre d'IA (0-{nb_joueurs-1}) :", True, NOIR)
    fenetre.blit(texte, (50, 50))  # Positionne le texte à (50, 50)

    # Crée une liste de boutons pour les choix possibles (0 à nb_joueurs-1)
    boutons = []
    for i in range(nb_joueurs):  # Boucle de 0 à nb_joueurs-1
        boutons.append(Bouton(50 + i * 100, 100, 80, 50, str(i)))

    # Affiche tous les boutons
    for bouton in boutons:
        bouton.afficher(fenetre)
    pygame.display.flip()  # Met à jour l'écran

    # Boucle pour attendre un clic sur un bouton
    while True:
        for event in pygame.event.get():  # Récupère tous les événements
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()  # Ferme Pygame
                exit()  # Quitte le programme
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si clic de souris
                x, y = event.pos  # Récupère les coordonnées du clic
                for bouton in boutons:
                    if bouton.est_clique(x, y):  # Si un bouton est cliqué
                        return int(bouton.texte)  # Retourne le nombre d'IA choisi

# Classe principale qui gère toute la logique du jeu
class JeuPygame:
    def __init__(self, nb_joueurs, nb_ia):
        # Vérifie que les nombres entrés sont valides
        if not 2 <= nb_joueurs <= 6 or nb_ia > nb_joueurs - 1:
            raise ValueError("Nombre de joueurs ou d'IA invalide.")

        # Crée les joueurs humains (nb_joueurs - nb_ia)
        self.joueurs = [Joueur(f"Joueur {i+1}") for i in range(nb_joueurs - nb_ia)]
        # Ajoute les IA
        for i in range(nb_ia):
            self.joueurs.append(IA(f"IA {i+1}"))
        # Mélange l'ordre des joueurs pour définir qui joue quand
        random.shuffle(self.joueurs)
        self.ordre_joueurs = self.joueurs.copy()  # Garde cet ordre fixe

        self.joueur_actuel_index = 0  # Index du joueur actuel dans l'ordre
        self.cartes_choisies = []     # Liste des cartes mises au centre
        self.etat = "CHOIX_CARTE"     # État du jeu : commence par choisir une carte
        self.boutons_direction = []   # Liste des boutons de direction (vide au départ)
        # Positions des tableaux des joueurs à l'écran (espacés de 250 pixels)
        self.positions_tableaux = [(50 + i * 250, 50) for i in range(nb_joueurs)]
        self.position_centre = (50, 400)  # Position des cartes au centre

    # Méthode pour afficher tout l'état du jeu à l'écran
    def afficher(self):
        fenetre.fill(BLANC)  # Efface l'écran en le remplissant de blanc

        # Affiche le tableau de chaque joueur
        for i, joueur in enumerate(self.joueurs):  # Boucle sur tous les joueurs
            x, y = self.positions_tableaux[i]  # Position du tableau du joueur
            for m in range(4):  # Lignes du tableau (0 à 3)
                for n in range(4):  # Colonnes du tableau (0 à 3)
                    carte = joueur.tableau[m][n]  # Récupère la carte à cette position
                    # Calcule la position de la carte à l'écran
                    carte_x = x + n * (carte_largeur + espacement)
                    carte_y = y + m * (carte_hauteur + espacement)
                    if carte is None:  # Si la case est vide
                        # Dessine un rectangle noir
                        pygame.draw.rect(fenetre, NOIR, (carte_x, carte_y, carte_largeur, carte_hauteur))
                    elif not carte.revelee:  # Si la carte est face cachée
                        # Dessine un rectangle gris
                        pygame.draw.rect(fenetre, GRIS, (carte_x, carte_y, carte_largeur, carte_hauteur))
                    else:  # Si la carte est révélée
                        # Dessine un rectangle blanc avec la valeur
                        pygame.draw.rect(fenetre, BLANC, (carte_x, carte_y, carte_largeur, carte_hauteur))
                        font = pygame.font.Font(None, 36)  # Police pour le texte
                        texte = font.render(str(carte.valeur), True, NOIR)  # Affiche la valeur
                        fenetre.blit(texte, (carte_x + 20, carte_y + 20))  # Centre le texte

        # Affiche les cartes au centre si on est dans cet état
        if self.etat == "CHOIX_CARTE_CENTRE":
            for k, carte in enumerate(self.cartes_choisies):  # Boucle sur les cartes au centre
                carte_x = self.position_centre[0] + k * (carte_largeur + espacement)
                carte_y = self.position_centre[1]
                # Dessine la carte en blanc avec sa valeur
                pygame.draw.rect(fenetre, BLANC, (carte_x, carte_y, carte_largeur, carte_hauteur))
                font = pygame.font.Font(None, 36)
                texte = font.render(str(carte.valeur), True, NOIR)
                fenetre.blit(texte, (carte_x + 20, carte_y + 20))

        # Affiche les boutons de direction si on est dans cet état
        if self.etat == "CHOIX_DIRECTION":
            for bouton in self.boutons_direction:  # Boucle sur les boutons
                bouton.afficher(fenetre)  # Affiche chaque bouton

        # Affiche un message indiquant ce que le joueur doit faire
        joueur_actuel = self.ordre_joueurs[self.joueur_actuel_index]
        if self.etat == "CHOIX_CARTE":
            message = f"{joueur_actuel.nom}, choisissez une carte face cachée"
        elif self.etat == "CHOIX_CARTE_CENTRE":
            message = f"{joueur_actuel.nom}, choisissez une carte du centre"
        elif self.etat == "CHOIX_DIRECTION":
            message = f"{joueur_actuel.nom}, choisissez une direction"
        font = pygame.font.Font(None, 36)  # Police pour le message
        texte = font.render(message, True, NOIR)  # Rend le texte en noir
        fenetre.blit(texte, (50, 20))  # Affiche le message en haut à gauche

        pygame.display.flip()  # Met à jour l'écran pour montrer les changements

    # Méthode pour trouver quelle carte a été cliquée dans un tableau
    def get_position_cliquee(self, x, y, tableau_x, tableau_y):
        for i in range(4):  # Boucle sur les lignes
            for j in range(4):  # Boucle sur les colonnes
                # Calcule la position de la carte à l'écran
                carte_x = tableau_x + j * (carte_largeur + espacement)
                carte_y = tableau_y + i * (carte_hauteur + espacement)
                # Vérifie si le clic (x, y) est dans les limites de la carte
                if carte_x <= x < carte_x + carte_largeur and carte_y <= y < carte_y + carte_hauteur:
                    return (i, j)  # Retourne la position (i, j) de la carte
        return None  # Retourne None si aucune carte n’est cliquée

    # Méthode pour calculer le score d’un joueur à la fin
    def calculer_score(self, tableau):
        # Crée une grille pour marquer les cases visitées
        visite = [[False for _ in range(4)] for _ in range(4)]
        somme = 0  # Somme des valeurs des cartes isolées
        for i in range(4):  # Boucle sur les lignes
            for j in range(4):  # Boucle sur les colonnes
                if not visite[i][j] and tableau[i][j]:  # Si non visité et carte présente
                    # Trouve le groupe de cartes adjacentes de même valeur
                    groupe = self.dfs(tableau, i, j, visite, tableau[i][j].valeur)
                    if len(groupe) == 1:  # Si le groupe contient une seule carte
                        somme += tableau[i][j].valeur  # Ajoute sa valeur au score
        return somme  # Retourne le score total

    # Méthode pour trouver les groupes de cartes adjacentes (DFS = Depth-First Search)
    def dfs(self, tableau, i, j, visite, valeur):
        # Vérifie si la position est valide et si la carte correspond à la valeur
        if (i < 0 or i >= 4 or j < 0 or j >= 4 or visite[i][j] or
            tableau[i][j] is None or tableau[i][j].valeur != valeur):
            return []  # Retourne une liste vide si conditions non remplies
        visite[i][j] = True  # Marque la case comme visitée
        groupe = [(i, j)]  # Ajoute la position actuelle au groupe
        # Vérifie les 4 directions : haut, bas, gauche, droite
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            groupe += self.dfs(tableau, i + di, j + dj, visite, valeur)  # Appel récursif
        return groupe  # Retourne le groupe complet

    # Boucle principale du jeu
    def main(self):
        running = True  # Variable pour garder la boucle active
        while running:
            self.afficher()  # Met à jour l’affichage à chaque tour
            for event in pygame.event.get():  # Récupère tous les événements
                if event.type == pygame.QUIT:  # Si l’utilisateur ferme la fenêtre
                    running = False  # Arrête la boucle
                elif event.type == pygame.MOUSEBUTTONDOWN and self.etat != "FIN":  # Si clic de souris
                    x, y = event.pos  # Récupère les coordonnées du clic
                    joueur = self.ordre_joueurs[self.joueur_actuel_index]  # Joueur actuel

                    # Si on choisit une carte dans son tableau (humain seulement)
                    if self.etat == "CHOIX_CARTE" and not joueur.est_ia:
                        idx = self.joueurs.index(joueur)  # Index du joueur dans la liste
                        tableau_x, tableau_y = self.positions_tableaux[idx]  # Position de son tableau
                        pos = self.get_position_cliquee(x, y, tableau_x, tableau_y)  # Carte cliquée
                        if pos:  # Si une carte a été cliquée
                            i, j = pos  # Récupère les coordonnées
                            if joueur.tableau[i][j] and not joueur.tableau[i][j].revelee:  # Si face cachée
                                carte = joueur.tableau[i][j]  # Récupère la carte
                                joueur.tableau[i][j] = None  # Vide la case
                                joueur.position_vide = (i, j)  # Marque la position vide
                                self.cartes_choisies.append(carte)  # Ajoute la carte au centre
                                self.joueur_actuel_index += 1  # Passe au joueur suivant
                                # Si tous les joueurs ont joué
                                if self.joueur_actuel_index >= len(self.joueurs):
                                    for carte in self.cartes_choisies:
                                        carte.revelee = True  # Révèle toutes les cartes
                                    self.etat = "CHOIX_CARTE_CENTRE"  # Passe à l’état suivant
                                    self.joueur_actuel_index = 0  # Retour au premier joueur

                    # Si on choisit une carte au centre (humain seulement)
                    elif self.etat == "CHOIX_CARTE_CENTRE" and not joueur.est_ia:
                        for k, carte in enumerate(self.cartes_choisies):  # Boucle sur les cartes au centre
                            carte_x = self.position_centre[0] + k * (carte_largeur + espacement)
                            carte_y = self.position_centre[1]
                            # Vérifie si le clic est sur cette carte
                            if (carte_x <= x < carte_x + carte_largeur and
                                carte_y <= y < carte_y + carte_hauteur):
                                joueur.carte_recuperee = carte  # Récupère la carte
                                self.cartes_choisies.remove(carte)  # Retire la carte du centre
                                self.etat = "CHOIX_DIRECTION"  # Passe à l’état suivant
                                i, j = joueur.position_vide  # Position de la case vide
                                idx = self.joueurs.index(joueur)  # Index du joueur
                                tableau_x, tableau_y = self.positions_tableaux[idx]  # Position du tableau
                                bouton_y = tableau_y + 4 * (carte_hauteur + espacement) + 20  # Position des boutons
                                self.boutons_direction = []  # Réinitialise les boutons
                                # Ajoute les boutons possibles selon la position vide
                                if j > 0:
                                    self.boutons_direction.append(Bouton(tableau_x, bouton_y, 60, 30, "Gauche"))
                                if j < 3:
                                    self.boutons_direction.append(Bouton(tableau_x + 70, bouton_y, 60, 30, "Droite"))
                                if i > 0:
                                    self.boutons_direction.append(Bouton(tableau_x + 140, bouton_y, 60, 30, "Haut"))
                                if i < 3:
                                    self.boutons_direction.append(Bouton(tableau_x + 210, bouton_y, 60, 30, "Bas"))
                                break

                    # Si on choisit une direction (humain seulement)
                    elif self.etat == "CHOIX_DIRECTION" and not joueur.est_ia:
                        for bouton in self.boutons_direction:  # Boucle sur les boutons
                            if bouton.est_clique(x, y):  # Si un bouton est cliqué
                                direction = bouton.texte.lower()  # Récupère la direction (en minuscules)
                                i, j = joueur.position_vide  # Position de la case vide
                                # Déplace les cartes selon la direction choisie
                                if direction == "gauche":
                                    for k in range(j, 0, -1):  # Décale vers la gauche
                                        joueur.tableau[i][k] = joueur.tableau[i][k-1]
                                    joueur.tableau[i][0] = None  # Nouvelle case vide
                                    joueur.position_vide = (i, 0)
                                elif direction == "droite":
                                    for k in range(j, 3):  # Décale vers la droite
                                        joueur.tableau[i][k] = joueur.tableau[i][k+1]
                                    joueur.tableau[i][3] = None  # Nouvelle case vide
                                    joueur.position_vide = (i, 3)
                                elif direction == "haut":
                                    for k in range(i, 0, -1):  # Décale vers le haut
                                        joueur.tableau[k][j] = joueur.tableau[k-1][j]
                                    joueur.tableau[0][j] = None  # Nouvelle case vide
                                    joueur.position_vide = (0, j)
                                elif direction == "bas":
                                    for k in range(i, 3):  # Décale vers le bas
                                        joueur.tableau[k][j] = joueur.tableau[k+1][j]
                                    joueur.tableau[3][j] = None  # Nouvelle case vide
                                    joueur.position_vide = (3, j)
                                # Place la carte récupérée dans la case vide
                                i, j = joueur.position_vide
                                joueur.tableau[i][j] = joueur.carte_recuperee
                                joueur.carte_recuperee.revelee = True  # Révèle la carte
                                joueur.position_vide = None  # Plus de case vide
                                self.boutons_direction = []  # Vide les boutons
                                self.joueur_actuel_index += 1  # Passe au joueur suivant
                                # Si tous les joueurs ont joué
                                if self.joueur_actuel_index >= len(self.joueurs):
                                    self.etat = "CHOIX_CARTE"  # Retour au début
                                    self.joueur_actuel_index = 0
                                else:
                                    self.etat = "CHOIX_CARTE_CENTRE"  # Continue avec le centre
                                break

            # Gestion des tours de l’IA
            joueur = self.ordre_joueurs[self.joueur_actuel_index]
            if joueur.est_ia:  # Si le joueur actuel est une IA
                if self.etat == "CHOIX_CARTE":  # Choix d’une carte
                    i, j = joueur.choisir_carte()  # L’IA choisit une carte
                    carte = joueur.tableau[i][j]  # Récupère la carte
                    joueur.tableau[i][j] = None  # Vide la case
                    joueur.position_vide = (i, j)  # Marque la position vide
                    self.cartes_choisies.append(carte)  # Ajoute au centre
                    self.joueur_actuel_index += 1  # Passe au suivant
                    if self.joueur_actuel_index >= len(self.joueurs):  # Si tous ont joué
                        for carte in self.cartes_choisies:
                            carte.revelee = True  # Révèle les cartes
                        self.etat = "CHOIX_CARTE_CENTRE"  # Passe au centre
                        self.joueur_actuel_index = 0

                elif self.etat == "CHOIX_CARTE_CENTRE":  # Choix d’une carte au centre
                    carte = joueur.choisir_carte_centre(self.cartes_choisies)  # L’IA choisit
                    joueur.carte_recuperee = carte  # Récupère la carte
                    self.cartes_choisies.remove(carte)  # Retire du centre
                    self.etat = "CHOIX_DIRECTION"  # Passe à l’état suivant

                elif self.etat == "CHOIX_DIRECTION":  # Choix d’une direction
                    direction = joueur.choisir_direction(joueur.position_vide)  # L’IA choisit
                    i, j = joueur.position_vide  # Position de la case vide
                    # Déplace les cartes selon la direction
                    if direction == "gauche":
                        for k in range(j, 0, -1):
                            joueur.tableau[i][k] = joueur.tableau[i][k-1]
                        joueur.tableau[i][0] = None
                        joueur.position_vide = (i, 0)
                    elif direction == "droite":
                        for k in range(j, 3):
                            joueur.tableau[i][k] = joueur.tableau[i][k+1]
                        joueur.tableau[i][3] = None
                        joueur.position_vide = (i, 3)
                    elif direction == "haut":
                        for k in range(i, 0, -1):
                            joueur.tableau[k][j] = joueur.tableau[k-1][j]
                        joueur.tableau[0][j] = None
                        joueur.position_vide = (0, j)
                    elif direction == "bas":
                        for k in range(i, 3):
                            joueur.tableau[k][j] = joueur.tableau[k+1][j]
                        joueur.tableau[3][j] = None
                        joueur.position_vide = (3, j)
                    # Place la carte récupérée
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

            # Vérifie si le jeu est fini (toutes les cartes révélées)
            toutes_revelees = True
            for joueur in self.joueurs:
                for ligne in joueur.tableau:
                    for carte in ligne:
                        if carte and not carte.revelee:  # S’il reste une carte face cachée
                            toutes_revelees = False
                            break
            if toutes_revelees:
                running = False  # Arrête le jeu

        # Fin du jeu : calcule et affiche les scores
        for joueur in self.joueurs:
            joueur.score = self.calculer_score(joueur.tableau)  # Calcule le score
            print(f"{joueur.nom} a un score de {joueur.score}")  # Affiche dans la console
        # Trouve le gagnant (celui avec le plus petit score)
        gagnant = min(self.joueurs, key=lambda j: j.score)
        print(f"Le gagnant est {gagnant.nom} avec un score de {gagnant.score}")
        pygame.quit()  # Ferme Pygame

# Point d’entrée du programme
if __name__ == "__main__":
    nb_joueurs = choisir_nombre_joueurs()  # Demande le nombre de joueurs
    nb_ia = choisir_nombre_ia(nb_joueurs)  # Demande le nombre d’IA
    jeu = JeuPygame(nb_joueurs, nb_ia)     # Crée une instance du jeu
    jeu.main()                             # Lance la boucle principale