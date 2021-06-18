import numpy as np


class GomokuMove(object):
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self):
        return "x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate) + " v:" + str(self.value)


class GomokuGameState(object):
    x = 1
    o = -1

    def __init__(self, state, next_to_move=1):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        # check if game is over
        '''rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        if any(rowsum == self.board_size) or any(
                        colsum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
            return 1.
        elif any(rowsum == -self.board_size) or any(
                        colsum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:

            return -1.
        elif np.all(self.board != 0):
            return 0.
        else:
            # if not over - no result
            return None'''
        
        for i in range(self.board_size):
            orow=0
            ocol=0
            xrow=0
            xcol=0
            for j in range(self.board_size):
                if self.board[i][j]==1:
                    xrow+=1
                    orow=0
                elif self.board[i][j]==-1:
                    xrow=0
                    orow+=1
                else:
                    xrow=0
                    orow=0
                    
                if self.board[j][i]==1:
                    xcol+=1
                    ocol=0
                elif self.board[j][i]==-1:
                    ocol+=1
                    xcol=0
                else:
                    xcol=0
                    ocol=0
                 
                if orow==5 or ocol==5:
                    return -1.
                elif xrow==5 or xcol==5:
                    return 1.
        rdiag=[(x,0)for x in range(self.board_size-4)]+[(0,y)for y in range(self.board_size-4)]
        ldiag=[(x,self.board_size-1)for x in range(6)]+[(0,y)for y in range(self.board_size-1,3,-1)]
        for i,j in rdiag:
            ordiag=0
            xrdiag=0
            while i<self.board_size and j<self.board_size:
                if self.board[i][j]==1:
                    xrdiag+=1
                    ordiag=0
                elif self.board[i][j]==-1:
                    ordiag+=1
                    xrdiag=0
                else:
                    ordiag=0
                    xrdiag=0
                if ordiag==5:
                    return -1.
                elif xrdiag==5:
                    return 1.
                i+=1
                j+=1
        for i,j in ldiag:
            oldiag=0
            xldiag=0
            while i<self.board_size and j>3:
                if self.board[i][j]==1:
                    xldiag+=1
                    oldiag=0
                elif self.board[i][j]==-1:
                    oldiag+=1
                    xldiag=0
                else:
                    oldiag=0
                    xldiag=0
                if oldiag==5:
                    return -1.
                elif xldiag==5:
                    return 1.
                i+=1
                j-=1
        if np.all(self.board != 0):
            return 0.
        else:
            return None
            
                

    def is_game_over(self):
        return self.game_result != None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board
        x_in_range = move.x_coordinate < self.board_size and move.x_coordinate >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = move.y_coordinate < self.board_size and move.y_coordinate >= 0
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.board + " is not legal")
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = GomokuGameState.o if self.next_to_move == GomokuGameState.x else GomokuGameState.x
        return GomokuGameState(new_board, next_to_move)

    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        return [GomokuMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]
