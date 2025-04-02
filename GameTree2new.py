import random
from GameStates import GameStates
import time
l = 2
# A class that represents a single Node in the game tree
class Node:
    def __init__(self, id, string, p1, p2, level):
        self.id = id
        self.string = string
        self.p1 = p1
        self.p2 = p2
        self.level = level
        self.heuristic_value = None

    def get_node(self):
        return self.id, self.string, self.p1, self.p2, self.level, self.heuristic_value


# A class that represents a game tree
class Game_Tree:
    def __init__(self):
        self.set_of_nodes = []
        self.set_of_arcs = dict()

    def adding_node(self, Node):
        self.set_of_nodes.append(Node)

    def adding_arcs(self, initial_node_id, end_node_id):
        self.set_of_arcs[initial_node_id] = self.set_of_arcs.get(initial_node_id, []) + [end_node_id]


def is_identical(current_node):
    cur_id = current_node.id
    cur_string = current_node.string
    cur_p1 = current_node.p1
    cur_p2 = current_node.p2
    cur_level = current_node.level
    for el in gt.set_of_nodes:
        if cur_string == el.string and cur_p1 == el.p1 and cur_p2 == el.p2 and cur_level == el.level:
            return True, el.id
    return False, cur_id


def move_checking(nodes_generated, current_node, depth=0):
    global j
    string = list(current_node[1])
    for i in range(len(string) - 1):
        p1_new = current_node[2]
        p2_new = current_node[3]
        pair = string[i] + string[i + 1]
        new_string = string[:i] + string[i + 2:]
        if pair == "00":
            p1_new += 1
            new_string.insert(i, "1")
        elif pair == "01":
            p2_new += 1
            new_string.insert(i, "0")
        elif pair == "10":
            p2_new -= 1
            new_string.insert(i, "1")
        elif pair == "11":
            p1_new += 1
            new_string.insert(i, "0")
        level_new = current_node[4] + 1
        id_new = 'A' + str(j)
        j += 1
        new_node = Node(id_new, "".join(new_string), p1_new, p2_new, level_new)
        identical, check_id = is_identical(new_node)
        if identical:
            j -= 1
            gt.adding_arcs(current_node[0], check_id)
        else:
            nodes_generated.append([id_new, "".join(new_string), p1_new, p2_new, level_new])
            gt.adding_node(new_node)
            gt.adding_arcs(current_node[0], new_node.id)


def heuristic(node, turn, player_is_maximizer):
    s = node.string
    pair_values = {
        '00': 1,
        '01': -1,
        '10': 1,
        '11': 1
    }
    eval_score = 0
    for i in range(len(s) - 1):
        pair = s[i:i+2]
        eval_score += pair_values.get(pair, 0)
    if player_is_maximizer:
        return (node.p2 - node.p1) + turn * eval_score
    return (node.p1 - node.p2) + turn * eval_score


def generate_children(node, is_maximizing):
    children = []
    string = list(node.string)
    for i in range(len(string) - 1):
        p1_new = node.p1
        p2_new = node.p2
        pair = string[i] + string[i + 1]
        new_string = string[:i] + string[i + 2:]
        if pair == "00":
            if is_maximizing:
                p1_new += 1
            else:
                p2_new += 1
            new_string.insert(i, "1")
        elif pair == "01":
            if is_maximizing:
                p2_new += 1
            else:
                p1_new += 1
            new_string.insert(i, "0")
        elif pair == "10":
            if is_maximizing:
                p2_new -= 1
            else:
                p1_new -= 1
            new_string.insert(i, "1")
        elif pair == "11":
            if is_maximizing:
                p1_new += 1
            else:
                p2_new += 1
            new_string.insert(i, "0")
        child = Node("temp", "".join(new_string), p1_new, p2_new, node.level + 1)
        children.append(child)
    return children


def minimax(node, depth, is_maximizing, max_depth, player_is_maximizer):
    global nodes_visited
    nodes_visited += 1
    if depth == max_depth or len(node.string) == 1:
        turn = 1 if is_maximizing else -1
        return heuristic(node, turn, player_is_maximizer)
    children = generate_children(node, is_maximizing)
    if not children:
        return heuristic(node, 1 if is_maximizing else -1, player_is_maximizer)
    if is_maximizing:
        return max(minimax(child, depth + 1, False, max_depth, player_is_maximizer) for child in children)
    return min(minimax(child, depth + 1, True, max_depth, player_is_maximizer) for child in children)


def ai_node_creation_minimax(game_states, player_is_maximizer):
    global l
    possible_moves = []
    current_node = game_states.get_last_node()
    string = list(current_node.string)
    for i in range(len(string) - 1):
        p1_new = current_node.p1
        p2_new = current_node.p2
        pair = string[i] + string[i + 1]
        new_string = string[:i] + string[i + 2:]
        if pair == "00":
            if player_is_maximizer:
                p2_new += 1
                new_string.insert(i, "1")
            else:
                p1_new += 1
                new_string.insert(i, "1")
        elif pair == "01":
            if player_is_maximizer:
                p1_new += 1
                new_string.insert(i, "0")
            else:
                p2_new += 1
                new_string.insert(i, "0")
        elif pair == "10":
            if player_is_maximizer:
                p1_new -= 1
                new_string.insert(i, "1")
            else:
                p2_new -= 1
                new_string.insert(i, "1")
        elif pair == "11":
            if player_is_maximizer:
                p2_new += 1
                new_string.insert(i, "0")
            else:
                p1_new += 1
                new_string.insert(i, "0")
        id_new = 'A' + str(l)
        l += 1
        level_new = current_node.level + 1
        new_node = Node(id_new, "".join(new_string), p1_new, p2_new, level_new)
        possible_moves.append(new_node)
    chosen_node = ai_move_choosing_minimax(possible_moves, player_is_maximizer=player_is_maximizer)
    game_states.add_node(chosen_node)
    return possible_moves, chosen_node


