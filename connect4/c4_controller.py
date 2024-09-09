"""
All this does it process input.

"""


import pygame
from pygame.locals import *
from c4_model import C4_Model
from c4_view import C4_View

# Isn't Git great?!

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
                    if self.model.getstatus()["GAME OVER"]:
                        pass # Ignore clicks if game is over
                    else:
                        print("Click at", event.pos)
                        column = self.view.convert_mousepos(event.pos)
                        self.model.makemove(column)