import pygame
import random
import sys
import time

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu Dékal")

# Chargement des images
try:
    game_background = pygame.image.load("images/fonjeumtn.png").convert()
    game_background = pygame.transform.scale(game_background, (1280, 720))

    bouton_img = pygame.image.load('images/FOND BOUTON.png').convert_alpha()
    bouton_img = pygame.transform.scale(bouton_img, (380, 100))
    bouton_hover_img = pygame.image.load('images/fond_bouton2.png').convert_alpha()
    bouton_hover_img = pygame.transform.scale(bouton_hover_img, (380, 100))

    card_back_img = pygame.image.load('images/tigre.webp').convert()
    card_face_img = pygame.image.load('images/avantvraicarterouge.png').convert()
except pygame.error:
    print("Images non trouvées, utilisation des couleurs par défaut")
    game_background = pygame.Surface((1280, 720))
    game_background.fill((50, 100, 150))

    bouton_img = pygame.Surface((380, 100))
    bouton_img.fill((70, 70, 70))
    bouton_hover_img = pygame.Surface((380, 100))
    bouton_hover_img.fill((100, 100, 100))

    card_back_img = pygame.Surface((50, 70))
    card_back_img.fill((200, 100, 0))
    card_face_img = pygame.Surface((50, 70))
    card_face_img.fill((150, 0, 0))

# Constantes de couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (100, 100, 100)
ROUGE = (255, 0, 0)
VERT = (0, 200, 0)

# Dimensions des cartes
CARTE_LARGEUR = 50
CARTE_HAUTEUR = 70
ESPACEMENT = 10

class Carte:
    def __init__(self, valeur, position=(0, 0), scale=(CARTE_LARGEUR, CARTE_HAUTEUR)):
        self.valeur = valeur
        self.position = position
        self.cote = 'dos'
        self.scale = scale

        self.image_back = pygame.transform.scale(card_back_img, scale)
        self.image_face = pygame.transform.scale(card_face_img, scale)
        self.image = self.image_back
        self.rect = self.image.get_rect(topleft=position)

        self.font = pygame.font.Font(None, 36)
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

    def update_position(self, position):
        self.position = position
        self.rect.topleft = position

class Joueur:
    def __init__(self, nom, est_ordi=False, position=(0, 0)):
        self.nom = nom
        self.est_ordi = est_ordi
        self.position = position
        self.tableau = [[Carte(random.randint(1, 10)) for _ in range(4)] for _ in range(4)]
        self.update_card_positions()
        self.pos_vide = None
        self.score = 0
        self.nb_cartes = 16
        self.carte_prise = None

    def update_card_positions(self):
        x_base, y_base = self.position
        for i in range(4):
            for j in range(4):
                if self.tableau[i][j]:
                    x = x_base + j * (CARTE_LARGEUR + ESPACEMENT)
                    y = y_base + i * (CARTE_HAUTEUR + ESPACEMENT)
                    self.tableau[i][j].update_position((x, y))

    def draw_tableau(self, screen):
        for i in range(4):
            for j in range(4):
                if self.tableau[i][j]:
                    self.tableau[i][j].draw(screen)
                else:
                    x, y = self.position
                    x += j * (CARTE_LARGEUR + ESPACEMENT)
                    y += i * (CARTE_HAUTEUR + ESPACEMENT)
                    pygame.draw.rect(screen, GRIS, (x, y, CARTE_LARGEUR, CARTE_HAUTEUR), 2)
        font = pygame.font.Font(None, 24)
        text = font.render(self.nom, True, BLANC)
        x, y = self.position
        screen.blit(text, (x, y - 30))

class OrdiNiv1(Joueur):
    def __init__(self, nom, position=(0, 0)):
        super().__init__(nom, est_ordi=True, position=position)

    def choisir_carte(self):
        choices = [(i, j) for i in range(4) for j in range(4)
                   if self.tableau[i][j] and self.tableau[i][j].cote == 'dos']
        return random.choice(choices)

    def choisir_carte_centre(self, cartes_centre):
        return min(cartes_centre, key=lambda c: c.valeur)

    def choisir_direction(self, position_vide):
        i, j = position_vide
        dirs = []
        if j > 0: dirs.append('gauche')
        if j < 3: dirs.append('droite')
        if i > 0: dirs.append('haut')
        if i < 3: dirs.append('bas')
        return random.choice(dirs)

