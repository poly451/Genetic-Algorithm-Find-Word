import utility
import numpy as np
import random, sys
import statistics
from operator import itemgetter
import dill
import constants as con

def sortSecond(val):
    return val[1]

# -------------------------------------------------------

def get_brain():
    the_environment = ["00000", "10000", "01000", "00100", "00010", "00001"]
    the_action = []
    for i in range(len(the_environment)):
        mystring = ""
        myran = random.randint(0, 5)
        for i in range(5+1):
            if myran == i:
                mystring += "1"
            else:
                mystring += "0"
        the_action.append(mystring)
    brain = []
    for env, act in zip(the_environment, the_action):
        brain.append([env, act])
    # print(brain)
    # sys.exit()
    return brain

# def get_brain():
#     brain = []
#     with open("data/data01.txt", "r") as f:
#         mylist = f.readlines()
#     mylist = [i.strip() for i in mylist]
#     for i, elem in enumerate(mylist):
#         # index = elem.find("|")
#         # brain[elem[:5]] = elem[5 + 1:]
#         sensed = elem[:5]
#         action = _get_random_action()
#         brain.append([sensed, action])
#         # brain[elem[:5]] = get_random_action()
#         # new_brain[str(i)] = elem[5 + 1:]
#     return brain

# -------------------------------------------------------

# def get_critters_for_testing(number_of_critters):
#     mycritters = []
#     for i in range(number_of_critters):
#         id = utility.get_unique_id()
#         score = random.randint(0, 8)
#         starting_x = 6
#         starting_y = 5
#         food_x = 2
#         food_y = 5
#         colour = utility.get_random_colour()
#         brain = get_brain()
#         mylist = [id, score, starting_x, starting_y, food_x, food_y, colour, brain]
#         mycritters.append(mylist)
#     return mycritters

# -------------------------------------------------------

# def get_phenotype(brain):
#     phenotype = []
#     for cell in brain:
#         action_to_take = cell[1]
#         if action_to_take != "000001":
#             phenotype.append([cell[0], action_to_take[:-1]])
#         else:
#             # move randomly
#             s = ""
#             ran_index = random.randint(0, 4)
#             for i in range(5):
#                 if ran_index == i:
#                     s += "1"
#                 else:
#                     s += "0"
#             action_to_take = s
#             phenotype.append([cell[0], action_to_take])
#     return phenotype

def create_critters(number_of_critters):
    mycritters = []
    for i in range(number_of_critters):
        id = utility.get_unique_id()
        score = 0
        starting_x = con.CRITTER_START_X
        starting_y = con.CRITTER_START_Y
        food_x = con.FOOD_START_X
        food_y = con.FOOD_START_Y
        end_x = 0
        end_y = 0
        brain = get_brain()
        colour = utility.get_color(brain[0][1])
        # brain_phenotype = get_phenotype(brain)
        mylist = [id, score, starting_x, starting_y, food_x, food_y, end_x, end_y, colour, brain]
        mycritters.append(mylist)
        # print(brain)
        # sys.exit()
    return mycritters

# -------------------------------------------------------

def _get_random_action():
    temp = ["","","","",""]
    myran = random.randint(0, 5)
    if myran == 0:
        return "00000"
    elif myran == 1:
        temp[random.randint(0, 4)] = "x"
    elif myran == 2:
        temp[random.randint(0, 4)] = "x"
        temp[random.randint(0, 4)] = "x"
    elif myran == 3:
        temp[random.randint(0, 4)] = "x"
        temp[random.randint(0, 4)] = "x"
        temp[random.randint(0, 4)] = "x"
    elif myran == 4:
        temp[random.randint(0, 4)] = "x"
        temp[random.randint(0, 4)] = "x"
        temp[random.randint(0, 4)] = "x"
        temp[random.randint(0, 4)] = "x"
    for i in range(5):
        if temp[i] == "":
            temp[i] = "0"
    return "".join(temp)

# -------------------------------------------------------

def generate_critter_brains(num_critters_in_population):
    """Creates random Critter brains."""
    brains = []
    for _ in range(num_critters_in_population):
        get_unique_id = utility.get_unique_id()
        brain = get_brain()
        brains.append([get_unique_id, brain])
    return brains

# -------------------------------------------------------

