class Puzzle:
    def __init__(self, size, board=None):
        self.size = size
        if board:
            self.board = board[:]
        else:
            self.board = list(range(size * size))
        self.blank = self.board.index(0)

    def clone(self):
        return Puzzle(self.size, self.board)

    def is_solved(self):
        return self.board == list(range(1, self.size * self.size)) + [0]

    def move(self, direction):
        row, col = divmod(self.board.index(0), self.size)
        new_row, new_col = row, col

        if direction == "up": new_row -= 1
        elif direction == "down": new_row += 1
        elif direction == "left": new_col -= 1
        elif direction == "right": new_col += 1

        if 0 <= new_row < self.size and 0 <= new_col < self.size:
            new_index = new_row * self.size + new_col
            zero_index = self.board.index(0)
            self.board[zero_index], self.board[new_index] = self.board[new_index], self.board[zero_index]

    def get_possible_moves(self):
        moves = []
        row, col = divmod(self.board.index(0), self.size)
        if row > 0: moves.append("up")
        if row < self.size - 1: moves.append("down")
        if col > 0: moves.append("left")
        if col < self.size - 1: moves.append("right")
        return moves

    def apply_move(self, move):
        new_puzzle = self.clone()
        new_puzzle.move(move)
        return new_puzzle
