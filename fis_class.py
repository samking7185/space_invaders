
import numpy as np
from fuzzy import *
import os
import time
import random
import sys
from operator import itemgetter

class steerFIS:
    def __init__(self, player, enemy):
        # player is the coordinates and angle of the player character
        # [X,Y,angle]
        self.player = player
        # enemy is an array of the enemy coordinate [X,Y]
        self.enemy = enemy
        self.angle = None
        self.calcAngle()

    def calcAngle(self):
        X1 = self.player[0]; Y1 = self.player[1]
        X2 = self.enemy[0];  Y2 = self.enemy[1]

        X = X1-X2
        Y = Y1-Y2
        # angle is in degrees
        if Y == 0:
            self.angle = np.arctan(X/0.001) * 180/np.pi
        else:
            self.angle = np.arctan(X/Y) * 180/np.pi


    def fuzzy_system(self):
        # angleE = self.enemy
        # angleP = self.player
        # print(angleE)
        # print(angleP)
        # input = angleP - angleE
        input = self.player[2] - self.angle
        MF = Membership(input)
        # print('------------------')
        # print(input)
        inMF_values = [(-90,-60,-30),
                     (-60,-30,0),
                     (-30,0,30),
                     (0,30,60),
                     (30,60,90)]

        outMF_values = [(-6,-5,-4),
                     (-4,-3,-2),
                     (-2,0,2),
                     (2,3,4),
                     (4,5,6)]

        in1 = MF.lshlder(inMF_values[0])
        in2 = MF.triangle(inMF_values[1])
        in3 = MF.triangle(inMF_values[2])
        in4 = MF.triangle(inMF_values[3])
        in5 = MF.rshlder(inMF_values[4])
        MU = [in1,in2,in3,in4,in5]
        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        return command

