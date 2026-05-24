import tkinter as tk
from tkinter import messagebox
import math

class TicTacToeAI:

    def __init__(self, root):

        self.root = root

        self.root.title("Tic-Tac-Toe AI")
        self.root.geometry("430x600")

        self.root.configure(bg="#121826")
        self.root.resizable(False, False)

        self.board = [" " for _ in range(9)]

        self.buttons = []

        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self.create_ui()

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="TIC-TAC-TOE AI",
            font=("Arial", 26, "bold"),
            bg="#121826",
            fg="white"
        )

        title.pack(pady=15)

        subtitle = tk.Label(
            self.root,
            text="Play Against Unbeatable AI",
            font=("Arial", 12),
            bg="#121826",
            fg="#9ca3af"
        )

        subtitle.pack()

        score_frame = tk.Frame(
            self.root,
            bg="#1f2937",
            padx=15,
            pady=10
        )

        score_frame.pack(pady=20)

        self.player_label = tk.Label(
            score_frame,
            text="Player: 0",
            font=("Arial", 14, "bold"),
            bg="#1f2937",
            fg="#74b9ff"
        )

        self.player_label.grid(row=0, column=0, padx=15)

        self.ai_label = tk.Label(
            score_frame,
            text="AI: 0",
            font=("Arial", 14, "bold"),
            bg="#1f2937",
            fg="#ff7675"
        )

        self.ai_label.grid(row=0, column=1, padx=15)

        self.draw_label = tk.Label(
            score_frame,
            text="Draw: 0",
            font=("Arial", 14, "bold"),
            bg="#1f2937",
            fg="#55efc4"
        )

        self.draw_label.grid(row=0, column=2, padx=15)

        board_frame = tk.Frame(
            self.root,
            bg="#121826"
        )

        board_frame.pack(pady=10)

        for i in range(9):

            button = tk.Button(
                board_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=5,
                height=2,
                bg="#1f2937",
                fg="white",
                activebackground="#374151",
                relief="flat",
                bd=0,
                command=lambda i=i: self.human_move(i)
            )

            button.grid(
                row=i // 3,
                column=i % 3,
                padx=8,
                pady=8
            )

            self.buttons.append(button)

        self.status_label = tk.Label(
            self.root,
            text="Your Turn (X)",
            font=("Arial", 15, "bold"),
            bg="#121826",
            fg="#55efc4"
        )

        self.status_label.pack(pady=20)

        button_frame = tk.Frame(
            self.root,
            bg="#121826"
        )

        button_frame.pack(pady=10)

        restart_btn = tk.Button(
            button_frame,
            text="Restart",
            font=("Arial", 13, "bold"),
            bg="#00b894",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.restart_game
        )

        restart_btn.grid(row=0, column=0, padx=10)

        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 13, "bold"),
            bg="#d63031",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.root.quit
        )

        exit_btn.grid(row=0, column=1, padx=10)

    def human_move(self, index):

        if self.board[index] == " ":

            self.board[index] = "X"

            self.buttons[index].config(
                text="X",
                fg="#74b9ff"
            )

            if self.check_winner("X"):

                self.player_score += 1

                self.update_scoreboard()

                self.show_result("You Win 🎉")

                return

            if self.is_draw():

                self.draw_score += 1

                self.update_scoreboard()

                self.show_result("It's a Draw 🤝")

                return

            self.status_label.config(text="AI Thinking...")

            self.root.after(50, self.ai_move)

    def ai_move(self):

        best_score = -math.inf
        best_move = None

        if self.board[4] == " ":
            best_move = 4

        else:

            for move in self.available_moves():

                self.board[move] = "O"

                score = self.minimax(
                    0,
                    False,
                    -math.inf,
                    math.inf
                )

                self.board[move] = " "

                if score > best_score:

                    best_score = score
                    best_move = move

        self.board[best_move] = "O"

        self.buttons[best_move].config(
            text="O",
            fg="#ff7675"
        )

        if self.check_winner("O"):

            self.ai_score += 1

            self.update_scoreboard()

            self.show_result("AI Wins 😎")

            return

        if self.is_draw():

            self.draw_score += 1

            self.update_scoreboard()

            self.show_result("It's a Draw 🤝")

            return

        self.status_label.config(text="Your Turn (X)")

    def minimax(self, depth, is_maximizing, alpha, beta):

        if self.check_winner("O"):
            return 10 - depth

        if self.check_winner("X"):
            return depth - 10

        if self.is_draw():
            return 0

        if is_maximizing:

            best_score = -math.inf

            for move in self.available_moves():

                self.board[move] = "O"

                score = self.minimax(
                    depth + 1,
                    False,
                    alpha,
                    beta
                )

                self.board[move] = " "

                best_score = max(best_score, score)

                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            return best_score

        else:

            best_score = math.inf

            for move in self.available_moves():

                self.board[move] = "X"

                score = self.minimax(
                    depth + 1,
                    True,
                    alpha,
                    beta
                )

                self.board[move] = " "

                best_score = min(best_score, score)

                beta = min(beta, best_score)

                if beta <= alpha:
                    break

            return best_score

    def available_moves(self):

        return [
            i for i, spot in enumerate(self.board)
            if spot == " "
        ]

    def check_winner(self, player):

        winning_combinations = [

            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],

            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],

            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in winning_combinations:

            if all(
                self.board[i] == player
                for i in combo
            ):

                return True

        return False

    def is_draw(self):

        return " " not in self.board

    def show_result(self, message):

        self.status_label.config(text=message)

        messagebox.showinfo(
            "Game Over",
            message
        )

    def update_scoreboard(self):

        self.player_label.config(
            text=f"Player: {self.player_score}"
        )

        self.ai_label.config(
            text=f"AI: {self.ai_score}"
        )

        self.draw_label.config(
            text=f"Draw: {self.draw_score}"
        )

    def restart_game(self):

        self.board = [" " for _ in range(9)]

        for button in self.buttons:

            button.config(text="")

        self.status_label.config(
            text="Your Turn (X)"
        )

root = tk.Tk()

app = TicTacToeAI(root)

root.mainloop()