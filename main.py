import pygame
import random
import math
import time

from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# Screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders - by Lourães")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background.png")

# Music

mixer.music.load("thememusic.wav")
mixer.music.set_volume(0.09)
mixer.music.play(-1)
m_playing = "yes"
print(m_playing)

# Player

playerImg = pygame.image.load("player64.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: {}".format(str(score_value)), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game
run = True
while run:
    screen.fill((0, 0, 0))

    # Bg Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # Encerramento do processo

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.QUIT:
            run = False

        # Sensores de Movimento

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_d:
                playerX_change = 0.3
            if event.key == pygame.K_a:
                playerX_change = -0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

        # Game Settings Auto Bindings

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if m_playing == "yes":
                        mixer.music.set_volume(0)
                        m_playing = "no"
                        print(m_playing)
                        break
                    if m_playing == "no":
                        mixer.music.set_volume(0.09)
                        m_playing = "yes"
                        print(m_playing)
                        break
    # bounds player

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy

    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            col_sound = mixer.Sound("explosion.wav")
            col_sound.set_volume(0.12)
            col_sound.play()

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Start

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