class leadFIS:
    def __init__(self, enemy, gene):
        self.enemy = enemy
        self.lead = None
        self.gene = gene
        self.fuzzy_system()

    # def calcAngle(self):
    #     X1 = self.player[0]; Y1 = self.player[1]
    #     X2 = self.enemy[0];  Y2 = self.enemy[1]
    #
    #     X = X1-X2
    #     Y = Y1-(Y2+self.lead)
    #     # angle is in degrees
    #     self.angle = np.arctan(X/Y) * 180/np.pi

    def fuzzy_system(self):
        enemyX = self.enemy[0]
        enemyY = self.enemy[1]

        MF1 = Membership(enemyX)
        MF2 = Membership(enemyY)

        Gin1 = np.array(self.gene[0]) * 25
        Gin1 = Gin1.tolist()

        Gin2 = np.array(self.gene[1]) * 25
        Gin2 = Gin2.tolist()

        Gout1 = np.array(self.gene[2]) * 10
        Gout1 = Gout1.tolist()

        Gout2 = np.array(self.gene[3]) * 10
        Gout2 = Gout2.tolist()

        GrulesX = self.gene[4]
        GrulesY = self.gene[5]

        inMF_values1 = [sorted((0, Gin1[0], Gin1[1])),
                        sorted((Gin1[2], Gin1[3], Gin1[4])),
                        sorted((Gin1[5], Gin1[6], Gin1[7])),
                        sorted((Gin1[8], Gin1[9], Gin1[10])),
                        sorted((Gin1[11], Gin1[12], 800))]


        inMF_values2 = [sorted((0, Gin2[0], Gin2[1])),
                        sorted((Gin2[2], Gin2[3], Gin2[4])),
                        sorted((Gin2[5], Gin2[6], Gin2[7])),
                        sorted((Gin2[8], Gin2[9], Gin2[10])),
                        sorted((Gin2[11], Gin2[12], 800))]

        outMF_values1 = [sorted((Gout1[0], Gout1[1], Gout1[2])),
                        sorted((Gout1[3], Gout1[4], Gout1[5])),
                        sorted((Gout1[6], Gout1[7], Gout1[8]))]

        outMF_values2 = [sorted((Gout2[0], Gout2[1], Gout2[2])),
                        sorted((Gout2[3], Gout2[4], Gout2[5])),
                        sorted((Gout2[6], Gout2[7], Gout2[8]))]

        in11 = MF1.lshlder(inMF_values1[0])
        in12 = MF1.triangle(inMF_values1[1])
        in13 = MF1.triangle(inMF_values1[2])
        in14 = MF1.triangle(inMF_values1[3])
        in15 = MF1.rshlder(inMF_values1[4])

        in21 = MF2.lshlder(inMF_values2[0])
        in22 = MF2.triangle(inMF_values2[1])
        in23 = MF2.triangle(inMF_values2[2])
        in24 = MF2.triangle(inMF_values2[3])
        in25 = MF2.rshlder(inMF_values2[4])

        R = Rulebase()

        Rules = [
            R.AND_rule([in11, in21]), R.AND_rule([in12, in21]), R.AND_rule([in13, in21]), R.AND_rule([in14, in21]), R.AND_rule([in15, in21]),
            R.AND_rule([in11, in22]), R.AND_rule([in12, in22]), R.AND_rule([in13, in22]), R.AND_rule([in14, in22]), R.AND_rule([in15, in22]),
            R.AND_rule([in11, in23]), R.AND_rule([in12, in23]), R.AND_rule([in13, in23]), R.AND_rule([in14, in23]), R.AND_rule([in15, in23]),
            R.AND_rule([in11, in24]), R.AND_rule([in12, in24]), R.AND_rule([in13, in24]), R.AND_rule([in14, in24]), R.AND_rule([in15, in24]),
            R.AND_rule([in11, in25]), R.AND_rule([in12, in25]), R.AND_rule([in13, in25]), R.AND_rule([in14, in25]), R.AND_rule([in15, in25])
            ]
        R1 = []
        R2 = []
        R3 = []
        R4 = []
        R5 = []
        R6 = []

        for idx, rule in enumerate(GrulesX):
            if rule == 1.0:
                R1.append(Rules[idx])
            elif rule == 2.0:
                R2.append(Rules[idx])
            elif rule == 3.0:
                R3.append(Rules[idx])

        for idx, rule in enumerate(GrulesY):
            if rule == 1.0:
                R4.append(Rules[idx])
            elif rule == 2.0:
                R5.append(Rules[idx])
            elif rule == 3.0:
                R6.append(Rules[idx])

        R11 = R.OR_rule(R1)
        R22 = R.OR_rule(R2)
        R33 = R.OR_rule(R3)
        R44 = R.OR_rule(R4)
        R55 = R.OR_rule(R5)
        R66 = R.OR_rule(R6)


        MU1 = [R11, R22, R33]
        MU2 = [R44, R55, R66]

        fz1 = Defuzz(MU1, outMF_values1)
        command1 = fz1.defuzz_out()

        fz2 = Defuzz(MU2, outMF_values2)
        command2 = fz2.defuzz_out()
        self.enemy = [(enemyX + command1), (enemyY + command2)]

