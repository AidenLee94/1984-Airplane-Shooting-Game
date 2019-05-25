# @Author: Aiden
# @Project: 15-112 Term Project
# @Date: 2017-12-7


import pygame
from pygame.locals import *
import math
import random
import pickle
import os

pygame.init()
pygame.font.init()


# This is how to initialize the result text file 
# To keep track of the highest score
storedScore = {0: "name", "name": 0}
pickle_out = open("result", "wb")
pickle.dump(storedScore, pickle_out)
pickle_out.close()


# Make a game screen
display_width, display_height = (700, 600)
screen = pygame.display.set_mode((display_width, display_height))

# Window title
pygame.display.set_caption("The Aeroplane Game")


# set up a RGB for colors 
black = (0,0,0)
white = (255,255,255)
green = (0, 200, 0)
lGreen = (0, 255, 0)
red = (200, 0,0)
lRed = (255, 0, 0) 
dGrey = (32,32,32)
dGreen = (0,102,102) 
blue = (0,0,150)
dBlue = (0,0,51)
lBlue = (0, 0, 200)
yellow = (200,200,0)
lYellow = (255, 255, 0)
GreenBlue = (153, 153, 255)
lightPink = (255, 204, 204)



# Make a game clock 
clock = pygame.time.Clock()
timer_enemy = 0
timer_item = 0

# Upload images
airplaneImg = pygame.image.load('images/first.png').convert_alpha()
second_AirplaneImg = pygame.image.load('images/second.png').convert_alpha()
enemyImg0 = pygame.image.load('images/enemy0.png').convert_alpha()
background = pygame.image.load('images/back.png').convert_alpha()
player1_missile1 = pygame.image.load('images/player1_missile1.png').convert_alpha()
player1_missile2 = pygame.image.load('images/player1_missile2.png').convert_alpha()
player1_missile3 = pygame.image.load('images/player1_missile3.png').convert_alpha()
player1_missile4 = pygame.image.load('images/player1_missile4.png').convert_alpha()
player2_missile1 = pygame.image.load('images/player2_missile1.png').convert_alpha()
player2_missile2 = pygame.image.load('images/player2_missile2.png').convert_alpha()
player2_missile3 = pygame.image.load('images/player1_missile3.png').convert_alpha()
player2_missile4 = pygame.image.load('images/player2_missile4.png').convert_alpha()
lifeImg = pygame.image.load("images/first.png").convert_alpha()
lifeImg = pygame.transform.scale(lifeImg, (40, 40))
lifeImg2 = pygame.image.load("images/second.png").convert_alpha()
lifeImg2 = pygame.transform.scale(lifeImg2, (40, 40))

global scores 
scores = 0



# This is the button function for Users on the startScreen
def buttonFunc(text, textColor, x, y, width, height, originColor, changedColor, size):
    curPos = pygame.mouse.get_pos()
    clickPos = pygame.mouse.get_pressed()
    if x < curPos[0] and curPos[0] < x + width:
        if y < curPos[1] and curPos[1] < y + height:
            pygame.draw.rect(screen, changedColor, (x,y,width,height))
            if clickPos[0] == 1:
                return True
    else:
         pygame.draw.rect(screen, originColor, (x,y,width,height))
    textButton(text, textColor, x,y, width, height,size)
    return None

