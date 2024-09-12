import tkinter as tk
from tkinter import messagebox
import math

# Constants
EMPTY = ' '
HUMAN = 'X'
AI = 'O'

# The board
board = [EMPTY] * 9

# Winning combinations
win_combos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# Initialize the GUI
root = tk.Tk()
root.title("Tic-Tac-Toe AI")

buttons = [tk.Button(root, text=EMPTY, font=('Arial', 24), width=5, height=2, command=lambda i=i: on_button_click(i)) for i in range(9)]
for i, button in enumerate(buttons):
    row, col = divmod(i, 3)
    button.grid(row=row, column=col)

def print_board():
    for i in range(9):
        buttons[i].config(text=board[i])

def check_win(player):
    return any(all(board[i] == player for i in combo) for combo in win_combos)

def check_tie():
    return all(cell != EMPTY for cell in board)

def minimax(board, depth, is_maximizing):
    if check_win(AI):
        return 10 - depth
    if check_win(HUMAN):
        return depth - 10
    if check_tie():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, depth + 1, False)
                board[i] = EMPTY
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = EMPTY
                best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = AI
    print_board()
    if check_win(AI):
        messagebox.showinfo("Game Over", "AI wins!")
        reset_game()
    elif check_tie():
        messagebox.showinfo("Game Over", "It's a tie!")

def on_button_click(index):
    if board[index] == EMPTY:
        board[index] = HUMAN
        buttons[index].config(text=HUMAN)
        if check_win(HUMAN):
            messagebox.showinfo("Game Over", "You win!")
            reset_game()
        elif check_tie():
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            ai_move()

def reset_game():
    global board
    board = [EMPTY] * 9
    print_board()

# Start the GUI event loop
root.mainloop()
