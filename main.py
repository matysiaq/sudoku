import copy
import time
import statistics
from tqdm import tqdm

from dfs_solver import solve_dfs
from EA import solve_ea
from Board import Board


def run_solver(solver, board):
    start_time = time.time()
    ok = solver(board)
    elapsed_time_ms = (time.time() - start_time) * 1000
    return elapsed_time_ms if ok else None


def display_statistics(times, method_name):
    if not times:
        print(f"No successful runs for {method_name}.")
        return

    stats = {
        "Average": statistics.mean(times),
        "Median": statistics.median(times),
        "Standard Deviation": statistics.stdev(times),
        "P95": statistics.quantiles(times, n=100)[94],
        "P99": statistics.quantiles(times, n=100)[98],
        "Min": min(times),
        "Max": max(times),
    }

    print(f"\nStatistics for {method_name}:")
    for stat, value in stats.items():
        print(f"{stat}: {value:.2f} ms")


if __name__ == "__main__":
    solvers = {
        "DFS": solve_dfs,
        "EA": solve_ea,
    }

    for diff in ("easy", "medium", "hard"):
        print(f"\nDifficulty: {diff}")

        results = {name: [] for name in solvers}
        failures = {name: 0 for name in solvers}

        n = 100  # Number of iterations

        for _ in tqdm(range(n), desc="Processing"):
            board = Board(diff)

            for name, solver in solvers.items():
                board_copy = copy.deepcopy(board)
                elapsed_time = run_solver(solver, board_copy)

                if elapsed_time is not None:
                    results[name].append(int(elapsed_time))
                else:
                    failures[name] += 1

        # Display statistics for each solver
        for name, times in results.items():
            display_statistics(times, f"{name} ({diff})")
            if failures[name] > 0:
                print(f"Failed runs for {name}: {failures[name]}")
