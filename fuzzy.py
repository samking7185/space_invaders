import numpy as np
import os
import time
import random

class Membership:
    def __init__(self, x):
        self.x = x
        self.le = None
        self.ce = None
        self.re = None
        self.mu = None

    def triangle(self, values):
        x = self.x
        le = values[0]
        ce = values[1]
        re = values[2]
        if x >= le and x < ce:
            mu = (x - le)/(ce - le)
        elif x >= ce and x <= re:
            mu = (re - x)/(re - ce)
        else:
            mu = 0
        return mu

    def rshlder(self, values):
        x = self.x
        le = values[0]
        ce = values[1]
        re = values[2]
        if x >= le and x < ce:
            mu = (x - le)/(ce - le)
        elif x >= ce and x <= re:
            mu = 1
        else:
            mu = 0
        return mu

    def lshlder(self, values):
        x = self.x
        le = values[0]
        ce = values[1]
        re = values[2]
        if x >= le and x < ce:
            mu = 1
        elif x >= ce and x <= re:
            mu = (re - x)/(re - ce)
        else:
            mu = 0
        return mu

class Rulebase:
    def __init__(self):
        self.output = None

    def AND_rule(self, input):
        self.output = np.amin(input)
        return self.output

    def OR_rule(self, input):
        self.output = np.amax(input)
        return self.output

class Defuzz:
    def __init__(self, mu, output):
        self.mu = mu
        self.output = output
        self.defuzz_out()

    def defuzz_out(self):
        A_out = []
        A_outC = []
        for i in range(len(self.mu)):
            # self.output should be list of tuples
            # (le, ce, re)
            outMF = list(self.output[i])

            A_outN = 0.5*self.mu[i]*(outMF[0] - outMF[2])
            A_out.append(A_outN)
            A_outC.append(outMF[1])

        union = np.sum(A_out)

        out_Num = np.multiply(A_out, A_outC)
        if abs(union) > 0.1:
            crisp_out = np.sum(out_Num)/union
        else:
            crisp_out = 0
        return crisp_out