def ai_move_choosing_minimax(possible_moves, max_depth=4, player_is_maximizer=True):
    best_score = float('-inf')
    best_nodes = []
    for node in possible_moves:
        score = minimax(node, 1, player_is_maximizer, max_depth, player_is_maximizer)
        node.heuristic_value = score
        if score > best_score:
            best_score = score
            best_nodes = [node]
        elif score == best_score:
            best_nodes.append(node)
    return random.choice(best_nodes)


def player_node_creation(game_states, i, player_is_maximizer):
    global l
    current_node = game_states.get_last_node()
    string = list(current_node.string)
    if i < 0 or i > len(string) - 2:
        raise ValueError(f"Invalid index: {i}. Must be between 0 and {len(string)-2}")
    p1_new = current_node.p1
    p2_new = current_node.p2
    pair = string[i] + string[i + 1]
    new_string = string[:i] + string[i + 2:]
    if pair == "00":
        if player_is_maximizer:
            p1_new += 1
            new_string.insert(i, "1")
        else:
            p2_new += 1
            new_string.insert(i, "1")
    elif pair == "01":
        if player_is_maximizer:
            p2_new += 1
            new_string.insert(i, "0")
        else:
            p1_new += 1
            new_string.insert(i, "0")
    elif pair == "10":
        if player_is_maximizer:
            p2_new -= 1
            new_string.insert(i, "1")
        else:
            p1_new -= 1
            new_string.insert(i, "1")
    elif pair == "11":
        if player_is_maximizer:
            p1_new += 1
            new_string.insert(i, "0")
        else:
            p2_new += 1
            new_string.insert(i, "0")
    id_new = 'A' + str(l)
    l += 1
    level_new = current_node.level + 1
    new_node = Node(id_new, "".join(new_string), p1_new, p2_new, level_new)
    game_states.add_node(new_node)
    return new_node


def alpha_beta(node, depth, alpha, beta, is_maximizing, max_depth, player_is_maximizer):
    global nodes_visited
    nodes_visited += 1
    if depth == max_depth or len(node.string) == 1:
        turn = 1 if is_maximizing else -1
        return heuristic(node, turn, player_is_maximizer)
    children = generate_children(node, is_maximizing)
    if not children:
        turn = 1 if is_maximizing else -1
        return heuristic(node, turn, player_is_maximizer)
    if is_maximizing:
        value = float('-inf')
        for child in children:
            value = max(value, alpha_beta(child, depth + 1, alpha, beta, False, max_depth, player_is_maximizer))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in children:
            value = min(value, alpha_beta(child, depth + 1, alpha, beta, True, max_depth, player_is_maximizer))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def ai_node_creation_alphabeta(game_states, player_is_maximizer, max_depth=4):
    global l
    possible_moves = []
    current_node = game_states.get_last_node()
    string = list(current_node.string)
    for i in range(len(string) - 1):
        p1_new = current_node.p1
        p2_new = current_node.p2
        pair = string[i] + string[i + 1]
        new_string = string[:i] + string[i + 2:]
        if pair == "00":
            if player_is_maximizer:
                p2_new += 1
                new_string.insert(i, "1")
            else:
                p1_new += 1
                new_string.insert(i, "1")
        elif pair == "01":
            if player_is_maximizer:
                p1_new += 1
                new_string.insert(i, "0")
            else:
                p2_new += 1
                new_string.insert(i, "0")
        elif pair == "10":
            if player_is_maximizer:
                p1_new -= 1
                new_string.insert(i, "1")
            else:
                p2_new -= 1
                new_string.insert(i, "1")
        elif pair == "11":
            if player_is_maximizer:
                p2_new += 1
                new_string.insert(i, "0")
            else:
                p1_new += 1
                new_string.insert(i, "0")
        id_new = 'A' + str(l)
        l += 1
        level_new = current_node.level + 1
        new_node = Node(id_new, "".join(new_string), p1_new, p2_new, level_new)
        possible_moves.append(new_node)
    best_score = float('-inf')
    best_nodes = []
    player_next_move_is_maximizing = player_is_maximizer
    for node in possible_moves:
        score = alpha_beta(node, 1, float('-inf'), float('inf'), player_next_move_is_maximizing, max_depth, player_is_maximizer)
        node.heuristic_value = score
        if score > best_score:
            best_score = score
            best_nodes = [node]
        elif score == best_score:
            best_nodes.append(node)
    chosen_node = random.choice(best_nodes)
    game_states.add_node(chosen_node)
    return possible_moves, chosen_node


gt = Game_Tree()
nodes_generated = []
j = 2
nodes_visited = 0
