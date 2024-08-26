
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
    def __init__(self, model):

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
        self.piece_radius = 0.4 * self.pixel_width / 7 # Piece diameter is 80% of grid cell size 

        # init pygame
        pygame.init()
        pygame.display.set_caption('Connect 4')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        # draw game widgets on a surface to blit on screen
        # so we dont re-loop inside the screen update.
        self.game_surf = pygame.Surface(self.screen_size)
        self.game_surf.set_colorkey(TRANSPARENT)

        self.redraw()

    def __draw_grid(self):
        for i in range(1, 7):
            pygame.draw.line(self.game_surf, WHITE, (i * self.pixel_width // 7, 0), (i * self.pixel_width // 7, self.pixel_height), width=1)
        for i in range(1, 6):
            pygame.draw.line(self.game_surf, WHITE, (0, i * self.pixel_height // 6), (self.pixel_width, i * self.pixel_height // 6), width=1)
            

    def __draw_pieces(self):
        def draw_piece(row, col, COLOUR):
            x = col * self.pixel_width // 7 + self.pixel_width // 7 // 2
            y = row * self.pixel_height // 6 + self.pixel_height // 6 // 2
            pygame.draw.circle(self.game_surf, COLOUR, (x, y), self.piece_radius)
        
        grid = self.model.getgrid()[::-1]
        for row in range(6):
            for col in range(7):
                if grid[row][col] == 1:
                    draw_piece(row, col, RED)
                elif grid[row][col] == 2:
                    draw_piece(row, col, GREEN)
        

    def convert_mousepos(self, pos):
        """ convert window (x, y) coords into board column value. """
        return pos[0] // (self.pixel_width // 7)

    def redraw(self):
        """
        ! Called by the model event handler.
        """
        self.__draw_grid()
        self.__draw_pieces()

    def blit(self):
        # we blank the screen, we may draw a nice background later in time
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.game_surf, (0, 0))
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    #! The model calls this function when a move is made
    def model_event(self, event_name):
        self.redraw()    
        self.blit()