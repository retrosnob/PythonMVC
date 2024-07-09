#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import pygame
from pygame.locals import *
from same_model import Same_M
from same_view import Same_V


class Same_C(object):
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
                if event.button:
                    row, col = self.view.convert_mousepos(event.pos)
                    if self.view.selection:
                        # ! If a selection exists...
                        if self.view.selection[row][col]:
                            # ! and the user has clicked in the selection
                            self.view.selection = None
                            # ! Misleading that the model's function is called
                            # ! select_blocks because it's nothing to do with the
                            # ! view's idea of a selection. It should be called 
                            # ! something like make_move:
                            self.model.select_blocks(row, col)
                            print('score: %s ' % (self.model.score, ))
                        else:
                            # ! Otherwise use the model's function to get the neighbours
                            # ! and set the view's selection to these cells before 
                            # ! redrawing. 
                            # ! Note how the model doesn't actually respond to the fact 
                            # ! that an initial selection has been made.
                            self.view.selection = (
                                    self.model.get_neighbours(row, col))
                    else:
                        # ! Slightly clunky that this line is repeated. We need to set
                        # ! the view's selection whether or not the click was in the 
                        # ! current selection.
                        self.view.selection = (
                                    self.model.get_neighbours(row, col))
                    # ! The view is asked to redraw. The model's state may have
                    # ! changed (a move was confirmed) or it may not (a new
                    # ! selection was made).
                    self.view.redraw()
