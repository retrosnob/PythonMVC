# c4model.py
from copy import deepcopy

class C4_Model:

    def __init__(self):
        self.__board = Board()
        self.__listeners = []

    def register_listener(self, listener):
        """Allows other objects to listen to model events.

        The other object calls this function, passing in a function
        of their own, which is called when the model's notify 
        function is run. In this way, the model can notify other
        objects of things that have happened that they might want
        to respond to, e.g. updating the screen.

        Args:
            listener (function): The listener function.
        """        
        # Add the listener function to the list
        self.__listeners.append(listener) 

    def __notify(self, event):
        """Notifies other objects by calling their listener functions.

        Loops through the list of listener functions, passing  the event
        to each of them.

        Args:
            event (ModelEvent): The event to notify the listeners of.
        """        
        for listener in self.__listeners:
            listener(event)

    def makemove(self, column):
        """Accepts a move in a particular column and updates the game.

        Args:
            column (int): The column where the move is being played.
        """        
        if not self.__board.islegalmove(column) or self.__board.getstate("GAME OVER"):
            # Ignore if input is invalid or game is over.
            return
        else:
            # Update the game grid and status
            self.__board.pushmove(column)
            # Notify listeners that a move has been mode
            self.__notify(ModelEvent("MOVE"))
            if self.__board.getstate("GAME OVER"):
                self.__notify(ModelEvent("RESULT"))
    
    def getstate(self, statusstring):
        return self.__board.getstate(statusstring)
    
    def getgrid(self):
        return self.__board.getgrid()    
    
    def getcurrentplayer(self):
        return self.__board.getcurrentplayer()
    
    def getboardcopy(self):
        return deepcopy(self.__board)

class ModelEvent:
    # A little object to wrap information about the event
    def __init__(self, message):
        self.message = message

class Board:
    def __init__(self):
        self.__currentplayer = 1
        self.__grid = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
        ]
        self.__columncounts = [0,0,0,0,0,0,0]        
        self.__reset_state()

    def __reset_state(self):
        self.__state = {
            "GAME OVER" : False,
            "WINNER" : None,
            "WINNING_LINE" : None
        }                        

    def __updatestate(self):
        # Must check for win before checking for draw
        if self.gamewon():
            self.__state["GAME OVER"] = True
            self.__state["WINNER"] = self.getcurrentplayer()
            self.__state["WINNING_LINE"] = self.getwinningline()
        elif self.gridfull():
            # Means draw if no winner
            self.__state["GAME OVER"] = True

    def __horizontalwin(self):
        for r, row in enumerate(self.__grid):
            for c in range(4):
                if (row[c] != 0 and
                    row[c] == row[c+1] and 
                    row[c] == row[c+2] and 
                    row[c] == row[c+3]):
                    self.__winningline = ((r,c), (r,c+1), (r,c+2), (r,c+3))
                    return True
        return False

    def __verticalwin(self):
        for c in range(7):
            for r in range(3):
                if (self.__grid[r][c] != 0 and
                    self.__grid[r][c] == self.__grid[r+1][c] and
                    self.__grid[r][c] == self.__grid[r+2][c] and
                    self.__grid[r][c] == self.__grid[r+3][c]):
                    self.__winningline = ((r,c), (r+1,c), (r+2,c), (r+3,c))
                    return True
        return False

    def __diagonalwin(self):
        # Top-left to Bottom-right
        # x x x x . . .
        # x x x x \ . .
        # x x x x \ \ .
        # . \ \ \ \ \ \
        # . . \ \ \ \ \
        # . . . \ \ \ \
        for r in range(3):
            for c in range(4):
                if (self.__grid[r][c] != 0 and
                    self.__grid[r][c] == self.__grid[r+1][c+1] and
                    self.__grid[r][c] == self.__grid[r+2][c+2] and
                    self.__grid[r][c] == self.__grid[r+3][c+3]):
                    self.__winningline = ((r,c), (r+1,c+1), (r+2,c+2), (r+3,c+3))
                    return True
        
        # Bottom-left to Top-right
        # . . . / / / /
        # . . / / / / /
        # . / / / / / /
        # x x x x / / .
        # x x x x / . .
        # x x x x . . .
        for r in range(3, 6):
            for c in range(4):
                if (self.__grid[r][c] != 0 and
                    self.__grid[r][c] == self.__grid[r-1][c+1] and
                    self.__grid[r][c] == self.__grid[r-2][c+2] and
                    self.__grid[r][c] == self.__grid[r-3][c+3]):
                    self.__winningline = ((r,c), (r-1,c+1), (r-2,c+2), (r-3,c+3))
                    return True
        
        return False

    def gridfull(self):
        # All columncounts 6
        for count in self.__columncounts:
            if count < 6:
                return False
        return True        
    
    def gamewon(self):
        if self.__horizontalwin() or self.__verticalwin() or self.__diagonalwin():
            # print(self.__winningline)
            # for x, y in self.__winningline:
            #     print(x,y)
            return True
        else:
            return False    
        
    def __togglecurrentplayer(self):
        if self.__currentplayer == 1:
            self.__currentplayer = 2
        else:
            self.__currentplayer = 1        

    def pushmove(self, column):
        """Makes a move in a particular colum.

        Args:
            column (int): The column where the move is being played.
        """        
         
        if column < 0 or column > 6 or self.__columncounts[column] >= 6:
            # Ignore if input is invalid or game is over.
            return
        else:
            # Update the game grid and status
            row = self.__columncounts[column]
            self.__grid[row][column] = self.__currentplayer
            self.__columncounts[column] += 1
            self.__updatestate() # Important to update state before toggling player
            self.__togglecurrentplayer()   

    def popmove(self, column):
        if self.__grid[0][column] == 0:
            raise ValueError("There is no piece in this column to pop!")
        elif self.__grid[5][column] != 0:
            # The column is full so it must be the top piece to remove
            self.__grid[5][column] = 0
        else:
            for row in range(1, 6):
                if self.__grid[row][column] == 0:
                    self.__grid[row-1][column] = 0
        # Remove the top piece from the column (set to 0)
        self.__columncounts[column] -= 1
        # Reset the state in case a winner was set by the popped move
        self.__reset_state()
        # toggle player
        self.__togglecurrentplayer()
 
    def getgrid(self):
        return deepcopy(self.__grid)        
    
    def islegalmove(self, column):
        return column >= 0 and column <= 6 and self.__columncounts[column] < 6
    
    def getlegalmoves(self):
        legalmoves = []
        for col in range(7):
            if self.islegalmove(col):
                legalmoves.append(col)
        return legalmoves
    
    def getwinningline(self):
        return self.__winningline
    
    def getcurrentplayer(self):
        return self.__currentplayer
    
    def getstate(self, property):
        return self.__state[property]
    
    def print(self):
        # This function is for testing only        
        for row in self.__grid[::-1]:
            print(self.__getrowasstring(row))

    def __getrowasstring(self, row):
        returnstring = ''
        for value in row:
            if value == 0:
                returnstring += "."    
            else:
                returnstring += str(value)
        return returnstring    