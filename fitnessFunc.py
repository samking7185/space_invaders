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

def sortEnemies(enemies):

    enemyArr = []
    enemyArrY = []
    for i in range(len(enemies)):
        enemyArr.append([getattr(enemies[i], 'x'), getattr(enemies[i], 'y')])

    minX = enemyArr.index(min(enemyArr, key=lambda x: x[0]))
    maxX = enemyArr.index(max(enemyArr, key=lambda x: x[0]))


    minCoords = [enemyArr[minX], enemyArr[maxX]]
    firstInd = minCoords.index(max(minCoords, key=lambda x: x[1]))
    firstEnemy = minCoords[firstInd]

    enemiesSorted = sorted(enemyArr, key=itemgetter(0))
    return enemiesSorted

def processFitness(fitArray):
    fitnessDict = fitArray[0]
    timer = fitArray[1]
    level = fitArray[2]
    fitnessArray = []
    # fitArray structure
    # [fitnessTemp ,timer, level]
    for val in fitnessDict.values():
        if not val:
            continue
        if val == [-50]:
            fitnessArray.append(-50)
        else:
            fitnessArray.append(np.max(val))
    fitnessValue = np.sum(fitnessArray)
    fitnessTotal = np.divide(np.multiply(fitnessValue, level), timer)
    return fitnessTotal

def game(gene, N):
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
    enemiesFIS = []
    wave_length = 0
    enemy_vel = 1
    player_vel = 5
    laser_vel = 5
    player_initx = 350
    player_inity = 630
    player = Player(player_initx,player_inity)
    check = True
    enemyLength = 0
    waitCounter = 0
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
            fitValue = processFitness([player.fitnessTemp ,timer, level])
            return fitValue
            quit()

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            enemyIndex = 0
            direction = 0
            level += 1
            wave_length += 2
            randomX = np.random.random_integers(1,70,1)
            enemyCoord = np.linspace(randomX, WIDTH - randomX, num=wave_length, dtype='int')
            for i in range(wave_length):
                # enemyCoord = np.linspace(10, WIDTH-70, num=wave_length, dtype='int')
                # enemyCoordY = np.full((1,len(enemyCoord)), 2)
                enemy = Enemy(int(enemyCoord[i]), random.randrange(1, 15), random.choice(["red", "green"]))
                enemies.append(enemy)
            enemyLength = len(enemies)

        gene_pieces = processGene(gene, N)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        keys = pygame.key.get_pressed()

        if enemies:
            # if check != 0:
            #     enemyIndex += 1
            #     check = 0
            enemyLength = len(enemies)
            enemyArray = sortEnemies(enemies)
            # enemyCoord = [enemy.x,enemy.y]
            enemyCoord = enemyArray[enemyIndex]
            playerCoord = [player_initx,player_inity,player.angle]
            fuzzy_lead = leadFIS(enemyCoord, gene_pieces)
            fuzzy_sys = steerFIS(playerCoord, fuzzy_lead.enemy)
            angleUpdate = fuzzy_sys.fuzzy_system()
            player.angle += angleUpdate*(-1)

            playerAngle = fuzzy_sys.player[2] - fuzzy_sys.angle
        # if enemies and abs(playerAngle) < 0.25:
        #     player.shoot()
        #     check = 11
        #     waitCounter = 1
            fuzzy_shoot = fireFIS(playerAngle, gene_pieces)
            if fuzzy_shoot.fire > 7:
                player.shoot()
               
        if keys[pygame.K_UP]:
            breakpoint()
        if keys[pygame.K_LEFT]:
            player.angle += 1
        if keys[pygame.K_RIGHT]:
            player.angle -= 1

        if keys[pygame.K_SPACE]:
            player.shoot()
            check = 11
        fitness_val = player.move_lasers(-laser_vel, enemies)
        # if fitness_val:
        #     for key,value in player.fitnessTemp.items():
        #         if key is laserCheck:
        #             if value:
        #                 if np.sum(value) > 0:
        #                     waitCounter = 0
        #                     enemyIndex += 1
        #                     if enemyIndex >= len(enemies):
        #                         enemyIndex = 0
