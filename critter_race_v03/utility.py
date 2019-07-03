import random, sys
from datetime import datetime
import json
import dill
import constants as con
import os

# -------------------------------------------------------

def get_hex_value_from_colour_value(colour_value):
    # remove blank spaces
    c = colour_value.replace(" ","")
    # print("colour value: {}".format(c))
    if c == "brown": return "#8B7D6B"
    if c == "red": return "#CD2626"
    if c == "lightred": return "#FF4040"
    if c == "darkred": return "#A52A2A"
    if c == "beige": return "#FFD39B"
    if c == "yellow": return "#FFD700"
    if c == "black": return "#000000"
    if c == "white": return "#FFFFFF"
    if c == "pink": return "#FF69B4"
    if c == "lightgreen": return "#9AFF9A"
    if c == "darkgreen": return "#548B54"
    if c == "green": return "#6B8E23"
    if c == "blue" : return "#2933C0"

def get_colour_value_from_hex_value(hex_value):
    # c = hex_value.replace("#","")
    c = hex_value
    # print("hex value: {}".format(c))
    if c == "#8B7D6B" : return "brown"
    if c == "#CD2626" : return "red"
    if c == "#FF4040" : return "light red"
    if c == "#A52A2A" : return "dark red"
    if c == "#FFD39B" : return "beige"
    if c == "#FFD700" : return "yellow"
    if c == "#000000" : return "black"
    if c == "#FFFFFF" : return "white"
    if c == "#FF69B4" : return "pink"
    if c == "#9AFF9A" : return "light green"
    if c == "#548B54" : return "dark green"
    if c == "#6B8E23" : return "green"
    if c == "#2933C0" : return "blue"

def get_random_colour():
    # no white because that is the current background color
    colours = ["brown", "red", "lightred", "darkred", "beige", "yellow", "black"]
    colours.append("pink")
    colours.append("lightgreen")
    colours.append("darkgreen")
    colours.append("green")
    colours.append("blue")
    myran = random.randint(0, len(colours)-1)
    return colours[myran]

def get_color(pattern):
    if pattern=="000000": return "red"
    elif pattern=="000010": return "orange"
    elif pattern=="000100": return "pink"
    elif pattern=="001000": return "blue"
    elif pattern=="010000": return "green"
    elif pattern=="100000": return "yellow"
    elif pattern=="000001": return "gold"
    else:
        s="this pattern ({}) was not found.".format(pattern)
        sys.exit(s)

def get_unique_filename(my_prefix, my_extension=".txt"):
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

def get_unique_id():
    now = datetime.now()
    id = "{}{}{}{}{}{}".format(now.year, now.month, now.day, now.minute, now.second, now.microsecond)
    return id

# -------------------------------------------------------

def save_population_results(brain, score, spread, found_food, filename):
    # time_saved = datetime.now()
    food = ""
    brain_string = ""
    for cell in brain:
        brain_string += cell[0] + "~~" + cell[1] + "||"
    if found_food:
        food = "T"
    else: food = "F"
    with open(filename, "a") as f:
        s = str(score) + "__" + brain_string + "__" + str(spread) + "__" + food + "\n"
        f.write(s)

def save_dill_pickle(filename, myobject):
    # json_string = json.dumps(myobject)
    with open(filename, "wb") as dill_file:
        dill.dump(myobject, dill_file)

def load_dill_pickle(filename):
    with open(filename, 'rb') as dill_file:
        myobject = dill.load(dill_file)
    # datastore = json.loads(json_string)
    return myobject

def save_json(filename, datastore):
    json_string = json.dumps(datastore)
    with open(filename, 'w') as f:
        json.dump(datastore, f)

def append_json(filename, datastore):
    json_string = json.dumps(datastore)
    with open(filename, 'a') as f:
        json.dump(datastore, f)

def load_json(filename):
    with open(filename, 'r') as dill_file:
        datastore = json.load(dill_file)
    return datastore

def append_to_file(filename, data):
    with open(filename, 'a') as f:
        f.write(data)

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

def remove_files(mydirectory, text_match):
    os.chdir(mydirectory)
    myfiles = os.listdir(mydirectory)
    to_delete = []
    for file in myfiles:
        if text_match in file:
            to_delete.append(file)
    # [print(i) for i in to_delete]
    for file in to_delete:
        os.remove(file)

# -------------------------------------------------------

if __name__ == "__main__":
    filename = get_unique_filename("myfile", ".txt")
    print(filename)
