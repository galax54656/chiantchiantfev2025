import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur = 800
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

class IA(Joueur):
    def __init__(self, nom):
        super().__init__(nom, est_ia=True)

    def choisir_carte(self):
        cartes_face_cachee = [(i, j) for i in range(4) for j in range(4) if self.tableau[i][j] and not self.tableau[i][j].revelee]
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

def choisir_mode_jeu():
    fenetre.fill(BLANC)
    font = pygame.font.Font(None, 36)
    texte = font.render("Choisissez le mode de jeu :", True, NOIR)
    fenetre.blit(texte, (50, 50))

    bouton_humain = Bouton(50, 100, 200, 50, "Contre un autre joueur")
    bouton_ia = Bouton(50, 160, 200, 50, "Contre l'ordinateur")

    bouton_humain.afficher(fenetre)
    bouton_ia.afficher(fenetre)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_humain.est_clique(x, y):
                    return "humain"
                elif bouton_ia.est_clique(x, y):
                    return "ia"

# Classe principale du jeu avec interface graphique
class JeuPygame:
    def __init__(self, nb_joueurs_humains):
        self.joueurs = [Joueur(f"Joueur {i+1}") for i in range(nb_joueurs_humains)]
        self.joueur_actuel_index = 0
        self.cartes_choisies = []
        self.etat = "CHOIX_CARTE"
        self.boutons_direction = []
        self.positions_tableaux = [(50 + i * 350, 50) for i in range(len(self.joueurs))]  # Positions des tableaux
        self.position_centre = (50, 400)  # Position des cartes au centre

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
            message = f"{self.joueurs[self.joueur_actuel_index].nom}, choisissez une carte face cachée"
        elif self.etat == "CHOIX_CARTE_CENTRE":
            message = f"{self.joueurs[self.joueur_actuel_index].nom}, choisissez une carte du centre"
        elif self.etat == "CHOIX_DIRECTION":
            message = f"{self.joueurs[self.joueur_actuel_index].nom}, choisissez une direction"
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
                    joueur = self.joueurs[self.joueur_actuel_index]

                    if self.etat == "CHOIX_CARTE" and not joueur.est_ia:
                        tableau_x, tableau_y = self.positions_tableaux[self.joueur_actuel_index]
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
                                tableau_x, tableau_y = self.positions_tableaux[self.joueur_actuel_index]
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
            joueur = self.joueurs[self.joueur_actuel_index]
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
            if all(all(carte and carte.revelee for carte in ligne) for joueur in self.joueurs for ligne in joueur.tableau):
                running = False

        # Afficher les scores
        for joueur in self.joueurs:
            joueur.score = self.calculer_score(joueur.tableau)
            print(f"{joueur.nom} a un score de {joueur.score}")
        gagnant = min(self.joueurs, key=lambda j: j.score)
        print(f"Le gagnant est {gagnant.nom} avec un score de {gagnant.score}")
        pygame.quit()

if __name__ == "__main__":
    mode_jeu = choisir_mode_jeu()
    if mode_jeu == "humain":
        jeu = JeuPygame(2)  # 2 joueurs humains
    else:
        jeu = JeuPygame(1)  # 1 joueur humain
        jeu.joueurs.append(IA("Ordinateur"))  # Ajouter l'IA
        jeu.positions_tableaux.append((400, 50))  # Ajouter la position du tableau de l'IA
    jeu.main()