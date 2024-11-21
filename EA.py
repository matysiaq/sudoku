import copy
import math
import random

from tqdm import tqdm


def decrement_position(pos):
    return 8 if pos == 0 else pos - 1


def increment_position(pos):
    return 0 if pos == 8 else pos + 1


def swap_mutation(target_gene_group, ref_gene_group, max_attempts=50):
    """Performs swap mutation on target_gene_group, while respecting givens in ref_gene_group"""
    for _ in range(max_attempts):
        a, b = random.sample(range(9), 2)

        row_a, col_a = a // 3, a % 3
        row_b, col_b = b // 3, b % 3

        if ref_gene_group[row_a][col_a] == 0 and ref_gene_group[row_b][col_b] == 0:
            target_gene_group[row_a][col_a] = target_gene_group[row_b][col_b]
            target_gene_group[row_b][col_b] = target_gene_group[row_a][col_a]
        return target_gene_group

    return target_gene_group


def three_swap_mutation(target_gene_group, ref_gene_group, max_attempts=50):
    """Performs three-sawp mutation on target_gene_group, while respecting givens in ref_gene_group"""
    for _ in range(max_attempts):
        a, b, c = random.sample(range(9), 3)

        row_a, col_a = a // 3, a % 3
        row_b, col_b = b // 3, b % 3
        row_c, col_c = c // 3, c % 3

        if ref_gene_group[row_a][col_a] == 0 and ref_gene_group[row_b][col_b] == 0 and ref_gene_group[row_c][
            col_c] == 0:
            target_gene_group[row_a][col_a], target_gene_group[row_b][col_b], target_gene_group[row_c][col_c] = (
                target_gene_group[row_c][col_c],
                target_gene_group[row_a][col_a],
                target_gene_group[row_b][col_b],
            )
            return target_gene_group

    return target_gene_group


def insertion_mutation(target_gene_group, ref_gene_group, max_attempts=50):
    """Performs insertion mutation on target_gene_group, while respecting givens in ref_gene_group"""
    # Flatten lists
    flat_tgg = [cell for row in target_gene_group for cell in row]
    flat_rgg = [cell for row in ref_gene_group for cell in row]

    for _ in range(max_attempts):
        a, b = random.sample(range(9), 2)
        if flat_rgg[a] == 0 and flat_rgg[b] == 0:
            value_to_move = flat_tgg[a]
            last_value = flat_tgg[b]
            flat_tgg[a] = 0
            if a < b:
                x = a if a == 8 else a
                y = 0 if a == 8 else a + 1

                while x != b:
                    x = decrement_position(x)
                    y = decrement_position(y)

                    while flat_rgg[x] != 0:
                        x = decrement_position(x)

                    while flat_rgg[y] != 0:
                        y = decrement_position(y)

                    flat_tgg[y] = flat_tgg[x]
                    flat_tgg[x] = 0

                flat_tgg[y] = last_value
                flat_tgg[b] = value_to_move
            else:  # a > b
                x = a
                y = decrement_position(a)

                while x != b:
                    x = increment_position(x)
                    y = increment_position(y)

                    while flat_rgg[x] != 0:
                        x = increment_position(x)

                    while flat_rgg[y] != 0:
                        y = increment_position(y)

                    flat_tgg[y] = flat_tgg[x]
                    flat_tgg[x] = 0

                flat_tgg[y] = last_value
                flat_tgg[b] = value_to_move
            break

    # Unflatten list
    new_tgg = [flat_tgg[i * len(target_gene_group):(i + 1) * len(target_gene_group)] for i in
               range(len(target_gene_group))]

    return new_tgg


def mutations(population, reference, elitism):
    """Performs mutations on the population, while respecting givens (reference)"""
    start_i = int(elitism * len(population) / 2) + 1
    for p in range(start_i, len(population)):
        # Iterate through all 9 sub-grids (3x3 genes)
        for i in range(9):
            r1 = random.random()
            if r1 > 0.15:
                continue
            r2 = random.random()
            tgg = population[p][1].get_gene_group(i)
            rgg = reference.get_gene_group(i)

            # Decide which mutation to apply
            if r2 <= 0.6:  # 60% chance
                tgg = swap_mutation(tgg, rgg)
            elif r2 <= 0.8:  # 20% chance
                tgg = three_swap_mutation(tgg, rgg)
            else:  # 20% chance
                tgg = insertion_mutation(tgg, rgg)

            population[p][1].set_gene_group(i, tgg)

    return population


def generate_offsprings(parent1, parent2):
    """Returns two offsprings generated from two parents"""
    child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
    child1[0], child2[0] = -1, -1
    for i in range(1, 10):
        if random.random() > 0.5:
            p1_gene = parent1[1].get_gene_group(i)
            p2_gene = parent2[1].get_gene_group(i)

            child1[1].set_gene_group(i, p2_gene)
            child2[1].set_gene_group(i, p1_gene)

    return child1, child2


