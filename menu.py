import pygame


from button import Button

class Menu:
    pygame.font.init()
 
        

    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.SysFont(None, 34)
        self.buttons = []
        self.labels = []

    def update(self):
        self.screen.fill("Blue")
        #self.screen.blit(self.bg, (0, 0))

        for button in self.buttons:
            button.draw()

        for label in self.labels:
            self.screen.blit(label[0], label[1])


    def addButton(self, id, x, y, w, h, image, text, size, color):
        self.font = pygame.font.SysFont(None, 34)
        img = self.font.render('Hello', True, 'BLUE')
        self.screen.blit(img, (20, 20))

        """ self.buttons.append(Button(id, x, y, w, h, image, self.screen, text, self.font, color))"""

    def addLabel(self, x, y, text, size, color):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20, "white")
        self.labels.append((self.font.render(text, True, color), (x,y)))

    def collide(self, x, y):
        for button in self.buttons:
            if button.collide(x, y):
                return (True,button.id)
        return (False, 0)