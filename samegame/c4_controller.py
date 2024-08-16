"""
All this does it process input.

"""


import pygame
from pygame.locals import *
from c4_model import C4_Model
from c4_view import C4_View


class C4_Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("left mouse button")
                elif event.button == 2:
                    print("middle mouse button")
                elif event.button == 3:
                    print("right mouse button")
                elif event.button == 4:
                    print("mouse wheel up")
                elif event.button == 5:
                    print("mouse wheel down")
