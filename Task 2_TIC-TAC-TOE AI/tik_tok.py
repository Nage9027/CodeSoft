def minimax(board, depth, isMaximizingPlayer):
    """
    Minimax algorithm to find the best move for a Tic-Tac-Toe game.

    Args:
        board: The current state of the board.
        depth: The current depth in the search tree.
        isMaximizingPlayer: Whether it's the maximizing player's turn.

    Returns:
        The best move (row, col) and its score.
    """

    # Check if the game has ended
    winner = check_winner(board)
    if winner:
        return None, winner if winner == 'X' else -winner

    # If it's the maximizing player's turn, find the maximum score
    if isMaximizingPlayer:
        bestVal = -float('inf')
        bestMove = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'X'
                    moveVal, _ = minimax(board, depth + 1, False)
                    board[i][j] = '-'
                    if moveVal > bestVal:
                        bestVal = moveVal
                        bestMove = (i, j)
        return bestMove, bestVal

    # If it's the minimizing player's turn, find the minimum score
    else:
        bestVal = float('inf')
        bestMove = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'O'
                    moveVal, _ = minimax(board, depth + 1, True)
                    board[i][j] = '-'
                    if moveVal < bestVal:
                        bestVal = moveVal
                        bestMove = (i, j)
        return bestMove, bestVal