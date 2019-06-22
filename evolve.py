import utility
import numpy as np
import random, sys
import statistics

def sortSecond(val):
    return val[1]

# -------------------------------------------------------

def adjust_scores(generation):
    # Make sure that the critters that actually FOUND FOOD
    # aren't removed even if they have a low score.
    # -----------------------------------------
    # get the sum of all the spreads

    mylist = [j for i, j, k in generation]
    my_stdev = statistics.stdev([int(j) for i, j, k in generation])
    sum = 0
    for elem in generation:
        sum += int(elem[1])
    average = sum/len(generation)
    # -----------------------------------------
    for elem in generation:
        new_val = 0
        if elem[2] == True:
            # print(elem[1])
            # print(sum)
            # print(average)
            new_val = int(elem[1]) + average + my_stdev
            # print(new_val)
            elem[1] = new_val
    # -----------------------------------------
    # standardize the scores and turn them into floats
    for elem in generation:
        stand = (int(elem[1]) * 100)/100
        elem[1] = stand
    # -----------------------------------------
    # sort the scores
    generation.sort(key=sortSecond)
    # -----------------------------------------
    # find out how many slackers there are
    num_of_critters_to_cut = round((15 * len(generation))/100)
    # -----------------------------------------
    # take the hardest workers
    good_critters = generation[num_of_critters_to_cut:]
    # for elem in good_critters:
    #     print(elem)
    return good_critters

# -------------------------------------------------------

def remove_slackers(good_critters):

    # need to get top 15% of critters in order to clone them
    good_critters.sort(key=sortSecond, reverse=True)
    num_excellent_critters = round((15 * len(good_critters)/100))
    excellent_critters = good_critters[0:num_excellent_critters]

    # we want all the good critters and twice the number of excellent critters
    new_critters = []
    for elem in good_critters:
        new_critters.append(elem)
    for elem in excellent_critters:
        new_critters.append(elem)
        new_critters.append(elem)

    # now that we have our new generation we no longer need info
    # about the spread or whether this critter found food. Let's
    # strip that out.
    return_me = []
    for elem in new_critters:
        return_me.append(elem[0])
    return return_me

# -------------------------------------------------------

def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        myran = random.randint(0,1)
        if myran == 0:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# -------------------------------------------------------

def mutate_dna_segment(dna):
    new_dna = ""
    for elem in dna:
        # do we mutate this character?
        flip_bit = random.randint(0, len(dna) - 1)
        if flip_bit == 0:
            # let's mutate!
            if elem == "0":
                new_dna += "x"
            else:
                new_dna += "0"
        else:
            new_dna += elem
    # print("dna: {}".format(dna))
    # print("new dna: {}".format(new_dna))
    return new_dna

def mutate(child):
    new_child = []
    num_mutations = 0
    total = 0
    for elem in child:
        please_mutate = random.randint(0, 40)
        # please_mutate = 1 # <------ DEBUGGING
        if please_mutate == 1:
            dna = elem[1]
            # print(dna)
            dna = mutate_dna_segment(dna)
            # print(dna)
            # sys.exit()
            new_chromosome = [elem[0], dna]
            # print(elem)
            # print(new_chromosome)
            # sys.exit()
            new_child.append(new_chromosome)
            num_mutations += 1
        else:
            new_child.append(elem)
        total += 1
    # print(num_mutations)
    # print(child)
    # print(new_child)
    return new_child
# -------------------------------------------------------

def have_a_good_time(critters, max_population):
    if len(critters) >= max_population:
        print("Error in evolve.have_a_good_time. len(critters) >= max_population")
        sys.exit()
    be_safe = 0
    new_critters = critters
    while len(new_critters) <= max_population:
        parent1_num = random.randint(0, len(critters) - 1)
        parent2_num = random.randint(0, len(critters) - 1)
        parent1 = critters[parent1_num]
        parent2 = critters[parent2_num]
        child = crossover(parent1, parent2)
        # print("parent1: {}".format(parent1))
        # print("parent2: {}".format(parent2))
        # print("child  : {}".format(child))
        child = mutate(child)
        # print("child  : {}".format(child))
        new_critters.append(child)
        be_safe += 1
        if be_safe > max_population * 2:
            print("Error in evolve.have_a_good_time. while loop out of control.")
            sys.exit()
    return new_critters

        # mutation, anyone?
        # for elem in child1:
        #     print(elem)

# -------------------------------------------------------

def main():
    max_population = 200
    generation = utility.read_generation_file_as_list()
    # for elem in generation:
    #     print(elem)
    # sys.exit()
    # --------------------------------------------------------------
    # we measures the success of a critter in an environment
    # by giving it a score. But we want to look for different things --
    # we value different things -- depending on the characteristics of
    # the population. eg., in the beginning we value variation
    # (move variation=more possible solutions), but once
    # there is enough variety then we might value efficiency.
    generation = adjust_scores(generation)
    # --------------------------------------------------------------
    # we've adjusted the weights, now we just need to remove the
    # critters with the lowest scores, etc.
    hard_workers = remove_slackers(generation)
    # for elem in hard_workers:
    #     print(elem)
    # sys.exit()
    new_gen = have_a_good_time(hard_workers, max_population) # crossover
    utility.save_new_population(new_gen)
    # for i, elem in enumerate(new_gen):
    #     print(i, elem)

if __name__ == "__main__":
    print("--- Begin Program ---")
    main()
    print("--- End Program ---")