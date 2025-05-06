import tkinter as tk
from tkinter import messagebox
import numpy as np
from minimax import MinimaxAI

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.configure(bg='#f0f0f0')
        
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 for human (X), -1 for AI (O)
        self.ai = MinimaxAI()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Create game title
        title = tk.Label(
            self.window,
            text="Tic Tac Toe",
            font=('Helvetica', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Create status label
        self.status_label = tk.Label(
            self.window,
            text="Your turn (X)",
            font=('Helvetica', 12),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.status_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Create game board
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.window,
                    text="",
                    font=('Helvetica', 20, 'bold'),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                    bg='#ffffff',
                    activebackground='#e6e6e6'
                )
                self.buttons[i][j].grid(row=i+2, column=j, padx=5, pady=5)
        
        # Create reset button
        reset_button = tk.Button(
            self.window,
            text="New Game",
            font=('Helvetica', 12),
            command=self.reset_game,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049'
        )
        reset_button.grid(row=5, column=0, columnspan=3, pady=10)
        
    def make_move(self, row, col):
        if self.board[row][col] == 0 and self.current_player == 1:
            # Human's move
            self.board[row][col] = 1
            self.buttons[row][col].config(text="X", fg='#2196F3')
            
            if self.check_winner() is None:
                self.current_player *= -1
                self.status_label.config(text="AI's turn (O)")
                self.window.update()
                self.window.after(500, self.ai_move)
            else:
                self.end_game()
    
    def ai_move(self):
        if self.current_player == -1:
            row, col = self.ai.get_best_move(self.board)
            self.board[row][col] = -1
            self.buttons[row][col].config(text="O", fg='#F44336')
            
            if self.check_winner() is None:
                self.current_player *= -1
                self.status_label.config(text="Your turn (X)")
            else:
                self.end_game()
    
    def check_winner(self):
        # Check rows, columns and diagonals
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3:  # Check rows
                return self.board[i][0]
            if abs(sum(self.board[:, i])) == 3:  # Check columns
                return self.board[0][i]
        
        # Check diagonals
        if abs(sum(np.diag(self.board))) == 3:
            return self.board[0][0]
        if abs(sum(np.diag(np.fliplr(self.board)))) == 3:
            return self.board[0][2]
        
        # Check for draw
        if 0 not in self.board:
            return 0
        
        return None
    
    def end_game(self):
        winner = self.check_winner()
        if winner == 1:
            messagebox.showinfo("Game Over", "Congratulations! You won!")
        elif winner == -1:
            messagebox.showinfo("Game Over", "AI wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")
        self.reset_game()
    
    def reset_game(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.status_label.config(text="Your turn (X)")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run() 