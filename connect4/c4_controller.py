import pygame
from pygame.locals import *
import threading
from c4_cpuplayer import RandomPlayer, MinimaxPlayer

class C4_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def process_input(self):
        # Process the pygame event queue.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    if self.model.getstate("GAME OVER"):
                        pass # Ignore clicks if game is over.
                    else:
                        # TODO This doesn't work if both players are cpus.
                        if self.playerishuman(self.model.getcurrentplayer()):
                            # If the click happened on a human's turn, then make the move.
                            column = self.view.convert_mousepos(event.pos)
                            self.model.makemove(column)
                            if not self.playerishuman(self.model.getcurrentplayer()) and not self.model.getstate("GAME OVER"):
                                # If it's now the CPU's turn, start a thread for Minimax.
                                threading.Thread(target=self.getcpumove).start()

    def getcpumove(self):
        # This function runs in its own thread, so that the game is still responsive,
        # e.g. to a click exiting the game, while the CPU player calculates.
        board = self.model.getboardcopy()
        MinimaxPlayer(board, self.cpumovecallback).calculate_move()

    def cpumovecallback(self, col):
        # This function is passed to the CPU player's constructor. When the CPU player is done
        # calculating, it calls this function and the model can go ahead and make the move.
        self.model.makemove(col)

    def playerishuman(self, playernumber):
        # TODO Assumes the first player is always human. This will need to be changed when
        # TODO we start supporting human as player 2.
        if playernumber == 1:
            return True
        else:
            return False