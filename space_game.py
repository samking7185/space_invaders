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
from fis_class import *

def game(enemy_no, level_quit):
    fitness = []
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
    player_initx = 350
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
        # time.sleep(2)
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
            wave_length = enemy_no
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-50, 0), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if level >= level_quit:
            return player.fitness
            quit()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                fitness.append(-10)
                enemies.remove(enemy)

        keys = pygame.key.get_pressed()
        playerCoord = [player_initx,player_inity,player.angle]
        enemyCoord = [enemy.x,enemy.y]
        # print(enemyCoord)
        # print(player.angle)
        try:
            fuzzy_lead = leadFIS(enemyCoord)
            fuzzy_sys = steerFIS(playerCoord, fuzzy_lead.enemy)
            angleUpdate = fuzzy_sys.fuzzy_system()
            player.angle += angleUpdate*(-1)
        except:
            continue

        fuzzy_shoot = fireFIS(angleUpdate, fuzzy_lead.enemy)
        if fuzzy_shoot.fire > 8:
            player.shoot()
        # if fuzzy_shoot > 8:
        #     player.shoot()

        if keys[pygame.K_LEFT]:
            player.angle += 1
        if keys[pygame.K_RIGHT]:
            player.angle -= 1

        if keys[pygame.K_SPACE]:
            player.shoot()
        fitness_val = player.move_lasers(-laser_vel, enemies)

if __name__ == "__main__":
    game()
