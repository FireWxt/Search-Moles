import pygame
import random

pygame.init()

#Création de la classe qui va permettre de gérer les taupes sur le jeu

class Taupe(pygame.sprite.Sprite):

    def __init__(self, x, y, points = 0):
        super().__init__()
        self.positionTaupe =[x, y]
        self.points = points
        
    def update(self) :
            self.rect.topleft = self.positionTaupe
                         
    

class TaupeMarron(Taupe):
    
    def __init__(self, x, y, points = 0):
        Taupe.__init__(self,x, y, points)
        self.image = pygame.image.load('././asset/taupe1.png')
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.pied = pygame.Rect(0, 0, self.rect.width * 0.5, 1)

class TaupeRouge(Taupe):
    
    def __init__(self, x, y, points = 0):
        Taupe.__init__(self,x ,y, points) 
        self.image = pygame.image.load('././asset/taupe2.png')
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.pied = pygame.Rect(0, 0, self.rect.width * 0.5, 1)


class TaupeJaune(Taupe):
    
    def __init__(self, x, y, points = 0):
        Taupe.__init__(self,x, y, points)   
        self.image = pygame.image.load('././asset/taupe_3.png')
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.pied = pygame.Rect(0, 0, self.rect.width * 0.5, 1)
        


    def getImage(self, x, y):
        image = pygame.Surface([75,75])
        #prendre 1 morceau de notre sprite 
        image.blit(self.image, (0,0), (x, y, 75, 75))
        return image