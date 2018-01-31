#!/usr/python
# -*- coding: utf-8 -*-

# Modules
# ---------------------------------------------------------------------
import pygame
from pygame.locals import *
import graphics
import config
# ---------------------------------------------------------------------

class Kate(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Cargamos el sheet
        self.sheet = graphics.load_image(config.test_sprites_kate, True)

        # Definimos medidas
        self.WIDTH = 52
        self.HEIGHT = 76

        # Definimos el tamaño de cada clip del sheet
        self.sheet.set_clip(pygame.Rect(0, 0, self.WIDTH, self.HEIGHT))

        # Recogemos la imagen inicial del sheet
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        # Recogemos el rect de la imagen
        self.rect = self.image.get_rect()

        # Establecemos el primer frame de la animacion a 0 (hay 4)
        self.frame = 0

        # Definimos cada estado con sus coordenadas
        self.left_states = {0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76)}
        self.right_states = {0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76)}
        self.up_states = {0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76)}
        self.down_states = {0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76)}

        # Definimos el delay de la animacion
        self.updated = pygame.time.get_ticks()

        # Definimos la velocidad de movimiento y salto
        self.speed = [1/config.device, 1/config.device]
        self.jump_force = 5

        # Flag para saber si esta saltando
        self.jumping = False


    # Funcion para recoger el sprite marcado por self.frame
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    # Funcion para
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))


    def update(self, direction, time):
        # Si es una animacion, pasamos el diccionario con las coordenadas de la animacion
        if direction == 'left':
            self.clip(self.left_states)
            # Si no esta en el borde izquierdo, le permitimos el movimiento
            if self.rect.x >= 0:
                self.rect.x -= self.speed[0] * time
        if direction == 'right':
            self.clip(self.right_states)
            if self.rect.x <= config.width-self.WIDTH:
                self.rect.x += self.speed[0] * time
        if direction == 'up':
            self.clip(self.up_states)
            if self.rect.y >= 0:
                self.rect.y -= self.speed[1] * time
        if direction == 'down':
            self.clip(self.down_states)
            if self.rect.y <= config.height-self.HEIGHT:
                self.rect.y += self.speed[1] * time

        # Si no es una animacion, pasamos el primer sprite del diccionario con las coordenadas de la animacion
        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())


    def calculate_gravity(self):
        if self.rect.y <= config.height:
            print 'bajando'
            print self.rect.y
            self.rect.y = self.rect.y + config.gravity


    def jump(self, jump_force):
        self.rect.y = -jump_force


    # Manejador de eventos
    def handle_event(self, time):
        self.calculate_gravity()
        if self.rect.y + self.HEIGHT > config.height:
            self.rect.y = config.height - self.HEIGHT
            self.jumping = False
        # Eventos continuos
        if self.updated + config.fps <= pygame.time.get_ticks():
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.update('left', time)
            if keys[K_RIGHT]:
                self.update('right', time)
            if keys[K_UP]:
                self.update('up', time)
            if keys[K_DOWN]:
                self.update('down', time)
            self.updated = pygame.time.get_ticks()

        # Eventos unicos
        for event in pygame.event.get(KEYUP):
            if event.key == pygame.K_LEFT:
                self.update('stand_left', time)
            if event.key == pygame.K_RIGHT:
                self.update('stand_right', time)
            if event.key == pygame.K_UP:
                self.update('stand_up', time)
            if event.key == pygame.K_DOWN:
                self.update('stand_down', time)
        for event in pygame.event.get(KEYDOWN):
            if event.key == pygame.K_SPACE:
                if not self.jumping:
                    self.jump(self.jump_force)
                    self.jumping = True