class fireFIS:
    def __init__(self, angleUpdate, enemy, gene):
        self.enemy = enemy
        self.fire = 0
        self.angle = angleUpdate
        self.gene = gene
        self.fuzzy_system()

    def fuzzy_system(self):
        enemyX = self.enemy[0]
        enemyY = self.enemy[1]
        angle = self.angle

        MF1 = Membership(enemyX)
        MF2 = Membership(enemyY)
        MF3 = Membership(angle)

        Gin3 = self.gene[6]
        Grules = self.gene[7]

        inMF_values1 = [(0, 100, 200),
                     (100,250,400),
                     (250,400,550),
                     (400,550,700),
                     (600,700,800)]

        inMF_values2 = [(0, 100, 200),
                     (100,250,400),
                     (250,400,550),
                     (400,550,700),
                     (600,700,800)]

        inMF_values3 = [
                        sorted((Gin3[0], Gin3[1], Gin3[2])),
                        sorted((Gin3[3], Gin3[4], Gin3[5])),
                        sorted((Gin3[6], Gin3[7], Gin3[8])),
                        sorted((Gin3[9], Gin3[10], Gin3[11])),
                        sorted((Gin3[12], Gin3[13], Gin3[14]))
                        ]

        outMF_values = [(0,1,2),(8,9,10)]

        in11 = MF1.lshlder(inMF_values1[0])
        in12 = MF1.triangle(inMF_values1[1])
        in13 = MF1.triangle(inMF_values1[2])
        in14 = MF1.triangle(inMF_values1[3])
        in15 = MF1.rshlder(inMF_values1[4])

        in21 = MF2.lshlder(inMF_values2[0])
        in22 = MF2.triangle(inMF_values2[1])
        in23 = MF2.triangle(inMF_values2[2])
        in24 = MF2.triangle(inMF_values2[3])
        in25 = MF2.rshlder(inMF_values2[4])

        in31 = MF3.triangle(inMF_values3[0])
        in32 = MF3.triangle(inMF_values3[1])
        in33 = MF3.triangle(inMF_values3[2])
        in34 = MF3.triangle(inMF_values3[3])
        in35 = MF3.triangle(inMF_values3[4])

        R = Rulebase()
        Rules = [
        R.AND_rule([in11, in21, in31]), R.AND_rule([in12, in21, in31]), R.AND_rule([in13, in21, in31]), R.AND_rule([in14, in21, in31]), R.AND_rule([in15, in21, in31]),
        R.AND_rule([in11, in22, in31]), R.AND_rule([in12, in22, in31]), R.AND_rule([in13, in22, in31]), R.AND_rule([in14, in22, in31]), R.AND_rule([in15, in22, in31]),
        R.AND_rule([in11, in23, in31]), R.AND_rule([in12, in23, in31]), R.AND_rule([in13, in23, in31]), R.AND_rule([in14, in23, in31]), R.AND_rule([in15, in23, in31]),
        R.AND_rule([in11, in24, in31]), R.AND_rule([in12, in24, in31]), R.AND_rule([in13, in24, in31]), R.AND_rule([in14, in24, in31]), R.AND_rule([in15, in24, in31]),
        R.AND_rule([in11, in25, in31]), R.AND_rule([in12, in25, in31]), R.AND_rule([in13, in25, in31]), R.AND_rule([in14, in25, in31]), R.AND_rule([in15, in25, in31]),
        R.AND_rule([in11, in21, in32]), R.AND_rule([in12, in21, in32]), R.AND_rule([in13, in21, in32]), R.AND_rule([in14, in21, in32]), R.AND_rule([in15, in21, in32]),
        R.AND_rule([in11, in22, in32]), R.AND_rule([in12, in22, in32]), R.AND_rule([in13, in22, in32]), R.AND_rule([in14, in22, in32]), R.AND_rule([in15, in22, in32]),
        R.AND_rule([in11, in23, in32]), R.AND_rule([in12, in23, in32]), R.AND_rule([in13, in23, in32]), R.AND_rule([in14, in23, in32]), R.AND_rule([in15, in23, in32]),
        R.AND_rule([in11, in24, in32]), R.AND_rule([in12, in24, in32]), R.AND_rule([in13, in24, in32]), R.AND_rule([in14, in24, in32]), R.AND_rule([in15, in24, in32]),
        R.AND_rule([in11, in25, in32]), R.AND_rule([in12, in25, in32]), R.AND_rule([in13, in25, in32]), R.AND_rule([in14, in25, in32]), R.AND_rule([in15, in25, in32]),
        R.AND_rule([in11, in21, in32]), R.AND_rule([in12, in21, in32]), R.AND_rule([in13, in21, in33]), R.AND_rule([in14, in21, in33]), R.AND_rule([in15, in21, in33]),
        R.AND_rule([in11, in22, in33]), R.AND_rule([in12, in22, in33]), R.AND_rule([in13, in22, in33]), R.AND_rule([in14, in22, in33]), R.AND_rule([in15, in22, in33]),
        R.AND_rule([in11, in23, in33]), R.AND_rule([in12, in23, in33]), R.AND_rule([in13, in23, in33]), R.AND_rule([in14, in23, in33]), R.AND_rule([in15, in23, in33]),
        R.AND_rule([in11, in24, in33]), R.AND_rule([in12, in24, in33]), R.AND_rule([in13, in24, in33]), R.AND_rule([in14, in24, in33]), R.AND_rule([in15, in24, in33]),
        R.AND_rule([in11, in25, in33]), R.AND_rule([in12, in25, in33]), R.AND_rule([in13, in25, in33]), R.AND_rule([in14, in25, in33]), R.AND_rule([in15, in25, in33]),
        R.AND_rule([in11, in21, in34]), R.AND_rule([in12, in21, in34]), R.AND_rule([in13, in21, in34]), R.AND_rule([in14, in21, in34]), R.AND_rule([in15, in21, in34]),
        R.AND_rule([in11, in22, in34]), R.AND_rule([in12, in22, in34]), R.AND_rule([in13, in22, in34]), R.AND_rule([in14, in22, in34]), R.AND_rule([in15, in22, in34]),
        R.AND_rule([in11, in23, in34]), R.AND_rule([in12, in23, in34]), R.AND_rule([in13, in23, in34]), R.AND_rule([in14, in23, in34]), R.AND_rule([in15, in23, in34]),
        R.AND_rule([in11, in24, in34]), R.AND_rule([in12, in24, in34]), R.AND_rule([in13, in24, in34]), R.AND_rule([in14, in24, in34]), R.AND_rule([in15, in24, in34]),
        R.AND_rule([in11, in25, in34]), R.AND_rule([in12, in25, in34]), R.AND_rule([in13, in25, in34]), R.AND_rule([in14, in25, in34]), R.AND_rule([in15, in25, in34]),
        R.AND_rule([in11, in21, in35]), R.AND_rule([in12, in21, in35]), R.AND_rule([in13, in21, in35]), R.AND_rule([in14, in21, in35]), R.AND_rule([in15, in21, in35]),
        R.AND_rule([in11, in22, in35]), R.AND_rule([in12, in22, in35]), R.AND_rule([in13, in22, in35]), R.AND_rule([in14, in22, in35]), R.AND_rule([in15, in22, in35]),
        R.AND_rule([in11, in23, in35]), R.AND_rule([in12, in23, in35]), R.AND_rule([in13, in23, in35]), R.AND_rule([in14, in23, in35]), R.AND_rule([in15, in23, in35]),
        R.AND_rule([in11, in24, in35]), R.AND_rule([in12, in24, in35]), R.AND_rule([in13, in24, in35]), R.AND_rule([in14, in24, in35]), R.AND_rule([in15, in24, in35]),
        R.AND_rule([in11, in25, in35]), R.AND_rule([in12, in25, in35]), R.AND_rule([in13, in25, in35]), R.AND_rule([in14, in25, in35]), R.AND_rule([in15, in25, in35]),
        R.AND_rule([in11, in21, in35]), R.AND_rule([in12, in21, in35])
        ]


        R1 = []
        R2 = []

        for idx, rule in enumerate(Grules):
            if rule == 1.0:
                R1.append(Rules[idx])
            elif rule == 2.0:
                R2.append(Rules[idx])

        R11 = R.OR_rule(R1)
        R22 = R.OR_rule(R2)

        MU = [R11, R22]

        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        self.fire = command

