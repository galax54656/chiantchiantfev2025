# game.py
import pygame
import random

# Chargement et transformation des images pour le jeu
game_background = pygame.image.load("images/fonjeumtn.png").convert()
game_background = pygame.transform.scale(game_background, (1280, 720))
card_back_img = pygame.image.load('images/tigre.webp').convert()
card_face_img = pygame.image.load('images/avantvraicarterouge.png').convert()


class Card:
    def __init__(self, position=(200, 200), scale=(100, 150)):
        self.value = random.randint(1, 10)
        self.position = position
        self.state = 'back'  # 'back' = face cachée, 'face' = face visible
        self.scale = scale

        self.image_back = pygame.transform.scale(card_back_img, scale)
        self.image_face = pygame.transform.scale(card_face_img, scale)

        self.image = self.image_back
        self.rect = self.image.get_rect(topleft=position)

        self.font = pygame.font.Font(None, 75)
        self.text = self.font.render(str(self.value), True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.state == 'face':
            text_rect = self.text.get_rect(center=self.rect.center)
            screen.blit(self.text, text_rect)

    def flip(self):
        if self.state == 'back':
            self.state = 'face'
            self.image = self.image_face
            self.rect.center = (640, 360)
        else:
            self.state = 'back'
            self.image = self.image_back
            self.rect.topleft = self.position


def game_loop(screen):
    clock = pygame.time.Clock()
    card = Card()  # Création d'une carte

    running = True
    while running:
        screen.blit(game_background, (0, 0))
        card.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Retour vers le main pour quitter
            if event.type == pygame.MOUSEBUTTONDOWN:
                if card.rect.collidepoint(event.pos):
                    card.flip()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"  # Retour au menu principal avec la touche Échap

        pygame.display.update()
        clock.tick(60)
