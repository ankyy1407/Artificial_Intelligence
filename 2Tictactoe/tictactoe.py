import numpy as np
from minimax import MinimaxAI

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 for human (X), -1 for AI (O)
        self.ai = MinimaxAI()
        
    def print_board(self):
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        print("\n")
        for i in range(3):
            print("-------------")
            for j in range(3):
                print(f"| {symbols[self.board[i][j]]} ", end="")
            print("|")
        print("-------------")
        
    def make_move(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            return True
        return False
    
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
    
    def play_game(self):
        print("Welcome to Tic Tac Toe!")
        print("You are X, AI is O")
        print("Enter moves as row,col (0-2)")
        
        while True:
            self.print_board()
            
            if self.current_player == 1:  # Human's turn
                while True:
                    try:
                        move = input("Enter your move (row,col): ")
                        row, col = map(int, move.split(','))
                        if 0 <= row <= 2 and 0 <= col <= 2:
                            if self.make_move(row, col):
                                break
                            else:
                                print("That position is already taken!")
                        else:
                            print("Invalid position! Use numbers between 0 and 2.")
                    except ValueError:
                        print("Invalid input! Use format: row,col")
            else:  # AI's turn
                print("AI is thinking...")
                row, col = self.ai.get_best_move(self.board)
                self.make_move(row, col)
                print(f"AI plays at position ({row}, {col})")
            
            winner = self.check_winner()
            if winner is not None:
                self.print_board()
                if winner == 1:
                    print("Congratulations! You won!")
                elif winner == -1:
                    print("AI wins!")
                else:
                    print("It's a draw!")
                break
            
            self.current_player *= -1  # Switch player

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game() 