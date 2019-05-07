from random import randint
import sys
"""
=======================================================
                class Myitem
=======================================================
"""
class Myitem:
    pool = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, length_of_target, id=-1):
        self.id = id
        self.chosen = False
        self.standardized_score = 0.0
        self.DNA = self.create_gene(length_of_target)
        self.fitness_score = 0

    def add_critter_from_file(self, fileline):
        mylist = fileline.split(",")
        self.id = int(mylist[0].strip())
        self.chosen = mylist[1].strip()
        self.fitness_score = int(mylist[2].strip())
        self.standardized_score = float(mylist[3].strip())
        self.DNA = mylist[4].strip()

    def create_critter(self, id, old_critter):
        self.id = id
        self.chosen = False
        self.standardized_score = 0.0
        self.fitness_score = 0
        self.DNA = old_critter.DNA


    def calculate_fitness_score(self, target):
        if len(target) == 0:
            sys.exit("Error. The length of 'target' should not be 0. Error in Myitem.calculate_fitness_score")
        if len(self.DNA) == 0:
            sys.exit("This critter has no DNA!!! Error in def calculate_fitness_score in class Myitems.")
        tempscore = 0
        # a point for every correct letter
        for letter in target:
            if letter in self.DNA:
                tempscore += 1
        # a point for every correct letter in the correct place.
        # NOTE: This one works a bit too well! Get the correct
        # result in about 20 generations.
        # for i in range(len(target)):
        #     if target[i] == self.DNA[i]:
        #         tempscore += 1
        # a point for every two letters that are correct and in the correct order.
        for i in range(len(target)):
            if target[i:i+2] == self.DNA[i:i+2]:
                tempscore += 1

        self.fitness_score = tempscore
        return tempscore

    def create_gene(self, DNA_length):
        # print("debugging: {}".format(DNA_length))
        this_DNA = ""
        for i in range(DNA_length):
            random_gene = self.pool[randint(0, len(self.pool)-1)]
            this_DNA = "{}{}".format(this_DNA, random_gene)
        # check data:
        # print("gene_length: {}".format(len(this_DNA)))
        # print("gene: {}".format(this_DNA))
        return this_DNA

    def calculate_standardized_score(self, total_fitness_scores, offset):
        # This is the individual's chance of reproducing
        if total_fitness_scores == 0:
            sys.exit("Error in Myitem.calculate_standardized_score. total_fitness_scores == 0")
        if self.fitness_score == 0:
            self.standardized_score = 0.0
        else:
            if offset > 0:
                self.standardized_score = (self.fitness_score/total_fitness_scores) * offset
            else:
                self.standardized_score = (self.fitness_score/total_fitness_scores)

    # -----------------------------------------------------

    def crossover(self, partner, new_id):
        child = Myitem(len(self.DNA), new_id)
        if len(self.DNA) == 0:
            sys.exit("Error in Myitem.mutation. len(self.DNA) == 0")
        random_index = randint(0, len(self.DNA)-1)
        child_DNA = self.DNA[:random_index]
        child_DNA = "{}{}".format(child_DNA, partner.DNA[random_index:])
        child.DNA = child_DNA
        # print("my ID: {}, my DNA: {}, my partner's DNA: {}, my child's DNA: {}".format(self.id, self.DNA, partner.DNA, child_DNA))
        # sys.exit("Debugging: Myitem.crossover --- end ---")
        return child

    def mutate(self, percent):
        new_strand = ""
        # print("mutate: before: {}".format(self.DNA))
        for gene in self.DNA:
            random_number = randint(1, 100)
            # chance_of_mutation = percent
            if random_number <= percent:
                r1 = randint(0, len(self.pool)-1)
                new_letter = self.pool[r1]
                new_strand = "{}{}".format(new_strand, new_letter)
                # print("r1: {}, new_letter: {}, new_strand: {}".format(r1, new_letter, new_strand))
            else:
                new_strand = "{}{}".format(new_strand, gene)
        self.DNA = new_strand
        # print("mutate: after: {}".format(self.DNA))

    # -----------------------------------------------------

    def debug_print(self):
        print("id: {}, chosen: {}, standardized_score: {:.6}, fitness_score: {}, DNA: {}".format(self.id,
                                                                                              self.chosen,
                                                                                              self.standardized_score,
                                                                                              self.fitness_score,
                                                                                              self.DNA))