def population_crossover(population, elitism):
    """Performs crossover on the population, with given elitism"""
    new_pop = copy.deepcopy(population[:int(elitism * len(population) / 2)])

    while len(new_pop) <= len(population):
        i1 = random.randint(int(elitism * len(population) / 2) + 1, int(elitism * len(population)))
        i2 = random.randint(int(elitism * len(population)) + 1, int(0.8 * len(population)))

        p1 = population[i1]
        p2 = population[i2]

        c1, c2 = generate_offsprings(p1, p2)

        new_pop.append(c1)
        if len(new_pop) >= len(population):
            break
        new_pop.append(c2)

    return new_pop


def calculate_row_sum_fitness(board):
    """Calculates the sum of each row in the board."""
    row_sums = []
    for row in board.grid:
        if abs(45 - sum(row)) > 0:
            row_sums.append(1)
    return row_sums


def calculate_column_sum_fitness(board):
    """Calculates the sum of each column in the board."""
    column_sums = []
    for col in range(9):
        column_sum = abs(45 - sum(board.grid[row][col] for row in range(9)))
        if column_sum > 0:
            column_sums.append(1)
    return column_sums


def calculate_row_product_fitness(board):
    """Calculates the product of each row in the board."""
    row_products = []
    for row in board.grid:
        product = 1
        for num in row:
            product *= num  # Multiply each element
        if math.sqrt(abs(math.factorial(9) - product)) > 0:
            row_products.append(1)
    return row_products


def calculate_column_product_fitness(board):
    """Calculates the product of each column in the board."""
    column_products = []
    for col in range(9):
        product = 1
        for row in range(9):
            product *= board.grid[row][col]
        if (math.sqrt(abs(math.factorial(9) - product))) > 0:
            column_products.append(1)
    return column_products


def calculate_missing_numbers_in_row(board):
    """Calculates the number of missing numbers in each row."""
    target_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    missing_counts = []

    for row in board.grid:
        row_set = set(row)
        missing_count = len(target_set - row_set)
        missing_counts.append(missing_count)

    return missing_counts


def calculate_missing_numbers_in_column(board):
    """Calculates the number of missing numbers in each column."""
    target_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    missing_counts = []

    for col in range(9):
        column_set = set(board.grid[row][col] for row in range(9))
        missing_count = len(target_set - column_set)
        missing_counts.append(missing_count)

    return missing_counts


def calculate_fitness(population):
    """Calculates the fitness value for each individual in the population"""
    for index in range(len(population)):
        y = (
                sum(calculate_row_sum_fitness(population[index][1])) +
                sum(calculate_column_sum_fitness(population[index][1])) +
                sum(calculate_row_product_fitness(population[index][1])) +
                sum(calculate_column_product_fitness(population[index][1])) +
                2 * (sum(calculate_missing_numbers_in_row(population[index][1])) +
                     sum(calculate_missing_numbers_in_column(population[index][1])))
        )

        population[index][0] = int(y)

    population.sort(key=lambda individual: individual[0])

    return population


def gen_initial_population(number, board):
    """Generates initial random population with [number] individuals"""
    initial_population = []

    for _ in range(number):
        board_copy = copy.deepcopy(board)
        grid = board_copy.grid

        for block_row in range(3):
            for block_col in range(3):
                numbers = list(range(1, 10))

                for r in range(block_row * 3, (block_row + 1) * 3):
                    for c in range(block_col * 3, (block_col + 1) * 3):
                        if grid[r][c] != 0:
                            if grid[r][c] in numbers:
                                numbers.remove(grid[r][c])

                random.shuffle(numbers)

                index = 0
                for r in range(block_row * 3, (block_row + 1) * 3):
                    for c in range(block_col * 3, (block_col + 1) * 3):
                        if grid[r][c] == 0:
                            grid[r][c] = numbers[index]
                            index += 1

        initial_population.append([-1, board_copy])

    return initial_population


def solve_ea(sudoku, population_size=100, generations=50000, max_no_improvement=50000, elitism=0.2):
    no_improvement_count = 0
    best_fitness = float('inf')

    population = gen_initial_population(population_size, sudoku)

    for i in tqdm(range(generations), desc="Evolving Population"):
        population = calculate_fitness(population)

        if population[0][0] < best_fitness:
            best_fitness = population[0][0]
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        if no_improvement_count > max_no_improvement:
            print("No improvement, stopping early.")
            return False

        if best_fitness < 1:
            sudoku.grid = population[0][1].grid
            population[0][1].print_board()
            return True

        population = population_crossover(population, elitism)
        population = mutations(population, sudoku, elitism)

    return False
