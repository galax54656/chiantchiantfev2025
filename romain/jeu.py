import pygame
import random

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))  # Initialise la fenêtre
pygame.display.set_caption("Jeu")  # Nom de la fenêtre

# Charger les images de la carte
arriere_carte = pygame.image.load('images/tigre.webp').convert()
carte_face = pygame.image.load('images/avantvraicarterouge.png').convert()


class Carte:
    def __init__(self, position_start=(200, 200), scale=[100, 150]):  # Taille par défaut
        self.valeur = random.randint(1, 10)
        self.position = position_start
        self.state = 'bas'  # Face cachée au début
        self.scale = scale

        # Charger les images et les redimensionner
        self.im_arriere = pygame.transform.scale(arriere_carte, (self.scale[0], self.scale[1]))
        self.im_face = pygame.transform.scale(carte_face, (self.scale[0], self.scale[1]))

        self.image = self.im_arriere  # Image affichée par défaut (face cachée)
        self.rect = self.image.get_rect(topleft=self.position)

        # Police pour afficher la valeur
        self.font = pygame.font.Font(None, 75)
        self.text = self.font.render(str(self.valeur), True, (255, 255, 255))

    def draw(self, screen):
        """Affiche la carte et la valeur si elle est retournée."""
        screen.blit(self.image, self.rect.topleft)  # Afficher l'image de la carte

        if self.state == 'haut':  # Si la carte est face visible, afficher la valeur
            text_rect = self.text.get_rect(center=self.rect.center)
            screen.blit(self.text, text_rect)

    def tourne(self):
        """Retourne la carte, met à jour son image et sa position."""
        if self.state == 'bas':  # Si elle est face cachée, la retourner et la mettre au centre
            self.state = 'haut'
            self.image = self.im_face
            self.rect.center = (640, 360)  # Déplacer au centre
        else:  # Sinon, la remettre à sa position initiale
            self.state = 'bas'
            self.image = self.im_arriere
            self.rect.topleft = (200, 200)  # Retour à la position de départ


class Board:
    def __init__(self, joueurs):
        self.joueurs = joueurs

    def draw(self, screen):
        """Dessine la ligne séparatrice si le mode est 2 joueurs."""
        if self.joueurs == 2:
            pygame.draw.line(screen, (0, 0, 0), (0, 360), (1280, 360), 3)


def jeu_a_2():
    # Charger l'image de fond
    background = pygame.image.load("images/fonjeumtn.png")
    background = pygame.transform.scale(background, (1280, 720))

    carte1 = Carte()  # Création d'une carte
    board1 = Board(2)  # Création du plateau

    # Boucle principale
    running = True
    while running:
        screen.blit(background, (0, 0))  # Afficher le fond
        board1.draw(screen)  # Dessiner le plateau
        carte1.draw(screen)  # Dessiner la carte

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if carte1.rect.collidepoint(event.pos):  # Vérification de la collision avec la souris
                    carte1.tourne()  # Retourner la carte

        pygame.display.flip()  # Mettre à jour l'affichage

    pygame.quit()


jeu_a_2()
