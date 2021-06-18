import numpy as np
from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from knight import *
from IPython.display import clear_output


def graphics(board):
    for i in range(8):
        for j in range(8):
            print('%2d'%c_board[j,i],end='')
        print()



def judge(state):
    if state.is_game_over():
        print('over')
        return 1
    else:
        return -1


state=np.zeros((8,8))
#a[3,4]=1
c_state= knightGameState(state, 1)
c_board = state
move1 = knightMove(0,0,1)
c_state = c_state.move(move1)
c_board = c_state.board
print('step = ',1)

i=2
while True:
    clear_output(wait=True)
    print('step = ',i)
    board_state = knightGameState(state=c_board, next_to_move=i)
    root = MonteCarloTreeSearchNode(state=board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(100000)
    c_state = best_node.state
    c_board = c_state.board
    i+=1
    
    #graphics(c_board)
    if judge(c_state)==1:
        graphics(c_board)
        break
    elif judge(c_state)==-1:
        continue
    