# This is the helper function for making the button for the users
def textButton(text, color, buttonX, buttonY, buttonWidth, buttonHeight, size):
    font = pygame.font.SysFont('comicsansms', size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = ((buttonX + buttonWidth/2), buttonY + buttonHeight/2)
    screen.blit(textSurface, textRect)


# This function is to display the highest score with the player name 
# on the gameOver screen
def showHighestScore(diction):
    result = ""
    for key in diction:
        if isinstance(key, str):
            result += key 
            result += " got " 
            result += str(diction[key])
            return result

# This function set up the game effect sounds 
def soundEffect(sound):
    shooting_sound = pygame.mixer.Sound(os.path.join('assets', 'pew.wav'))
    missile_sound = pygame.mixer.Sound(os.path.join('assets', 'rocket.ogg'))
    if sound == "missile":
        pygame.mixer.Sound.play(shooting_sound)
    else:
        pygame.mixer.Sound.play(missile_sound)

    


# This is the function that writes a text in the screen 
def textDisplay(screen, text, size, color, positionX, positionY):
    font = pygame.font.SysFont('comicsansms', size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = positionX, positionY
    screen.blit(textSurface, textRect)



# This is the function that displays players' remaining lives by using
# images
def newLifeDisplay(screen, player1_lives, player2_lives = None):
    startX = 20
    startY = 20
    margin = 20
    if player2_lives == None:
        for i in range(1, player1_lives+1):
            positionDisplay(screen, startX*i + margin * i,startY, lifeImg)        
    else:
        for i in range(1, player1_lives+1):
            positionDisplay(screen, startX*i + margin * i,startY, lifeImg)  

        for j in range(1, player2_lives+1):
            positionDisplay(screen, startX*j + margin * j,startY + 40, lifeImg2)        


# This is the function that displays player's score
def scoreDisplay(screen, score):
    size = 40 
    myfont = pygame.font.Font(None, size)
    text = myfont.render("Scores: " +str(score), True, white)    
    text_rect = text.get_rect(center=(display_width/2, display_height/14))
    screen.blit(text, text_rect)



# This function displays the images with the x,y coordinates
def positionDisplay(screen, x,y, img):
    screen.blit(img,(x,y))


 

# This is the player class that works for the player's airplane 
class Player(pygame.sprite.Sprite):
    def __init__(self, lives = 3, second = True):
        pygame.sprite.Sprite.__init__(self)
        self.image = airplaneImg
        self.image = pygame.transform.scale(self.image, (80, 120))  
        self.rect = self.image.get_rect()
        self.second = second
        if second == True:
            self.rect.centerx = display_width * 1/4    
        else:
            self.rect.centerx = display_width / 2
        self.rect.centery = display_height - 30
        self.lives = lives 
        # weapon level starts at 1
        self.level = 1
        self.dx = 0
        self.dy = 0
        self.shootTimer = 0
        self.shootTimerMax = 3


    # This function is the helper function that updates player's movement
    def update(self):
        # To limit the player's Bound
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom > display_height:
            self.rect.bottom = display_height

        button = pygame.key.get_pressed()
        # To move the airplane
        if button[pygame.K_LEFT]:
            self.dx = -8
        elif button[pygame.K_RIGHT]:
            self.dx = 8
        if button[pygame.K_UP]:
            self.dy = -8
        elif button[pygame.K_DOWN]:
            self.dy = 8
        
        # To shoot a missile
        if button[pygame.K_SPACE]:
            # This function is to prevent the missiles to get trailled 
            self.shootTimer += 1
            if self.shootTimer == self.shootTimerMax:
                self.shoot()
                self.shootTimer = 0
            
        self.rect.x += self.dx
        self.rect.y += self.dy

    # If the airplane dies, then it starts from the bottom if it has a live
    def reset(self):
        self.rect = self.image.get_rect()
        if self.second == True:
            self.rect.centerx = display_width * 1/4    
        else:
            self.rect.centerx = display_width / 2
        self.rect.centery = display_height - 30

    # This is the helper function for the airplane that shoots a missile
    def shoot(self):
        # Player can upgrade its weapon
        if self.level == 1:
            missile = Missile(self.rect.centerx, self.rect.top, 1, "single")
            missiles.add(missile)
            soundEffect('missile')

        elif self.level == 2:
            missile1 = Missile(self.rect.left, self.rect.top, 2, "single")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "single")
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect('missile')


        elif self.level == 3:
            missile0 = Missile(self.rect.centerx, self.rect.top,3, "single")
            missile1 = Missile(self.rect.left, self.rect.top, 2, "single")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "single")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("rocket")


        elif self.level == 4:
            missile0 = Missile(self.rect.centerx, self.rect.top,3, "single")
            missile1 = Missile(self.rect.left, self.rect.top, 2, "single", "left_up")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "single", "right_up")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("rocket")


            
        elif self.level == 5:
            missile0 = Missile(self.rect.centerx, self.rect.top,3, "single", None,  "size_up")
            missile1 = Missile(self.rect.left, self.rect.top, 2, "single", "left_up", "size_up")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "single", "right_up", "size_up")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("rocket")


        elif self.level == 6:
            missile0 = Missile(self.rect.centerx, self.rect.top,3, "single", None,  "size_up")
            missile1 = Missile(self.rect.left, self.rect.top, 2, "single", "left_up", "size_up")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "single", "right_up", "size_up")
            missile3 = Missile(self.rect.midleft, self.rect.midtop, 2, "single", "left", "size_up") 
            missile4 = Missile(self.rect.midright, self.rect.midtop, 2, "single", "right", "size_up")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            missiles.add(missile3)
            missiles.add(missile4)
            soundEffect("missile")
            soundEffect("rocket")
            

    # if player gets an item, then it upgrades the weapon
    def upgrade(self):
        self.level += 1


