class GameStates:
    def __init__(self):
        self.states = []
        self.current_state = None
    def add_node(self, node):
        self.states.append(node)
        self.current_state = node
    def get_last_node(self):
        return self.current_state
    #this is only to show node to user
    def show_last_node(self):
        return self.current_state.get_node()
    #this is only to show game states to user
    def show_states(self):
        return [node.get_node() for node in self.states]