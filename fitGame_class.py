import pygame
import os
import time
import random
import numpy as np

pygame.font.init()

WIDTH, HEIGHT = 800, 800

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

#Player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow3.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH,HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.fitness = []

    def draw(self,window):
        window.blit(self.img, (self.x,self.y))

    def move(self, vel, angle):
        velx = np.sin(angle*np.pi/180)
        vely = np.cos(angle*np.pi/180)
        self.y += round(vel*vely)
        self.x += round(vel*velx)

    def moveY(self, vel):
        self.y += vel

    def off_screenY(self,height):
        return not (self.y <= height and self.y >= 0)

    def off_screenX(self,width):
        return not (self.x <= width and self.x >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def buffer_collision(self, obj):
        return collide_buffer(self, obj)

class Player:
    COOLDOWN = 50
    def __init__(self,x,y,health=100, angle=0):
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.angle = angle
        self.x = x
        self.y = y
        self.health = health
        self.lasers = []
        self.cool_down_counter = 0
        self.fitness = []

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            laser_obj = (laser,self.angle)
            self.lasers.append(laser_obj)
            self.cool_down_counter = 1
            # self.fitness.append('s')

    def draw(self, window):
        angle = self.angle
        rotated_surface = self.ship_img.copy()
        rotated_rect = self.ship_img.get_rect(center = (self.x+50,self.y+45))
        rotated_surface = pygame.transform.rotozoom(rotated_surface, angle, 1)
        rotated_rect = rotated_surface.get_rect(center = rotated_rect.center)
        window.blit(rotated_surface,(rotated_rect))

        for (index,tuple) in enumerate(self.lasers):
            laser = tuple[0]
            laser.draw(window)

    def move_lasers(self, vel, objs):
        # self.cooldown()
        for (index,tuple) in enumerate(self.lasers):
            laserangle = tuple[1]
            laser = tuple[0]
            laser.move(vel,laserangle)

            if laser.off_screenY(HEIGHT):
                laser.fitness.append(-50)
                self.lasers.remove(tuple)
            elif laser.off_screenX(WIDTH):
                laser.fitness.append(-50)
                self.lasers.remove(tuple)

            else:
                for obj in objs:
                    if laser.collision(obj):
                        laser.fitness.append(100)
                        objs.remove(obj)
                        if laser in self.lasers[0]:
                            self.lasers.remove(tuple)
                    if laser.buffer_collision(obj):
                        val = np.max(laser.buffer_collision(obj))
                        laser.fitness.append(val)
            if laser.fitness:
                if laser.fitness == [-50]:
                    self.fitness.append(laser.fitness[0])
                elif laser.fitness == [100]:
                    self.fitness.append(laser.fitness[0])
                else:
                    self.fitness.append(np.amax(laser.fitness))
                final_fit = self.fitness
                return final_fit

class Enemy():
    COOLDOWN = 100
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER)
                }
    def __init__(self,x,y,color,health=100,angle=0):
        self.x = x
        self.y = y
        self.health = health
        self.lasers = []
        self.cool_down_counter = 0
        self.fitness = []
        self.angle = 0
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.buffer = pygame.mask.from_surface(pygame.transform.scale(self.ship_img,(round(self.ship_img.get_width()*2) , round(self.ship_img.get_height()*2))))
        self.buffer1 = pygame.mask.from_surface(pygame.transform.scale(self.ship_img,(round(self.ship_img.get_width()*3) , round(self.ship_img.get_height()*3))))
        self.buffer2 = pygame.mask.from_surface(pygame.transform.scale(self.ship_img,(round(self.ship_img.get_width()*4) , round(self.ship_img.get_height()*4))))

    def move(self, vel):
        self.y += vel

    def off_screenY(self,height):
        return not (self.y <= height and self.y >= 0)

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def collide_buffer(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    fitness = []
    if obj1.mask.overlap(obj2.buffer, (offset_x, offset_y)) != None:
        fitness.append(30)
    elif obj1.mask.overlap(obj2.buffer1, (offset_x, offset_y)) != None:
        fitness.append(20)
    elif obj1.mask.overlap(obj2.buffer2, (offset_x, offset_y)) != None:
        fitness.append(10)

    if fitness:
        fitness = np.amax(fitness)
    return fitness
