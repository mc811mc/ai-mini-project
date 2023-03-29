from game import *


moves = [0, 1, 2, 3]
depth = 3


def get_move(board):
    """
    Returns the expectimax action using self.depth and self.evaluationFunction

    All ghosts should be modeled as choosing uniformly at random from their
    legal moves.
    """
    max_depth = depth * 3  # 1 max layer (player), 2 expect layers (2 or 4 and placement)
    val, move = max_value(board, 1, max_depth)
    return move


def max_value(board, current_depth, max_depth):
    if game_state(board) == 'lose':
        return -999999, None
    elif current_depth > max_depth:
        return evaluation_function(board), None
    value = -999999999
    best_move = None
    for move in moves:
        new_board = perform_move(board, move)[0]
        if np.array_equal(board, new_board):  # don't consider a move that does nothing
            continue
        else:
            new_value, _ = expect_value(new_board, current_depth + 1, max_depth)
            if new_value > value:
                value, best_move = new_value, move
    return value, best_move


def expect_value(board, current_depth, max_depth):
    empty_cells = get_empty_cells(board)
    expected_value = 0
    chance = 1 / len(empty_cells)
    for cell in empty_cells:
        new_value, _ = expect_value2(board, cell, current_depth + 1, max_depth)
        expected_value += (chance * new_value)
    return expected_value, None


def expect_value2(board, cell, current_depth, max_depth):
    expected_value = 0
    # 90% chance of 2
    board[cell[0]][cell[1]] = 2
    new_value, _ = max_value(board, current_depth + 1, max_depth)
    expected_value += (.9 * new_value)
    # 10% chance of 4
    board[cell[0]][cell[1]] = 4
    new_value, _ = max_value(board, current_depth + 1, max_depth)
    expected_value += (.1 * new_value)
    return expected_value, None


def evaluation_function(board):
    num_empty = len(get_empty_cells(board))

    merges = 0
    # check available merges in columns
    for i in range(len(board)):
        prev = None
        for j in range(len(board[i])):
            if board[i][j] != 0:
                if board[i][j] == prev:
                    merges += 1
                prev = board[i][j]
    # check available merges in rows
    for j in range(len(board[0])):
        prev = None
        for i in range(len(board)):
            if board[i][j] != 0:
                if board[i][j] == prev:
                    merges += 1
                prev = board[i][j]

    left_monotonicity = 0
    right_monotonicity = 0
    for i in range(len(board)):
        for j in range(1, len(board[i])):
            if board[i][j - 1] > board[i][j]:
                left_monotonicity += board[i][j - 1] - board[i][j]
            else:
                right_monotonicity += board[i][j] - board[i][j - 1]
    if left_monotonicity < right_monotonicity:
        horizontal_monotonicity = left_monotonicity
    else:
        horizontal_monotonicity = right_monotonicity
    up_monotonicity = 0
    down_monotonicity = 0
    for j in range(len(board)):
        for i in range(1, len(board[i])):
            if board[i - 1][j] > board[i][j]:
                up_monotonicity += board[i - 1][j] - board[i][j]
            else:
                down_monotonicity += board[i][j] - board[i - 1][j]
    if up_monotonicity < down_monotonicity:
        vertical_monotonicity = up_monotonicity
    else:
        vertical_monotonicity = down_monotonicity

    # try raising monotonicities to a power to add more weight to larger cells
    return (300 * num_empty) + (700 * merges) - (50 * horizontal_monotonicity + vertical_monotonicity)


def main():
    iterations = 10
    scores = np.zeros(iterations)
    for i in range(iterations):
        board = new_game(4)
        board = add_two(board)
        board = add_two(board)
        lost = False
        print(board)
        print()
        while not lost:
            board, new_score = perform_move(board, get_move(board))
            scores[i] += new_score
            board = add_two(board)
            print(np.array(board))
            print()
            if game_state(board) == 'lose':
                print(np.array(board))
                print()
                print(f"Game {i} score: {scores[i]}")
                print()
                lost = True
    print(f'Average score: {scores.mean()}')


if __name__ == "__main__":
    main()
