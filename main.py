import random
from config.configuration import *

def load_items(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    size, capacity = map(float, lines[0].split())
    size = int(size)
    capacity = int(capacity)
    items = []
    for line in lines[1:]:
        value, weight = map(float, line.split())
        items.append((int(value), int(weight)))
    return items, size, capacity

def fitness(chromosome, items, capacity):
    total_weight = 0
    total_value = 0
    for gene, (value, weight) in zip(chromosome, items):
        if gene:
            total_weight += weight
            total_value += value
    if total_weight > capacity:
        return 0
    return total_value

def mutate(chromosome):
    index = random.randint(0, len(chromosome) - 1)
    chromosome[index] = 1 - chromosome[index]

def crossover(parent1, parent2, crossover_prob):
    if random.random() < crossover_prob:
        point = random.randint(1, len(parent1) - 2)
        return parent1[:point] + parent2[point:]
    else:
        return parent1[:]

def two_point_crossover(parent1, parent2, crossover_prob):
    if random.random() < crossover_prob:
        point1 = random.randint(1, len(parent1) - 2)
        point2 = random.randint(point1 + 1, len(parent1) - 1)
        child = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        return child
    else:
        return parent1[:] 

def generate_population(pop_size, items):
    population = []
    chromosome_len = len(items)
    
    for _ in range(pop_size):
        chromosome = [0] * chromosome_len
        total_weight = 0
        indices = list(range(chromosome_len))
        random.shuffle(indices)
        for i in indices:
            weight = items[i][1]
            if total_weight + weight <= capacity:
                chromosome[i] = 1
                total_weight += weight
        population.append(chromosome)
    return population

def roulette_selection(population, fitnesses, num_selected):
    min_fit = min(fitnesses)
    adjusted_fitnesses = [f - min_fit + 1 for f in fitnesses]
    selected = random.choices(population, weights=adjusted_fitnesses, k=num_selected)
    return selected

def rank_selection(population, fitnesses, num_selected):
    sorted_pairs = sorted(zip(fitnesses, population), key=lambda x: -x[0])
    sorted_population = [ch for _, ch in sorted_pairs]
    n = len(sorted_population) 
    if n == 0:
        return []
    weights = [(n - i) for i in range(n)]
    selected = random.choices(sorted_population, weights=weights, k=num_selected)
    return selected

def tournament_selection(population, fitnesses, num_selected, tournament_size):
    selected = []
    pop_size = len(population)

    for _ in range(num_selected):
        contestants_idx = random.sample(range(pop_size), tournament_size)
        best_idx = max(contestants_idx, key=lambda i: fitnesses[i])
        selected.append(population[best_idx][:])
    
    return selected

def knapsack_genetic_algorithm(items, capacity, pop_size, mutation_prob, generations, crossover_prob, use_fitness, use_mutation, use_crossover, use_selection):

    population = generate_population(pop_size, items)
    global_best_value = 0
    global_best_chromosome = None

    print('Value')

    for gen in range(generations):
        if use_fitness:
            fitnesses = [fitness(ch, items, capacity) for ch in population]
            best_index = fitnesses.index(max(fitnesses))
            best_value = fitnesses[best_index]
            if best_value > global_best_value:
                global_best_value = best_value
                global_best_chromosome = population[best_index][:]
            print(f"{best_value}")

        selected = population
        num_selected = len(population)
        if use_selection == 'roulette' and use_fitness:
            selected = roulette_selection(population, fitnesses, num_selected)
        elif use_selection == 'rank' and use_fitness:
            selected = rank_selection(population, fitnesses, num_selected)
        elif use_selection == 'tournament' and use_fitness:
            selected = tournament_selection(population, fitnesses, num_selected, tournament_size=3)

        new_population = []

        while len(new_population) < pop_size:
            parent1, parent2 = random.choice(selected), random.choice(selected)
            child = parent1[:]

            if use_crossover == 'one_point':
                child = crossover(parent1, parent2, crossover_prob)
            elif use_crossover == 'two_point':
                child = two_point_crossover(parent1, parent2, crossover_prob)

            if use_mutation:
                if random.random() < mutation_prob:
                    mutate(child)
            new_population.append(child)

        population = new_population

    return global_best_chromosome, global_best_value

items, size, capacity = load_items(data['file'])

best_chromosome, best_value = knapsack_genetic_algorithm(
    items, capacity,
    pop_size=pop_size['pop_size'],
    mutation_prob=mutation_prob['mutation_prob'],
    generations=generations['generations'],
    crossover_prob=crossover_prob['crossover_prob'],
    use_fitness=fitness_function['fitness_function'],
    use_mutation=mutation_function['mutation_function'],
    use_crossover=crossover_function['crossover_function'],
    use_selection=selection_function['selection_function']
)

print("Best solution value:", best_value)
print("Selected items:", sum(best_chromosome))