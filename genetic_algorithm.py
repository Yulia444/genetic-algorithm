from random import randint, choice
import math
import copy


def probability(chromosome, population, distances):
    path = sum_path(chromosome, distances)
    paths = [sum_path(chrmosome, distances) for chrmosome in population]
    filtered_paths = []
    for p in paths:
        if p not in filtered_paths:
            filtered_paths.append(p)
    return (1 / path) / sum([1 / p for p in paths])


def seletion(population, distances, count):
    ppltn = copy.deepcopy(population)
    ppltn = sorted(ppltn, key=lambda x: probability(x, population, distances), 
                   reverse=True)
    return ppltn[:count]


def mutation(chromosome):
    chromosome = chromosome[:-1]
    index1 = choice([i for i in range(len(chromosome))])
    index2 = choice([i for i in range(len(chromosome)) if i != index1])
    chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
    chromosome.append(chromosome[0])
    return chromosome


def crossing(chromosome1, chromosome2):
    chromosome1 = chromosome1[:-1]
    chromosome2 = chromosome2[:-1]
    parents = [chromosome1, chromosome2]
    length = len(chromosome1)
    child = []
    for gen in range(length):
        if gen == 0:
            selected_gen = choice([i for i in range(length)])
            child.append(selected_gen)
        else:
            select_parent = choice([0, 1])
            index = parents[select_parent].index(child[gen-1])
            if index == length-1:
                left, right = index-1, -length
            elif index == 0:
                left, right = -1, index + 1
            else:
                left, right = index - 1, index + 1
            side = choice(['left', 'right'])
            if side == 'left' and parents[select_parent][left] not in child:
                selected_gen = parents[select_parent][left]
            elif side == 'right' and parents[select_parent][right] not in child:
                selected_gen = parents[select_parent][right]
            else:
                if side == "left" and parents[select_parent-1][left] not in child:
                    selected_gen = parents[select_parent-1][left]
                elif side == "right" and parents[select_parent-1][right] not in child:
                    selected_gen = parents[select_parent-1][right]
                else:
                    selected_gen = [i for i in range(length) if i not in child][0]
            child.append(selected_gen)
    child.append(child[0])
    return child


def build_path(count):
    cities = [_ for _ in range(count)]
    visited_cities = []
    start_city = randint(0, count-1)
    visited_cities.append(start_city)
    for i in range(len(cities)-1):
        next_city = choice([city for city in cities if city not in visited_cities])
        visited_cities.append(next_city)
    visited_cities.append(start_city)
    
    return visited_cities


def find_distance(first, second):
    X1, X2 = first[0], second[0]
    Y1, Y2 = first[1], second[1]
    if Y1 == Y2:
        return math.fabs(X2-X1)
    elif X1 == X2:
        return math.fabs(Y2-Y1)
    else:
        return math.sqrt((X2-X1)**2 + (Y2-Y1)**2)


def matrix_distance(nodes):
    count = len(nodes.keys())
    i, j = 0, 0
    distance_matrix = [[0]*count for i in range(count)]
    for key1 in nodes.keys():
        for key2 in nodes.keys():
            distance_matrix[i][j] = find_distance(nodes[key1], nodes[key2])
            j+=1
        i+=1
        j=0
    return distance_matrix


def sum_path(visited_cities, distances):
    sum = 0
    for i in range(1, len(visited_cities)):
        prev, now = visited_cities[i-1], visited_cities[i]
        if prev < now:
            sum += distances[prev][now]
        elif prev > now:
            sum += distances[now][prev]
    return sum


def find_short_distance(nodes):
    count = len(list(nodes.keys()))
    distances = matrix_distance(nodes)
    population = [build_path(count) for _ in range(count)]
    distances_set = set()
    generations = 40
    for generation in range(generations):
        offspring = []
        for i in range(5):
            child = crossing(population[randint(0, len(population[:count])-1)], 
                             population[randint(0, len(population[:count])-1)])
            child = mutation(child)
            offspring.append(child)
            distances_set.add(sum_path(offspring[i], distances))
            
        population.extend(seletion(offspring, distances, count))
        population = sorted(population, key=lambda x: sum_path(x, distances))
    built_path = [list(nodes.keys())[population[0][i]] for i in range(len(population[0]))]
    return built_path





