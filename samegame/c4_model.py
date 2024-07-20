# c4model.py

class C4_Model:

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
        self.__status = {
            "GAME OVER" : False,
            "WINNER" : None
        }
        self.__listeners = []

    def register_listener(self, listener):
        # Add the listener function to the list
        self.__listeners.append(listener)

    def notify(self, event):
        # Pass the event to each listener
        for listener in self.__listeners:
            listener(event)

    def makemove(self, column):
        if column < 0 or column > 6 or self.__columncounts[column] >= 6 or self.__status["GAME OVER"] == True:
            return
        else:
            row = self.__columncounts[column]
            self.__grid[row][column] = self.__currentplayer
            self.__columncounts[column] += 1
            self.__updatestatus()
            self.__togglecurrentplayer()
            self.__notify(ModelEvent("MOVE")) # Controller tells view to update boards
    
    def __updatestatus(self):
        # Must check for win before checking for draw
        if self.__gamewon():
            self.__status["GAME OVER"] = True
            self.__status["WINNER"] = self.__currentplayer
            self.__notify(ModelEvent("RESULT"))
        elif self.__gridfull():
            # Means draw if no winner
            self.__status["GAME OVER"] = True
            self.__notify(ModelEvent("RESULT"))

    def __togglecurrentplayer(self):
        if self.__currentplayer == 1:
            self.__currentplayer = 2
        else:
            self.__currentplayer = 1

    def __gamewon(self):
        if self.__horizontalwin() or self.__verticalwin() or self.__diagonalwin():
            return True
        else:
            return False

    def __horizontalwin(self):
        for row in self.__grid:
            for i in range(4):
                if (row[i] != 0 and
                    row[i] == row[i+1] and 
                    row[i] == row[i+2] and 
                    row[i] == row[i+3]):
                    return True
        return False

    def __verticalwin(self):
        for col in range(7):
            for row in range(3):
                if (self.__grid[row][col] != 0 and
                    self.__grid[row][col] == self.__grid[row+1][col] and
                    self.__grid[row][col] == self.__grid[row+2][col] and
                    self.__grid[row][col] == self.__grid[row+3][col]):
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
        for row in range(3):
            for col in range(4):
                if (self.__grid[row][col] != 0 and
                    self.__grid[row][col] == self.__grid[row+1][col+1] and
                    self.__grid[row][col] == self.__grid[row+2][col+2] and
                    self.__grid[row][col] == self.__grid[row+3][col+3]):
                    return True
        
        # Bottom-left to Top-right
        # . . . / / / /
        # . . / / / / /
        # . / / / / / /
        # x x x x / / .
        # x x x x / . .
        # x x x x . . .
        for row in range(3, 6):
            for col in range(4):
                if (self.__grid[row][col] != 0 and
                    self.__grid[row][col] == self.__grid[row-1][col+1] and
                    self.__grid[row][col] == self.__grid[row-2][col+2] and
                    self.__grid[row][col] == self.__grid[row-3][col+3]):
                    return True
        
        return False

    def __gridfull(self):
        # All columncounts 6
        for count in self.__columncounts:
            if count < 6:
                return False
        return True

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
    
    def getstatus(self):
        return self.__status

class ModelEvent:
    # A little object to wrap information about the event
    def __init__(self, message):
        self.message = message