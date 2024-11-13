
import pygame, simpleGE, random

class TransparentCatcher(simpleGE.Sprite):
    
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("catcher.png")
        self.setSize(1,480)
        self.position = (0,240)

class Pitcher(simpleGE.Sprite):
    
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("pitcher.png")
        self.setSize(50,70)
        self.position = (520,240)

class Ball(simpleGE.Sprite):
    
    def __init__(self, scene):
        super().__init__(scene)   
        self.setImage("ball.png")
        self.setSize(25, 25)
        self.minSpeed = -10
        self.maxSpeed = -1
        self.screenWidth = 520  
        self.screenHeight = 480
        self.reset()

            
    def reset(self):
        self.x = self.screenWidth
        self.y = random.randint(0,self.screenHeight)
        self.dx = random.randint(self.minSpeed,self.maxSpeed)
            

class Batter(simpleGE.Sprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        self.originalImage = "batter.png"
        self.setImage(self.originalImage)
        self.setSize(50, 70)
        self.position = (120, 240)
        self.contactImage = "homerun.png"
        self.contactDuration = 500
        self.contactTimer = 0

    def process(self):
        keysDown = pygame.key.get_pressed()
        if keysDown[pygame.K_UP]:
            self.y -= 7
        if keysDown[pygame.K_DOWN]:
            self.y += 7
        if self.contactTimer > 0:
            self.contactTimer -= 1000 / 30
            if self.contactTimer <= 0:
                self.setImage(self.originalImage)
                
    def hit(self):
        self.setImage(self.contactImage)  
        self.setSize(50, 70)  
        self.contactTimer = self.contactDuration
    
    

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("field.jpg")
        self.batter = Batter(self)
        self.pitcher = Pitcher(self)
        self.transparentCatcher = TransparentCatcher(self)
        self.numBall = 5
        self.ball = []
        for i in range(self.numBall):
            self.ball.append(Ball(self))
            
        self.sprites = [self.batter
                        , self.ball
                        , self.pitcher
                        , self.transparentCatcher]
        
        self.hits = 0
        self.strikes = 0
        self.outs = 0
        self.innings = 0
        

        
    def process(self):
        for ball in self.ball:
            if self.batter.collidesWith(ball):
                self.hits += 1
                ball.reset()
                self.batter.hit()
                
        for ball in self.ball:
            if self.transparentCatcher.collidesWith(ball):
                self.strikes += 1
                if self.strikes == 3:
                    self.outs += 1
                    self.strikes = 0
                    if self.outs == 3:
                        self.innings += 1
                        self.outs =0

def main():
    game = Game()
    keepGoing = True
    while keepGoing:
        game.start()
        game.process()
        
        if game.hits >= 30:
            if game.innings < 10:
                print ("Batter Won!!!")
                keepGoing = False
            
        elif game.innings >= 10:
            if game.hits < 30:
                print("Pitcher Won!!!")
                keepGoing = False
                
        elif game.hits >= 30:
            if game.innings >= 10:
                print ("Its a tie...")
                keepGoing = False

if __name__ == "__main__":
    main()