from mcts.nodes import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    def best_action(self, simulations_number):          #輸入模擬次數，模擬完後尋找最佳動作
        for _ in range(0, simulations_number):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        return self.root.best_child(c_param=0.)

    def tree_policy(self):                             #若還沒擴展玩，則繼續擴展，若擴展完了，選擇最佳的子節點
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
