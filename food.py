import pygame
from snake import Snake
class Food:
    def __init__(self, game):
        self.game = game
        self.taille = game.zoom_jeu
        self.rect = pygame.Rect([0, 0, game.zoom_jeu - 2, game.zoom_jeu - 2])
        self.rect.center = self.game.snake.position_aleatoire()

    def dessiner_fruit(self):
        pygame.draw.rect(self.game.screen, 'purple', self.rect)