# This is the class for the second player
class Second_Player(pygame.sprite.Sprite):
    def __init__(self, lives = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image = second_AirplaneImg
        self.image = pygame.transform.scale(self.image, (80, 120))  
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.centerx = display_width * 3/4 
        self.rect.centery = display_height - 30
        self.lives = lives 
        # weapon level starts at 1
        self.level = 1
        self.dx = 0
        self.dy = 0
        self.shootTimer = 0
        self.shootTimerMax = 3



    # This function is the helper function that updates second_player's movement
    def update(self):
        # To limit the player's Bound
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom > display_height:
            self.rect.bottom = display_height

   
        button = pygame.key.get_pressed()
        # To move the airplane
        if button[pygame.K_a]:
            self.dx = -8
        elif button[pygame.K_d]:
            self.dx = 8
        if button[pygame.K_w]:
            self.dy = -8
        elif button[pygame.K_s]:
            self.dy = 8
        # To shoot a missile
        if button[pygame.K_TAB]:
            # This function is to prevent the missiles to get trailled 
            self.shootTimer += 1
            if self.shootTimer == self.shootTimerMax:
                self.shoot()
                self.shootTimer = 0

        self.rect.x += self.dx
        self.rect.y += self.dy


    # If the airplane dies, then it starts from the bottom if it has a live
    def reset(self):
        self.rect = self.image.get_rect()
        self.rect.centerx = display_width * 3/4 
        self.rect.centery = display_height - 30


    # This is the helper function for the airplane that shoots a missile
    def shoot(self):
        # Player can upgrade its weapon
        if self.level == 1:
            missile = Missile(self.rect.centerx, self.rect.top, 1, "double")
            missiles.add(missile)
            soundEffect("missile")
            
        elif self.level == 2:
            missile1 = Missile(self.rect.left, self.rect.top, 2, "double")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "double")
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("missile")



        elif self.level == 3:
            missile0 = Missile(self.rect.centerx, self.rect.top,3, "double")
            missile1 = Missile(self.rect.left, self.rect.top, 2, "double")
            missile2 = Missile(self.rect.right, self.rect.top, 2, "double")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("rocket")
        
        elif self.level == 4:
            missile0 = Missile(self.rect.centerx, self.rect.top,3,  "double")
            missile1 = Missile(self.rect.left, self.rect.top, 2,  "double", "left_up")
            missile2 = Missile(self.rect.right, self.rect.top, 2,  "double", "right_up")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("rocket")
        

            
        elif self.level == 5:
            missile0 = Missile(self.rect.centerx, self.rect.top,3,  "double", None,  "size_up")
            missile1 = Missile(self.rect.left, self.rect.top, 2, "double", "left_up", "size_up")
            missile2 = Missile(self.rect.right, self.rect.top, 2,  "double", "right_up", "size_up")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            soundEffect("missile")
            soundEffect("rocket")
        


        elif self.level == 6:
            missile0 = Missile(self.rect.centerx, self.rect.top,3,  "double", None,  "size_up")
            missile1 = Missile(self.rect.left, self.rect.top, 2,  "double", "left_up", "size_up")
            missile2 = Missile(self.rect.right, self.rect.top, 2,  "double", "right_up", "size_up")
            missile3 = Missile(self.rect.midleft, self.rect.midtop, 2,  "double", "left", "size_up") 
            missile4 = Missile(self.rect.midright, self.rect.midtop, 2,  "double", "right", "size_up")
            missiles.add(missile0)
            missiles.add(missile1)
            missiles.add(missile2)
            missiles.add(missile3)
            missiles.add(missile4)
            soundEffect("missile")
            soundEffect("rocket")
        
            
            
    # if player gets an item, then it upgrades the weapon
    def upgrade(self):
        self.level += 1



# This is the Enemy class that controls the attributes of the enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameLevel, player_x = 0, player_y = 0):
        pygame.sprite.Sprite.__init__(self)
        if gameLevel == "hard":
            number = random.choice([0,1,2,3,3,3,3])            
        else:
            number = random.randint(0,3)
        self.number = number
        self.player_x = player_x
        self.player_y = player_y
        # There are four types enemies and one final boss
        if number == 0:
            self.image = pygame.image.load("images/enemy0.png")
        elif number == 1:
            self.image = pygame.image.load("images/enemy1.png")
        elif number == 2:
            self.image = pygame.image.load("images/enemy2.png")
        elif number == 3:
            self.image = pygame.image.load("images/enemy3.png")
        if number != 3:   
            self.image = pygame.transform.scale(self.image, (100,80))
        else:
            self.image = pygame.transform.scale(self.image, (140,120))

        image_width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, display_width - image_width)
        self.rect.y = random.randrange(-20, 0)
        self.position = random.choice([-1,1])
        self.speedX = random.randint(-7,7)
        self.speedY = random.randint(0,7)
        self.gameLevel = gameLevel
        if self.gameLevel == "hard":
            self.speedX = random.randint(-10,10)
            self.speedY = random.randint(0,10)
            


    # This function updates the enemy's movement
    def update(self, player):
        self.rect.centery += self.speedY
        if self.rect.top >= display_height:
            self.kill()

        # To limit the enemy's Bound
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_width:
            self.rect.right = display_width

        if self.number != 3:     
            if self.position > 0:
                if self.speedX >= 0:
                    self.rect.centerx += self.speedX
                else:
                    self.rect.centerx -= self.speedX
            else:
                if self.speedX >= 0:
                    self.rect.centerx -= self.speedX    
                else:
                    self.rect.centerx += self.speedX                    
        
            if self.rect.right >= display_width or self.rect.left <= 0:
                self.position = self.position * (-1)


        else:
            speedX = random.randint(2,6)
            if self.gameLevel == "hard":
                speedX = random.randint(4,8)

            # Adding a certain behavior of an enemy
            # If an enemy is type3, it approaches to the airplane
            if self.rect.left <= 0:
                self.rect.x += speedX

            elif self.rect.right >= display_width:
                self.rect.x -= speedX

            else:
                if not(self.rect.left <= player.rect.left and player.rect.right <= self.rect.right):
                    if not(self.rect.x > player.rect.x or self.rect.x < player.rect.x):
                        self.rect.x += speedX 
                    else:
                        if self.rect.x > player.rect.x:
                            self.rect.x -= speedX
                        elif self.rect.x < player.rect.x:
                            self.rect.x += speedX
                
        # To increase the difficuty of the game 
        temp = random.randint(0, 100)
        if self.gameLevel == "hard":
            if temp == 0 or temp == 100 or temp == 50:
                self.enemyMissile = self.shoot()
                return self.enemyMissile    

        # This part is to randomize the enemy's shooting
        else:
            if temp == 0:
                self.enemyMissile = self.shoot()
                return self.enemyMissile

    # This helper function helps enemy to shoot a missile 
    def shoot(self):
        enemyMissile = EnemyMissile(self.rect.centerx, self.rect.bottom)
        enemyMissiles.add(enemyMissile)
    

