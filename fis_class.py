
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
        self.l = None
        self.angle = None
        self.command = None
        self.calcAngle()

    def calcAngle(self):
        X1 = self.player[0]; Y1 = self.player[1]
        X2 = self.enemy[0];  Y2 = self.enemy[1]

        X = X1-X2
        Y = Y1-Y2
        # angle is in degrees
        self.angle = np.arctan(X/Y) * 180/np.pi


    def fuzzy_system(self):
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
        in5 = MF.rshlder(inMF_values[4])
        MU = [in1,in2,in3,in4,in5]

        fz = Defuzz(MU, outMF_values)
        command = fz.defuzz_out()
        return command

class leadFIS:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.command = None

    def calcAngle(self):
        X1 = self.player[0]; Y1 = self.player[1]
        X2 = self.enemy[0];  Y2 = self.enemy[1]

        X = X1-X2
        Y = Y1-(Y2+lead)
        # angle is in degrees
        self.angle = np.arctan(X/Y) * 180/np.pi

    def fuzzy_system(self):
        enemy = self.enemy
        player = self.player

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

        outMF_values = [(-45,-30,-15),
                     (-30,-15,0),
                     (-15,0,15),
                     (0,15,30),
                     (15,30,45)]

        in11 = MF.lshlder(inMF_values1[0])
        in12 = MF.triangle(inMF_values1[1])
        in13 = MF.triangle(inMF_values1[2])
        in14 = MF.triangle(inMF_values1[3])
        in15 = MF.rshlder(inMF_values1[4])

        in21 = MF.lshlder(inMF_values2[0])
        in22 = MF.triangle(inMF_values2[1])
        in23 = MF.triangle(inMF_values2[2])
        in24 = MF.triangle(inMF_values2[3])
        in25 = MF.rshlder(inMF_values2[4])
