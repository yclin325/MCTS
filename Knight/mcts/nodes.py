import numpy as np
from collections import defaultdict
from knight import *

class MonteCarloTreeSearchNode(object):
    def __init__(self, state: knightGameState, parent=None):
        self._number_of_visits = 0.              #訪問次數
        self._results = defaultdict(int)         #紀錄輸贏次數
        self.state = state
        self.parent = parent                     #此節點的父節點(上一個節點)
        self.children = []                       #記錄此節點的子節點

    @property
    #未嘗試過的動作
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    
    #勝利次數
    def q(self):
        wins = self._results[1]
        #wins = self._results[self.parent.state.next_to_move]
        #loses = self._results[-1 * self.parent.state.next_to_move]
        return wins

    @property
    #訪問次數
    def n(self):
        return self._number_of_visits

    #擴展子節點
    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    #是否是最後節點(遊戲是否結束)
    def is_terminal_node(self):
        return self.state.is_game_over()

    #模擬
    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    #更新
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    #是否完全擴展
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    #最佳子節點
    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]
    
    #
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
