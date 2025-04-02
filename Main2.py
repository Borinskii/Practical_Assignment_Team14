import tkinter as tk
from Gui2 import GUI2
from GameStates import GameStates
from GameTree2new import *  # Node, ai_node_creation_minimax, ai_node_creation_alphabeta, player_node_creation
import random

def main():
    root = tk.Tk()
    gui = GUI2(root)

    gui.setTurnInProgress(False)
    gui.replay_requested = False
    start_game(gui, root)
    gui.displayStartScreen()
    wait_for_user_config(gui, root)
    root.mainloop()

def wait_for_user_config(gui, root):
    if not gui.getHasChosen():
        root.after(500, wait_for_user_config, gui, root)
    else:
        global l
        l = 2
        length, first_turn, algo = gui.getGameInfo()
        binary_string = ''.join(random.choice('01') for _ in range(length))
        game = GameStates()
        game.add_node(Node("A1", binary_string, 0, 0, 1))
        run_game_loop(gui, root, game, first_turn, algo, first_turn == 0)

def run_game_loop(gui, root, game, turn, algo, player_is_maximizer):
    current_node = game.get_last_node()
    if getattr(gui, "turn_in_progress", False):
        return  # Avoid overlapping turns

    gui.turn_in_progress = True  # Lock turn
    current_node = game.get_last_node()


    if len(current_node.string) == 1:
        gui.displayEndScreen(current_node.p1, current_node.p2, lambda: start_game(gui, root))
        return

    gui.displayGameScreen(current_node.string, current_node.p1, current_node.p2, turn)

    if turn == 0:
        wait_for_player_move(gui, root, game, turn, algo, player_is_maximizer)
    else:
        root.after(1000, lambda: handle_ai_turn(gui, root, game, turn, algo, player_is_maximizer))

def wait_for_player_move(gui, root, game, turn, algo, player_is_maximizer):
    if not gui.getHasPlayed():
        root.after(500, wait_for_player_move, gui, root, game, turn, algo, player_is_maximizer)
        return
    else:
        index = gui.getIndex()
        try:
            player_node_creation(game, index, player_is_maximizer)
        except ValueError as ve:
            from tkinter import messagebox
            if not gui.getInvalidMoveShown():
                gui.setInvalidMoveShown(True)
                messagebox.showerror("Incorrect Move", str(ve))
            gui.setHasPlayed(False)
            root.after(100, wait_for_player_move, gui, root, game, turn, algo, player_is_maximizer)
            return

        gui.setInvalidMoveShown(False)  #reset on success
        gui.setHasPlayed(False)
        gui.turn_in_progress = False
        run_game_loop(gui, root, game, 1, algo, player_is_maximizer)

def handle_ai_turn(gui, root, game, turn, algo, player_is_maximizer):
    if algo == 0:
        _, _ = ai_node_creation_minimax(game, player_is_maximizer)
    else:
        _, _ = ai_node_creation_alphabeta(game, player_is_maximizer)
    gui.turn_in_progress = False  # Unlock turn for not increasing string
    run_game_loop(gui, root, game, 0, algo, player_is_maximizer)

def start_game(gui, root):
    gui.__init__(root)
    gui.displayStartScreen()

    def wait_for_config():
        if not gui.getHasChosen():
            root.after(500, wait_for_config)
        else:
            global l
            l = 2
            length, first_turn, algo = gui.getGameInfo()
            binary_string = ''.join(random.choice('01') for _ in range(length))
            game = GameStates()
            game.add_node(Node("A1", binary_string, 0, 0, 1))
            run_game_loop(gui, root, game, first_turn, algo, first_turn == 0)

    root.after(100, wait_for_config)

if __name__ == '__main__':
    main()
