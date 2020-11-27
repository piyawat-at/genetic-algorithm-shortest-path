import random
import matplotlib.pyplot as plt
import time

class Generation:
    def __init__(self,chromosome,distance,fitness):
        self.chromosome = chromosome
        self.distance = distance
        self.fitness = fitness

    def __repr__(self):
            return '({},{},{})'.format(self.chromosome,self.distance,self.fitness)


def sortbydistance(p):
    return p.distance

table = [
    [0, 10, 28, 23, 65, 16, 16, 42, 16, 21]
    , [10, 0, 76, 72, 150, 52, 52, 104, 42, 62]
    , [28, 76, 0, 106, 74, 48, 83, 28, 88, 58]
    , [23, 72, 106, 0, 180, 82, 82, 134, 18, 92]
    , [65, 150, 74, 180, 0, 122, 157, 56, 162, 132]
    , [16, 52, 48, 82, 122, 0, 59, 76, 64, 34]
    , [16, 52, 83, 82, 157, 59, 0, 111, 64, 69]
    , [42, 104, 28, 134, 56, 76, 111, 0, 116, 106]
    , [16, 42, 88, 18, 162, 64, 64, 116, 0, 74]
    , [21, 62, 58, 92, 132, 34, 69, 106, 74, 0]
]
def dist(arr):
    total = 0
    for i in range(0, len(arr) - 1):
        tmp = table[arr[i] - 1][arr[i + 1] - 1]
        total = total + tmp
    return total

def random_list():
    randomlist = random.sample(range(2, 11), 9)
    randomlist.insert(0, 1)
    randomlist.append(1)
    return randomlist
def print_list(list):
    for x in list:
        print(x.chromosome,x.distance,x.fitness)

def average(population_sorted):
    total = 0
    for x in population_sorted:
        total += x.distance
    avg = total/len(population_sorted)
    return avg

def parent_section(population_sorted):
    parent = []
    for i in range(len(population_sorted)-2):
        index = roulettle_wheel_selection(population_sorted)
        parent.append(population_sorted[index])
    return parent


def roulettle_wheel_selection(population_sorted):

        max = sum(x.fitness for x in population_sorted)
        pick = random.uniform(0, max)  # random float number 0 -> max
        current = 0
        for i in range(len(population_sorted)):
            current += population_sorted[i].fitness
            if (current > pick):
                return i


def crossover_pair(parent_,child):
    parent = [x.chromosome for x in parent_]

    parent_len = len(parent[0]) # = 10
                                    #(a,b) a->b-1
    firstCrossPoint = random.randint(1, parent_len - 2) # 1->7
    secondCrossPoint = random.randint(firstCrossPoint + 1, parent_len - 1)

    cross_p1 = parent[0][firstCrossPoint:secondCrossPoint]
    cross_p2 = parent[1][firstCrossPoint:secondCrossPoint]

    #print(cross_p1,cross_p2)
    tmp_child1 = (parent[0][:firstCrossPoint] + cross_p2 + parent[0][secondCrossPoint:])

    tmp_child2 = (parent[1][:firstCrossPoint] + cross_p1 + parent[1][secondCrossPoint:])

    for i in range(1, firstCrossPoint):
        check = True
        while (check):
            check = False
            for j in range(firstCrossPoint, secondCrossPoint):
                if (tmp_child1[i] == tmp_child1[j]):
                    tmp_child1[i] = parent[0][j]
                    check = True

    for i in range(secondCrossPoint, parent_len):
        check = True
        while (check):
            check = False
            for j in range(firstCrossPoint, secondCrossPoint):
                if tmp_child1[i] == tmp_child1[j]:
                    tmp_child1[i] = parent[0][j]
                    check = True

    for i in range(0, firstCrossPoint):
        check = True
        while (check):
            check = False
            for j in range(firstCrossPoint, secondCrossPoint):
                if (tmp_child2[i] == tmp_child2[j]):
                    tmp_child2[i] = parent[1][j]
                    check = True

    for i in range(secondCrossPoint, parent_len):
        check = True
        while (check):
            check = False
            for j in range(firstCrossPoint, secondCrossPoint):
                if (tmp_child2[i] == tmp_child2[j]):
                    tmp_child2[i] = parent[1][j]
                    check = True

    child.append(tmp_child1)
    child.append(tmp_child2)

def termination_criteria(list,count_termination,gen):

    if(gen!=0):
        if(list[gen]) == (list[gen-1]):
             count_termination += 1
        else : count_termination = 0

    return count_termination

def GA():
    limit_count_termination = 50 - 1  # change first number
    count_termination = 0
    population_num = 500
    all_1st_elite_dist = []
    all_avg_elite_dist = []
    child = []
    gen = 0

    while (count_termination != limit_count_termination):

        population = []
        population_sorted = []
        elite = []
        parent = []

        tmp = []

        print("Generation :", gen)
        index = 0
        for i in range(population_num):
            if (gen == 0):
                tmp_chromosome = random_list()
            else:
                tmp_chromosome = child[index]

            tmp_distance = dist(tmp_chromosome)
            tmp_fitness = 1 / tmp_distance
            tmp = Generation(tmp_chromosome, tmp_distance, tmp_fitness)
            population.append(tmp)
            index += 1

        # print("population")
        # print_list(population)

        population_sorted = sorted(population, key=sortbydistance)

        # print("population_sorted")
        # print_list(population_sorted)

        elite.append(population_sorted[0])
        all_1st_elite_dist.append(population_sorted[0].distance)
        best_chromosome = population_sorted[0].chromosome
        elite.append(population_sorted[1])

        avg = average(population_sorted)
        all_avg_elite_dist.append(avg)

        print("average distance : ", avg)
        print("best path : ", population_sorted[0].chromosome, " dist : ", population_sorted[0].distance,"\n")

        # print("elite")
        # print_list(elite)

        parent = parent_section(population_sorted)
        child = []
        # print("parent")
        # print_list(parent)

        count_termination = termination_criteria(all_1st_elite_dist, count_termination, gen)

        if (count_termination != limit_count_termination):

            for i in range((len(population_sorted) // 2) - 1):
                rate = random.randint(1, 10)
                # crossover 80%
                if rate <= 8:
                    crossover_pair((parent[2 * i:(2 * i) + 2]), child)  # i = 0 parent[0:2] 0 1
                    # i = 1 parent [2:4] 2 3
                else:
                    child.append(parent[2 * i].chromosome)
                    child.append(parent[(2 * i) + 1].chromosome)

        child.append(elite[0].chromosome)
        child.append(elite[1].chromosome)
        # print("child")
        # print(child)
        gen += 1

    x = [i for i in range(gen)]
    y = [i for i in all_avg_elite_dist]
    z = [i for i in all_1st_elite_dist]
    #print(x, y)
    plt.plot(x, y)
    plt.show()
    plt.plot(x, z)
    plt.show()
    print("Shortest path :", all_1st_elite_dist[gen - 1],"km\nRoute  : ", best_chromosome)





# main code

start_time = time.time()
if __name__ == "__main__":
    GA()
print("Run time : %1.3f seconds " %(time.time() - start_time) )
