import random
from deap import base, creator, tools, algorithms

# Parametry problemu
# Wymiary magazynu
WAREHOUSE_WIDTH = 1000
WAREHOUSE_HEIGHT = 300
WAREHOUSE_DEPTH = 1000
WAREHOUSE_DIMENSIONS =   WAREHOUSE_WIDTH * WAREHOUSE_HEIGHT * WAREHOUSE_DEPTH
PACKAGES = [
    # (szerokość, wysokość, głębokość, wartość)
(240, 152, 293, 141) ,
(271, 167, 204, 150) ,
(229, 181, 278, 34) ,
(252, 195, 250, 41) ,
(216, 156, 253, 80) ,
(286, 173, 240, 34) ,
(233, 169, 297, 105) ,
(257, 188, 204, 140) ,
(268, 163, 207, 110) ,
(238, 177, 207, 47) ,
(248, 145, 207, 83) ,
(299, 100, 300, 62) ,
(122, 147, 172, 29) ,
(159, 147, 220, 146) ,
(148, 131, 163, 99) ,
(285, 120, 132, 138) ,
(169, 153, 122, 100) ,
(262, 156, 110, 89) ,
(140, 133, 222, 141) ,
(257, 103, 226, 59) ,
(141, 128, 171, 66) ,
(102, 138, 117, 6) ,
(242, 122, 191, 90) ,
(252, 112, 288, 55) ,
(129, 171, 225, 35) ,
(253, 195, 210, 82) ,
(290, 102, 278, 60) ,
(291, 189, 175, 89) ,
(143, 102, 106, 81) ,
(123, 157, 177, 85) ,
(232, 176, 179, 66) ,
(261, 176, 292, 7) ,
(257, 108, 150, 67) ,
(155, 193, 148, 88) ,
(115, 106, 153, 9) ,
(198, 145, 229, 150) ,
(131, 182, 266, 67) ,
(127, 169, 203, 124) ,
(256, 116, 240, 144) ,
(276, 128, 119, 20) ,
(149, 183, 133, 75) ,
(299, 156, 106, 77) ,
(274, 157, 105, 86) ,
(193, 144, 294, 56) ,
(204, 134, 247, 48) ,
(109, 198, 240, 39) ,
(274, 183, 214, 54) ,
(200, 178, 294, 2) ,
(152, 120, 236, 134) ,
(152, 121, 160, 130)
]

# Definicja funkcji oceny
creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

def evaluate(individual):
    used_volume = 0  # (szerokość, wysokość, głębokość)
    value = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            used_volume += PACKAGES[i][0] * PACKAGES[i][1] * PACKAGES[i][2]
            value += PACKAGES[i][3]
    if used_volume > WAREHOUSE_DIMENSIONS :
        return 0,  # Przekroczenie maksymalnej pojemności magazynu, kara
    return value,

# Inicjalizacja narzędzi DEAP
toolbox = base.Toolbox()

# Definiowanie jak tworzony jest osobnik oraz populacja
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(PACKAGES))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Rejestracja operacji genetycznych
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Parametry algorytmu
population = toolbox.population(n=100)
N_GEN = 100
CXPB, MUTPB = 0.5, 0.1

# Algorytm ewolucyjny
for gen in range(N_GEN):
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    # Krzyżowanie i mutacja
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Ewaluacja nieocenionych osobników
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    print(" === GEN {} TOP SOLUTION === \n{}\nWartość: {}\n\n".format(gen, tools.selBest(population, 1)[0], evaluate(tools.selBest(population, 1)[0])[0]))

    # Zamiana starej populacji na potomstwo
    population[:] = offspring

# Wyświetlenie najlepszego rozwiązania
best_ind = tools.selBest(population, 1)[0]
print("\nNajlepsze rozwiązanie:\n{}\nWartość: {}\n".format(best_ind, evaluate(best_ind)[0]))

# Wypisywanie populacji wraz z wartościami
"""
for i in range(len(population)):
    print (f"Osobnik {i+1} : {population[i]} Wartosc: {evaluate(population[i])[0]}")

"""
