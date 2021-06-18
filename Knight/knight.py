import numpy as np


#騎士旅程
class knightMove(object):
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate    #x坐標
        self.y_coordinate = y_coordinate    #y坐標
        self.value = value                  #第幾步

    #印出坐標及步數
    def __repr__(self):
        return "x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate) + " v:" + str(self.value)



class knightGameState(object):
    dy=np.array([-2,-1,1,2,2,1,-1,-2])
    dx=np.array([1,2,2,1,-1,-2,-2,-1])
    cbx=8
    cby=8
    def __init__(self, state,next_to_move=1):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        
        now=np.where(self.board==np.max(self.board))
        l=0
        for i in range(8):
            ny=now[0]+knightGameState.dy[i]
            nx=now[1]+knightGameState.dx[i]
            if nx>= 0 and nx < 8 and ny >= 0 and ny < 8:
                if self.board[ny,nx]==0:
                    l+=1
            
        if l==0:
            if np.max(self.board)==64:
                #print(1)
                return 1
            else:
                #print(0)
                return 0
        else :
            return None
                

    def is_game_over(self):
        return self.game_result != None

    def is_move_legal(self, move):
        # check if inside the board
        x_in_range = move.x_coordinate < self.board_size and move.x_coordinate >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = move.y_coordinate < self.board_size and move.y_coordinate >= 0
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.board[move.y_coordinate, move.x_coordinate] == 0

    def move(self, move):
        
        if not self.is_move_legal(move):
            raise ValueError(" is not legal")
        new_board = np.copy(self.board)
        new_board[move.y_coordinate, move.x_coordinate] = self.next_to_move
        next_to_move = self.next_to_move+1
        return knightGameState(new_board, next_to_move)

    def get_legal_actions(self):
        now=np.where(self.board==np.max(self.board))
        ok_moves=[]
        for i in range(8):
            ny=now[0]+knightGameState.dy[i]
            nx=now[1]+knightGameState.dx[i]
            if nx>= 0 and nx < 8 and ny >= 0 and ny < 8:
                if self.board[ny,nx]==0:
                    ok_moves.append([nx,ny])
            
        return [knightMove(coords[0], coords[1], self.next_to_move) for coords in ok_moves]
