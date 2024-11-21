import random

from dfs_solver import solve_dfs, has_multiple_solutions


class Board:
    def __init__(self, difficulty):
        self.grid = [[0] * 9 for _ in range(9)]
        self.difficulty = difficulty
        self.produce_board()

    def print_board(self):
        """Prints the Sudoku board in a formatted way."""
        for i in range(len(self.grid)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(len(self.grid[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")

    def produce_board(self):
        """Modifies the completely solved grid based on difficulty
        level to produce a Sudoku puzzle with a unique solution."""
        solve_dfs(self, randomize=True)

        difficulty_settings = {
            'easy': 36,
            'medium': 31,
            'hard': 26,
            'pro': 17
        }
        clues_left = 81 - difficulty_settings.get(self.difficulty)

        filled_positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(filled_positions)

        for i, j in filled_positions:
            if clues_left <= 0:
                break

            removed_value = self.grid[i][j]
            self.grid[i][j] = 0

            if not has_multiple_solutions(self):
                clues_left -= 1
            else:
                self.grid[i][j] = removed_value

    def get_gene_group(self, group):
        """Returns the 3x3 sub-grid based on the specified group number (1-9)."""
        g = []
        start_row = 3 * ((group - 1) // 3)
        start_col = 3 * ((group - 1) % 3)

        for i in range(3):
            g.append(self.grid[start_row + i][start_col:start_col + 3])

        return g

    def set_gene_group(self, group, new_gene):
        """Replaces the specified gene (3x3 sub-grid) with new values."""
        start_row = 3 * ((group - 1) // 3)
        start_col = 3 * ((group - 1) % 3)

        for i in range(3):
            self.grid[start_row + i][start_col:start_col + 3] = new_gene[i]
