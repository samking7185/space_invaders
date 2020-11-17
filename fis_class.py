
import numpy as np
from fuzzy import *
import os
import time
import random
import sys
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
        in5 = MF.rshlder(inMF_values[4])
        MU = [in1,in2,in3,in4,in5]

        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        # print(command)
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

        Gout = np.array(self.gene[2]) * 10
        Gout = Gout.tolist()

        Grules = self.gene[3]

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

        outMF_values = [sorted((Gout[0], Gout[1], Gout[2])),
                        sorted((Gin2[3], Gin2[4], Gin2[5])),
                        sorted((Gin2[6], Gin2[7], Gin2[8]))]

        # inMF_values1 = [(0, 100, 200),
        #              (100,250,400),
        #              (250,400,550),
        #              (400,550,700),
        #              (600,700,800)]
        #
        # inMF_values2 = [(0, 100, 200),
        #              (100,250,400),
        #              (250,400,550),
        #              (400,550,700),
        #              (600,700,800)]
        #
        # outMF_values = [(-10,10,30),
        #              (0,20,40),
        #              (20,40,60)]

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
        # R1 = [R.AND_rule([in11, in21]), R.AND_rule([in12, in21]), R.AND_rule([in13, in21]), R.AND_rule([in14, in21]), R.AND_rule([in15, in21])]
        # R2 = [R.AND_rule([in11, in22]), R.AND_rule([in12, in22]), R.AND_rule([in13, in22]), R.AND_rule([in14, in22]), R.AND_rule([in15, in22])]
        # R3 = [R.AND_rule([in11, in23]), R.AND_rule([in12, in23]), R.AND_rule([in13, in23]), R.AND_rule([in14, in23]), R.AND_rule([in15, in23])]
        # R4 = [R.AND_rule([in11, in24]), R.AND_rule([in12, in24]), R.AND_rule([in13, in24]), R.AND_rule([in14, in24]), R.AND_rule([in15, in24])]
        # R5 = [R.AND_rule([in11, in25]), R.AND_rule([in12, in25]), R.AND_rule([in13, in25]), R.AND_rule([in14, in25]), R.AND_rule([in15, in25])]

        # R11 = R1
        # R11.extend(R2[1:4])
        # R11.append(R3[2])
        # R22 = []
        # R22.extend([R2[0], R2[4], R3[0], R3[1], R3[3], R3[4]])
        # R33 = R4
        # R33.extend(R5)

        # R111 = R.OR_rule(R11)
        # R222 = R.OR_rule(R22)
        # R333 = R.OR_rule(R33)
        # MU = [R111, R222, R333]

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

        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        self.enemy = [enemyX, (enemyY + command)]

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
        angle = np.absolute(self.angle)

        MF1 = Membership(enemyX)
        MF2 = Membership(enemyY)
        MF3 = Membership(angle)

        Gin1 = np.array(self.gene[0]) * 25
        Gin1 = Gin1.tolist()

        Gin2 = np.array(self.gene[1]) * 25
        Gin2 = Gin2.tolist()

        Gin3 = self.gene[2]

        # inMF_values1 = [(0, 100, 200),
        #              (100,250,400),
        #              (250,400,550),
        #              (400,550,700),
        #              (600,700,800)]
        #
        # inMF_values2 = [(0, 100, 200),
        #              (100,250,400),
        #              (250,400,550),
        #              (400,550,700),
        #              (600,700,800)]
        #
        # inMF_values3 = [(-0.125, 0, 0.04),
        #              (0, 0.25, 0.5),
        #              (0.25,0.5,1)]

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

        inMF_values3 = [sorted((Gin3[0], Gin3[1], Gin3[2])),
                        sorted((Gin3[3], Gin3[4], Gin3[5])),
                        sorted((Gin3[6], Gin3[7], Gin3[8]))]

        outMF_values = [(8, 9, 10)]

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
        in33 = MF3.rshlder(inMF_values3[2])


        R = Rulebase()
        Rules = [R.AND_rule([in11, in21, in31]), R.AND_rule([in12, in21, in31]), R.AND_rule([in13, in21, in31]), R.AND_rule([in14, in21, in31]), R.AND_rule([in15, in21, in31]),
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
        R.AND_rule([in11, in25, in33]), R.AND_rule([in12, in25, in33]), R.AND_rule([in13, in25, in33]), R.AND_rule([in14, in25, in33]), R.AND_rule([in15, in25, in33])]


        MU = [R.OR_rule(Rules)]

        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        self.fire = command
