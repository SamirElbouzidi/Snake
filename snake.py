import pygame
import random

larg_hau = pygame.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.taille = game.zoom_jeu
                    #pygame.Rect  (left, top, width, height)
        self.rect = pygame.Rect([0, 0, game.zoom_jeu - 2, game.zoom_jeu - 2])
        self.rect.center = self.position_aleatoire()
        self.direction = larg_hau(0, 0)
        self.directions = { pygame.K_UP: True, 
                            pygame.K_DOWN: True, 
                            pygame.K_LEFT: True, 
                            pygame.K_RIGHT: True
                        }
        
        self.vitesse_snake = 70  # milliseconde
        self.temp = 0
        self.longueur = 1
        self.segments = []
       

    # Indiquer les direction du serpent avec les touche du clavier
    def controlleur(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.directions[pygame.K_UP]:
                self.direction = larg_hau(0, -self.taille)
                self.directions = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: True, pygame.K_RIGHT: True}

            if event.key == pygame.K_DOWN and self.directions[pygame.K_DOWN]:
                self.direction = larg_hau(0, self.taille)
                self.directions = {pygame.K_UP: False, pygame.K_DOWN: True, pygame.K_LEFT: True, pygame.K_RIGHT: True}

            if event.key == pygame.K_LEFT and self.directions[pygame.K_LEFT]:
                self.direction = larg_hau(-self.taille, 0)
                self.directions = {pygame.K_UP: True, pygame.K_DOWN: True, pygame.K_LEFT: True, pygame.K_RIGHT: False}

            if event.key == pygame.K_RIGHT and self.directions[pygame.K_RIGHT]:
                self.direction = larg_hau(self.taille, 0)
                self.directions = {pygame.K_UP: True, pygame.K_DOWN: True, pygame.K_LEFT: False, pygame.K_RIGHT: True}
                
    # La vitesse du jeu
    def vitesse(self):
        nouveau_temp = pygame.time.get_ticks() # renvoie le nombre en milliseconde
        if nouveau_temp - self.temp > self.vitesse_snake:
            self.temp = nouveau_temp
            return True
        return False
    
    # Position aléatoire du Fruit / Serpent
    def position_aleatoire(self):
        return [random.randrange(self.taille // 2, self.game.taille_ecran - self.taille // 2, self.taille)] * 2

        # Limitation de la zone à la taille d'ecran
    def verifier_zone(self):
        if self.rect.left < 0 or self.rect.right > self.game.taille_ecran:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.taille_ecran:
            self.game.new_game()

        # Verifier si il y a un fruit
    def verifie_fruit(self):
        # Si le serpent et situer au meme endroit que le fruit
        if self.rect.center == self.game.fruit.rect.center:
            # alors le fruit change de position aléatoirement
            self.game.fruit.rect.center = self.position_aleatoire()
            # Rajoute un segment au serpent
            self.longueur += 1
            
        # Verifier si il se mange lui meme
    def mange_lui_meme(self):
        # Renvoie la longeur du serpent 
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.new_game()

        # Mouvement du serpent
    def mouvement(self):
        if self.vitesse():
            # Renvoie un nouveau rectangle qui est déplacé par le décalage donné.
            self.rect.move_ip(self.direction)
            # Ajoute dans la liste et fait une Copie superficielle de la taille du serpent
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.longueur:]

    def update(self):
        self.mange_lui_meme()
        self.verifier_zone()
        self.verifie_fruit()
        self.mouvement()

    def dessiner_serpent(self):
        [pygame.draw.rect(self.game.screen, 'yellow', segment) for segment in self.segments]

#-----------------------------------------------------------------------------------------------------
class Food:
    def __init__(self, game):
        self.game = game
        self.taille = game.zoom_jeu
        self.rect = pygame.Rect([0, 0, game.zoom_jeu - 2, game.zoom_jeu - 2])
        self.rect.center = self.game.snake.position_aleatoire()

    def dessiner_fruit(self):
        pygame.draw.rect(self.game.screen, 'purple', self.rect)

#------------------------------------------------------------------------------------------------
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