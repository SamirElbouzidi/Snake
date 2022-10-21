import pygame
import random

from food import Food
from snake import Snake

# code : BARF
# Rendu Python

        
class Game:
    def __init__(self):
        pygame.init()
        self.taille_ecran = 700
        self.zoom_jeu = 35
        self.screen = pygame.display.set_mode([self.taille_ecran] * 2)
        self.clock = pygame.time.Clock()
        self.new_game()

    # Creation de grille en fond d'ecran
    def dessiner_grille(self):
         # pygame.draw.line(surface, color, start_position, end_position)
        [pygame.draw.line(self.screen, [50, 50, 168] , (x, 0), (x, self.taille_ecran))
                                             for x in range(0, self.taille_ecran, self.zoom_jeu)]
        [pygame.draw.line(self.screen, [50, 50, 168], (0, y), (self.taille_ecran, y))
                                             for y in range(0, self.taille_ecran, self.zoom_jeu)]
    # Nouvelle partie
    def new_game(self):
        self.snake = Snake(self)
        self.fruit = Food(self)

    def mise_a_jour(self):
        self.snake.update()
        pygame.display.flip()
        self.clock.tick(60)

    def dessiner(self):
        # Fond d'ecran du jeu
        self.screen.fill('green')
        # Dessiner les grille en fond d'ecran
        self.dessiner_grille()
        # Dessiner la classe Fruit
        self.fruit.dessiner_fruit()
        # Dessiner la classe serpent 
        self.snake.dessiner_serpent()

    def verifier_evenement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # La méthode controlleur
            self.snake.controlleur(event)

    def run(self):
        while True:
            self.verifier_evenement()
            self.mise_a_jour()
            self.dessiner()


if __name__ == '__main__':
    jeu = Game()
    jeu.run()