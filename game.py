import pygame
import time
import pytmx
import pyscroll 
import random as ra


from entity import Taupe,TaupeMarron, TaupeJaune,TaupeRouge
from player import Player
pygame.init()



class Game: 

    def __init__(self):
        pygame.display.set_caption("Search Moles") 
        #créer la fenêtre du jeu 
        pygame.font.init()
        self.screen = pygame.display.set_mode((800,800))
        # charger la carte de jeu format TMX
        tmxData = pytmx.util_pygame.load_pygame("map.tmx")
        #on récupérer la carte
        mapData = pyscroll.data.TiledMapData(tmxData)
        #chargement des calques de la map
        mapLayer = pyscroll.orthographic.BufferedRenderer(mapData, self.screen.get_size())
        #Ajout des variables permettant de controler la vitesse et le nombre de taupe qui apparaîssent
        self.spawnTime = 50000/1000
        self.nombreSpawn = 25
        # Ajout d'une variable pour indiquer si le temps est écoulé
        self.finTemps = False
        self.score = 0
        playerPosition = tmxData.get_object_by_name("player")
        self.player = Player(playerPosition.x, playerPosition.y)
        positionTaupe = tmxData.get_object_by_name("taupe")
        self.taupes = Taupe(positionTaupe.x, positionTaupe.y)
        self.bottesCouldown = 5
        self.timeBottes = 0

        #Initialisation des variables permettant de savoir si les touches sont enfoncés
        self.touche1 = False
        self.touche2 = False
        self.touche3 = False

 
        #définition d'une liste qui va stocker les possibles points de spawn des taupes
        self.taupe = []

        for moles in tmxData.objects:
            if moles.name == "taupe":
                self.taupe.append(pygame.Rect(int(moles.x), int(moles.y), int(moles.width), int(moles.height)))

        #définition d'une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmxData.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height)))


        self.totalSecondes = 60# 1 minute
        self.tempsActuel = self.totalSecondes
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.clock = pygame.time.Clock()

        self.feverPourcentage = 0
        self.activationFever = False
        self.feverActiverUneFois = False

        #Ajout des variable permettant de controler le nombre d'item
        self.nbBombe = 3
        self.nbBottes = 3
        self.nbChrono = 3

        #dessiner le groupe de calques 
        #position par défaut du joueur pour default_layer soit 1 
        self.group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=4)
        self.group.add(self.player)    

         
    
    #définition du choix de la taupe aléatoirement
                   
    def choixTaupe(self):
        rando = ra.randint(1,3) 
        choix = ra.choice(self.taupe)
        if rando == 1 :
            self.taupeSelectione = TaupeMarron(choix.x, choix.y, points = 1)
        elif rando == 2 :
            self.taupeSelectione= TaupeRouge(choix.x, choix.y, points = 5)
        elif rando == 3:
            self.taupeSelectione = TaupeJaune(choix.x, choix.y, points = 10)
        self.group.add(self.taupeSelectione)

    # Ajout de la méthode qui permet de faire apparaitre les taupe aléatoirement sur la carte
    def spawnAutoTaupes(self):
        if not self.finTemps and self.tempsActuel > 0:
            if pygame.time.get_ticks() % self.spawnTime == 0:
                for i in range(self.nombreSpawn):
                    self.choixTaupe()


    
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if not self.finTemps:
            if pressed[pygame.K_UP]:
                self.player.moveUp()    
                self.player.changeAnimation('up')
            elif pressed[pygame.K_DOWN]:
                self.player.moveDown()
                self.player.changeAnimation('down')
            elif pressed[pygame.K_RIGHT]:
                self.player.moveRight()
                self.player.changeAnimation('right')
            elif pressed[pygame.K_LEFT]:
                self.player.moveLeft()
                self.player.changeAnimation('left')
            elif pressed[pygame.K_KP_1] and not self.touche1:
                self.bombe()
                self.touche1 = True
            elif not pressed[pygame.K_KP_1]:
                self.touche1 = False
            if pressed[pygame.K_KP_2] and not self.touche2:
                self.bottes()
                self.touche2 = True
            elif not pressed[pygame.K_KP_2]:
                self.touche2 = False
            if pressed[pygame.K_KP_3] and not self.touche3:
                self.chrono()
                self.touche3 = True
            elif not pressed[pygame.K_KP_3]:
                self.touche3 = False
            
            """ #elif pressed[pygame.K_SPACE]:
                #self.choixTaupe()
            les 2 lignes du dessus me permettait de faire appaître les taupes quand j'appuyais sur la touche espace,
            cela permet de faire des test"""
    #Ajout d'une méthode qui permet de calculer le % de fever
    
            
             


    def update(self):
        
        self.group.update()
        # Vérif collisions avec les taupes
        for taupe in self.group.sprites():
            if taupe != self.player and taupe.rect.colliderect(self.player.rect):
                # Collision détectée, retire la taupe touchée
                print(f"Collision avec la taupe! Points ajoutés : {taupe.points}")
                self.score += taupe.points
                self.group.remove(taupe)

        if time.time() > self.timeBottes + self.bottesCouldown:
            self.player.speed = 3
        
                
        #verif collisions
        for sprite in self.group.sprites():
            if sprite.pied.collidelist(self.walls) > -1:
                sprite.moveBack()

        

        self.spawnAutoTaupes()

    def affichageScore(self):
        scoreText = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(scoreText, (544, 32))

    def fever(self):
        # Mise à jour de la "fever"
        if self.tempsActuel >30 and self.feverPourcentage != 100:
            self.activationFever = False
            self.feverActiverUneFois = False
        elif self.tempsActuel < 30 and self.feverPourcentage >=100:
            print("OK")
            self.activationFever = True
            self.feverActiverUneFois = True
            self.player.speed = 3
        elif self.tempsActuel < 15:
            self.activationFever = False
            self.feverActiverUneFois = False
            self.player.speed = 3
        if self.feverPourcentage < 100:
            self.feverPourcentage += 0.07


    def affichageFever(self):
        fever = self.font.render(f"Fever : {int(self.feverPourcentage)} %", False, (255, 255, 255))
        self.screen.blit(fever, (272, 32))
                                 
    def bombe(self):
        if self.nbBombe > 0:

            for taupe in self.group.sprites():
                if type(taupe) != Player:
                    self.score +=taupe.points
                    self.group.remove(taupe)
            self.nbBombe -=1


    
    def afficherBombe(self):
        self.bombeSprite = pygame.image.load("././asset/bombe.png")
        bombeText = self.font.render(f"Bombe : {self.nbBombe} ", False, (255, 255, 255))
        self.screen.blit(self.bombeSprite, (224,704))
        self.screen.blit(bombeText, (225, 672))

    def bottes(self):
        if self.nbBottes > 0:
            self.timeBottes = time.time()
            self.player.speed = self.player.speed * 1.2
            self.nbBottes -=1


    def afficherBottes(self):
        self.bottesSprite = pygame.image.load("././asset/bottes.png")
        bottesText = self.font.render(f"Bottes : {self.nbBottes} ", False, (255, 255, 255))
        self.screen.blit(self.bottesSprite, (352, 704))
        self.screen.blit(bottesText, (352, 672))

    def chrono(self):
        if self.nbChrono > 0:
            self.tempsActuel += 10
            self.nbChrono -=1



    def afficherChronoItem(self):
        
        self.spriteChrono = pygame.image.load("././asset/chrono.png")
        chronoItemtxt = self.font.render(f"Chrono : {self.nbChrono} ", False, (255, 255, 255))
        self.screen.blit(self.spriteChrono, (480, 704))
        self.screen.blit(chronoItemtxt, (480, 672))

    def updateChrono(self, tempsEcoule):

        # Décrémente le temps écoulé
        # Vérifie si le temps n'est pas écoulé
        if not self.finTemps:   
            self.tempsActuel -= tempsEcoule 
            if self.tempsActuel <= 0:
                self.finTemps = True
                self.tempsActuel = 0

    def affichageChrono(self):
        minutes = int(self.tempsActuel) // 60
        secondes = int(self.tempsActuel) % 60

        # Affiche le temps restant à l'écran en format mm:ss
        chronoText = self.font.render(f"Time: {max(0, minutes):02d}:{max(0, secondes):02d}", True, (255, 255, 255))
        #Utilise les coordonnées de l'objet "TexteChrono" ici
        self.screen.blit(chronoText, (48, 32))


    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            tempsEcoule = self.clock.tick(60)/1000.0

            self.player.saveLocation()

            if not self.finTemps:
                self.handle_input()



            # Met à jour le chronomètre
            self.updateChrono(tempsEcoule)

            self.fever()

            # Dessine les calques
            self.group.draw(self.screen)

            # Affiche le chronomètre
            self.affichageChrono()
            
            #Affiche le score
            self.affichageScore()

            self.affichageFever()

            self.afficherBombe()
            self.afficherBottes()
            self.afficherChronoItem()

            # Mise à jour des sprites
            self.update()

            # Rafraîchit l'écran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

    pygame.quit()