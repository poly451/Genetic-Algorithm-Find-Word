import random, sys
from datetime import datetime
import os


# -------------------------------------------------------

def get_unique_filename(my_prefix, my_extension):
    now = datetime.now()
    # year = now.year
    # month = now.month
    # day = now.day
    # minute = now.minute
    # second = now.second
    # microsecond = now.microsecond
    filename = "{}_{}_{}_{}__{}_{}_{}{}".format(my_prefix, now.year, now.month, now.day,
                                                now.minute, now.second, now.microsecond, my_extension)
    # print(filename)
    # sys.exit()
    return filename

# -------------------------------------------------------

def save_population_results(brain, score, spread, found_food):
    # time_saved = datetime.now()
    food = ""
    brain_string = ""
    for key, value in brain.items():
        brain_string += key + "~~" + value + "||"
    if found_food:
        food = "T"
    else: food = "F"
    with open("brains.txt", "a") as f:
        s = str(score) + "__" + brain_string + "__" + str(spread) + "__" + food + "\n"
        f.write(s)

def save_new_population(population):
    print_string = ""
    for critter in population:
        brain_string = ""
        for brain_cell in critter:
            # print(brain_cell)
            brain_string += brain_cell[0] + "~~" + brain_cell[1] + "||"
        print_string += brain_string + "\n"
    # print(print_string)
    new_filename = get_unique_filename("brains", ".txt")
    new_filename = os.path.join("data", new_filename)
    with open(new_filename, "w") as f:
        f.write(print_string)

# -------------------------------------------------------

def get_random_action():
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

def get_brain():
    brain = {}
    with open("data01.txt", "r") as f:
        mylist = f.readlines()
    mylist = [i.strip() for i in mylist]
    for i, elem in enumerate(mylist):
        index = elem.find("|")
        # brain[elem[:5]] = elem[5 + 1:]
        brain[elem[:5]] = get_random_action()
        # new_brain[str(i)] = elem[5 + 1:]
    return brain

# -------------------------------------------------------

def _get_actions():
    actions = []
    with open("data01.txt", "r") as f:
        mylist = f.readlines()
    mylist = [i.strip() for i in mylist]
    for i, elem in enumerate(mylist):
        index = elem.find("|")
        # brain[elem[:5]] = elem[5 + 1:]
        actions.append(elem[5+1:])
        # new_brain[str(i)] = elem[5 + 1:]
    return actions

# -------------------------------------------------------

def get_random_thoughts():
    # Might be better to just assign the values randomly?
    counting_list = []
    random_list = []
    brain = get_brain()
    actions = _get_actions()
    random.shuffle(actions)
    random_brain = {}
    for a_brain, an_action in zip(brain, actions):
        # print(a_brain, an_action)
        random_brain[a_brain] = an_action
    return random_brain

# -------------------------------------------------------

def interpret_action_string(action_string):
    if not "x" in action_string:
        return action_string
    mylist = []
    if action_string[0] == "x":
        mylist.append(0)
    if action_string[1] == "x":
        mylist.append(1)
    if action_string[2] == "x":
        mylist.append(2)
    if action_string[3] == "x":
        mylist.append(3)
    if action_string[4] == "x":
        mylist.append(4)
    # randomly choose one of these spaces
    mymarker = random.randint(0, len(mylist) - 1)
    # myindex is the index of action_string that I want to turn to a "1"
    myindex = mylist[mymarker]
    newstring = ""
    for i in range(len(action_string)):
        if i == myindex:
            newstring += "1"
        else:
            newstring += "0"
    return newstring

# -------------------------------------------------------

def read_generation_file_as_list():
    # bain cell is a list rather than a dictionary
    filepath = "generation01.txt"
    with open(filepath, "r") as f:
        mylist = f.readlines()
    # There are going to be about 100 or so elements in mylist
    mylist = [i.strip() for i in mylist]
    ts = ""
    generation = []
    for elem in mylist:
        brain_cell = []
        ts = elem
        n1 = ts.find("__")
        NUM_GENS = int(ts[0:n1])
        ts = ts[n1+2:]

        for _ in range(32):
            CELL1_1 = ts[0:ts.find("~~")]
            ts = ts[ts.find("~~") + 2:]
            CELL1_2 = ts[0:ts.find("||")]
            ts = ts[ts.find("||") + 2:]
            brain_cell.append([CELL1_1, CELL1_2])

        ts = ts[ts.find("__")+2:]
        spread = ts[0:ts.find("__")]
        ts = ts[ts.find("__") + 2:]
        food_found = False
        if ts == "F":
            food_found = False
        elif ts == "T":
            food_found = True
        # --------------------------------------
        generation.append([brain_cell, spread, food_found])
        # --------------------------------------
    # for elem in brain:
    #     print(elem[1])
    return generation

def read_generation_file():
    filepath = "generation01.txt"
    with open(filepath, "r") as f:
        mylist = f.readlines()
    # There are going to be about 100 or so elements in mylist
    mylist = [i.strip() for i in mylist]
    ts = ""
    generation = []
    for elem in mylist:
        brain_cell = {}
        ts = elem
        n1 = ts.find("__")
        NUM_GENS = int(ts[0:n1])
        ts = ts[n1+2:]

        for _ in range(32):
            CELL1_1 = ts[0:ts.find("~~")]
            ts = ts[ts.find("~~") + 2:]
            CELL1_2 = ts[0:ts.find("||")]
            ts = ts[ts.find("||") + 2:]
            brain_cell[CELL1_1] = CELL1_2

        ts = ts[ts.find("__")+2:]
        spread = ts[0:ts.find("__")]
        ts = ts[ts.find("__") + 2:]
        food_found = False
        if ts == "F":
            food_found = False
        elif ts == "T":
            food_found = True
        # --------------------------------------
        generation.append([brain_cell, spread, food_found])
        # --------------------------------------
    # for elem in brain:
    #     print(elem[1])
    return generation

# -------------------------------------------------------

if __name__ == "__main__":
    filename = get_unique_filename("myfile", ".txt")
    print(filename)
    # read_generation_file()
    # brain = get_brain()
    # save_brain(brain, 25, 10, False)