"""
All this does it process input.

"""


import pygame
from pygame.locals import *
import threading
from c4_model import C4_Model
from c4_view import C4_View
from c4_cpuplayer import RandomPlayer, MinimaxPlayer

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
                    # print(threading.active_count())
                    if self.model.getstate("GAME OVER"):
                        pass # Ignore clicks if game is over
                    else:
                        # This doesn't work if both players are cpus
                        if self.playerishuman(self.model.getcurrentplayer()):
                            column = self.view.convert_mousepos(event.pos)
                            self.model.makemove(column)
                            if not self.playerishuman(self.model.getcurrentplayer()) and not self.model.getstate("GAME OVER"):
                                threading.Thread(target=self.getcpumove).start()

    def getcpumove(self):
        board = self.model.getboardcopy()
        cpuplayer = MinimaxPlayer(board, self.cpumovecallback)
        cpuplayer.get_move()

    def cpumovecallback(self, col):
        self.model.makemove(col)

    def playerishuman(self, playernumber):
        if playernumber == 1:
            return True
        else:
            return False