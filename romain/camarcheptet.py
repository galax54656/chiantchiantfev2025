import pygame
import random
import asyncio
import platform

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu Dékal")

# Chargement des images
game_background = pygame.image.load("images/fonjeumtn.png").convert()
game_background = pygame.transform.scale(game_background, (1280, 720))

bouton_img = pygame.image.load('images/FOND BOUTON.png').convert_alpha()
bouton_img = pygame.transform.scale(bouton_img, (100, 50))
bouton_hover_img = pygame.image.load('images/fond_bouton2.png').convert_alpha()
bouton_hover_img = pygame.transform.scale(bouton_hover_img, (100, 50))

card_back_img = pygame.image.load('images/tigre.webp').convert()
card_face_img = pygame.image.load('images/avantvraicarterouge.png').convert()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

class Carte:
    def __init__(self, valeur, position=(0, 0)):
        self.valeur = valeur
        self.position = position
        self.cote = 'dos'
        self.scale = (50, 70)
        self.image_back = pygame.transform.scale(card_back_img, self.scale)
        self.image_face = pygame.transform.scale(card_face_img, self.scale)
        self.image = self.image_back
        self.rect = self.image.get_rect(topleft=position)
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(str(self.valeur), True, NOIR)

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
    def __init__(self, nom, ordi=False, position=(0, 0)):
        self.nom = nom
        self.ordi = ordi
        self.position = position
        self.tableau = []
        for i in range(4):
            ligne = []
            for j in range(4):
                carte = Carte(random.randint(1, 10))
                carte.position = (position[0] + j * 60, position[1] + i * 80)
                carte.rect.topleft = carte.position
                ligne.append(carte)
            self.tableau.append(ligne)
        for ligne in self.tableau:
            for carte in ligne:
                carte.cote = "dos"
        self.pos_vide = None
        self.score = 0
        self.carte_prise = None

class OrdiNiv1(Joueur):
    def __init__(self, nom, position=(0, 0)):
        super().__init__(nom, ordi=True, position=position)

    def choisir_carte(self):
        cartes_pas_retourne = []
        for i in range(4):
            for j in range(4):
                carte = self.tableau[i][j]
                if carte is not None and carte.cote == "dos":
                    cartes_pas_retourne.append((i, j))
        return random.choice(cartes_pas_retourne)

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
        self.rect = self.current_image.get_rect(topleft=pos)
        self.text_surf = self.font.render(self.text, True, self.base_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

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
    texte = font.render("Choisissez le nombre total de joueurs (2-6) :", True, NOIR)
    screen.blit(texte, (50, 50))
    boutons = []
    for i in range(2, 7):
        pos_x = 50 + (i - 2) * 150
        boutons.append(Bouton((pos_x, 100), str(i), font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)))
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
    texte = font.render(f"Choisissez le nombre d'IA (0-{nb_joueurs-1}) :", True, NOIR)
    screen.blit(texte, (50, 50))
    boutons = []
    for i in range(nb_joueurs):
        pos_x = 50 + i * 150
        boutons.append(Bouton((pos_x, 100), str(i), font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)))
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

def all_cards_revealed(joueurs):
    for joueur in joueurs:
        for ligne in joueur.tableau:
            for carte in ligne:
                if carte is not None and carte.cote == "dos":
                    return False
    return True

def calculate_score(tableau):
    visited = [[False for _ in range(4)] for _ in range(4)]
    score = 0
    def dfs(i, j, valeur):
        if (i < 0 or i >= 4 or j < 0 or j >= 4 or visited[i][j] or
            tableau[i][j] is None or tableau[i][j].valeur != valeur):
            return []
        visited[i][j] = True
        component = [(i, j)]
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            component += dfs(i + di, j + dj, valeur)
        return component
    for i in range(4):
        for j in range(4):
            if not visited[i][j] and tableau[i][j] is not None:
                component = dfs(i, j, tableau[i][j].valeur)
                if len(component) == 1:
                    score += tableau[i][j].valeur
    return score