"""
=======================================================
                class Mypopulation
=======================================================
"""
class Mypopulation:
    item_id = 0
    number_of_generations = 0

    def __init__(self, population = []):
        self.item_id = 0
        self.population = population
        self.target = ""
        self.max_population_size = 0
        self.total_fitness = 0
        self.number_of_generations = 0
        self.average_fitness = 0.0

    def initialize_population(self):
        self.item_id = 0
        self.population = []
        self.target = ""
        self.max_population_size = 0
        self.total_fitness = 0
        self.number_of_generations = 0
        self.average_fitness = 0.0

    def create_random_population(self, target, max_population, offset):
        self.offset = offset
        self.max_population_size = max_population
        self.target = target
        self.population = []
        self._create_population()
        # Calculate scores
        self.calculate_fitness_scores_for_each_critter()
        self.total_fitness = self.calculate_total_fitness()
        self.average_fitness = self.calculate_average_fitness()
        self.calculate_standardized_scores(self.total_fitness, self.offset)

    def _create_population(self):
        for i in range(self.max_population_size):
            self.item_id += 1
            critter = Myitem(len(self.target), id=self.item_id)
            # print(critter.id)
            self.population.append(critter)

    def calculate_fitness_scores_for_each_critter(self):
        for critter in self.population:
            critter.calculate_fitness_score(self.target)

    def create_population_from_file(self):
        with open("critters.txt", "r") as f:
            mylist = f.readlines()
        mylist = [i.strip() for i in mylist]
        self.target = mylist[0]
        self.max_population_size = int(mylist[1])
        mylist = mylist[2:]
        for i in range(len(mylist)):
            critter = Myitem(len(self.target))
            critter.add_critter_from_file(mylist[i])
            self.add_critter(critter)
        self.debug_print()

    def add_critter(self, critter):
        if self.max_population_size == 0:
            sys.exit("Error in Myitem.add_critter. The maximum population size CANNOT be 0.")
        if len(self.population) >= self.max_population_size:
            mystring = "Error in Myitem.add_critter(). The population is at maximum! Cannot add any more!!!\n"
            mystring += "If you don't believe me, here it is, see for yourself:"
            print(mystring)
            self.debug_print()
            sys.exit("Error in Myitem.add_critter(). The population is at maximum! Cannot add any more!!!")
        self.population.append(critter)

    # ----------------------------------------------------

    def fitnessSort(self, elem):
        return elem[2]

    def sort_by_fitness_score(self):
        mylist = []
        for critter in self.population:
            myelem = []
            myelem.append(critter.id)
            myelem.append(critter.chosen)
            myelem.append(critter.fitness_score)
            myelem.append(critter.standardized_score)
            myelem.append(critter.DNA)
            mylist.append(myelem)
        # print(mylist)
        mylist.sort(key=self.fitnessSort, reverse=True)
        return mylist

    def calculate_total_fitness(self):
        total_fitness = 0
        for critter in self.population:
            total_fitness += critter.fitness_score
        if total_fitness == 0 and self.number_of_generations > 1:
            sys.exit("Error in Mypopulation.calculate_total_fitness. Total_fitness == 0")
        return total_fitness

    def calculate_average_fitness(self):
        if len(self.population) == 0:
            return 0.0
        return self.calculate_total_fitness()/len(self.population)

    def calculate_standardized_scores(self, total_fitness, offset):
        if total_fitness == 0:
            sys.exit("Error in Mypopulation.calculate_standardized_scores. total_fitness == 0")
        for critter in self.population:
            critter.calculate_standardized_score(total_fitness, offset)

    def calculate_average_fitness_of_breeding_pool(self, breeding_pool):
        if len(breeding_pool) == 0:
            sys.exit("Error in calculate_average_fitness_of_breeding_pool. len(breeding_pool) == 0")
        temptotalfit = 0
        for critter in breeding_pool:
            temptotalfit += critter.fitness_score
        return temptotalfit/len(breeding_pool)

    # ----------------------------------------------------
    #               get_breeding_pool
    # ----------------------------------------------------

    def get_breeding_pool(self):
        # print("---- entered get_breeding_pool ----")
        breeding_pool = []
        if len(self.population) == 0:
            sys.exit("self.population = 0. This shouldn't be. Error in Mypopulation.get_breeding_pool()")
        for critter in self.population:
            for i in range(round(critter.standardized_score)):
                # critter.debug_print()
                breeding_pool.append(critter)

        # Sometimes the breeding pool (because of rounding error)
        # has more or fewer critters than the population. Let's
        # make sure that the breeding population has at least max_pop
        # individuals in it.

        besafe = 0
        while len(breeding_pool) < self.max_population_size:
            # print("len(breeding_pool): {}, len(self.population): {}".format(len(breeding_pool), len(self.population)))
            # add a random individual from the population
            myran = randint(0, len(self.population)-1)
            breeding_pool.append(self.population[myran])
            besafe += 1
            if besafe > 10000:
                sys.exit("Error in Mypopulation.get_breeding_pool. besafe > 10,000")

        # print("---- exited get_breeding_pool ----")
        return breeding_pool

    def target_reached(self):
        for critter in self.population:
            if critter.DNA == self.target:
                return True
        return False
    
    # ----------------------------------------------------
    #               crossover_and_mutation
    # ----------------------------------------------------

    def crossover_and_mutation(self, breeding_pool):
        change_of_mutation = 1
        # self.not_fit_enough()

        new_population = Mypopulation()
        new_population.initialize_population()
        # print("^^^^^^^ In crossover_and_mutation: len(new_population.population): {}, new_population.max_pop: {}".format(
        #     len(new_population.population),
        #     new_population.max_population_size))
        # new_population.debug_print()


        new_population.max_population_size = self.max_population_size
        new_population.target = self.target
        new_population.number_of_generations = self.number_of_generations + 1
        # new_population.offset = self.offset

        besafe = 0
        while len(new_population.population) < new_population.max_population_size:
            # Choose parents
            random_index = randint(0, len(breeding_pool) - 1)
            parent1 = breeding_pool[random_index]

            random_index = randint(0, len(breeding_pool) - 1)
            parent2 = breeding_pool[random_index]

            self.item_id += 1
            child1 = parent1.crossover(parent2, self.item_id)

            self.item_id += 1
            child2 = parent2.crossover(parent1, self.item_id)

            child1.mutate(change_of_mutation)
            child2.mutate(change_of_mutation)

            new_population.add_critter(child1)
            new_population.add_critter(child2)

            # print("&&&&&&&& children: &&&&&&&&")
            # child1.debug_print()
            # child2.debug_print()

            besafe += 1
            if besafe > 10000:
                sys.exit("Something has gone wrong in crossover_and_mutation. besafe is > 10000.")
        return new_population




    # =========== Main Procedures =================

    # ----------------------------------------------------
    #               evaluate_population
    # ----------------------------------------------------

    def evaluate_population(self, offset):
        self.calculate_fitness_scores_for_each_critter()
        self.total_fitness = self.calculate_total_fitness()
        self.average_fitness = self.calculate_average_fitness()
        self.calculate_standardized_scores(self.total_fitness, offset)

    # ----------------------------------------------------
    #               breed_population
    # ----------------------------------------------------

    def breed_population(self, multiplication_factor):
        # Figure out how many copies of each critter will
        # go into the breeding pool. A critter with a standardized score
        # of 0 has no chance, where one who has a score of 4 will have
        # 4 copies in the breeding pool.

        # print("&&&&&&&&&&&& Entering breed_population &&&&&&&&&&&&&")

        size_of_population = len(self.population)
        breeding_pool = self.get_breeding_pool()
        size_of_breeding_pool = len(breeding_pool)
        # print("size of population: {}, size of breeding pool: {}".format(size_of_population, size_of_breeding_pool))
        #
        # print("-------------- Breeding Pool ----------------")
        # [i.debug_print() for i in breeding_pool]
        # print("Average fitness of breeding pool: {}".format(self.calculate_average_fitness_of_breeding_pool(breeding_pool)))
        # print("---------------------------------------------")

        # if size_of_population != size_of_breeding_pool:
            # sys.exit("The size of the population ({}) != the size of the breeding_pool ({}).".format(size_of_population, size_of_breeding_pool))
            # print("ATTENTION!!!!! The size of the population ({}) != the size of the breeding_pool ({}).".format(size_of_population, size_of_breeding_pool))
        if len(breeding_pool) == 0:
            sys.exit("There is no breeding pool! Error in breed_population()")
        # print("&&&&&&&&&&&& Leaving breed_population &&&&&&&&&&&&&")
        return breeding_pool
        # print("Children:")
        # [i.debug_print() for i in children]

    # ----------------------------------------------------
    #               debug printing
    # ----------------------------------------------------

    def debug_population_DNA(self):
        mystring = ""
        for critter in self.population:
            mystring = "{} {}".format(mystring, critter.DNA)
        print(mystring)

    def debug_print(self):
        print("--------------- debug print (begin) ----------------")
        if len(self.population) == 0:
            print("self.population: {}".format(self.population))
        if len(self.population) > 0:
            print("ID CHOSEN STANDARD_SCORE FITNESS DNA")
        for critter in self.population:
            critter.debug_print()
            # total_fitness += critter.calculate_fitness_score

        print("target: {}".format(self.target))
        print("number of generations: {}".format(self.number_of_generations))
        print("max_pop_size: {}".format(self.max_population_size))
        print("population_size: {}".format(len(self.population)))
        print("total_population_fitness: {}".format(self.calculate_total_fitness()))
        print("average_fitness: {}".format(self.calculate_average_fitness()))
        # for critter in self.population:
        #     critter.debug_print()
        # print("ID, CHOSEN, FITNESS, STANDARDIZED_SCORE, DNA")
        # mylist = self.sort_by_fitness_score()
        # [print(i) for i in mylist]
        print("--------------- debug print (end) ----------------")

