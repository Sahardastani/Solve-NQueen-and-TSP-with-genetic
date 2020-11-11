import random
import matplotlib.pyplot as plt
import numpy as np


def cost(chromosome):
    cost = 0
    for i in range(City_Number - 1):
        cost += np.array(Distances)[chromosome[i], chromosome[i + 1]]
    cost += np.array(Distances)[chromosome[City_Number - 1], chromosome[0]]
    return cost


def parent_selection():
    best = []
    score = 10000
    for _ in range(Population_Size):
        ch = random.choice(Population)
        if ch[-1] < score:
            best = ch
            score = ch[-1]
    return best


def crossover(parent1, parent2):
    p = random.randint(1, City_Number - 2)
    child1 = parent2
    child2 = parent1
    child1[0: p] = parent1[0: p]
    child2[0: p] = parent2[0: p]
    child1[-1] = cost(child1)
    child2[-1] = cost(child2)
    return [child1, child2]


def mutation(chromosome):
    p = random.randint(0, City_Number - 2)
    temp = chromosome[p]
    chromosome[p] = chromosome[p + 1]
    chromosome[p + 1] = temp
    chromosome[-1] = cost(chromosome)


def initialize_population():
    for _ in range(Population_Size):
        chromosome = list(range(City_Number))
        random.shuffle(chromosome)
        chromosome.append(cost(chromosome))
        Population.append(chromosome)
    print('initialize population : ')
    print(*Population, sep = "\n")


def start():
    cost_list = list()
    iteration_count = 0
    initialize_population()
    Population.sort(key=lambda q: q[-1])
    cost_list.append(Population[0][-1])
    # print("%dth iteration, current cost: %d" % (iteration_count, Population[0][-1]))
    while Population[0][-1] and (iteration_count < Max_Iteration):
        random.shuffle(Population)
        new_children = list()
        for _ in range(Population_Size // 3):  # maximum number of children is Population_Size//3
            p1 = parent_selection()
            p2 = parent_selection()
            done = False
            if random.random() < CP:
                children = crossover(p1, p2)
                done = True
            else:
                children = [p1, p2]
            for child in children:
                if random.random() < MP or not done:
                    mutation(child)
                new_children.append(child)
        Population.extend(new_children)
        Population.sort(key=lambda q: q[-1])
        del Population[Population_Size:]
        cost_list.append(Population[0][-1])
        iteration_count += 1
        # if iteration_count % 10 == 0:
        #     print("%dth iteration, current state: " % (iteration_count)+str( Population[0][-1]))
    # del Population[0][-1]
    print('------------------------------->')
    print("solution for TSP is: ")
    ans = []
    for i in range(City_Number - 1):
        ans.append([Population[0][i], Population[0][i + 1]])
    ans.append([Population[0][City_Number - 1], Population[0][0]])
    print(ans)
    print("final cost: %d" % (Population[0][-1]))
    return cost_list


City_Number = int(input("Enter number of cities: "))  # Number of cities >=7
Distances = []
for i in range(City_Number):
    temp = []
    for j in range(City_Number):
        if i == j:
            temp.append(0)
        elif i > j:
            temp.append(np.array(Distances)[j, i])
        else:
            temp.append(int(input("Enter distance of city " + str(i) + " to " + str(j))))
    Distances.append(temp)
Population_Size = 2 * City_Number  # Maximum number of people can live in environment
Population = list()  # Environment
Max_Iteration = 3000  # Maximum number of iteration to find best result in Algorithm
CP = 0  # Probability of crossover
MP = 0.95  # Probability of mutation

cost_list = start()