# def adjust_scores02(generation):
#     # Make sure that the critters that actually FOUND FOOD
#     # aren't removed even if they have a low score.
#     # -----------------------------------------
#     # get the sum of all the spreads
#
#     mylist = [j for i, j, k in generation]
#     mylist = [3, 0, 5, 4, 1, 8]
#     my_stdev = statistics.stdev([int(j) for i, j, k in generation])
#     sum = 0
#     for elem in generation:
#         sum += int(elem[1])
#     average = sum/len(generation)
#     # -----------------------------------------
#     for elem in generation:
#         new_val = 0
#         if elem[2] == True:
#             # print(elem[1])
#             # print(sum)
#             # print(average)
#             new_val = int(elem[1]) + average + my_stdev
#             # print(new_val)
#             elem[1] = new_val
#     # -----------------------------------------
#     # standardize the scores and turn them into floats
#     for elem in generation:
#         stand = (int(elem[1]) * 100)/100
#         elem[1] = stand
#     # -----------------------------------------
#     # sort the scores
#     generation.sort(key=sortSecond)
#     # -----------------------------------------
#     # find out how many slackers there are
#     num_of_critters_to_cut = round((15 * len(generation))/100)
#     # -----------------------------------------
#     # take the hardest workers
#     good_critters = generation[num_of_critters_to_cut:]
#     # for elem in good_critters:
#     #     print(elem)
#     return good_critters

# -------------------------------------------------------

def adjust_scores(generation, percentage_to_cut):
    generation.sort(key=sortSecond)
    # -----------------------------------------
    # find out how many slackers there are
    num_of_critters_to_cut = round((percentage_to_cut * len(generation))/100)
    # -----------------------------------------
    # take the hardest workers
    good_critters = generation[num_of_critters_to_cut:]
    return good_critters

# -------------------------------------------------------

def remove_slackers(good_critters, excellent_critter_percentage):

    # need to get top 15% of critters in order to clone them
    good_critters.sort(key=sortSecond, reverse=True)
    num_excellent_critters = round((excellent_critter_percentage * len(good_critters)/100))
    excellent_critters = good_critters[0:num_excellent_critters]

    # we want all the good critters and twice the number of excellent critters
    new_critters = []
    for elem in good_critters:
        new_critters.append(elem)
    for elem in excellent_critters:
        new_critters.append(elem)
        new_critters.append(elem)
    return new_critters

# -------------------------------------------------------

def crossover(parent1, parent2):
    new_id = utility.get_unique_id()
    new_score = 0
    starting_x = parent1[2]
    starting_y = parent1[3]
    food_x = parent1[4]
    food_y = parent1[5]
    end_x = parent1[6]
    end_y = parent1[7]
    child_brain = []
    for i in range(len(parent1[-1])):
        myran = random.randint(0,1)
        if myran == 0:
            child_brain.append(parent1[-1][i])
        else:
            child_brain.append(parent2[-1][i])
    colour = utility.get_color(child_brain[0][1])
    # print("brain: ", child_brain)
    # print("colour: ", colour)
    # sys.exit()
    child = [new_id, new_score, starting_x, starting_y, food_x, food_y, end_x, end_y, colour, child_brain]
    # The following assigns the critter a colour based on "00000"
    return child

# -------------------------------------------------------

def mutate_dna_segment(dna):
    new_dna = ""
    rand_index = random.randint(0, 5)
    for i in range(6):
        if i == rand_index:
            new_dna += "1"
        else:
            new_dna += "0"
    # print("dna: ", dna)
    # print("new_dna: ", new_dna)
    # sys.exit()
    return new_dna

def mutate(child, mutation_rate=20):
    new_brain = []
    dna_mutated = []
    num_mutations = 0
    total = 0
    for elem in child[-1]:
        please_mutate = random.randint(0, mutation_rate)
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
            new_brain.append(new_chromosome)
            num_mutations += 1
            dna_mutated.append(elem)
        else:
            new_brain.append(elem)
        total += 1
    # print("mutations: {}, total: {}".format(num_mutations, total))
    # print("mutations: {}, total: {}, dna: {}".format(num_mutations, total, dna_mutated))
    # give the new brain to the child
    child[-1] = new_brain
    return child

# -------------------------------------------------------

def have_a_good_time(critters, max_population, mutation_rate=40):
    # print(critters)
    # sys.exit()
    be_safe = 0
    new_critters = []
    while len(new_critters) < max_population:
        parent1_num = random.randint(0, len(critters) - 1)
        parent2_num = random.randint(0, len(critters) - 1)
        parent1 = critters[parent1_num]
        parent2 = critters[parent2_num]
        # print(parent1)
        # sys.exit()
        child = crossover(parent1, parent2)
        # print(child)
        # sys.exit()
        child = mutate(child, mutation_rate)
        # print(parent1)
        # print(parent2)
        # print(child)
        # sys.exit()
        new_critters.append(child)
        be_safe += 1
        if be_safe > max_population * 2:
            s="Error (evolve.py) in evolve.have_a_good_time. while loop out of control."
            sys.exit(s)
    return new_critters

