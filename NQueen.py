import random
import matplotlib.pyplot as plt


def cost(chromosome):
    return sum([1 for i in range(Queen_Number) for j in range(i + 1, Queen_Number) if
                abs(j - i) == abs(chromosome[j] - chromosome[i])])


def parent_selection():
    tmp = (list(), Queen_Number)
    for _ in range(Population_Size // 5):
        ch = random.choice(Population)
        if ch[-1] < tmp[1]:
            tmp = (ch, ch[-1])
    return tmp[0]


def crossover(parent1, parent2):
    children = list()
    for _ in range(random.randint(1, 2)):  # max offspring is 2
        child = [-1] * (Queen_Number + 1)
        p, q = random.randint(1, Queen_Number // 2 - 1), random.randint(Queen_Number // 2 + 1, Queen_Number - 2)
        child[p: q + 1] = parent1[p: q + 1]
        for i in range(p, q + 1):
            if parent2[i] not in child:
                t = i
                while p <= t <= q:
                    t = parent2.index(parent1[t])
                child[t] = parent2[i]
        for j in range(Queen_Number):
            if child[j] == -1:
                child[j] = parent2[j]
        child[-1] = cost(child)
        children.append(child)
        parent1, parent2 = parent2, parent1
    return children


def mutation(chromosome):
    p, q = random.randint(0, Queen_Number - 1), random.randint(0, Queen_Number - 1)
    chromosome[p], chromosome[q] = chromosome[q], chromosome[p]
    chromosome[-1] = cost(chromosome)


def initialize_population():
    for _ in range(Population_Size):
        chromosome = list(range(1, Queen_Number + 1))
        random.shuffle(chromosome)
        chromosome.append(cost(chromosome))
        Population.append(chromosome)


def start():
    cost_list = list()
    iteration_count = 0
    initialize_population()
    Population.sort(key=lambda q: q[-1])
    cost_list.append(Population[0][-1])
    print("%dth iteration, current cost: %d" % (iteration_count, Population[0][-1]))
    while Population[4][-1] and iteration_count < Max_Iteration:
        random.shuffle(Population)
        new_children = list()
        for _ in range(Population_Size // 3):  # maximum number of children is Population_Size//3
            p1, p2 = parent_selection(), parent_selection()
            done = False
            if random.random() < CP:
                children = crossover(p1, p2)
                done = True
            else:
                children = [p1[:], p2[:]]
            for child in children:
                if random.random() < MP or not done:
                    mutation(child)
                new_children.append(child)
        Population.extend(new_children)
        Population.sort(key=lambda q: q[-1])
        del Population[Population_Size:]
        cost_list.append(Population[0][-1])
        iteration_count += 1
        if iteration_count % 10 == 0:
            print("%dth iteration, current cost: %d" % (iteration_count, Population[0][-1]))
    del Population[0][-1]
    print('------------------------------->')
    print("number of iteration: %d , final cost: %d" % (iteration_count, Population[4][-1]))
    print("solution for %d Queen is: %s" % (Queen_Number, str([pair[::-1] for pair in enumerate(Population[0], 1)])))
    return cost_list


def show_result():
    iteration = range(len(cost_list))
    plt.plot(iteration, cost_list)
    plt.grid(True)
    if len(cost_list) > 0:
        plt.ylim((0, max(cost_list) + 1))
        plt.ylabel('cost value (number of attacks)')
        plt.xlabel('iteration')
        plt.title(str(str(Queen_Number) + "-Queen "))
        plt.show()


Queen_Number = int(input("Enter number of queens: "))  # Number of Queens >=7
Population_Size = 2 * Queen_Number  # Maximum number of people can live in environment
Population = list()  # Environment
Max_Iteration = 30000  # Maximum number of iteration to find best result in Algorithm
CP = 0.5  # Probability of crossover
MP = 0.95  # Probability of mutation

cost_list = start()
show_result()
# remember number of queen must be 5 or >=7