# This is the class for the finalboss
class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, gameLevel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/boss.png")
        self.image = pygame.transform.scale(self.image, (300,180))
        self.rect = self.image.get_rect()
        self.rect.center = (display_width/2, 50)
        self.position = random.choice([-1,1])
        self.speedX = random.randint(5,10)
        self.speedY = random.randint(0,5)
        self.damage = 0
        self.widthSize = self.image.get_width()
        self.heightSize = self.image.get_height()


    # This function updates the boss's movement
    def update(self, player):   
        # To limit the boss's Bound
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.top <= 0:
            self.rect.top = 0
        

        # At first, the boss will move left and right
        if self.damage < 20:
            if self.rect.right >= display_width or self.rect.left <= 0:
                self.position = self.position * (-1)
            
            if self.position > 0:
                if self.speedX >= 0:
                    self.rect.centerx += self.speedX
                else:
                    self.rect.centerx -= self.speedX
            else:
                if self.speedX >= 0:
                    self.rect.centerx -= self.speedX    
                else:
                    self.rect.centerx += self.speedX                    
        elif self.damage < 1000:
            margin = 8
            if not(self.rect.centerx <= player.rect.left and player.rect.centerx <= self.rect.right):
                if self.rect.centerx > player.rect.centerx:
                    if abs(self.rect.centerx - player.rect.centerx) >= margin:
                        self.rect.centerx -= self.speedX
                elif self.rect.centerx < player.rect.centerx:
                    if abs(self.rect.centerx - player.rect.centerx) >= margin:
                        self.rect.centerx += self.speedX
        
                
        # At the end, it will oscillate until it dies
        else:
            if not(self.rect.centerx <= player.rect.left and player.rect.centerx <= self.rect.right):
                #if not(self.rect.x > player.rect.x or self.rect.x < player.rect.x):
                #    self.rect.x += self.speedX 
                #else:
                if self.rect.centerx > player.rect.centerx:
                    self.rect.centerx -= self.speedX
                elif self.rect.centerx < player.rect.centerx:
                    self.rect.centerx += self.speedX
        
    
        temp = random.randint(0, 25)
        # This part is to randomize the boss's shooting
        if temp == 0:
            self.bossMissile = self.shoot()
            return self.bossMissile



    # This helper function helps the final boss to shoot a missile 
    def shoot(self):
        bossMissile = BossMissile(self.rect.centerx, self.rect.bottom)
        bossMissiles.add(bossMissile)
        


