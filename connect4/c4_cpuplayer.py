"""
Need to be able to 

push and pop moves
evaluate the board
see whose move it is
get all legal moves

We don't want to duplicate functions that are already defined in the model.
Perhaps we abstract shared functions out into a separate class. Otherwise
we pass the cpuplayer's representation of the board back to the model for 
evaluation, etc.
"""

class RandomPlayer:
    def __init__(self, board, callback):
        self.board = board
        self.callback = callback

    def get_move(self):
        from random import choice
        from time import sleep
        sleep(2)
        col = choice([col for col in range(7) if self.board.islegalmove(col)])
        self.callback(col)

class MinimaxPlayer():
    def __init__(self, board, callback):
        self.best_move = None # Use this to get the move
        self.board = board
        self.callback = callback

    def get_move(self):
        self.minimax(0, 3, self.board.getcurrentplayer())
        self.callback(self.best_move)

    def evaluate(self, turn) -> float:
        """[summary]


        Args:
            grid (List): The current position as a 5x5 list with 1 or 2 for player pieces
            or 0 for empty.
            turn (Int): The player from whose pov to calculate the evaluation. A good 
            evaluation is positive for this player.


        Returns:
            float: The evaluation.
            
        There are two options here. We can always evaluate the position from the pov of the 
        maximising player by using an instance variable that never changes, or we can pass
        in the player from whose pov to evaluate the position. If the player passed in is
        always the maximising player, then these are equivalent. Alternatively, we could call
        this function with the player whose turn it is, whether or not they are the maximising
        player, and negate it if they aren't.
        
        In this implementation, we always pass in the maximising player, not the player whose
        turn it is.
        
        The function uses a table to calculate scores for piece positions as a way of preferring
        centralisation of the pieces. Other than that, if there is a result on the horizon,
        the static evaluations will dominate.
        """
        table = [
            [ 3, 4, 5, 7, 5, 4, 3], 
            [ 4, 6, 8,10, 8, 6, 4], 
            [ 5, 8,11,13,11, 8, 5], 
            [ 5, 8,11,13,11, 8, 5], 
            [ 4, 6, 8,10, 8, 6, 4], 
            [ 3, 4, 5, 7, 5, 4, 3] 
            ]
        score1 = score2 = 0
        table = [score for row in table for score in row] # flatten
        grid = [piece for row in self.board.getgrid() for piece in row] # flatten
        me, him = (1,2) if turn == 1 else (2, 1)
        
        for i in range(len(table)):
            if grid[i] == me:
                score1 += table[i]
            elif grid[i] == him:
                score2 += table[i]
        # Positive is good for the player represented by the turn argument
        return score1 - score2 

    def minimax(self, depth: int, max_depth: int, maximising_player: int) -> float:
        # self.board.print()
        currentplayer = self.board.getcurrentplayer()
        if self.board.getstate('GAME OVER'): 
            if not self.board.getstate('WINNER'): 
                # print(depth, ":draw")
                # Draw
                # Return static draw evaluation
                evaluation = 0
                return evaluation
            else:
                # print(f'{depth}: {currentplayer} wins')
                # Win
                # Return static win evaluation
                evaluation = 999 if maximising_player == self.board.getstate('WINNER') else -999
                return evaluation
        elif depth == max_depth:
            # print(f'{depth}: max depth reached')
            # Game is not over and depth is reached
            # Return static position evaluation
            # Note that we always evaluate from the pov of the maximising player
            # so that a negative score is good for the minimiser.
            evaluation = self.evaluate(maximising_player)
            print(f'Evaluation: {evaluation}')
            return evaluation
        else:
            # Game is not over and depth not reached so make next recursive minimax call
            moves = self.board.getlegalmoves()
            bestscore = -float('inf') if maximising_player == currentplayer else float('inf')
            for move in moves:
                print(f'player before push: {self.board.getcurrentplayer()}')
                self.board.pushmove(move)
                print(f'player after push: {self.board.getcurrentplayer()}')
                # ***********
                # Note that we keep the maximising_player from the original call.
                # We don't use the player whose turn it is.
                score = self.minimax(depth+1, max_depth, maximising_player)
                # ***********
                print(f'player before pop: {self.board.getcurrentplayer()}')
                self.board.popmove(move)
                print(f'player after pop: {self.board.getcurrentplayer()}')
                if depth == 0:
                    print(f'Candidate move: {move}, score: {score}')
                if maximising_player == currentplayer:
                    if score > bestscore:
                        bestscore = score
                        if depth == 0:
                            self.best_move = move
                            # print('best move for maximizer')
                else:
                    if score < bestscore:
                        bestscore = score
                        if depth == 0:
                            self.best_move = move
                            # print('best move for minimizer')
            return bestscore