class Bouton:
    def __init__(self, pos, text, font, base_color, hover_color, image=None, hover_image=None, scale=None):
        self.pos = pos
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        if image:
            self.image = pygame.transform.scale(image, scale) if scale else image
            self.hover_image = pygame.transform.scale(hover_image, scale) if hover_image else self.image
            self.current_image = self.image
            self.rect = self.current_image.get_rect(center=pos)
        else:
            self.rect = pygame.Rect(0, 0, 100, 50)
            self.rect.center = pos
        self.text_surf = self.font.render(self.text, True, self.base_color)
        self.text_rect = self.text_surf.get_rect(center=pos)

    def update(self, screen):
        if hasattr(self, 'current_image'):
            screen.blit(self.current_image, self.rect)
        else:
            pygame.draw.rect(screen, GRIS, self.rect)
            pygame.draw.rect(screen, NOIR, self.rect, 2)
        screen.blit(self.text_surf, self.text_rect)

    def est_survole(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text_surf = self.font.render(self.text, True, self.hover_color)
            if hasattr(self, 'hover_image'):
                self.current_image = self.hover_image
        else:
            self.text_surf = self.font.render(self.text, True, self.base_color)
            if hasattr(self, 'image'):
                self.current_image = self.image

def choix_nombre_joueurs():
    screen.blit(game_background, (0, 0))
    font = pygame.font.Font(None, 36)
    texte = font.render("Choisissez le nombre total de joueurs (2-6):", True, BLANC)
    screen.blit(texte, (400, 100))
    boutons = [Bouton((640, 200 + (i-2) * 80), str(i), font, BLANC, ROUGE,
                      bouton_img, bouton_hover_img, (200, 60)) for i in range(2, 7)]
    for btn in boutons: btn.update(screen)
    pygame.display.flip()
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for btn in boutons:
            btn.change_color(mouse_pos)
            btn.update(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in boutons:
                    if btn.est_survole(mouse_pos): return int(btn.text)

def choisir_nombre_ia(nb_joueurs):
    screen.blit(game_background, (0, 0))
    font = pygame.font.Font(None, 36)
    texte = font.render(f"Choisissez le nombre d'Ordinateurs (0-{nb_joueurs-1}):", True, BLANC)
    screen.blit(texte, (400, 100))
    boutons = [Bouton((640, 200 + i * 80), str(i), font, BLANC, ROUGE,
                      bouton_img, bouton_hover_img, (200, 60)) for i in range(nb_joueurs)]
    for btn in boutons: btn.update(screen)
    pygame.display.flip()
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for btn in boutons:
            btn.change_color(mouse_pos)
            btn.update(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in boutons:
                    if btn.est_survole(mouse_pos): return int(btn.text)

class JeuDekal:
    def __init__(self, nb_joueurs, nb_ordis):
        if not 2 <= nb_joueurs <= 6 or nb_ordis > nb_joueurs - 1:
            raise ValueError("Nombre de joueurs ou d'IA invalide.")

        self.nb_joueurs = nb_joueurs
        self.nb_ordis = nb_ordis
        self.tour_actuel = 0

        self.positions_joueurs = self.calculer_positions(nb_joueurs)
        self.joueurs = []

        for i in range(nb_joueurs):
            position = self.positions_joueurs[i]
            if i < nb_ordis:
                self.joueurs.append(OrdiNiv1(f"Ordi {i+1}", position))
            else:
                self.joueurs.append(Joueur(f"Joueur {i+1}", position))

        self.cartes_centre = [Carte(random.randint(1, 10)) for _ in range(3)]
        self.update_positions_cartes_centre()

    def update_positions_cartes_centre(self):
        centre_x = 640 - (len(self.cartes_centre) * (CARTE_LARGEUR + ESPACEMENT)) // 2
        y = 310
        for idx, carte in enumerate(self.cartes_centre):
            x = centre_x + idx * (CARTE_LARGEUR + ESPACEMENT)
            carte.update_position((x, y))

    def dessiner(self, screen):
        screen.blit(game_background, (0, 0))
        for joueur in self.joueurs:
            joueur.draw_tableau(screen)
        for carte in self.cartes_centre:
            carte.draw(screen)
        pygame.display.flip()

    def gerer_tour(self):
        joueur = self.joueurs[self.tour_actuel]

        if joueur.est_ordi:
            i, j = joueur.choisir_carte()
            joueur.tableau[i][j].flip()
            time.sleep(1)
        else:
            en_attente = True
            while en_attente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for i in range(4):
                            for j in range(4):
                                carte = joueur.tableau[i][j]
                                if carte and carte.rect.collidepoint(pos):
                                    carte.flip()
                                    en_attente = False
                                    break
                            if not en_attente:
                                break
                self.dessiner(screen)

        self.tour_actuel = (self.tour_actuel + 1) % self.nb_joueurs


def main():
    nb_joueurs = choix_nombre_joueurs()
    nb_ordis = choisir_nombre_ia(nb_joueurs)
    jeu = JeuDekal(nb_joueurs, nb_ordis)

    clock = pygame.time.Clock()
    while True:
        jeu.gerer_tour()
        jeu.dessiner(screen)
        clock.tick(30)

if __name__ == "__main__":
    main()
