import tkinter as tk
from tkinter import messagebox

class GUI2:
    def __init__(self, master):
        self.master = master
        self.master.title("Two person game")
        self.gameInfo = []
        self.hasChosen = False
        self.hasPlayed = False
        self.userIndex = None
        self.invalidMoveShown = False  #for preventing duplicate popups
        self.turn_in_progress = False

    def setTurnInProgress(self, val):
        self.turn_in_progress = val

    def getTurnInProgress(self):
        return self.turn_in_progress

    def setHasChosen(self, val):
        self.hasChosen = val

    def getHasChosen(self):
        return self.hasChosen

    def setHasPlayed(self, val):
        self.hasPlayed = val

    def getHasPlayed(self):
        return self.hasPlayed

    def getIndex(self):
        return self.userIndex

    def setIndex(self, index):
        self.userIndex = index

    def getGameInfo(self):
        return self.gameInfo

    def setGameInfo(self, info):
        self.gameInfo = info

    def setInvalidMoveShown(self, val):  #setter for popup control
        self.invalidMoveShown = val

    def getInvalidMoveShown(self):       #getter for popup control
        return self.invalidMoveShown

    def displayStartScreen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title = tk.Label(self.master, text="Two person game", font=("Verdana", 20))
        title.pack(pady=10)

        self.length_label = tk.Label(self.master, text="Choose String length (15-25):", font=("Verdana", 14))
        self.length_label.pack()
        self.length_spin = tk.Spinbox(self.master, from_=15, to=25, font=("Verdana", 14))
        self.length_spin.pack(pady=5)

        self.first_label = tk.Label(self.master, text="Who plays first?", font=("Verdana", 14))
        self.first_label.pack()
        self.first_choice = tk.IntVar(value=0)
        tk.Radiobutton(self.master, text="User", variable=self.first_choice, value=0, font=("Verdana", 12)).pack()
        tk.Radiobutton(self.master, text="AI", variable=self.first_choice, value=1, font=("Verdana", 12)).pack()

        self.algo_label = tk.Label(self.master, text="Choose AI Algorithm:", font=("Verdana", 14))
        self.algo_label.pack()
        self.algo_choice = tk.IntVar(value=0)
        tk.Radiobutton(self.master, text="Minimax", variable=self.algo_choice, value=0, font=("Verdana", 12)).pack()
        tk.Radiobutton(self.master, text="Alpha-Beta", variable=self.algo_choice, value=1, font=("Verdana", 12)).pack()

        tk.Button(self.master, text="Start Game", font=("Verdana", 14), command=self.startGame).pack(pady=20)

    def startGame(self):
        try:
            length = int(self.length_spin.get())
            if 15 <= length <= 25:
                first = self.first_choice.get()
                algo = self.algo_choice.get()
                self.setGameInfo([length, first, algo])
                self.setHasChosen(True)
            else:
                messagebox.showerror("Incorrect Input!", "Length must be between 15 and 25.")
                return
        except ValueError:
            messagebox.showerror("Incorrect Input!", "Please enter a number between 15 and 25.")
            return

    def displayGameScreen(self, string, p1_score, p2_score, turn):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Binary String: {string}", font=("Verdana", 16)).pack(pady=10)
        tk.Label(self.master, text=f"Scores: P1 = {p1_score} | P2 = {p2_score}", font=("Verdana", 14)).pack(pady=5)

        if turn == 0:
            tk.Label(self.master, text="Your Turn! Choose index:", font=("Verdana", 14)).pack()
            self.index_spin = tk.Spinbox(self.master, from_=0, to=len(string)-2, font=("Verdana", 14))
            self.index_spin.pack(pady=5)
            tk.Button(self.master, text="Play Turn", font=("Verdana", 14), command=self.playUserTurn).pack(pady=10)
        else:
            tk.Label(self.master, text="AI is making move...", font=("Verdana", 14)).pack(pady=20)

    def playUserTurn(self):
        index = int(self.index_spin.get())
        self.setIndex(index)
        self.setHasPlayed(True)

    def displayEndScreen(self, p1, p2, restart_callback=None,  player_is_maximizer=True):
        if player_is_maximizer:
            #Player is p1
            if p1 > p2:
                result = "You win!"
            elif p2 > p1:
                result = "AI wins!"
            else:
                result = "It's a draw!"
        else:
            # Player is p2
            if p2 > p1:
                result = "You win!"
            elif p1 > p2:
                result = "AI wins!"
            else:
                result = "It's a draw!"

        for widget in self.master.winfo_children():
            widget.destroy()

        #result = "It's a draw!"
        # if p1 > p2:
        #     result = "Player 1 (You) win!"
        # elif p2 > p1:
        #     result = "Player 2 (AI) wins!"

        tk.Label(self.master, text="Game Over", font=("Verdana", 20)).pack(pady=10)
        tk.Label(self.master, text=f"Final Score: P1 = {p1} | P2 = {p2}", font=("Verdana", 16)).pack(pady=5)
        tk.Label(self.master, text=result, font=("Verdana", 16)).pack(pady=10)

        if restart_callback:
            tk.Button(self.master, text="Play Again", font=("Verdana", 14), command=restart_callback).pack(pady=20)
        else:
            tk.Button(self.master, text="Play Again", font=("Verdana", 14), command=self.displayStartScreen).pack(pady=20)
