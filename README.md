# Sudoku Evolutionary Solver

## Problem definition

***PB1**. Evolutionary algorithm for the automated solving the Sudoku puzzle
Design the evolutionary heuristics for solving the Sudoku puzzle. The application should
allow for the automated initial state generation for various difficulty levels. Design the
representation of the single solution (genotype), succession method and genetic operators.
Determine the particular parameters of the algorithm: population size, crossover and mutation
probabilities. The project should present the solution process and enable the comparison
between the proposed algorithm and the depth-first search*


## Run

```bash
pip install -r requirements.txt
```

```bash
python3 main.py
```

## Results: DFS vs EA

```yaml
Statistics for DFS (easy):
Average: 2.66 ms
Median: 1.00 ms
Standard Deviation: 6.49 ms
P95: 18.70 ms
P99: 45.84 ms
Min: 0.00 ms
Max: 38.00 ms

Statistics for EA (easy):
Average: 36329.20 ms
Median: 5092.00 ms
Standard Deviation: 63952.27 ms
P95: 211137.90 ms
P99: 304123.14 ms
Min: 327.00 ms
Max: 283109.00 ms

Statistics for DFS (medium):
Average: 11.28 ms
Median: 5.00 ms
Standard Deviation: 23.06 ms
P95: 59.65 ms
P99: 159.54 ms
Min: 0.00 ms
Max: 137.00 ms

Statistics for EA (medium):
Average: 42941.56 ms
Median: 18038.00 ms
Standard Deviation: 59016.95 ms
P95: 206723.50 ms
P99: 235717.04 ms
Min: 957.00 ms
Max: 226604.00 ms
Failed runs for EA: 5

Statistics for DFS (hard):
Average: 74.96 ms
Median: 30.00 ms
Standard Deviation: 94.32 ms
P95: 301.40 ms
P99: 413.44 ms
Min: 0.00 ms
Max: 386.00 ms

Statistics for EA (hard):
Average: 94209.11 ms
Median: 74433.00 ms
Standard Deviation: 75626.39 ms
P95: 261098.00 ms
P99: 286618.00 ms
Min: 13158.00 ms
Max: 270998.00 ms
Failed runs for EA: 22
```

## References

- [Sudoku - Wikipedia](https://en.wikipedia.org/wiki/Sudoku)
- [The History of Sudoku](https://www.sudokuonline.io/tips/history-of-sudoku)
- [Algorithm to Solve Sudoku | Sudoku Solver](https://www.geeksforgeeks.org/sudoku-backtracking-7/)
- [Solving Sudoku using Depth-First Search](https://kevinkle.in/posts/2021-02-28-sudoku_dfs/)
- [Sudoku and Inference](https://ai.dmi.unibas.ch/_files/teaching/fs13/ki/material/ki10-sudoku-inference.pdf)
- [New Developments in Artificial Intelligence and the Semantic Web](https://www.researchgate.net/publication/228840763_New_Developments_in_Artificial_Intelligence_and_the_Semantic_Web)
- [Elitism in Evolutionary Algorithms](https://www.baeldung.com/cs/elitism-in-evolutionary-algorithms)
- [Uniform Crossover in Genetic Algorithms](http://www.tomaszgwiazda.com/uniformX.htm)
- [Sudoku Solver using Backtracking in Python](https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking)
