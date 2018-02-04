#!/usr/python
# -*- coding: utf-8 -*-


# Modules
# ---------------------------------------------------------------------
import pygame as pg
import random
from config import *
from character import Character
# ---------------------------------------------------------------------


class Mob(Character):
    def __init__(self):
        Character.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-200, SCREEN_WIDTH+200)
        self.rect.y = random.randrange(-100, -40)
        self.radius = 20
        self.speedy = random.randrange(1, 4)
        self.speedx = 0


    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(-300, SCREEN_WIDTH+300)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)