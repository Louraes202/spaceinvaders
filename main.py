#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import pygame
import random
import math
import logging


from pygame import mixer

pygame.init()
clock = pygame.time.Clock()


# Screen

screen = pygame.display.set_mode((800, 600))

# Title and Icon

pygame.display.set_caption("Space Invaders - by Lourães")
icon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(icon)

# Lag Solver

def loadimg(imgname):
    return pygame.image.load(imgname).convert_alpha()

# Background

background = loadimg("background.png")

# Music 

mixer.music.load("thememusic.wav")
mixer.music.set_volume(0.09)
mixer.music.play(-1)
m_playing = "yes"
print(m_playing)

# Player

playerImg = loadimg("player64.png")
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
    enemyImg.append(loadimg("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet

bulletImg = loadimg("bullet.png")
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

# Game Over Text

over_font = pygame.font.Font("freesansbold.ttf", 64)

overX = 0
overY = 0

def show_score(x, y):
    score = font.render("Score: {}".format(str(score_value)), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOver():
    go_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(go_text, (200, 250))

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

scr1 = True
while scr1:
    clock.tick(2000000)
    logging.basicConfig(filename="logfilename.log", level=logging.INFO)
    # Bg Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # Encerramento do processo

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                scr1 = False

        if event.type == pygame.QUIT:
            scr1 = False

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

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
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
