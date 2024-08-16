
import pygame
from pygame.locals import *
from c4_model import C4_Model

FRAMERATE = 60

TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
PURPLE = (220, 0, 220)
COLORS = (BLACK, PURPLE, GREEN, BLUE)

BG_COLOR = BLACK
SELECTION_COLOR = WHITE


class C4_View(object):
    def __init__(self, pixel_width, pixel_height, model):

        # we may observe the model
        self.model = model

        # listen for model events
        """
        ! Here we pass a function to the model, which it can call
        ! when it wants to notify us of an event.
        """
        model.register_listener(self.model_event)

        # calculate each piece size, and set our viewport size.
        # Set width and height in ratio 7 : 6
        self.pixel_width = 420
        self.pixel_height = 360
        self.screen_size = self.pixel_width, self.pixel_height 
        self.piece_radius = 0.4 * pixel_width / 7 # Piece diameter is 80% of grid cell size 

        # init pygame
        pygame.init()
        pygame.display.set_caption('same game')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        # draw game widgets on a surface to blit on screen
        # so we dont re-loop inside the screen update.
        self.game_surf = pygame.Surface(self.screen_size)
        self.game_surf.set_colorkey(TRANSPARENT)

        # draw selection regions on a surface to blit, too.
        self.select_surf = pygame.Surface(self.screen_size)
        self.select_surf.set_colorkey(TRANSPARENT)

    def __draw_grid(self):
        pass

    def __draw_pieces(self):
        pass

    def convert_mousepos(self, pos):
        """ convert window (x, y) coords into game field (row, col) values. """
        # ! Had to fix this line because it was return indexes as floats
        return int(pos[1] / self.block_size), int(pos[0] / self.block_size)

    def __redraw(self):
        """
        ! Called by the model event handler.
        """
        self.__draw_grid()
        self.__draw_pieces()

    def blit(self):
        # we blank the screen, we may draw a nice background later in time
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.game_surf, (0, 0))
        if self.selection:
            self.screen.blit(self.select_surf, (0, 0))
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    #! The model calls this function when a move is made
    def model_event(self, event_name, data):
        if event_name == "THE NAME OF THE EVENT":
            self.redraw()    
            self.blit()