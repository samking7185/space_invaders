# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 20:23:17 2020

@author: SKing
"""

# Space Invaders

# Set up screen

import pygame
import os
import time
import random
import math
import numpy as np
from game_class import *
from fuzzy import *

class FIS:
    def __init__(self, player, enemy):
        # player is the coordinates and angle of the player character
        # [X,Y,angle]
        self.player = player
        # enemy is an array of the enemy coordinate [X,Y]
        self.enemy = enemy
        self.l = None
        self.angle = None
        self.command = None
        self.calcAngle()
        self.fuzzy_sys()

    def calcAngle(self):
        X1 = self.player[0]; Y1 = self.player[1]
        X2 = self.enemy[0];  Y2 = self.enemy[1]

        X = X2-X1
        Y = Y2-Y1
        # angle is in degrees
        self.angle = np.arctan(X/Y) * 180/np.pi


    def fuzzy_sys(self):
        angleE = self.angle
        angleP = self.player[2]

        input = angleP - angleE
        MF = Membership(input)

        inMF_values = [(-90,-60,-30),
                     (-60,-30,0),
                     (-30,0,30),
                     (0,30,60),
                     (30,60,90)]

        outMF_values = [(-3,-2,-1),
                     (-2,-1,0),
                     (-1,0,1),
                     (0,1,2),
                     (1,2,3)]

        in1 = MF.lshlder(inMF_values[0])
        in2 = MF.triangle(inMF_values[1])
        in3 = MF.triangle(inMF_values[2])
        in4 = MF.triangle(inMF_values[3])
        in5 = MF.lshlder(inMF_values[4])

        MU = [in1,in2,in3,in4,in5]
        fz = Defuzz(MU, outMF_values)
        self.command = fz.crisp()

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 0
    enemy_vel = 1
    player_vel = 5
    laser_vel = 5
    player_initx = 300
    player_inity = 630
    player = Player(player_initx,player_inity)
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0))
        #Draw Text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        WIN.blit(lives_label,(10, 10))
        WIN.blit(level_label,(WIDTH - level_label.get_width() - 10 ,10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost", 1, (255,255,255))
            WIN.blit(lost_label, (round(WIDTH/2 - lost_label.get_width()/2), 350))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            # wave_length += 1
            wave_length = 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        keys = pygame.key.get_pressed()
        playerCoord = [player_initx,player_inity,player.angle]
        enemyCoord = [enemy.x,enemy.y]

        fuzzy_sys = FIS(playerCoord, enemyCoord)
        player.angle += fuzzy_sys.command()
        # if keys[pygame.K_LEFT]:
        #     player.angle += 1
        # if keys[pygame.K_RIGHT]:
        #     player.angle -= 1

        if keys[pygame.K_SPACE]:
            player.shoot()



        player.move_lasers(-laser_vel, enemies)

main()
