import pygame
import random
import math
from pygame import mixer

# initialise the module
pygame.init()

# method to create a screen with width of 800 and height of 600
screen = pygame.display.set_mode((800,600))

# Title and Icon
# To open file from right folder go type 'cd C:\Projects\pythontutorialvid'
pygame.display.set_caption("Space Invaders")  # set title of window 
icon = pygame.image.load("ufo.png")  # set icon of window 
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background.jpg")

# Background sound
mixer.music.load("background.wav")  # we use mixer.music because this is a long sound and repeats, its a song 
mixer.music.play(-1)  # -1 value makes it repeat forever

# player 
playerImg = pygame.image.load("player64.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0 

# enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
# Ready state means you cant see the bullet on the screen 
# Fire state means the bullet is currently moving 
bullet_state = "ready"

# Score
score_value = 0
# creating a font ("font name", font size)
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))  #Adding the values is to make sure the bullet appears in the centre of the spaceship

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    return False 

# Game loop, infinite until the window is closed 
running = True
while running:
    # Make sure the screen is drawn before anything else, if this was the opposite way around then the player would be underneath the screen 
    # Parameters here are RGB
    screen.fill((100, 100, 100))

    #background image 
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checks whether keystroke is left/right arrow
        if event.type == pygame.KEYDOWN:    # checks whether ANY key has been pressed 
            if event.key == pygame.K_LEFT:   # Checks whether the key pressed is the left arrow
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:  # Checks whether the key pressed is the right arrow
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # to make sure you can only fire another bullet when there isnt already another bullet on the screen 
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # Checks when the key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # Checks whether the key released is the right or left arrow 
                playerX_change = 0
    
    # makes sure the spaceship cant go off the screen
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    # checks the enemy boundries and changes the x co-ords to the opposite direction when it hits one 
    for i in range(num_of_enemies):   # need for loop so that you know which enemy you are talking about 

        # Game over 
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480  # first reset bullet 
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    playerX += playerX_change  # Adds the value of your keystroke to the X co-ord depending on which key you pressed
    
    # Bullet movement 
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_sound = mixer.Sound("laser.wav")
        bullet_sound.play()
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change  # we take away the Y value because the window starts at 0 at the top and increases down 

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

# tutorial followed: https://youtu.be/FfWpgLFMI7w

