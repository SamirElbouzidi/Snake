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