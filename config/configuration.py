import yaml

with open('config/config.yml', 'r') as fp:
    knapsack_configuration = yaml.safe_load(fp)

data = {}
fitness_function = {}
mutation_function = {}
crossover_function = {}
selection_function = {}
pop_size = {}
mutation_prob = {}
generations = {}
crossover_prob = {}

if 'file' in knapsack_configuration.get('data', {}):
    data['file'] = knapsack_configuration['data']['file']

functions = knapsack_configuration.get('functions', {})

if all(key in functions for key in ['fitness_function', 'mutation_function', 'crossover_function', 'selection_function']):
    fitness_function['fitness_function'] = functions['fitness_function']
    mutation_function['mutation_function'] = functions['mutation_function']
    crossover_function['crossover_function'] = functions['crossover_function']
    selection_function['selection_function'] = functions['selection_function']

cfg = knapsack_configuration.get('configuration', {})

if all(key in cfg for key in ['pop_size', 'mutation_prob', 'generations', 'crossover_prob']):
    pop_size['pop_size'] = cfg['pop_size']
    mutation_prob['mutation_prob'] = cfg['mutation_prob']
    generations['generations'] = cfg['generations']
    crossover_prob['crossover_prob'] = cfg['crossover_prob']