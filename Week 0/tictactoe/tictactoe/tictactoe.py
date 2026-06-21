"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #evaulates turn numbers to determine which player's turn it is
    #if there are an equal number of X's and O's, it's X's turn, otherwise it's O's turn
    x_count=0
    o_count=0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    if x_count == o_count:
        return X
    else:
        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #iterates through the board and decides which cells are empty, then adds those cells to a set of possible actions
    possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")

    import copy
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board    
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #We're NOT checking if all 3 rows are same ,checking each row individually in loop
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] != EMPTY:
            return board[0][j]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    
    # Check diagonal top-right to bottom-left
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    
    # No winner
    return None                
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    # If any empty cell exists, game still in progress after checking for winner
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    
    # No winner and no empty cells = tie = game over
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # X is maximizer
    if player(board) == X:
        best_score = -math.inf
        best_action = None
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
        return best_action
    
    # O is minimizer
    else:
        best_score = math.inf
        best_action = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action
        return best_action
        
    raise NotImplementedError
