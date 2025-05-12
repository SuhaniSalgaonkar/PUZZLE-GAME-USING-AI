from heapq import heappush, heappop
from puzzle import Puzzle

def manhattan_distance(board, size):
    distance = 0
    for index, value in enumerate(board):
        if value == 0:
            continue
        target_x, target_y = divmod(value, size)
        current_x, current_y = divmod(index, size)
        distance += abs(target_x - current_x) + abs(target_y - current_y)
    return distance

def a_star_solver(start_board):
    size = int(len(start_board) ** 0.5)
    start_puzzle = Puzzle(size, start_board)
    if start_puzzle.is_solved():
        return []

    frontier = []
    counter = 0  # Unique sequence count
    visited = set()

    # Push with a counter to avoid comparing Puzzle objects
    cost = manhattan_distance(start_puzzle.board, size)
    heappush(frontier, (cost, counter, start_puzzle, []))

    while frontier:
        _, _, current_puzzle, path = heappop(frontier)
        board_tuple = tuple(current_puzzle.board)

        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        if current_puzzle.is_solved():
            return path

        for move in current_puzzle.get_possible_moves():
            neighbor = current_puzzle.apply_move(move)
            if tuple(neighbor.board) in visited:
                continue
            new_path = path + [move]
            cost = len(new_path) + manhattan_distance(neighbor.board, size)
            counter += 1
            heappush(frontier, (cost, counter, neighbor, new_path))

    return []