# -------------------------------------------------------

def change_score(newval, oldlist):
    newlist = []
    newlist.append(oldlist[0])
    newlist.append(newval)
    newlist.append(oldlist[2])
    newlist.append(oldlist[3])
    newlist.append(oldlist[4])
    newlist.append(oldlist[5])
    newlist.append(oldlist[6])
    newlist.append(oldlist[7])
    return newlist

# -------------------------------------------------------

def evolve_population(last_gen, percent_cut=15, percent_double=15):
    # print("last gen")
    # print(last_gen)
    # sys.exit()
    # ----------------------------------------------------
    percentage_to_cut = percent_cut
    excellent_critter_percentage = percent_double
    max_population = len(last_gen)
    # ----------------------------------------------------
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
    generation = adjust_scores(last_gen, percentage_to_cut)
    # print(generation)
    # sys.exit()
    # --------------------------------------------------------------
    # we've adjusted the weights, now we just need to remove the
    # critters with the lowest scores, etc.
    hard_workers = remove_slackers(generation, excellent_critter_percentage)
    # print(hard_workers)
    # sys.exit()
    new_gen = have_a_good_time(hard_workers, max_population) # crossover
    # [print(i) for i in hard_workers]
    # [print(i) for i in new_gen]
    # sys.exit()
    # for i, elem in enumerate(new_gen):
    #     print(i, elem)
    return new_gen

    # -------------------------------------------------------

# def evolve_population(generation, percent_cut=15, percent_double=15):
#     if len(generation) == 0:
#         sys.exit("ERROR in evolve_population in evolve.py. len(generation) == 0")
#     # ----------------------------------------------------
#     percentage_to_cut = percent_cut
#     excellent_critter_percentage = percent_double
#     max_population = len(generation)
#     # ----------------------------------------------------
#     # for elem in generation:
#     #     print(elem)
#     # sys.exit()
#     # --------------------------------------------------------------
#     # we measures the success of a critter in an environment
#     # by giving it a score. But we want to look for different things --
#     # we value different things -- depending on the characteristics of
#     # the population. eg., in the beginning we value variation
#     # (move variation=more possible solutions), but once
#     # there is enough variety then we might value efficiency.
#     generation = adjust_scores(generation, percentage_to_cut)
#     # --------------------------------------------------------------
#     # we've adjusted the weights, now we just need to remove the
#     # critters with the lowest scores, etc.
#     hard_workers = remove_slackers(generation, excellent_critter_percentage)
#     new_gen = have_a_good_time(hard_workers, max_population) # crossover
#     # [print(i) for i in hard_workers]
#     # [print(i) for i in new_gen]
#     # sys.exit()
#     filename = utility.get_unique_filename("new_gen", ".txt")
#     utility.save_json(filename, new_gen)
#     # for i, elem in enumerate(new_gen):
#     #     print(i, elem)
#     return new_gen

# -------------------------------------------------------
# -------------------------------------------------------

def iterate_generations(generation, counter):
    counter -= 1
    pop01 = evolve_population(generation)
    # give the population dummy scores.
    for elem in pop01:
        elem[1] = random.randint(0, 32)
        print(elem[-1])
    # [print(i) for i in pop01]
    print("--------------------------------------------------")
    if counter > 0:
        iterate_generations(pop01, counter)

def random_selection():
    """ Thi is what happens when there's no selection pressure. """
    # The population converges on what, initially, are random values.
    new_population = get_critters_for_testing(6)
    iterate_generations(new_population, 100)
    print("--------------------------------------------------")
    pop01 = evolve_population(new_population)
    # give the population dummy scores.
    for elem in pop01:
        elem[1] = random.randint(0, 8)
    [print(i) for i in pop01]
    print("--------------------------------------------------")
    pop02 = evolve_population(pop01)
    # give the population dummy scores.
    for elem in pop02:
        elem[1] = random.randint(0, 8)
    [print(i) for i in pop02]
    print("--------------------------------------------------")
    pop03 = evolve_population(pop02)
    # give the population dummy scores.
    for elem in pop03:
        elem[1] = random.randint(0, 8)
    [print(i) for i in pop03]
    print("--------------------------------------------------")
    for elem in pop03:
        print(elem[7])

if __name__ == "__main__":
    critters = create_critters(1)
