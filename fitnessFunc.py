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
from fitGame_class import *
from fis_class import *

def processGene(gene, N):
    allele = gene[0].tolist()

    gene_pieces = []
    Nvals = np.cumsum(N)
    Nvals = Nvals.tolist()

    Nvals.insert(0,0)
    for idx in range(len(Nvals[:-1])):
        val = allele[Nvals[idx]:Nvals[idx+1]]
        gene_pieces.append(val)
    return gene_pieces

def game(enemy_no, level_quit, gene, N, indices, iterations):
    timer = 0
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
    check = 0
    # player.cool_down_counter = 0
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
        timer += 1
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
            if iterations:
                for i in range(enemy_no):
                    enemyCoord = np.linspace(10, WIDTH-10, num=iterations, dtype='int')
                    enemy = Enemy(enemyCoord[indices], 5, random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
            else:
                for i in range(enemy_no):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(0, 10), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
            # player.cool_down_counter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        if level >= level_quit:
            return np.divide(player.fitness,timer)
            quit()

        keys = pygame.key.get_pressed()
        playerCoord = [player_initx,player_inity,player.angle]
        enemyCoord = [enemy.x,enemy.y]

        gene_pieces = processGene(gene, N)
        fuzzy_lead = leadFIS(enemyCoord, gene_pieces)
        fuzzy_sys = steerFIS(playerCoord, fuzzy_lead.enemy)
        angleUpdate = fuzzy_sys.fuzzy_system()
        player.angle += angleUpdate*(-1)
        fuzzy_shoot = fireFIS(angleUpdate, fuzzy_lead.enemy, gene_pieces)
        if fuzzy_shoot.fire > 8:
            player.shoot()
            check = 11

        if keys[pygame.K_LEFT]:
            player.angle += 1
        if keys[pygame.K_RIGHT]:
            player.angle -= 1

        if keys[pygame.K_SPACE]:
            player.shoot()
            check = 11

        if len(player.lasers) == 0 and check == 11:
            break
        fitness_val = player.move_lasers(-laser_vel, enemies)
