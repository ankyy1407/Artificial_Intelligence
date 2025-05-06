import numpy as np
import random

class MinimaxAI:
    def __init__(self):
        self.max_depth = 9  # Maximum depth for minimax search
        
    def get_best_move(self, board):
        best_score = float('-inf')
        best_moves = []
        
        # Get all available moves
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]
        
        # Try each available move
        for move in available_moves:
            row, col = move
            board[row][col] = -1  # Make move for AI
            score = self.minimax(board, 0, float('-inf'), float('inf'), False)
            board[row][col] = 0  # Undo move
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        # If multiple best moves, choose randomly among them
        return random.choice(best_moves)
    
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        # Check for terminal states
        winner = self.check_winner(board)
        if winner is not None:
            return self.evaluate_winner(winner)
        
        if depth >= self.max_depth:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = -1
                        score = self.minimax(board, depth + 1, alpha, beta, False)
                        board[i][j] = 0
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, depth + 1, alpha, beta, True)
                        board[i][j] = 0
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
    
    def check_winner(self, board):
        # Check rows, columns and diagonals
        for i in range(3):
            if abs(sum(board[i, :])) == 3:  # Check rows
                return board[i][0]
            if abs(sum(board[:, i])) == 3:  # Check columns
                return board[0][i]
        
        # Check diagonals
        if abs(sum(np.diag(board))) == 3:
            return board[0][0]
        if abs(sum(np.diag(np.fliplr(board)))) == 3:
            return board[0][2]
        
        # Check for draw
        if 0 not in board:
            return 0
        
        return None
    
    def evaluate_winner(self, winner):
        if winner == -1:  # AI wins
            return 1
        elif winner == 1:  # Human wins
            return -1
        else:  # Draw
            return 0 