import pygame
import pytmx
import pyscroll


pygame.init()

class Player (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.spriteSheet = pygame.image.load("basil.png")
        self.image = self.getImage(0,0)
        self.image.set_colorkey([0, 0, 0])

         #enlève la couleur de fond du joueur Basil     
        self.rect = self.image.get_rect()

        #positioin du joueur au centre de la map
        self.position =[x, y]
        
        #création d'un dictionnaire qui permet de stocké toutes les orientations du personnages
        self.images = {
            'down' : self.getImage(0, 0),
            'left' : self.getImage(0, 60),
            'right' : self.getImage(0, 124),
            'up': self.getImage(0, 188)
        }

        self.pied = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        #vitesse de déplacement
        self.speed = 3

    def update(self) :
            self.rect.topleft = self.position
            self.pied.midbottom = self.rect.midbottom

    def saveLocation(self): 
        self.old_position = self.position.copy()

    def changeAnimation(self, name): 
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def moveRight(self): self.position[0] +=self.speed
    
    def moveLeft(self): self.position[0] -=self.speed
    
    def moveUp(self): self.position[1] -=self.speed
    
    def moveDown(self): self.position[1] +=self.speed
         
    def moveBack(self):
         self.position = self.old_position
         self.rect.topleft = self.position
         self.pied.midbottom = self.rect.midbottom

    

    def getImage(self, x, y):
        image = pygame.Surface([75,75])
        #prendre 1 morceau de notre sprite 
        image.blit(self.spriteSheet, (0,0), (x, y,70, 70))
        return image
        
     #permet d'actualiser la position du joueur lors de ses déplacements avec sa vitesse
    def movRight(self) : self.position[0] += self.speed
    def moveLeft(self) : self.position[0] -= self.speed
    def moveUp(self) : self.position[1] -= self.speed
    def moveDown(self) : self.position[1] += self.speed