class threatFIS:
    def __init__(self, enemies, player, gene):
        self.enemies = enemies
        self.player = player
        self.gene = gene
        self.sortAngles = None
        self.sortY = None
        self.sortEnemy()

    def calcAngle(self, enemy):
        X1 = self.player.x; Y1 = self.player.y
        X2 = enemy[0];  Y2 = enemy[1]

        X = X2-X1
        Y = Y2-Y1
        # angle is in degrees
        if Y == 0:
            angle = np.arctan(X/0.001) * 180/np.pi
        else:
            angle = np.arctan(X/Y) * 180/np.pi
        return angle

    def sortEnemy(self):
        enemies = self.enemies
        player = self.player
        enemyArr = []
        enemyArrY = []
        for i in range(len(enemies)):
            enemyArr.append([getattr(enemies[i], 'x'), getattr(enemies[i], 'y')])
            enemyArrY.append(getattr(enemies[i], 'y'))
        self.sortY = enemyArrY
        enemyAngles = []
        for i in range(len(enemies)):
            enemyAngles.append(self.calcAngle(enemyArr[i]))
        self.sortAngles = [x - player.angle for x in enemyAngles]
        # minX = enemyArr.index(min(enemyArr, key=lambda x: x[0]))
        # maxX = enemyArr.index(max(enemyArr, key=lambda x: x[0]))
        #
        # minCoords = [enemyArr[minX], enemyArr[maxX]]
        # firstInd = minCoords.index(max(minCoords, key=lambda x: x[1]))
        # firstEnemy = minCoords[firstInd]

        # if firstInd == 0:
        #     enemiesSorted = sorted(enemyArr, key=itemgetter(0))
        # else:
        #     enemiesSorted = sorted(enemyArr, key=itemgetter(0), reverse=True)
        # return enemiesSorted

    def fuzzy_system(self):
        enemies = self.enemies
        enemyY = self.sortY
        angle = self.sortAngles
        enemyFinal = []
        Gin1 = np.array(self.gene[8]) * 25
        Gin1 = Gin1.tolist()

        Gin2 = np.array(self.gene[9])
        Gin2 = Gin2.tolist()

        Grules = self.gene[10]

        for i in range(len(enemyY)):
            MF1 = Membership(enemyY[i])
            MF2 = Membership(angle[i])

            inMF_values1 = [sorted((0, Gin1[0], Gin1[1])),
                            sorted((Gin1[2], Gin1[3], Gin1[4])),
                            sorted((Gin1[5], Gin1[6], Gin1[7])),
                            sorted((Gin1[8], Gin1[9], Gin1[10])),
                            sorted((Gin1[11], Gin1[12], 800))]

            inMF_values2 = [sorted((Gin2[0], Gin2[1], Gin2[2])),
                            sorted((Gin2[3], Gin2[4], Gin2[5])),
                            sorted((Gin2[6], Gin2[7], Gin2[8])),
                            sorted((Gin2[9], Gin2[10], Gin2[11])),
                            sorted((Gin2[12], Gin2[13], Gin2[14]))]

            outMF_values = [(0,1,2),(2,3,4),(4,5,6)]

            in11 = MF1.lshlder(inMF_values1[0])
            in12 = MF1.triangle(inMF_values1[1])
            in13 = MF1.triangle(inMF_values1[2])
            in14 = MF1.triangle(inMF_values1[3])
            in15 = MF1.rshlder(inMF_values1[4])

            in21 = MF2.lshlder(inMF_values2[0])
            in22 = MF2.triangle(inMF_values2[1])
            in23 = MF2.triangle(inMF_values2[2])
            in24 = MF2.triangle(inMF_values2[3])
            in25 = MF2.rshlder(inMF_values2[4])

            R = Rulebase()

            Rules = [
                R.AND_rule([in11, in21]), R.AND_rule([in12, in21]), R.AND_rule([in13, in21]), R.AND_rule([in14, in21]), R.AND_rule([in15, in21]),
                R.AND_rule([in11, in22]), R.AND_rule([in12, in22]), R.AND_rule([in13, in22]), R.AND_rule([in14, in22]), R.AND_rule([in15, in22]),
                R.AND_rule([in11, in23]), R.AND_rule([in12, in23]), R.AND_rule([in13, in23]), R.AND_rule([in14, in23]), R.AND_rule([in15, in23]),
                R.AND_rule([in11, in24]), R.AND_rule([in12, in24]), R.AND_rule([in13, in24]), R.AND_rule([in14, in24]), R.AND_rule([in15, in24]),
                R.AND_rule([in11, in25]), R.AND_rule([in12, in25]), R.AND_rule([in13, in25]), R.AND_rule([in14, in25]), R.AND_rule([in15, in25])
                ]

            R1 = []
            R2 = []
            R3 = []

            for idx, rule in enumerate(Grules):
                if rule == 1.0:
                    R1.append(Rules[idx])
                elif rule == 2.0:
                    R2.append(Rules[idx])
                elif rule == 3.0:
                    R3.append(Rules[idx])

            R11 = R.OR_rule(R1)
            R22 = R.OR_rule(R2)
            R33 = R.OR_rule(R3)

            MU = [R11, R22, R33]
            maxMu = MU.index(max(MU))
            enemyFinal.append(maxMu)

        zipped_lists = zip(enemyFinal, enemies)
        enemyOut = sorted(zipped_lists, key=lambda x: x[0])
        enemyOutObj = [x[1] for x in enemyOut]
        enemyOutCoord = [[x.x, x.y] for x in enemyOutObj]
        return enemyOutCoord
