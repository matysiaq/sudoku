import random


def solve_dfs(sudoku, randomize=False):
    """
    Solves the Sudoku board in place using backtracking.
    If `randomize` is True, it shuffles the numbers to solve in a random order.
    """
    grid = sudoku.grid
    find = find_empty(grid)
    if not find:
        return True  # Puzzle solved

    row, col = find
    numbers = random.sample(range(1, 10), 9) if randomize else range(1, 10)

    for num in numbers:
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num

            if solve_dfs(sudoku, randomize):
                return True

            # Backtrack if no solution is found
            grid[row][col] = 0

    return False


def count_solutions(sudoku):
    """
    Counts the number of solutions using a backtracking approach.
    Returns the number of valid solutions.
    """
    solution_count = [0]
    _count_solutions_dfs(sudoku.grid, solution_count)
    return solution_count[0]


def _count_solutions_dfs(grid, solution_count):
    """Helper function for counting the number of solutions."""
    find = find_empty(grid)
    if not find:
        solution_count[0] += 1
        return

    row, col = find

    for num in range(1, 10):
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num

            # Recursively count the solutions
            _count_solutions_dfs(grid, solution_count)

            # Stop early if more than one solution is found
            if solution_count[0] > 1:
                grid[row][col] = 0
                return

            # Backtrack
            grid[row][col] = 0


def is_valid(grid, num, pos):
    """
    Checks if placing `num` at position `pos` (row, col) is valid.
    Returns True if the number can be placed, False otherwise.
    """
    row, col = pos

    # Check row and column
    if any(grid[row][j] == num for j in range(9)) or any(grid[i][col] == num for i in range(9)):
        return False

    # Check 3x3 box
    box_row, box_col = row // 3 * 3, col // 3 * 3
    if any(grid[i][j] == num for i in range(box_row, box_row + 3) for j in range(box_col, box_col + 3)):
        return False

    return True


def find_empty(grid):
    """
    Finds an empty cell in the grid.
    Returns a tuple (row, col) of the empty cell, or None if no empty cells.
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


def has_multiple_solutions(sudoku):
    """
    Checks if the Sudoku puzzle has more than one solution.
    Returns True if there are multiple solutions, False otherwise.
    """
    return count_solutions(sudoku) > 1
