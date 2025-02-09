import pygame

screen = pygame.display.set_mode((1280, 720))  # initialise la fenêtre ainsi que sa taille(X,Y)

class carte():
    def __init__(self, valeur, position_start=(0,0)):
        self.valeur = valeur
        self.position = position_start
        self.state = 'bas'#face vers le bas='bas'
class board():
    def __init__(self, joueurs):
        if joueurs==2:
            pygame.draw.line(screen, (0, 0, 0), (0, 360), (1280,360))


def jeu_a_2():
    # Initialisation de Pygame
    pygame.init()
    pygame.display.set_caption("Jeu")  # donne le nom à la fenêtre

    # Charger l'image de fond
    background = pygame.image.load("images/fonjeumtn.png")
    background = pygame.transform.scale(background, (1280, 720))

    # Boucle principale
    running = True
    while running:
        screen.blit(background, (0, 0))  # Afficher le fond d'abord

        # Dessiner la ligne après le fond pour éviter qu'elle soit recouverte
        pygame.draw.line(screen, (0, 0, 0), (0, 360), (1280, 360), 3)  # Ajout de l'épaisseur

        menu_mouse_pos = pygame.mouse.get_pos()  # facilite la récupération de la position de la souris

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Mettre à jour l'affichage

    pygame.quit()


jeu_a_2()
