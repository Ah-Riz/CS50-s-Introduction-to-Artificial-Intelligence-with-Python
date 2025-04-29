"""
Tic Tac Toe Player
"""

import math
import copy

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
    if terminal(board):
        return None
    
    X_count = 0
    O_count = 0
    E_count = 0

    for i in board:
        for j in i:
            if j == X:
                X_count += 1
            elif j == O:
                O_count += 1
            elif j == EMPTY:
                E_count += 1
    
    if E_count > 0:
        if X_count > O_count:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board):
        return None
    
    possible_actions = set()

    for i_index, i in enumerate(board):
        for j_index, j in enumerate(i):
            if j == EMPTY:
                possible_actions.add((i_index, j_index))
    
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    board_copy = copy.deepcopy(board)

    for selected in action:
        if selected > 2 or selected < 0:
            raise ValueError("Invalid action")
    
    if board_copy[action[0]][action[1]] == EMPTY:
        board_copy[action[0]][action[1]] = current_player
    else:
        raise ValueError("Invalid action")
    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        #check vertical
        if (board[i][0] == board[i][1] == board[i][2]) and board[i][0] != EMPTY:
            return board[i][0]
        #check horizontal
        if (board[0][i] == board[1][i] == board[2][i]) and board[0][i] != EMPTY:
            return board[0][i]
    #check diagonal \
    if (board[0][0] == board[1][1] == board[2][2]) and board[0][0] != EMPTY:
        return board[0][0]
    #check diagonal /
    if (board[0][2] == board[1][1] == board[2][0]) and board[0][2] != EMPTY:
        return board[0][2]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    result = winner(board)

    if result is not None:
        return True
    
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)

    if terminal(board):
        return None

    if current_player == X:
        _, optimal_action = max_value(board, -math.inf, math.inf)
    else:
        _, optimal_action = min_value(board, -math.inf, math.inf)

    return optimal_action

def max_value(board, alpha, beta):
    """
    Returns the maximum utility value and the corresponding action for the maximizer.
    """
    if terminal(board):
        return utility(board), None

    best_score = -math.inf
    best_action = None

    for action in actions(board):
        score, _ = min_value(result(board, action), alpha, beta)
        if score > best_score:
            best_score = score
            best_action = action
        alpha = max(alpha, best_score)
        if beta <= alpha:
            break  # Prune the branch

    return best_score, best_action

def min_value(board, alpha, beta):
    """
    Returns the minimum utility value and the corresponding action for the minimizer.
    """
    if terminal(board):
        return utility(board), None

    best_score = math.inf
    best_action = None

    for action in actions(board):
        score, _ = max_value(result(board, action), alpha, beta)
        if score < best_score:
            best_score = score
            best_action = action
        beta = min(beta, best_score)
        if beta <= alpha:
            break  # Prune the branch

    return best_score, best_action