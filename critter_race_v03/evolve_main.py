import utility
import random
import constants as con
import sys
import tkinter as tk
import threading
import evolve_helper as evolve
from operator import itemgetter, attrgetter
import display
import os

# ==================================================================
#                         Critter
# ==================================================================

class Critter:
    def __init__(self, d):
        self.p = False
        self.id = d["id"]
        self.score = d["score"]
        self.x = d["x"]
        self.y = d["y"]
        self.food_x = d["food_x"]
        self.food_y = d["food_y"]
        self.end_x = d["end_x"]
        self.end_y = d["end_y"]
        self.colour = d["colour"]
        self.brain = d["brain"]
        # self.brain_phenotype = d["brain_phenotype"]

    def __repr__(self):
        s = ""
        s += "id: {}, calculated score: {}, calculated spread: {}, ".format(self.id, self.get_score(), self.get_spread())
        s += "x,y: {},{} end_x,end_y: {},{} ".format(self.x, self.y, self.end_x, self.end_y)
        s += "food_x,food_y: {},{}, colour: {}, ".format(self.food_x, self.food_y, self.colour)
        s += "EVOLVED SCORE: {}\n".format(self.score)
        s += "brain: {}".format(self.brain)
        # s += "brain phenotype: {}".format(self.brain_phenotype)
        if self.x == self.food_x and self.y == self.food_y:
            s += "\nFOOD FOUND!!!!!!"
        return s

    def get_score(self):
        x_diff = abs(self.x - self.food_x)
        y_diff = abs(self.y - self.food_y)
        return x_diff + y_diff

    def get_spread(self):
        x_diff = abs(con.CRITTER_START_X - self.end_x)
        y_diff = abs(con.CRITTER_START_Y - self.end_y)
        return x_diff + y_diff

    def get_food_found(self):
        if self.get_score() == 0:
            return True
        return False

    def look_up(self, food_x, food_y):
        if self.y == 0:
            return False
        new_x = self.x
        new_y = self.y - 1
        if new_x == food_x:
            if new_y == food_y:
                self.food_seen = True
                return True
        return False

    def look_down(self, food_x, food_y):
        if self.x == con.BOARDSIZE:
            return False
        new_x = self.x
        new_y = self.y + 1
        if new_x == food_x:
            if new_y == food_y:
                self.food_seen = True
                return True
        return False

    def look_right(self, food_x, food_y):
        if self.y == con.BOARDSIZE:
            return False
        new_x = self.x + 1
        new_y = self.y
        if new_x == food_x:
            if new_y == food_y:
                self.food_seen = True
                return True
        return False

    def look_left(self, food_x, food_y):
        if self.x == 0:
            return False
        new_x = self.x - 1
        new_y = self.y
        if new_x == food_x:
            if new_y == food_y:
                self.food_seen = True
                return True
        return False

    # -----------------------------------------------------------

    # def search_for_x(self):
    #     for cell in self.brain:
    #         if "x" in cell[1]:
    #             return True
    #     return False

    def dna_okay(self):
        for cell in self.brain:
            counter = 0
            for gene in cell[1]:
                # print("gene: ", gene)
                if gene == "1":
                    counter += 1
            if counter > 1:
                return False
        return True

    # -----------------------------------------------------------

    def move_up(self):
        if self.y > 0:
            self.y -= 1
            if self.p: print("moving UP: -y: {}".format(self.y))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move_down(self):
        if (self.y * con.CRITTER_SIZE) < (con.BOARDSIZE) - con.CRITTER_SIZE:
            self.y += 1
            if self.p: print("moving DOWN: +y: {}".format(self.y))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move_left(self):
        # print("in Critters.move_left. self.x: {}, self.y: {}".format(self.x, self.y))
        if self.x > 0:
            self.x -= 1
            if self.p: print("moving LEFT: -x: {}".format(self.x))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move_right(self):
        # print("in Critters.move_right. self.x: {}, self.y: {}".format(self.x, self.y))
        # if (self.x * self.size) < self.board_size - self.size:
        if (self.x * con.CRITTER_SIZE) < ((con.BOARDSIZE) - con.CRITTER_SIZE):
            self.x += 1
            if self.p: print("moving RIGHT: +x: {}".format(self.x))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def critter_found_food(self):
        if self.x == self.food_x:
            if self.y == self.food_y:
                return True
        return False

    def look_around(self):
        """Produces a string that represents the world as the critter sees it at that time. Eg: 00010."""
        # ------------------------
        senses = ""
        # ------------------------
        if self.look_up(self.food_x, self.food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.look_down(self.food_x, self.food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.look_right(self.food_x, self.food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.look_left(self.food_x, self.food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.critter_found_food():
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        return senses

    # -----------------------------------------------------------

    def move(self, action):
        if len(action) != 6:
            s = "Error in evolve_main.py def move(self, action). len(action) != 6"
            sys.exit(s)
        if action == "000000":
            pass
        elif action == "100000":
            # up
            self.move_up()
        elif action == "010000":
            # down
            self.move_down()
        elif action == "001000":
            # right
            self.move_right()
        elif action == "000100":
            # left
            self.move_left()
        elif action == "000010":
            # eat
            if self.get_food_found() == True:
                # minimum score possible, which is zero.
                self.end_x = self.x
                self.end_y = self.y
                return True
        elif action == "000001":
            rand_index = random.randint(0, 4)
            s = ""
            for i in range(5):
                if i == rand_index:
                    s += "1"
                else:
                    s += "0"
            s += "0"
            action = s
            # print(action)
            # sys.exit()
            self.move(action)
        return False

    # -----------------------------------------------------------

    def decide_on_action(self, sensed):
        """ Decides on the action the player will take. If random, that's cashed out."""
        action_to_take = "-1"
        for cell in self.brain:
            if cell[0] == sensed:
                return cell[1]
        s = "Error in Critter.decide_on_action. That sensed pattern was not found."
        sys.exit(s)

    # -----------------------------------------------------------

    def generation(self, max_steps):
        r = False
        for i in range(max_steps):
            mysenses = self.look_around()
            myaction = self.decide_on_action(mysenses)
            # print(myaction)
            success = self.move(myaction)
            if success == True:
                print("Success!!!! You ({}) found AND ATE the cheese.".format(self.id))
                self.end_x = self.x
                self.end_y = self.y
                r = True
                break
        if self.p: print("You ({}) failed!!!".format(self.id))
        self.end_x = self.x
        self.end_y = self.y
        if self.p: print("------------- failure ----------------")
        return r

    # -----------------------------------------------------------

    def display(self):
        print("-----------------------------------------------------")
        print("player: {},{}".format(self.x, self.y))
        print("food: {},{}".format(self.food_x, self.food_y))
        print("-----------------------------------------------------")

    # -----------------------------------------------------------

    def get_list(self):
        """ This is the list we'll save (JSON) and use to evolve the population. """
        mylist1 = [self.id, self.score, con.CRITTER_START_X, con.CRITTER_START_Y]
        mylist2 = [con.FOOD_START_X, con.FOOD_START_Y, self.end_x, self.end_y, self.colour, self.brain]
        mylist = mylist1 + mylist2
        return mylist

# ==================================================================
#                         Critters
# ==================================================================

class Critters:
    def __init__(self, max_steps=20):
        self.p = False
        self.critters = []
        self.max_steps = max_steps

    def __repr__(self):
        s = ""
        for critter in self.critters:
            s += "---------------- a_critter.id: {} -------------------\n".format(critter.id)
            s += critter.__repr__() + "\n"
        return s

    def __getitem__(self, item):
        return self.critters[item]

    def __setitem__(self, key, value):
        self.critters[key] = value

    def __delitem__(self, key):
        newlist = []
        for i, elem in enumerate(self.critters):
            if key != i:
                newlist.append(elem)
        self.critters = newlist

    def __len__(self):
        return len(self.critters)

    # -----------------------------------------------------------

    def add_critter(self, critter):
        self.critters.append(critter)

    def remove_critter(self, critter_id):
        new_pop = []
        for critter in self.critters:
            if critter.id == critter_id:
                pass
            else:
                new_pop.append(critter)
        self.critters = new_pop

    def get_critter(self, x, y):
        for critter in self.critters:
            if critter.x == x and critter.y == y:
                return critter
        return None

    # -----------------------------------------------------------

    def move(self):
        for critter in self.critters:
            if self.p: print("---- critter.id: {} ----".format(critter.id))
            critter.generation(self.max_steps)
            # print(critter)
            # sys.exit()

    # -----------------------------------------------------------

    # def search_for_x(self):
    #     for critter in self.critters:
    #         if critter.search_for_x():
    #             # print(critter)
    #             return True
    #     return False

    def dna_okay(self):
        for critter in self.critters:
            if not critter.dna_okay():
                print("DNA not okay! ({})".format(critter.brain))
                return False
        return True

    # -----------------------------------------------------------

    def get_highest_score(self):
        max_score = -1
        for critter in self.critters:
            if critter.get_score() > max_score:
                max_score = critter.get_score()
        return max_score

    def calculate_score(self):
        """ 1. get highest score, 2. flip the scores, 3. add max score if found food
        4. If you moved, make sure your score isn't zero.
        """
        highest_score = self.get_highest_score()
        if highest_score == -1:
            s = "evolve02.py. Error in Critters.calculate_score. max_score = -1."
            sys.exit(s)
        for critter in self.critters:
            new_score = abs(critter.get_score() - highest_score)
            critter.score = new_score
            if critter.end_x == con.FOOD_START_X:
                if critter.end_y == con.FOOD_START_Y:
                    new_score += highest_score
            if critter.get_spread() > 0:
                critter.score += (highest_score/len(self.critters))

    # -----------------------------------------------------------

    def get_list(self):
        new_list = []
        for critter in self.critters:
            new_list.append(critter.get_list())
        return new_list

    # -----------------------------------------------------------

    def are_we_done_yet(self):
        result = []
        total = len(self.critters)
        won = 0
        for critter in self.critters:
            if critter.critter_found_food():
                won += 1
        percent = round((won / total) * 100)
        result.append(percent)
        if total == won:
            result.append(True)
        else:
            result.append(False)
        return result

    # -----------------------------------------------------------

    def display(self):
        s = ""
        for i in range(con.TILES_WIDE):
            l = ""
            for j in range(con.TILES_WIDE):
                temp = "[ ]"
                a_critter = self.get_critter(j, i)
                if a_critter == None:
                    pass
                else:
                    temp = "[C]"
                if j == con.FOOD_START_X and i == con.FOOD_START_Y:
                    if temp == "[C]":
                        temp = "[X]"
                    else:
                        temp = "[F]"
                l += temp
            s += l + "\n"
        print(s)

    # -----------------------------------------------------------

    def write_to_file(self, filename):
        all_critters = []
        for critter in self.critters:
            a_critter = critter.get_list()
            all_critters.append(a_critter)
        utility.save_json(filename, all_critters)

# ==================================================================
#                         SetUpGame
# ==================================================================

class SetUpGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.center(self)

    def center(self, myroot):
        # from:
        # https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        # Gets the requested values of the height and width.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        # print("Width", windowWidth, "Height", windowHeight)
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

    # start_game = SetUpGame()
    # start_game.mainloop()

# ==================================================================
# ==================================================================

def search_for_x(population):
    brain = population[0][-1]
    for i in range(len(population)):
        brain = population[i][-1]
        for elem in brain:
            # print(elem[1])
            if "x" in elem[1]:
                return True
    return False

def alive(new_gen, number_of_generations):
    new_population = new_gen
    p = False
    for j in range(number_of_generations):
        mycritters = Critters()
        for i in range(len(new_population)):
            mydict = {}
            mydict["id"] = new_population[i][0]
            mydict["score"] = new_population[i][1]
            mydict["x"] = new_population[i][2]
            mydict["y"] = new_population[i][3]
            mydict["food_x"] = new_population[i][4]
            mydict["food_y"] = new_population[i][5]
            mydict["end_x"] = -1
            mydict["end_y"] = -1
            mydict["colour"] = new_population[i][8]
            mydict["brain"] = new_population[i][9]
            # mydict['brain_phenotype'] = new_population[i][10]
            mycritter = Critter(mydict)
            mycritters.add_critter(mycritter)

        if not mycritters.dna_okay():
            s = "Something is wrong with he critters DNA! Error in evolve_main.py in def alive."
            sys.exit(s)
        mycritters.move()
        if p: print(mycritters)
        mycritters.calculate_score()
        # print(mycritters)
        # sys.exit()
        # -------------------------------------------------------
        # check to see how many (if any) critters have found the food.
        # -------------------------------------------------------
        the_result = mycritters.are_we_done_yet()
        print("the result: {}".format(the_result))
        if the_result[1]:
            print("All the critters found the food!!!! :-D")
            print("Number of steps: {}".format(j))
            new_filename = utility.get_unique_filename("evolved", ".txt")
            mycritters.write_to_file(new_filename)
            sys.exit()
        print(mycritters)
        # -------------------------------------------------------
        # print(mycritters)
        new_filename = utility.get_unique_filename("evolved", ".txt")
        mycritters.write_to_file(new_filename)
        # -------------------------------------------------------
        # display.main()
        # -------------------------------------------------------
        needs_evaluation = mycritters.get_list()
        new_population = evolve.evolve_population(needs_evaluation)
        # print(new_generation)
        # new_population = new_generation

if __name__ == "__main__":
    # -------------- Clear log files ------------------------
    utility.remove_files(os.getcwd(), "evolved_")
    # -------------------------------------------------------
    num_critters = 3
    number_of_generations = 3
    new_population = evolve.create_critters(num_critters)
    alive(new_population, number_of_generations)
    # [print(i) for i in new_population]