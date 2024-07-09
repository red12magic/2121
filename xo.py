import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def set_name(self, name):
        self.name = name

    def set_symbol(self, symbol):
        self.symbol = symbol.upper()

class Menu:
    def __init__(self, root, start_game_callback, quit_game_callback):
        self.root = root
        self.start_game_callback = start_game_callback
        self.quit_game_callback = quit_game_callback
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        self.root.title("X-O Game")
        tk.Label(self.root, text="Welcome to my X-O game!").pack()
        tk.Button(self.root, text="Start Game", command=self.start_game_callback).pack()
        tk.Button(self.root, text="Quit Game", command=self.quit_game_callback).pack()

    def create_endgame_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Game Over!").pack()
        tk.Button(self.root, text="Restart Game", command=self.start_game_callback).pack()
        tk.Button(self.root, text="Quit Game", command=self.quit_game_callback).pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class Board:
    def __init__(self, root, make_move_callback):
        self.root = root
        self.make_move_callback = make_move_callback
        self.board = [str(i) for i in range(1, 10)]
        self.buttons = []

    def create_board(self):
        self.clear_board()
        for i in range(9):
            button = tk.Button(self.root, text=self.board[i], width=10, height=3,
                               command=lambda i=i: self.make_move_callback(i + 1))
            self.buttons.append(button)
            button.grid(row=i // 3, column=i % 3)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            self.buttons[choice - 1].config(text=symbol, state=tk.DISABLED)
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]
        self.create_board()

    def clear_board(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []

    def check_win(self, symbol):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if all(self.board[i] == symbol for i in condition):
                return True
        return False

    def is_draw(self):
        return all(not cell.isdigit() for cell in self.board)

class Game:
    def __init__(self, root):
        self.root = root
        self.players = [Player(), Player()]
        self.board = Board(root, self.make_move)
        self.menu = Menu(root, self.setup_players, self.quit_game)
        self.current_player_index = 0

    def setup_players(self):
        self.menu.clear_window()
        for number, player in enumerate(self.players, start=1):
            name = self.get_input(f"Player {number}, enter your name (letters only): ")
            while not name.isalpha():
                name = self.get_input(f"Invalid name. Player {number}, enter your name (letters only): ")
            player.set_name(name)

            symbol = self.get_input(f"{player.name}, choose your symbol (a single letter): ")
            while not (symbol.isalpha() and len(symbol) == 1):
                symbol = self.get_input(f"Invalid symbol. {player.name}, choose your symbol (a single letter): ")
            player.set_symbol(symbol)
        
        self.play_game()

    def get_input(self, prompt):
        result = tk.simpledialog.askstring("Input", prompt)
        return result if result else ""

    def play_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.game_loop()

    def game_loop(self):
        if not self.board.is_draw() and not self.board.check_win(self.players[self.current_player_index].symbol):
            self.current_player = self.players[self.current_player_index]
        else:
            self.end_game()

    def make_move(self, choice):
        if self.board.update_board(choice, self.current_player.symbol):
            if self.board.check_win(self.current_player.symbol):
                messagebox.showinfo("Game Over", f"Congratulations, {self.current_player.name}! You win!")
                self.menu.create_endgame_menu()
            elif self.board.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.menu.create_endgame_menu()
            else:
                self.current_player_index = 1 - self.current_player_index
                self.game_loop()

    def end_game(self):
        self.menu.create_endgame_menu()

    def quit_game(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