class BossMissile(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy_missile.png")
        self.image = pygame.transform.scale(self.image, (25,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    # This function updates the Boss's missile 
    # Boss's missile will chase the player
    def update(self, player, finalBoss):
        if self.rect.top >= display_height:
            self.kill()
        else:
            speedY = random.choice([5,6,7])
            self.rect.move_ip(0, speedY)  
            if finalBoss.damage <= 20:
                speedX = 0

            if 20 < finalBoss.damage and finalBoss.damage < 100:
                speedX = 5
            elif 100 <= finalBoss.damage:
                speedX = 7
            
            if not(self.rect.left <= player.rect.left and player.rect.right <= self.rect.right):
                if not(self.rect.x > player.rect.x or self.rect.x < player.rect.x):
                    self.rect.x += speedX 
                else:
                    if self.rect.x > player.rect.x:
                        self.rect.x -= speedX
                    elif self.rect.x < player.rect.x:
                        self.rect.x += speedX



# This is the Player's missile class
class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y, level, status, direction = None, size = None):
        pygame.sprite.Sprite.__init__(self)
        self.level = level
        if status == "single":

            if level == 1:
                self.image = player1_missile1
            elif level == 2:
                self.image = player1_missile2
            elif level == 3:
                self.image = player1_missile3

        
        elif status == "double":
            if level == 1:
                self.image = player2_missile1
            elif level == 2:
                self.image = player2_missile2
            elif level == 3:
                self.image = player2_missile3
        
        self.direction = direction
        self.sizeUpgrade = size 
        if size != "size_up":
            self.image = pygame.transform.scale(self.image, (20,50))
        else:
            self.image = pygame.transform.scale(self.image, (30,75))

        if direction == "left":
            if status == "single":
                self.image = player1_missile4
                self.image = pygame.transform.scale(self.image, (75,30))

            else:
                self.image = player2_missile4
                self.image = pygame.transform.scale(self.image, (75,30))

        elif direction == "right":
            if status == "single":
                self.image = player1_missile4
                self.image = pygame.transform.scale(self.image, (75,30))
            else:
                self.image = player2_missile4
                self.image = pygame.transform.scale(self.image, (75,30))
        
        self.rect = self.image.get_rect()
        if direction == "left":    
            self.rect.right = x[0]
            self.rect.centery = x[1]

        elif direction == "right": 
            self.rect.left = x[0]
            self.rect.centery = x[1]
            
        else:
            self.rect.centerx = x
            self.rect.bottom = y

    # This function updates the missile of the player 
    def update(self):
        #print(self.level, self.direction, self.sizeUpgrade)
        # This part is to get rid of missile if it is off the board 
        if self.rect.top <= 0:
            self.kill()
        else:    
            if self.direction == None:
                self.rect.move_ip(0, -12)

            elif self.direction == "right_up":
                self.rect.move_ip(6, -12)

            elif self.direction == "left_up":
                self.rect.move_ip(-6, -12)

            elif self.direction == "left":
                self.rect.move_ip(-12, 0)

            elif self.direction == "right":
                self.rect.move_ip(12, 0)




        
# This is the Enemy's missile class 
class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy_missile.png")
        self.image = pygame.transform.scale(self.image, (25,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    # This function updates the Enemy's missile 
    def update(self):
        if self.rect.top >= display_height:
            self.kill()
        else:    
            speedY = random.choice([5,6,7])
            self.rect.move_ip(0, speedY)  


# This the item class 
class Item(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        temp = random.randint(0,1)
        if temp == 0:
            self.type = 'weapon'
            self.image = pygame.image.load("images/weapon_upgrade.png")
            self.image = pygame.transform.scale(self.image, (18, 30))
        else:
            self.type = 'health'
            self.image = pygame.image.load("images/health_upgrade.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, display_width - self.rect.width)
        self.speedY = 5


    def update(self):
        if self.rect.top >= display_height:
            self.kill()

        else:    
            self.rect.move_ip(0, self.speedY)  




# This is the helper function for the helper screen
def helpScreen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "startMenu"

                elif event.key == pygame.K_p:
                    return "gamePlay"
            else:
                startImg = pygame.image.load("images/black.jpg")
                startImg = pygame.transform.scale(startImg, (display_width, display_height))
                positionDisplay(screen, 0,0, startImg)
                textDisplay(screen, "Press [ENTER] to go back to startMenu", 35, white, display_width/2, display_height/2 - 240)
                textDisplay(screen, "Press [p] to play!", 35, white, display_width/2, display_height/2 - 190)
                textDisplay(screen, "How To Play!", 45, white, display_width/2, display_height/2 - 100)
                textDisplay(screen, "For Player 1:", 35, GreenBlue, display_width/2, display_height/2 - 40)
                textDisplay(screen, "Use up, down, left, and right key to move", 35, GreenBlue, display_width/2, display_height/2 - 10)
                textDisplay(screen, "Press [Spacebar] to shoot a missile", 35, GreenBlue, display_width/2, display_height/2 + 20)
                textDisplay(screen, "For Player 2:", 35, lightPink, display_width/2, display_height/2 + 70)
                textDisplay(screen, "Use w, s, a, and d key to move", 35, lightPink, display_width/2, display_height/2 + 100)
                textDisplay(screen, "Press [Tab] to shoot a missile", 35, lightPink, display_width/2, display_height/2 + 130)
                textDisplay(screen, "Try to win the final boss!", 40, white, display_width/2, display_height/2 + 200)
                pygame.display.update()

# This is the function for the start screen
# This works as the main loop  
def gameStart():
    # To play a background music
    pygame.mixer.music.load("assets/music.mp3")
    pygame.mixer.music.play(-1)
    
    startImg = pygame.image.load("images/startScreen.png")
    startImg = pygame.transform.scale(startImg, (display_width, display_height))
    positionDisplay(screen, 0,0, startImg)

    startMenu = True
    while startMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            else:
                temp1 = buttonFunc("Play", white,  display_width/6, display_height - 60 , 120, 40, blue, lBlue, 40)
                temp2 = buttonFunc("Help", white,  display_width/2 - 60, display_height - 60 , 120, 40, red, lRed, 40)                
                temp3 = buttonFunc("Quit", white,  display_width* 5/6 - 120 , display_height - 60 , 120, 40, green, lGreen, 40)
                # If play button is clicked
                if temp1 != None:
                    mode = gameLevel()
                    # If startMenu is clicked 
                    if mode == "startMenu":
                        positionDisplay(screen, 0,0, startImg)
                        pygame.display.update()
                        break

                    
                    numPlayer = checkPlayer()
                    if numPlayer == "startMenu":
                        positionDisplay(screen, 0,0, startImg)
                        pygame.display.update()
                        break

                    currentScore = game(mode, numPlayer)
                    gameOverStage(currentScore)


                elif temp2 != None:
                    stage = helpScreen()
                    if stage == "startMenu":
                        positionDisplay(screen, 0,0, startImg)
                        pygame.display.update()
                        break
                    elif stage == "gamePlay":
                        mode = gameLevel()
                        if mode == "startMenu":
                            positionDisplay(screen, 0,0, startImg)
                            pygame.display.update()
                            break
                        numPlayer = checkPlayer()
                        if numPlayer == "startMenu":
                            positionDisplay(screen, 0,0, startImg)
                            pygame.display.update()
                            break

                        currentScore = game(mode, numPlayer)
                        gameOverStage(currentScore)


                elif temp3 != None:
                    pygame.quit()
                    quit()

                pygame.display.update()
                

# This function is to create a screen that allows users to choose 
# the game level 
def gameLevel():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_RETURN:
                    return "startMenu"
                elif event.key == pygame.K_e:
                    return "easy"
                elif event.key == pygame.K_h:
                    return "hard"
            else:
                startImg = pygame.image.load("images/spaceImg.png")
                startImg = pygame.transform.scale(startImg, (display_width, display_height))
                positionDisplay(screen, 0,0, startImg)
                textDisplay(screen, "Press [e] for Easy Level", 55, dBlue, display_width * 1/2, display_height/2 - 70)
                textDisplay(screen, "[h] for Hard Level", 55, lightPink, display_width * 1/2, display_height/2 + 10)
                textDisplay(screen, "[ENTER] for MainMenu", 45, white, display_width * 1/2, display_height/2 + 120)
                pygame.display.update()
 


# This function is to create a screen and allows users to choose
# how many players would play the game
def checkPlayer():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_RETURN:
                    return "startMenu"
                elif event.key == pygame.K_1:
                    # Single player is being chosen!
                    return None
                elif event.key == pygame.K_2:
                    # Second player is being chosen!
                    return True
            else:
                startImg = pygame.image.load("images/spaceImg.png")
                startImg = pygame.transform.scale(startImg, (display_width, display_height))
                positionDisplay(screen, 0,0, startImg)
                textDisplay(screen, "Press [1] for 1 Player", 55, dBlue, display_width * 1/2, display_height/2 - 70)
                textDisplay(screen, "[2] for 2 Players", 55, lightPink, display_width * 1/2, display_height/2 + 10)
                textDisplay(screen, "[ENTER] for MainMenu", 45, white, display_width * 1/2, display_height/2 + 120)
                pygame.display.update()


 
#lightPink
#GreenBlue


# This is the main game loop 
# the parameter "second" is to check whether the player clicks single player 
# mode or 2 players mode
def game(mode, second = None):
    # Stop the start music 
    pygame.mixer.music.stop()
    # Play the game music
    pygame.mixer.music.load("assets/game.mp3")
    pygame.mixer.music.play(-1)
    

    y = 0
    
    ######################################################
    
    global timer_enemy
    global timer_item
    global airplaneSprite
    global missiles
    global enemies
    global enemyMissiles
    global bossMissiles
    global items
    global bombs
    global scores 
    

    scores = 0
    finalBoss = None
    gameOver = False

    # It will make sprite groups for each of the class
    # so that it can be easier to update and draw
    airplaneSprite = pygame.sprite.Group()
    player = Player(3, second)
    airplaneSprite.add(player)

    enemies = pygame.sprite.Group()
    missiles = pygame.sprite.Group()
    enemyMissiles = pygame.sprite.Group()
    items = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    boss_sprite = pygame.sprite.Group()
    bossMissiles = pygame.sprite.Group()

    if second == True:
        global second_airplaneSprite
        global second_missiles
        second_airplaneSprite = pygame.sprite.Group()
        player2 = Second_Player()
        second_airplaneSprite.add(player2)
        second_missiles = pygame.sprite.Group()

    
    

    # Main loop 
    while not gameOver:
        clock.tick(60)
        # This is to move the background 
        startImg = pygame.image.load("images/back.png")
        startImg = pygame.transform.scale(startImg, (display_width, display_height))
        height_size = startImg.get_rect().height
        relative_y = y % height_size
        positionDisplay(screen, 0,relative_y -height_size, startImg)
        if relative_y < display_height:
            positionDisplay(screen, 0,relative_y, startImg)
        y += 2
    


        
        # For all events that the player makes
        for event in pygame.event.get():
            # If user clicks 'x' of the screen, then it quits the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if second == True:                    
                    if event.key == pygame.K_p:
                        pause()

                    elif event.key == pygame.K_LEFT:
                        player.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        player.dx = 5
                    elif event.key == pygame.K_UP:
                        player.dy = -5
                    elif event.key == pygame.K_DOWN:
                        player.dy = 5

                    if event.key == pygame.K_a:
                        player2.dx = -5
                    elif event.key == pygame.K_d:
                        player2.dx = 5
                    elif event.key == pygame.K_w:
                        player2.dy = -5
                    elif event.key == pygame.K_s:
                        player2.dy = 5 


                else:
                    if event.key == pygame.K_p:
                        pause()
                    elif event.key == pygame.K_LEFT:
                        player.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        player.dx = 5
                    elif event.key == pygame.K_UP:
                        player.dy = -5
                    elif event.key == pygame.K_DOWN:
                        player.dy = 5

            if event.type == pygame.KEYUP:
                if second == True:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player.dy = 0       
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        player2.dx = 0
                    elif event.key == pygame.K_w or event.key == pygame.K_s:
                        player2.dy = 0
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player.dy = 0       

        if second == True:
            second_airplaneSprite.update()
            second_missiles.update()
            enemies.update(player2)

        airplaneSprite.update()
        enemies.update(player)
        missiles.update()
        enemyMissiles.update()
        items.update()
        boss_sprite.update(player)
        bossMissiles.update(player, finalBoss)

        if second == True:
            second_airplaneSprite.draw(screen)
            second_missiles.draw(screen)

        airplaneSprite.draw(screen)
        enemies.draw(screen)
        missiles.draw(screen)
        enemyMissiles.draw(screen)
        items.draw(screen)
        boss_sprite.draw(screen)
        bossMissiles.draw(screen)

        if second == True:
            newLifeDisplay(screen, player.lives, player2.lives)
        else:
            newLifeDisplay(screen, player.lives)            
                      
        scoreDisplay(screen, scores)
        pygame.display.update()

        # create new enemy
        timer_enemy += 1
        if mode == "easy": 
            if timer_enemy % 20 == 0:
                enemy = Enemy(mode, player.rect.x, player.rect.y)
                enemies.add(enemy)
        else:
            if timer_enemy % 10 == 0:
                enemy = Enemy(mode, player.rect.x, player.rect.y)
                enemies.add(enemy)

        timer_item += 1
        if timer_item % 100 == 0:
            item = Item()
            items.add(item)

        #If player kills 50 enemies, then the final boss will be created
        if mode == "easy":
            if scores == 200:
                if (len(boss_sprite) == 0): 
                    finalBoss = FinalBoss(mode)
                    boss_sprite.add(finalBoss)

        else:
            if scores == 400:
                if (len(boss_sprite) == 0): 
                    finalBoss = FinalBoss(mode)
                    boss_sprite.add(finalBoss)

        for intersect in pygame.sprite.groupcollide(items, airplaneSprite, 1, 0):
            
            # Player's total possible level is 6
            if intersect.type == 'weapon':
                if player.level <= 5:
                    player.level += 1
            
            # Player's total possible live is 3
            elif intersect.type == 'health':
                if player.lives <= 2:
                    player.lives += 1

            

        for intersect in pygame.sprite.groupcollide(missiles, enemies, 1, 1):            
            scores += 5

            
        for intersect in pygame.sprite.groupcollide(missiles, boss_sprite, 1, 0):
            scores += 7

            finalBoss.damage += 5
            if  finalBoss.damage == 20:
                finalBoss.speedX += 5 

            # This will end the game if you kill the final boss
            if finalBoss.damage == 2000:
                finalBoss.kill()
                gameOver = True 
                return scores


        for intersect in pygame.sprite.groupcollide(enemies, airplaneSprite, 1, 0):            
            if player.lives == 1:
                gameOver = True
                return scores

            else:
                pygame.time.wait(80)
                player.__init__(player.lives-1)

        #if finalBoss !- 
        for intersect in pygame.sprite.groupcollide(boss_sprite, airplaneSprite, 0, 0):            
            if player.lives == 1:
                gameOver = True
                return scores

            else:
                pygame.time.wait(80)
                player.__init__(player.lives-1)



        for intersect in pygame.sprite.groupcollide(enemyMissiles, airplaneSprite, 1, 0):            
            if player.lives == 1:
                gameOver = True
                return scores
                
            else:
                pygame.time.wait(80)
                player.__init__(player.lives-1)


        for intersect in pygame.sprite.groupcollide(bossMissiles, airplaneSprite, 1, 0):            
            if player.lives == 1:
                gameOver = True     
                return scores           
            else:
                pygame.time.wait(80)
                player.__init__(player.lives-1)

        if second == True:
            if timer_enemy % 52 == 0:
                enemy = Enemy(player2.rect.x, player2.rect.y)
                enemies.add(enemy)
        

            for intersect in pygame.sprite.groupcollide(items, second_airplaneSprite, 1, 0):
                # Second Player's total possible level is 6
                if intersect.type == 'weapon':
                    if player2.level <= 5:
                        player2.level += 1
                
                # Second Player's total possible live is 6                        
                elif intersect.type == 'health':
                    if player2.lives <= 2:
                        player2.lives += 1


            for intersect in pygame.sprite.groupcollide(missiles, enemies, 1, 1):            
                scores += 5            


            for intersect in pygame.sprite.groupcollide(missiles, boss_sprite, 1, 0):
                scores += 7
                finalBoss.damage += 5
                if  finalBoss.damage == 200 or finalBoss.damate == 1000:
                    finalBoss.speedX += 5 

                if finalBoss.damage == 2000:
                    self.kill()
                    gameOver = True 
                    return scores

            for intersect in pygame.sprite.groupcollide(enemies, second_airplaneSprite, 1, 0):            
                if player2.lives == 1:
                    gameOver = True
                    return scores

                else:
                    pygame.time.wait(80)
                    player2.__init__(player2.lives-1)


            for intersect in pygame.sprite.groupcollide(enemyMissiles, second_airplaneSprite, 1, 0):            
                if player2.lives == 1:
                    gameOver = True
                    return scores
                    
                else:
                    pygame.time.wait(80)
                    player2.__init__(player2.lives-1)


            for intersect in pygame.sprite.groupcollide(bossMissiles, second_airplaneSprite, 1, 0):            
                if player2.lives == 1:
                    gameOver = True     
                    return scores           
                else:
                    pygame.time.wait(80)
                    player2.__init__(player2.lives-1)

            for intersect in pygame.sprite.groupcollide(boss_sprite, second_airplaneSprite, 0, 0):            
                if player2.lives == 1:
                    gameOver = True
                    return scores

                else:
                    pygame.time.wait(80)
                    player2.__init__(player2.lives-1)

# This function creates pause screen 
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

            else:
                #pygame.mixer.music.stop()
                startImg = pygame.image.load("images/pause.png")
                startImg = pygame.transform.scale(startImg, (display_width, display_height))
                positionDisplay(screen, 0,0, startImg)
                textDisplay(screen, "Paused", 70, GreenBlue, display_width/2, display_height/2- 100)
                textDisplay(screen, "Press [p] To continue", 40, GreenBlue, display_width/2, display_height/2 + 120)
                pygame.display.update()
                clock.tick(0)

# The result(game score) will be stored in this way 
#>>> a = {0: "Aiden", "Aiden":87}
                
def gameOverStage(score):
    pickle_in = open("result", "rb")
    storedScore = pickle.load(pickle_in)
    name = storedScore[0]
    highestScore = storedScore[name]
    pickle_in.close()
    if highestScore < score:
        pygame.mixer.music.stop()
        startImg = pygame.image.load("images/name.jpg")
        startImg = pygame.transform.scale(startImg, (display_width, display_height))
        positionDisplay(screen, 0,0, startImg)
        textDisplay(screen, "Congrats! Enter your name:", 40, dBlue, display_width/2, display_height/14)
        pygame.display.update()
        pickle_out = open("result","wb")
        name = input("Enter your name: ")
        name_score = dict()
        name_score[0] = name
        name_score[name] = score
        pickle.dump(name_score, pickle_out)
        pickle_out.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameStart()

                elif event.key == pygame.K_p:
                    mode = gameLevel()
                    # If startMenu is clicked 
                    if mode == "startMenu":
                        positionDisplay(screen, 0,0, startImg)
                        pygame.display.update()
                        break
                    numPlayer = checkPlayer()
                    if numPlayer == "startMenu":
                        positionDisplay(screen, 0,0, startImg)
                        pygame.display.update()
                        break
                    currentScore = game(mode, numPlayer)
                    gameOverStage(currentScore)
        
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            else:
                pickle_in = open("result", "rb")
                highestScore = pickle.load(pickle_in)
                pickle_in.close()
                result = showHighestScore(highestScore)
                pygame.mixer.music.stop()
                startImg = pygame.image.load("images/pause.png")
                startImg = pygame.transform.scale(startImg, (display_width, display_height))
                positionDisplay(screen, 0,0, startImg)
                textDisplay(screen, "GAME OVER", 60, white, display_width/2, display_height/2 - 150)
                textDisplay(screen, "Best Score: " + str(result), 55, yellow, display_width/2, display_height/2 - 80)
                textDisplay(screen, "Press [ENTER] To Go Back To menu", 35, white, display_width/2, display_height/2 + 80)
                textDisplay(screen, "[p] To Play", 35, white, display_width/2, display_height/2 + 120)
                textDisplay(screen, "[q] To Exit", 35, white, display_width/2, display_height/2 + 160)
                pygame.display.update()
                

gameStart()
pygame.quit()
quit()