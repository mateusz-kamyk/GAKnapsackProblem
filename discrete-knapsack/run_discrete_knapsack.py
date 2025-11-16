import numpy as np
import random

def load_items(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    size, capacity = map(int, lines[0].split())

    items = []
    for line in lines[1:]:
        value, weight = map(int, line.split())

        items.append((weight, value))

    return items, size, capacity

def discrete_knapsack(items, size, weight):
    cache = np.zeros((size + 1, weight + 1))

    for i in range(1, size + 1):
        for w in range(weight + 1):
            item_weight, item_value = items[i - 1]
            if item_weight > w:
                cache[i, w] = cache[i - 1, w]
            else:
                cache[i, w] = max(cache[i - 1, w], cache[i - 1, w - item_weight] + item_value)
    return cache[size, weight]

items, size, capacity = load_items("dane.txt")
num_items = len(items)
print("Discrete knapsack - max value:", discrete_knapsack(items, size, capacity))

