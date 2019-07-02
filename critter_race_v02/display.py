import tkinter as tk
import sys
import utility
import constants as con
from operator import itemgetter, attrgetter
import evolve02 as evolve
import time
import os

# ==================================================================
#                         Critter
# ==================================================================

class Critter:

    def __init__(self, canvas, critter_attributes):
        self.p = False
        self.canvas = canvas
        d = critter_attributes
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
        block_critter_x = self.x * con.CRITTER_SIZE
        block_critter_y = self.y * con.CRITTER_SIZE
        self.body = self.canvas.create_rectangle(block_critter_x, block_critter_y,
                                                    block_critter_x + con.CRITTER_SIZE,
                                                    block_critter_y + con.CRITTER_SIZE,
                                                    fill="green")

    # -----------------------------------------------------------

    def critter_found_food(self):
        if self.x == self.food_x:
            if self.y == self.food_y:
                print("found food: critter: {},{}, food: {},{} ".format(self.x, self.y, self.food_x, self.food_y))
                return True
        return False

    # -----------------------------------------------------------

    def move_up(self):
        if self.y > 0:
            self.y -= 1
            self.canvas.move(self.body, 0, -20)
            if self.p: print("moving UP: -y: {}".format(self.y))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move_down(self):
        if (self.y * con.CRITTER_SIZE) < (con.BOARDSIZE) - con.CRITTER_SIZE:
            self.y += 1
            self.canvas.move(self.body, 0, 20)
            if self.p: print("moving DOWN: +y: {}".format(self.y))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move_left(self):
        # print("in Critters.move_left. self.x: {}, self.y: {}".format(self.x, self.y))
        if self.x > 0:
            self.x -= 1
            self.canvas.move(self.body, -20, 0)
            if self.p: print("moving LEFT: -x: {}".format(self.x))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move_right(self):
        # print("in Critters.move_right. self.x: {}, self.y: {}".format(self.x, self.y))
        # if (self.x * self.size) < self.board_size - self.size:
        if (self.x * con.CRITTER_SIZE) < ((con.BOARDSIZE) - con.CRITTER_SIZE):
            self.x += 1
            self.canvas.move(self.body, 20, 0)
            if self.p: print("moving RIGHT: +x: {}".format(self.x))
            # self.world.new_player_position(self.x, self.y)

    # -----------------------------------------------------------

    def move(self, action):
        if action == "00000":
            pass
        elif action == "10000":
            # up
            self.move_up()
        elif action == "01000":
            # down
            self.move_down()
        elif action == "00100":
            # right
            self.move_right()
        elif action == "00010":
            # left
            self.move_left()
        elif action == "00001":
            # eat
            if self.critter_found_food() == True:
                # minimum score possible, which is zero.
                self.end_x = self.x
                self.end_y = self.y
                return True
        return False

    # -----------------------------------------------------------

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

    def look_around(self):
        """Produces a string that represents the world as the critter sees it at that time. Eg: 00010."""
        if self.p: print("player: {},{}".format(self.x, self.y))
        if self.p: print("food: {},{}".format(self.food_x, self.food_y))
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
        # print(world)
        return senses

    # -----------------------------------------------------------

    def decide_on_action(self, sensed):
        for cell in self.brain:
            if cell[0] == sensed:
                return cell[1]
        s = "Error in Critter.decide_on_action. That sensed pattern was not found."
        sys.exit(s)

# ==================================================================
#                         SetUpGame
# ==================================================================

class SetUpGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.after_id = None
        self.ready = False
        self.max_steps = 20
        self.generation_counter = 0
        self.step_counter = 0
        self.after_id = None
        self.center(self)
        self.bind('<Escape>', self.program_close)
        self.body = None
        self.board_width = con.TILES_WIDE * con.CRITTER_SIZE
        # ---------------------------------------
        self.canvas = tk.Canvas(self, width=self.board_width, height=self.board_width)
        self.canvas.pack(fill="both", expand=True)
        # ---------------------------------------
        self.filenames = self.get_filenames(os.getcwd(), "evolved_")
        self.display_best_critter()

    def display_best_critter(self):
        if self.ready == False:
            if self.generation_counter > len(self.filenames):
                print("That's all folks!")
                sys.exit()
            critters = utility.load_json(self.filenames[self.generation_counter])
            self.generation_counter += 1
            sorted_critters = sorted(critters, key=itemgetter(1), reverse=True)
            # get best performing critter of population/generation
            sorted_critters = sorted_critters[0]
            # sorted_critters = sorted_critters[-1]
            # ---------------------------------------
            critter_score = sorted_critters[1]
            critter_start_x = sorted_critters[2]
            critter_start_y = sorted_critters[3]
            critter_end_x = sorted_critters[6]
            critter_end_y = sorted_critters[7]
            food_start_x = sorted_critters[4]
            food_start_y = sorted_critters[5]
            critter_colour = sorted_critters[8]
            critter_brain = sorted_critters[9]
            # ---------------------------------------
            block_food_x = food_start_x * con.FOOD_SIZE
            block_food_y = food_start_y * con.FOOD_SIZE
            self.food = self.canvas.create_rectangle(block_food_x, block_food_y, block_food_x + con.FOOD_SIZE,
                                                     block_food_y + con.FOOD_SIZE, fill="red")

            # ---------------------------------------

            d = {}
            d["id"] = sorted_critters[0]
            d["score"] = critter_score
            d["x"] = critter_start_x
            d["y"] = critter_start_y
            d["food_x"] = food_start_x
            d["food_y"] = food_start_y
            d["end_x"] = critter_end_x
            d["end_y"] = critter_end_y
            d["colour"] = critter_colour
            d["brain"] = critter_brain
            # ---------------------------------------
            self.mycritter = Critter(self.canvas, d)
            self.ready = True
            self.move()
        self.after_id2 = self.after(1000, self.display_best_critter)

    def move(self):
        if self.ready == True:
            self.step_counter += 1
            print("step_counter: {}".format(self.step_counter))
            sensed = self.mycritter.look_around()
            myaction = self.mycritter.decide_on_action(sensed)
            success = self.mycritter.move(myaction)
            if success == True:
                print("Food found!!!")
                # sys.exit()
            if self.step_counter > self.max_steps:
                # self.canvas.delete(self.body)
                self.canvas.delete("all")
                self.after_cancel(self.after_id)
                self.after_id = None
                self.step_counter = 0
                self.ready = False
                return True
        self.after_id = self.after(500, self.move)

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

    def get_filenames(self, mydirectory, text_match):
        os.chdir(mydirectory)
        myfiles = os.listdir(mydirectory)
        to_return = []
        for filename in myfiles:
            if text_match in filename:
                to_return.append(filename)
        # [print(i) for i in to_return]
        return to_return

    def program_close(self, event):
        sys.exit()

# ==================================================================
# ==================================================================

def main():
    start_game = SetUpGame()
    start_game.mainloop()

if __name__ == "__main__":
    main()
