
import pygame
from pygame.locals import *

FRAMERATE = 60

TRANSPARENT = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
PURPLE = (220, 0, 220)
YELLOW = (255, 255, 0)
COLORS = (BLACK, PURPLE, GREEN, BLUE)

BG_COLOR = BLACK

class C4_View:
    def __init__(self, model):

        # We need to keep a reference to the model so we can get the grid.
        self.model = model

        # Pass a function to the model that it can call when it wants us to update the screen.
        model.register_listener(self.model_event)

        # Calculate each piece size, and set the screen size.
        # Set width and height in ratio 7 : 6, the same as a Connect 4 board.
        self.pixel_width = 420
        self.pixel_height = 360
        self.screen_size = self.pixel_width, self.pixel_height 
        self.piece_radius = 0.4 * self.pixel_width / 7 # Piece diameter is 80% of grid cell size 

        # Initialise pygame.
        pygame.init()
        pygame.display.set_caption('Connect 4')
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        # Create the surface to draw on.
        # We will draw to a surface and then blit it all at once.
        self.game_surf = pygame.Surface(self.screen_size)
        self.game_surf.set_colorkey(TRANSPARENT)

        # Draw the starting position.
        self.draw()

    def __draw_grid(self):
        # Draw the lines. Just requires a little arithmetic.
        
        # Vertical lines.
        for i in range(1, 7):
            pygame.draw.line(self.game_surf, WHITE, (i * self.pixel_width // 7, 0), (i * self.pixel_width // 7, self.pixel_height), width=1)
        
        # Horizontal lines.
        for i in range(1, 6):
            pygame.draw.line(self.game_surf, WHITE, (0, i * self.pixel_height // 6), (self.pixel_width, i * self.pixel_height // 6), width=1)
            

    def __draw_pieces(self):
        # Get the current grid from the model.
        grid = self.model.getgrid()
        for row in range(6):
            for col in range(7):
                if grid[row][col] == 1:
                    self.__draw_piece(5-row, col, RED)
                elif grid[row][col] == 2:
                    self.__draw_piece(5-row, col, GREEN)
    
    def __draw_piece(self, row, col, COLOUR, width = 0):
        # Calculates the pixel coordinates on the screen from the index of the piece in the grid.
        x = col * self.pixel_width // 7 + self.pixel_width // 7 // 2
        y = row * self.pixel_height // 6 + self.pixel_height // 6 // 2
        pygame.draw.circle(self.game_surf, COLOUR, (x, y), self.piece_radius, width)

    def __draw_winning_line(self):
        # Highlight the winning line. Only gets called (by the draw function) when someone has won the game.
        line = self.model.getstate("WINNING_LINE")
        for r, c in line:
            self.__draw_piece(5-r, c, YELLOW, 3)
            
    def convert_mousepos(self, pos):
        # Convert the x coordinate of a click to a column number of the grid.
        return pos[0] // (self.pixel_width // 7)

    def draw(self):
        # Draw the grid and the pieces (and the winning line if there is one) to the surface and blit it.
        self.__draw_grid()
        self.__draw_pieces()
        if self.model.getstate("WINNING_LINE"):
            self.__draw_winning_line()
        self.__blit()

    def __blit(self):
        # Blank the screen and then draw the surface to the screen.
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.game_surf, (0, 0))
        pygame.display.flip()
        self.clock.tick(FRAMERATE)

    #! The model calls this function when a move is made
    def model_event(self, event):
        # Check the event type and then (re-)draw the screen.
        if event.message == "RESULT":
            if self.model.getstate("WINNER"):
                print(self.model.getstate("WINNER"))
            else:
                print("Draw")
        self.draw()    