def jeu(screen, nb_joueurs, nb_ordis):
    font = pygame.font.Font(None, 36)
    joueurs = []
    positions = [(50 + i * 250, 50) for i in range(nb_joueurs)]
    for i in range(nb_joueurs - nb_ordis):
        joueurs.append(Joueur(f"Joueur {i+1}", position=positions[i]))
    for i in range(nb_joueurs - nb_ordis, nb_joueurs):
        joueurs.append(OrdiNiv1(f"Ordi {i+1 - (nb_joueurs - nb_ordis)}", position=positions[i]))
    random.shuffle(joueurs)
    joueur_actuel_index = 0
    cartes_choisies = []
    etat = "CHOIX_CARTE"
    boutons_direction = []
    while True:
        screen.blit(game_background, (0, 0))
        for joueur in joueurs:
            for ligne in joueur.tableau:
                for carte in ligne:
                    if carte is not None:
                        carte.draw(screen)
        if etat in ["CHOIX_CARTE_CENTRE", "CHOIX_DIRECTION"]:
            for k, carte in enumerate(cartes_choisies):
                carte.rect.topleft = (50 + k * 60, 600)
                carte.draw(screen)
        if etat == "CHOIX_DIRECTION":
            for bouton in boutons_direction:
                bouton.update(screen)
        texte = font.render(f"Tour de {joueurs[joueur_actuel_index].nom}", True, NOIR)
        screen.blit(texte, (50, 20))
        pygame.display.flip()

        if etat == "CHOIX_CARTE" and not joueurs[joueur_actuel_index].ordi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(4):
                        for j in range(4):
                            carte = joueurs[joueur_actuel_index].tableau[i][j]
                            if (carte is not None and carte.cote == "dos" and
                                carte.rect.collidepoint(event.pos)):
                                joueurs[joueur_actuel_index].carte_prise = carte
                                joueurs[joueur_actuel_index].pos_vide = (i, j)
                                cartes_choisies.append(carte)
                                carte.rect.topleft = (50 + (len(cartes_choisies) - 1) * 60, 600)
                                joueurs[joueur_actuel_index].tableau[i][j] = None
                                joueur_actuel_index += 1
                                if joueur_actuel_index >= len(joueurs):
                                    for c in cartes_choisies:
                                        c.flip()
                                    etat = "CHOIX_CARTE_CENTRE"
                                    joueur_actuel_index = 0
                                break
        elif etat == "CHOIX_CARTE" and joueurs[joueur_actuel_index].ordi:
            i, j = joueurs[joueur_actuel_index].choisir_carte()
            carte = joueurs[joueur_actuel_index].tableau[i][j]
            joueurs[joueur_actuel_index].carte_prise = carte
            joueurs[joueur_actuel_index].pos_vide = (i, j)
            cartes_choisies.append(carte)
            carte.rect.topleft = (50 + (len(cartes_choisies) - 1) * 60, 600)
            joueurs[joueur_actuel_index].tableau[i][j] = None
            joueur_actuel_index += 1
            if joueur_actuel_index >= len(joueurs):
                for c in cartes_choisies:
                    c.flip()
                etat = "CHOIX_CARTE_CENTRE"
                joueur_actuel_index = 0
        elif etat == "CHOIX_CARTE_CENTRE" and not joueurs[joueur_actuel_index].ordi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for carte in cartes_choisies:
                        if carte.rect.collidepoint(event.pos):
                            joueurs[joueur_actuel_index].carte_prise = carte
                            cartes_choisies.remove(carte)
                            etat = "CHOIX_DIRECTION"
                            i, j = joueurs[joueur_actuel_index].pos_vide
                            grid_x, grid_y = joueurs[joueur_actuel_index].position
                            boutons_direction = []
                            if j > 0:
                                boutons_direction.append(Bouton((grid_x, grid_y + 330), "Gauche", font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)))
                            if j < 3:
                                boutons_direction.append(Bouton((grid_x + 110, grid_y + 330), "Droite", font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)))
                            if i > 0:
                                boutons_direction.append(Bouton((grid_x + 220, grid_y + 330), "Haut", font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)))
                            if i < 3:
                                boutons_direction.append(Bouton((grid_x + 330, grid_y + 330), "Bas", font, "White", "Red", bouton_img, bouton_hover_img, (100, 50)))
                            break
        elif etat == "CHOIX_CARTE_CENTRE" and joueurs[joueur_actuel_index].ordi:
            carte = min(cartes_choisies, key=lambda c: c.valeur)
            joueurs[joueur_actuel_index].carte_prise = carte
            cartes_choisies.remove(carte)
            i, j = joueurs[joueur_actuel_index].pos_vide
            directions = []
            if j > 0: directions.append("gauche")
            if j < 3: directions.append("droite")
            if i > 0: directions.append("haut")
            if i < 3: directions.append("bas")
            direction = random.choice(directions)
            tableau = joueurs[joueur_actuel_index].tableau
            if direction == "gauche":
                for k in range(j, 0, -1):
                    tableau[i][k] = tableau[i][k-1]
                tableau[i][0] = None
                joueurs[joueur_actuel_index].pos_vide = (i, 0)
            elif direction == "droite":
                for k in range(j, 3):
                    tableau[i][k] = tableau[i][k+1]
                tableau[i][3] = None
                joueurs[joueur_actuel_index].pos_vide = (i, 3)
            elif direction == "haut":
                for k in range(i, 0, -1):
                    tableau[k][j] = tableau[k-1][j]
                tableau[0][j] = None
                joueurs[joueur_actuel_index].pos_vide = (0, j)
            elif direction == "bas":
                for k in range(i, 3):
                    tableau[k][j] = tableau[k+1][j]
                tableau[3][j] = None
                joueurs[joueur_actuel_index].pos_vide = (3, j)
            i, j = joueurs[joueur_actuel_index].pos_vide
            tableau[i][j] = joueurs[joueur_actuel_index].carte_prise
            tableau[i][j].cote = "face"
            tableau[i][j].position = (joueurs[joueur_actuel_index].position[0] + j * 60, joueurs[joueur_actuel_index].position[1] + i * 80)
            tableau[i][j].rect.topleft = tableau[i][j].position
            joueurs[joueur_actuel_index].pos_vide = None
            joueur_actuel_index += 1
            if joueur_actuel_index >= len(joueurs):
                if all_cards_revealed(joueurs):
                    for joueur in joueurs:
                        joueur.score = calculate_score(joueur.tableau)
                    gagnant = min(joueurs, key=lambda j: j.score)
                    print(f"Le gagnant est {gagnant.nom} avec un score de {gagnant.score}")
                    return "menu"
                else:
                    etat = "CHOIX_CARTE"
                    joueur_actuel_index = 0
            else:
                etat = "CHOIX_CARTE_CENTRE"
        elif etat == "CHOIX_DIRECTION" and not joueurs[joueur_actuel_index].ordi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for bouton in boutons_direction:
                        if bouton.au_dessus(event.pos):
                            direction = bouton.text.lower()
                            i, j = joueurs[joueur_actuel_index].pos_vide
                            tableau = joueurs[joueur_actuel_index].tableau
                            if direction == "gauche":
                                for k in range(j, 0, -1):
                                    tableau[i][k] = tableau[i][k-1]
                                tableau[i][0] = None
                                joueurs[joueur_actuel_index].pos_vide = (i, 0)
                            elif direction == "droite":
                                for k in range(j, 3):
                                    tableau[i][k] = tableau[i][k+1]
                                tableau[i][3] = None
                                joueurs[joueur_actuel_index].pos_vide = (i, 3)
                            elif direction == "haut":
                                for k in range(i, 0, -1):
                                    tableau[k][j] = tableau[k-1][j]
                                tableau[0][j] = None
                                joueurs[joueur_actuel_index].pos_vide = (0, j)
                            elif direction == "bas":
                                for k in range(i, 3):
                                    tableau[k][j] = tableau[k+1][j]
                                tableau[3][j] = None
                                joueurs[joueur_actuel_index].pos_vide = (3, j)
                            i, j = joueurs[joueur_actuel_index].pos_vide
                            tableau[i][j] = joueurs[joueur_actuel_index].carte_prise
                            tableau[i][j].cote = "face"
                            tableau[i][j].position = (joueurs[joueur_actuel_index].position[0] + j * 60, joueurs[joueur_actuel_index].position[1] + i * 80)
                            tableau[i][j].rect.topleft = tableau[i][j].position
                            joueurs[joueur_actuel_index].pos_vide = None
                            boutons_direction = []
                            joueur_actuel_index += 1
                            if joueur_actuel_index >= len(joueurs):
                                if all_cards_revealed(joueurs):
                                    for joueur in joueurs:
                                        joueur.score = calculate_score(joueur.tableau)
                                    gagnant = min(joueurs, key=lambda j: j.score)
                                    print(f"Le gagnant est {gagnant.nom} avec un score de {gagnant.score}")
                                    return "menu"
                                else:
                                    etat = "CHOIX_CARTE"
                                    joueur_actuel_index = 0
                            else:
                                etat = "CHOIX_CARTE_CENTRE"
                            break

async def main():
    nb_joueurs = choix_nombre_joueurs()
    nb_ordis = choisir_nombre_ia(nb_joueurs)
    result = jeu(screen, nb_joueurs, nb_ordis)
    if result == "quit":
        pygame.quit()
        exit()

FPS = 60
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())