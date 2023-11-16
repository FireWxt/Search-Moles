import  pygame 
pygame.init()

from game import Game

if __name__== "__main__":
    game = Game()
    game.run()

      
#créer la fenêtre du jeu 
ecran = pygame.display.set_mode((800,800))
pygame.display.set_caption("Search Moles")      

def run():
    #boucle du jeu pour laisser la fenêtre ouverte et la fermer avec la croix 
    running = True             
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    



