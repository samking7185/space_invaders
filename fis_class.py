
import numpy as np
from fuzzy import *
import os
import time
import random

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
    def __init__(self, enemy):
        self.enemy = enemy
        self.lead = None
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

        outMF_values = [(-20,0,20),
                     (0,20,40),
                     (20,40,60)]

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
        R1 = [R.AND_rule([in11, in21]), R.AND_rule([in12, in21]), R.AND_rule([in13, in21]), R.AND_rule([in14, in21]), R.AND_rule([in15, in21])]
        R2 = [R.AND_rule([in11, in22]), R.AND_rule([in12, in22]), R.AND_rule([in13, in22]), R.AND_rule([in14, in22]), R.AND_rule([in15, in22])]
        R3 = [R.AND_rule([in11, in23]), R.AND_rule([in12, in23]), R.AND_rule([in13, in23]), R.AND_rule([in14, in23]), R.AND_rule([in15, in23])]
        R4 = [R.AND_rule([in11, in24]), R.AND_rule([in12, in24]), R.AND_rule([in13, in24]), R.AND_rule([in14, in24]), R.AND_rule([in15, in24])]
        R5 = [R.AND_rule([in11, in25]), R.AND_rule([in12, in25]), R.AND_rule([in13, in25]), R.AND_rule([in14, in25]), R.AND_rule([in15, in25])]

        R11 = R1
        R11.extend(R2[1:4])
        R11.append(R3[2])
        R22 = R4[1:4]
        R22.extend([R2[0], R2[4], R3[0], R3[1], R3[3], R3[4]])
        R33 = R5
        R33.extend([R4[0], R4[4]])

        R111 = R.OR_rule(R11)
        R222 = R.OR_rule(R22)
        R333 = R.OR_rule(R33)
        MU = [R111, R222, R333]

        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        self.enemy = [enemyX, (enemyY + command)]
        print(command)
