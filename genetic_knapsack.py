from bitarray import bitarray
from itertools import islice, dropwhile, filterfalse, compress, accumulate, takewhile, chain
from functools import reduce
import random
from random import randint
import operator
from collections import deque



def random_bool_list(num_of_bools):
    return [random.choice([True, False]) for i in range(0, num_of_bools)]

class Knapsack:

    # TODO: Random bitset function

    def __init__(self, items, weights, profits, num_genes, max_weight, num_iterations):
        self.items = items
        self.itemlen = len(items)
        self.weights = weights
        self.profits = profits
        self.num_genes = num_genes
        self.genes = num_genes * [None]
        self.max_weight = max_weight
        self.num_iterations = num_iterations



    def randomize_genes(self):
        generated_genes = self.num_genes * [None]
        for i in range(0, self.num_genes):
            generated_genes[i] = bitarray(random_bool_list(self.itemlen))
        return generated_genes

    def get_fitness_indexs(self, population):
        # shouldn't need this
        fitness_indexes = []
        for index, elem in enumerate(population):
            if elem is True:
                fitness_indexes.append(index)
        return fitness_indexes

    def compute_fitness_for_gene(self, to_reduce, gene):
        compressed = compress(to_reduce, gene)
        # we want to use accumulate for the future time when we want to throw out all genes whose weight goes over the limit
        return reduce(lambda x, y: x+y, compressed, 0)
        #return takewhile(lambda x: x < self.max_weight, accumulate(compressed, operator.add))

    def get_final_fitness(self, n, iterable):
        # modified tail - we only want the final value, not an iterator to it
        return next(iter(deque(iterable, maxlen=n)))

    def crossover(self, bitarr1, bitarr2):
        r = randint(1, self.itemlen)
        return bitarr1[:r] + bitarr2[r:], bitarr2[:r]+bitarr1[r:]

    def pairwise(self, iterable):
        # modified pairwise, s0(s1).. s2(s3) ... s4(s5).....
        i = iter(iterable)
        while True:
            yield next(i), next(i)

    def mutate(self, bitarr, probability):
        # random bit flip
        for i in range(0, self.itemlen):
            if random.random() < probability:
                bitarr[i] = not bitarr[i]
        return bitarr

    def gen_children(self, population_list):
        children_list = self.num_genes * [None]
        i = 0
        for ba1, ba2 in self.pairwise(population_list):
            child1, child2 = self.crossover(ba1, ba2)
            mut_child1 = self.mutate(child1, 0.7)
            mut_child2 = self.mutate(child2, 0.3)
            children_list[i] = mut_child1
            children_list[i + 1] = mut_child2
            i = i + 2
        return children_list

    def compute_weights_values(self, population_list):
        fitness_size = self.num_genes * 2 
        values_list = fitness_size * [None]
        for index, a_gene in enumerate(population_list):
            canidate = True
            value = self.compute_fitness_for_gene(self.profits, a_gene)
            weight = self.compute_fitness_for_gene(self.weights, a_gene)
            if weight > self.max_weight: 
                canidate = False
            values_list[index] = (a_gene, value, weight, canidate)# profit, weight
        maximized_profits = sorted(values_list, key=lambda x: x[1], reverse=True)
        sorted_list = sorted(maximized_profits, key=lambda x: x[3], reverse=True)
        return sorted_list


    def truncation_selection(self, selection_list, num):
        selection = selection_list[0:num]
        return selection

    def genetic_knapsack(self):
        randomized_genes = self.randomize_genes()
        self.genes = randomized_genes
        #print(self.genes)
        iteration = 0
        stop = False
        the_best = 0
        while stop is False:
            children_list = self.gen_children(self.genes)
            combined_list = chain(self.genes, children_list)
            fit_list = self.compute_weights_values(combined_list)
            best_half = self.truncation_selection(fit_list, self.num_genes)
            best = best_half[0]
            if best != the_best:
                print("----------------ITERATION NUM:" + str(iteration))
                print(best)
            iteration = iteration + 1
            the_best = best
            self.genes = [i[0] for i in best_half] # Prematurly converging... need to guarantee some randomness 
            #for i in range(self.itemlen, self.itemlen - 10, -1):
            #    self.genes[i] == randomized_genes[i]
            if iteration > self.num_iterations:
                stop = True
                print("BEST FOUND:")
                print(best)
        return self.genes



items=[20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
         130, 140, 150, 160, 170, 180, 190, 200, 210, 220]

weights=[2, 12, 14, 18, 19, 21, 23, 30, 33, 35, 37,
           39, 40, 43, 48, 49, 60, 68, 70, 78, 80]

profits=[200, 300, 400, 500, 600, 700, 800, 950, 980, 100, 300,
           300, 140, 190, 160, 230, 180, 300, 200, 350, 680]

def random_list(upto, num_of_nums):
    return random.sample(range(1, upto), num_of_nums)


random_profits = random_list(100000, 1000)
random_weights = random_list(10000, 1000)
random_items = random_weights


a_knapsack = Knapsack(random_items, random_weights, random_profits, 100, 2500000, 20000)

gene1 = a_knapsack.genetic_knapsack()

#gene2 = a_knapsack.randomize_genes()
#children = a_knapsack.gen_children(gene2)
#print(children)
#print(a_knapsack.mutate(gene2, 0.5))

# print(a_knapsack.mutate(gene1, 0.3))
#pairwise_genes=a_knapsack.compute_fitness_for_gene(weights, gene1)

#gene_list = a_knapsack.compute_weights_values(chain(gene2, children))
#maximized_profits = sorted(gene_list, key=lambda x: x[1], reverse=True)

#minimized_weights = sorted(maximized_profits, key=lambda x: x[3], reverse=True)


#print(a_knapsack.truncation_selection(gene_list, 100)[0])
# print(gene1, gene2)


# new_gene1, new_gene2 = a_knapsack.crossover(gene1, gene2)

# print("crossed over genes:")
# print(new_gene1, new_gene2)
