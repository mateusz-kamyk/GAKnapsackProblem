# GAKnapsackProblem
This project implements a configurable genetic algorithm (GA) to solve the 0/1 knapsack optimization problem.
The implementation includes multiple selection, crossover, and mutation strategies, and supports experiments on low-dimensional and large-scale datasets.

## Requirements
- Python 3.8+
- PyYAML
- Standard Python libraries (random, etc.)

## Algorithm configuration

You can freely adjust algorithm parameters without modifying the main code.  
Edit the file: `config/config.yml`.

Example configuration:

```yaml
data:
  file: "data/large_scale/knapPI_1_200_1000_1"

functions:
  fitness_function: True
  mutation_function: True
  # crossover_function possible options: one_point, two_point
  crossover_function: two_point
  # selection_function possible options: tournament, rank, roulette
  selection_function: tournament

configuration:
  pop_size: 500
  mutation_prob: 0.1
  generations: 50
  crossover_prob: 1.0
```
## How to run
1. Open a terminal in the project directory.
2. Execute:   
`python main.py`