# =====================================================================
# =====================================================================

def save_fitness_values(list_of_fitness_values):
    # clear the file
    print("fitness values: {}".format(list_of_fitness_values))
    filename = "logfile.txt"
    open(filename, 'w').close()
    with open(filename, 'a') as file:
        for item in list_of_fitness_values:
            # print(item)
            mystr = "{}{}".format(str(item), " ")
            file.write(mystr)

# =====================================================================

def main():
    max_pop = 1000
    offset = max_pop
    target = "evolution"
    number_of_generations = 10000
    population_fitness_values = []
    breeding_population_fitness_values = []
    # ------------------------------
    mytext = "Searching for: {}".format(target)
    # ------------------------------
    critters = Mypopulation()
    # critters.create_population_from_file()
    critters.create_random_population(target, max_pop, offset)
    # critters.debug_print()
    if critters.target_reached() == True:
        sys.exit("We did it! :-D")
    # ------------------------------
    # critters.debug_print()
    breeding_population = critters.breed_population(offset)
    breeding_population_fitness = critters.calculate_average_fitness_of_breeding_pool(breeding_population)
    breeding_population_fitness_values.append((breeding_population_fitness))
    # The following takes a list of children and makes them a Mypopulation object.
    critters = critters.crossover_and_mutation(breeding_population)
    critters.evaluate_population(offset)
    average_fitness = critters.calculate_average_fitness()
    # print("average fitness: {}".format(average_fitness))
    population_fitness_values.append(average_fitness)

    # critters.debug_print()
    if critters.target_reached() == True:
        print("We did it! :-D")
    # ------------------------------

    breeding_population = critters.breed_population(offset)
    breeding_population_fitness = critters.calculate_average_fitness_of_breeding_pool(breeding_population)
    breeding_population_fitness_values.append((breeding_population_fitness))
    critters = critters.crossover_and_mutation(breeding_population)
    critters.evaluate_population(offset)
    average_fitness = critters.calculate_average_fitness()
    # print("average fitness: {}".format(average_fitness))
    population_fitness_values.append(average_fitness)

    # critters.debug_print()
    if critters.target_reached() == True:
        print("We did it! :-D")

    for i in range(number_of_generations):
        # ------------------------------
        breeding_population = critters.breed_population(offset)
        breeding_population_fitness = critters.calculate_average_fitness_of_breeding_pool(breeding_population)
        breeding_population_fitness_values.append((breeding_population_fitness))
        critters = critters.crossover_and_mutation(breeding_population)
        critters.evaluate_population(offset)
        average_fitness = critters.calculate_average_fitness()
        # print("gen: {}, average fitness: {}".format(critters.number_of_generations, average_fitness))
        population_fitness_values.append(average_fitness)

        # critters.debug_print()
        if critters.target_reached() == True:
            # critters.debug_print()
            print("Found word ({}) after {} generations.".format(target, critters.number_of_generations))
            print("Population size: {}".format(max_pop))
            sys.exit("We did it! :-D")
    # ------------------------------
    # critters.debug_population_DNA()
    # save_fitness_values(population_fitness_values)


if __name__ == "__main__":
    main()
