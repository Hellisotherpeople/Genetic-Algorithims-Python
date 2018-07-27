import pandas as pd
from jellyfish import hamming_distance
import random
from random import choice
import heapq
from itertools import tee, chain, starmap, islice
import string


def random_string_array(string_size, num_strings):
    rand_arr = ["".join([choice(string.printable) for i in range(string_size)])
                for j in range(num_strings)]
    return rand_arr


def crossover(s1, s2, target_string):
  # at a random chiasma
    r = random.randint(1, len(target_string))
    return s1[:r]+s2[r:], s2[:r]+s1[r:]


def mutate(a_string, probability):

    # TODO: make it choose only currently wrong parts of the string to mutate over... or maybe not - research this!
    string_list = list(a_string)
    for i in range(0, len(string_list)):
        random_letter = random.choice(string.printable)
        if random.random() < probability:
            string_list[i] = random_letter
    return "".join(string_list)


def find_differing_indexs(s1, s2):
    return [i for i, (c1, c2) in enumerate(zip(s1, s2)) if c1 != c2]


def mutate_domain_specific(a_string, target_string):
    indexs = find_differing_indexs(a_string, target_string)
    string_list = list(a_string)
    random_letter = random.choice(string.printable)
    for elem in indexs:
        string_list[elem] = random_letter
    return "".join(string_list)


def select_fitness(population, target, population_size):
    fitness_size = population_size * 2 
    res_list = fitness_size * [None]
    for index, a_str in enumerate(population):
        comp_dist = hamming_distance(a_str, target)
        res_list[index] = (index, a_str, comp_dist)  # index, string, fitness
    return res_list


def pairwise(iterable):
    # modified pairwise, s0(s1).. s2(s3) ... s4(s5).....
    i = iter(iterable)
    while True:
        yield next(i), next(i)


def gen_children(population_list, target_string):
    children_list = []
    for s1, s2 in pairwise(population_list):
        child1, child2 = crossover(s1, s2, target_string)
        mut_child1 = mutate(child1, 0.05)
        mut_child2 = mutate(child2, 0.5)
        children_list.append(mut_child1)
        children_list.append(mut_child2)
    return children_list


def gen_children_size(population_list, target_string, population_size):
    children_list = population_size * [None]
    i = 0 
    for s1, s2 in list(pairwise(population_list)): 
        child1, child2 = crossover(s1, s2, target_string)
        mut_child1 = mutate(child1, 0.05)
        mut_child2 = mutate(child2, 0.5)
        children_list[i] = mut_child1
        children_list[i + 1] = mut_child2
        i = i + 2
    return children_list




def gen_children_domain(population_list, target_string):
    children_list = []
    for s1 in population_list:
        mut_child = mutate_domain_specific(s1, target_string)
        children_list.append(mut_child)
    return children_list


def truncation_selection(selection_list, num):
    ten_best_fitnesses = heapq.nsmallest(
        num, selection_list, key=lambda x: x[2])
    return ten_best_fitnesses


def genetic_string_matching(target_string, population_size):
    stop = False
    iteration = 0
    population_list = random_string_array(
        len(target_string), population_size)
    while stop is False:
        children_list = gen_children_size(population_list, target_string, population_size)

        combined_list = chain(population_list, children_list)
        #print(len(list(combined_list)))
        fit_list = select_fitness(combined_list, target_string, population_size)
        #print(len(fit_list))
        best_10 = truncation_selection(fit_list, population_size)
        best = best_10[0]
        if iteration % 30 == 0:
            print("-----------ITERATION NUM:" + str(iteration))
            print(best)
        iteration = iteration + 1
        population_list = [i[1] for i in best_10]

        if best[2] == 0:
            stop = True
            print(best)

    return best

genetic_string_matching("I like big butts and I can not lie, 123456!", 100)
#population_list = random_string_array(10, 100) 

#the_list = gen_children_size(population_list, "Ilikebigbu", 100)
#print(len(the_list))
