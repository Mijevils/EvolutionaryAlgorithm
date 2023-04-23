from random import choice
import random

### EVOLUTIONARY ALGORITHM ###

def evolve():
    """Initiates the evolutionary algorithm. """
    population = create_pop()
    fitness_population = evaluate_pop(population)
    for gen in range(NUMBER_GENERATION):
        mating_pool = select_pop(population, fitness_population)
        offspring_population = crossover_pop(mating_pool)
        population = mutate_pop(offspring_population)
        fitness_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        print("Generation: ", gen+1, "Fit: ", best_fit)
        check = []
        for i in range(len(best_ind)):
            check.append(best_ind[i])
            if (len(check) >= 9):
                print(check)
                check = []

### POPULATION-LEVEL OPERATORS ###

def create_pop():
    return [create_ind() for _ in range(POPULATION_SIZE)]

def evaluate_pop(population):
    return [evaluate_ind(individual) for individual in population]

def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]

def crossover_pop(population):
    return [ crossover_ind(choice(population), choice(population)) for _ in range(POPULATION_SIZE) ]

def mutate_pop(population):
    return [ mutate_ind(individual) for individual in population ]

def best_pop(population, fitness_population):
    return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

#target  = list("HELLO WORLD!")
alphabet = [1,2,3,4,5,6,7,8,9]
INDIVIDUAL_SIZE = 81
# Unneeded in Sudoku problem

def create_ind():
    """Creates a sudoku grid with numbers 1 to 9. It does not ensure this sudoku grid is correct."""
    grid = []
    chances = [1,2,3,4,5,6,7,8,9]
    for i in range(len(INITIAL_STATE)):
        if INITIAL_STATE[i] in chances:
            chances.remove(INITIAL_STATE[i])
        if INITIAL_STATE[i] == 0:
            pick = random.choice(chances)
            grid.append(pick)
            chances.remove(pick)
        elif INITIAL_STATE[i] != 0:
            grid.append(INITIAL_STATE[i])
        if (i % 9 == 0):
            chances = [1,2,3,4,5,6,7,8,9]

    return grid

def evaluate_ind(grid):
    """Function that checks how correct a given sudoku grid is.
    This is measured by giving it a score based on how many rows, columns and subgrids are valid (have numbers 1 to 9).
    1 point is added to the total score for every one of them that are valid. Therefore the maximum score
    (correct sudoku) is of 27. """
    score = 0

    ## Checking rows are valid (numbers 1 to 9)
    check = []
    for i in range(len(grid)):
        check.append(grid[i])
        if (1 in check and 2 in check and 3 in check and 4 in check and 5 in check and 6 in check and 7 in check and 8 in check and 9 in check):
            score += 1
        if (len(check) >= 9):
            check = []

    ## Checking columns are valid (numbers 1 to 9)
    checkc = []
    for i in range(0, 9):
        checkc.append(grid[i])
        checkc.append(grid[i + 9])
        checkc.append(grid[i + 18])
        checkc.append(grid[i + 27])
        checkc.append(grid[i + 36])
        checkc.append(grid[i + 45])
        checkc.append(grid[i + 54])
        checkc.append(grid[i + 63])
        checkc.append(grid[i + 72])

        if (1 in checkc and 2 in checkc and 3 in checkc and 4 in checkc and 5 in checkc and 6 in checkc and 7 in checkc and 8 in checkc and 9 in checkc):
            score += 1

        checkc = []

    ## Checking subgrids are valid (numbers 1 to 9)
    checks = [[], [], [], [], [], [], [], [], []]
    for i in range(81):
        row = (i // 9)
        column = (i % 9)
        checks[(row // 3) * 3 + (column // 3)].append(grid[i])
    for i in range(len(checks)):
        if (1 in checks[i] and 2 in checks[i] and 3 in checks[i] and 4 in checks[i] and 5 in checks[i] and 6 in checks[i] and 7 in checks[i] and 8 in checks[i] and 9 in checks[i]):
            score += 1

    return score

def crossover_ind(individual1, individual2):
    return [ choice(ch_pair) for ch_pair in zip(individual1, individual2) ]

def mutate_ind(individual):
    """Mutates the current individual when called."""
    for i in range(len(INITIAL_STATE)):
        if INITIAL_STATE[i] == 0:
           individual[i] = random.choice(alphabet)
    return individual

### PARAMERS VALUES ###

NUMBER_GENERATION = 100
POPULATION_SIZE = 30
TRUNCATION_RATE = 0.5 # % of population that is cut off
MUTATION_RATE = 1.0 / INDIVIDUAL_SIZE
INITIAL_STATE = [3,0,0,0,0,5,0,4,7,0,0,6,0,4,2,0,0,1,0,0,0,0,0,7,8,9,0,0,5,0,0,1,6,0,0,2,0,0,3,0,0,0,0,0,4,8,1,0,0,0,0,7,0,0,0,0,2,0,0,0,4,0,0,5,6,0,8,7,0,1,0,0,0,0,0,3,0,0,6,0,0]

### EVOLVE! ###

evolve()

