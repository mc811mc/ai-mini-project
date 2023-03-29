from game import *

moves = [0, 1, 2, 3]


def get_move():
    return random.choice(moves)


def main():
    iterations = 1000
    scores = np.zeros(iterations)
    for i in range(iterations):
        board = new_game(4)
        board = add_two(board)
        board = add_two(board)
        lost = False
        while not lost:
            board, new_score = perform_move(board, get_move())
            scores[i] += new_score
            board = add_two(board)
            if game_state(board) == 'lose':
                print(f"Game {i} score: {scores[i]}")
                lost = True
    print(f'Average score: {scores.mean()}')


if __name__ == "__main__":
    main()
