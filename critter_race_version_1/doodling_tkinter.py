import tkinter as tk
import sys, random
import utility, time
# import threading
# timer = None
# seconds = 1  # Initial time must be the time+1 (now 0+1)
# ==================================================================
#                         WorldMap
# ==================================================================

class WorldMap:
    def __init__(self, tiles_wide, player_x, player_y, food_x, food_y):
        self.tiles_wide = tiles_wide
        self.world_map = self.initialize_world()
        self.player_x = player_x
        self.player_y = player_y
        self.food_x = food_x
        self.food_y = food_y

    def __repr__(self):
        s = "player position: {},{}\n".format(self.player_x, self.player_y)
        s += "food position: {},{}\n".format(self.food_x, self.food_y)
        for i in range(self.tiles_wide):
            r = ""
            for j in range(self.tiles_wide):
                if self.player_x == i and self.player_y == j:
                    r += "[P]"
                elif self.food_x == i and self.food_y == j:
                    r += "[F]"
                else:
                    r += "[.]"
            s += r + "\n"
        return s

    def player_found_food(self):
        if self.player_x == self.food_x:
            if self.player_y == self.food_y:
                return True
        return False

    def new_food_position(self, x, y):
        self.food_x = y
        self.food_y = x
        # print("food position: {},{}".format(self.food_x, self.food_y))

    def new_player_position(self, x, y):
        self.player_x = y
        self.player_y = x
        # print("player position: {},{}".format(self.player_x, self.player_y))

    def get_food_location(self):
        return self.food_x, self.food_y

    def initialize_world(self):
        temp_array = []
        for i in range(self.tiles_wide):
            row_array = []
            for j in range(self.tiles_wide):
                row_array.append("grass")
            temp_array.append(row_array)
        return temp_array

# ==================================================================
#                         Food
# ==================================================================

class Food:
    def __init__(self, canvas, x, y, food_size, world_map):
        self.x = x
        self.y = y
        self.food_size = food_size
        self.world_map = world_map
        self.canvas = canvas
        # self.body = self.canvas.create_rectangle(self.x, self.y, self.food_size, self.food_size, fill="#B20404")
        x = self.x * self.food_size
        y = self.y * self.food_size
        self.body = self.canvas.create_rectangle(x, y, x + self.food_size, y + self.food_size, fill="#B20404")
        # self.x += 1
        # self.canvas.move(self.body, 20, 0) # right
        # self.y += 1
        # self.canvas.move(self.body, 0, 20) # down
        self.world_map.new_food_position(self.x, self.y)
        # print("food position: {},{}".format(self.x, self.y))

# ==================================================================
#                         Player
# ==================================================================

class Player:
    def __init__(self, canvas, x, y, player_size, board_size, world_map):
        # myObject.__init__(self, canvas, x, y, player_size)
        self.initial_x = x
        self.initial_y = y
        self.player_size = player_size
        self.highest_x = 0
        self.highest_y = 0
        self.lowest_x = board_size
        self.lowest_y = board_size
        self.x = x
        self.y = y
        x = self.x * self.player_size
        y = self.y * self.player_size
        self.canvas = canvas
        self.board_size = board_size
        self.world_map = world_map
        print("initial player coords: {},{}".format(self.x, self.y))
        self.body = self.canvas.create_rectangle(x, y, x + self.player_size, y + self.player_size, fill="#476042")
        self.world_map.new_player_position(self.x, self.y)
        # -----------------------------------------------------
        self.brain = utility.get_brain()
        print(self.brain)
        # -----------------------------------------------------
        self.number_of_moves = 0
        self.did_eat = False
        self.score = 0
        # -----------------------------------------------------
        self.generation_counter = 0
        # -----------------------------------------------------
        self.update_loop()

    # ----------------------------------------------------------------

    def food_found(self):
        if self.world_map.player_found_food():
            return True
        return False

    def look_up(self, food_x, food_y):
        if self.y == 0:
            return False
        new_y = self.x
        new_x = self.y - 1
        if new_x == food_x:
            if new_y == food_y:
                return True
        return False

    def look_down(self, food_x, food_y):
        if self.x == self.board_size:
            return False
        new_x = self.x + 1
        new_y = self.y
        if new_x == food_x:
            if new_y == food_y:
                return True
        return False

    def look_right(self, food_x, food_y):
        if self.y == self.board_size:
            return False
        new_y = self.x
        new_x = self.y
        new_y += 1
        if new_x == food_x:
            if new_y == food_y:
                return True
        return False

    def look_left(self, food_x, food_y):
        if self.x == 0:
            return False
        new_x = self.x
        new_y = self.y - 1
        # print("new player coords: {},{}".format(new_x, new_y))
        if new_x == food_x:
            if new_y == food_y:
                return True
        return False

    def look_around(self):
        """Produces a string that represents the world as the critter sees it at that time. Eg: 00010."""
        food_x, food_y = self.world_map.get_food_location()
        print("player: {},{}".format(self.x, self.y))
        print("food: {},{}".format(food_x, food_y))
        senses = ""
        # ------------------------
        if self.look_up(food_x, food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.look_down(food_x, food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.look_right(food_x, food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.look_left(food_x, food_y):
            senses += "1"
        else:
            senses += "0"
        # ------------------------
        if self.food_found():
            senses += "1"
        else:
            senses += "0"
        print(self.world_map)
        return senses

    def react_to_environment(self, env):
        # This is the optimal reaction.
        # 00100
        thought = self.brain[env]
        # action_string = ""
        # if env[0] == 1:
        #     # eat!
        #     action_string = "10000"
        # if env[4] == 1:
        #     # move up
        #     action_string = "01000"
        # if env[3] == 1:
        #     # move down
        #     action_string = "00100"
        # if env[2] == 1:
        #     # move right
        #     action_string = "00010"
        # if  env[1] == 1:
        #     # move left
        #     action_string = "00001"
        return thought

    # ---------------------------------------------------

    def move_up(self):
        if self.y > 0:
            self.y -= 1
            self.canvas.move(self.body, 0, -20)
            self.world_map.new_player_position(self.x, self.y)

    def move_down(self):
        if (self.y * self.player_size) < self.board_size - self.player_size:
            self.y += 1
            self.canvas.move(self.body, 0, 20)
            self.world_map.new_player_position(self.x, self.y)

    def move_left(self):
        if self.x > 0:
            self.x -= 1
            self.canvas.move(self.body, -20, 0)
            self.world_map.new_player_position(self.x, self.y)

    def move_right(self):
        if (self.x * self.player_size) < self.board_size - self.player_size:
            self.x += 1
            self.canvas.move(self.body, 20, 0)
            self.world_map.new_player_position(self.x, self.y)

    def implement_action(self, action_string):
        # action_string = "10000"
        print("In 'implement_action': {}".format(action_string))

        if action_string[0] == '1':
            # eat!
            # at the moment the penalty for eating when there is no
            # food is a wasted move.
            print("eat!")

        if action_string[1] == '1':
            # move up
            print("move up")
            self.move_up()

        if action_string[2] == '1':
            # move down
            print("move down")
            self.move_down()

        if action_string[3] == '1':
            # move right
            print("move right")
            self.move_right()

        if action_string[4] == '1':
            # move left
            # self.move_left()
            print("move left")
            self.move_left()
    # ---------------------------------------------------

    def move_player(self, event):
        key = event.keysym
        # print("self.x: {}, self.y: {}".format(self.x, self.y))
        if key == "Left":
            if self.x > 0:
                self.x -= 1
                self.canvas.move(self.body, -20, 0)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "Right":
            if (self.x * self.player_size) < self.board_size-self.player_size:
                self.x += 1
                self.canvas.move(self.body, 20, 0)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "Up":
            if self.y > 0:
                self.y -= 1
                self.canvas.move(self.body, 0, -20)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "Down":
            if (self.y * self.player_size) < self.board_size - self.player_size:
                self.y += 1
                self.canvas.move(self.body, 0, 20)
                self.world_map.new_player_position(self.x, self.y)
        elif key == "m":
            for i in range(1000):
                # player is controlled by the program
                # string = (eg) 00100 # what the critter SEES
                # LOOK
                immediate_environment = self.look_around()
                print("immediate_environment: {}".format(immediate_environment))
                # --------------------
                # Action string is what the character has decided to do
                # THINK
                action_string = self.react_to_environment(immediate_environment)
                print("action_string: {}".format(action_string))
                # --------------------
                # we need to sort out strings of the form: "xxx0" etc
                action_string = utility.interpret_action_string(action_string)
                # --------------------
                # implement_action carries out the action the critter decided on.
                # MOVE
                self.implement_action(action_string)
                # --------------------
                self.number_of_moves += 1
                if self.food_found():
                    print("Food found! :-)")
                    print("Number of moves: {}".format(self.number_of_moves))
                    utility.save_brain(self.brain, self.number_of_moves)
                    sys.exit()
            print("Food NOT found")
            print("Number of moves: {}".format(self.number_of_moves))
            utility.save_brain(self.brain, self.number_of_moves)
            sys.exit()
        # -----------------------------------------------------
        self.number_of_moves += 1
        if self.food_found():
            print("Food found!!! :-)")
            self.did_eat = True
            if self.score == 0:
                self.score = self.number_of_moves
            print("Number of moves: {}".format(self.score))
        # print(self.world_map)


    def update_loop(self):
        # player is controlled by the program
        # string = (eg) 00100 # what the critter SEES
        # LOOK
        immediate_environment = self.look_around()
        print("immediate_environment: {}".format(immediate_environment))
        # --------------------
        # Action string is what the character has decided to do
        # THINK
        action_string = self.react_to_environment(immediate_environment)
        print("action_string: {}".format(action_string))
        # --------------------
        # we need to sort out strings of the form: "xxx0" etc
        action_string = utility.interpret_action_string(action_string)
        # --------------------
        # implement_action carries out the action the critter decided on.
        # MOVE
        self.implement_action(action_string)
        # --------------------
        if self.x > self.highest_x:
            print("highest x: ", self.x, self.highest_x)
            self.highest_x = self.x
        if self.y > self.highest_y:
            print("highest y: ", self.y, self.highest_y)
            self.highest_y = self.y
        if self.x < self.lowest_x:
            self.lowest_x = self.x
        if self.y < self.lowest_y:
            self.lowest_y = self.y
        # --------------------
        self.number_of_moves += 1
        if self.number_of_moves >= 1000:
            print("Food not found, critter has moved over {} times.".format(self.number_of_moves))
            print("spread x: {},{}".format(self.highest_x, self.lowest_x))
            print("spread y: {},{}".format(self.highest_y, self.lowest_y))
            spread = abs(self.highest_x - self.lowest_x) + abs(self.highest_y - self.lowest_y)
            print("spread: {}".format(spread))
            found_food = False
            utility.save_population_results(self.brain, self.number_of_moves, spread, found_food)
            sys.exit()
        if self.food_found():
            print("Food found! :-)")
            print("Number of moves: {}".format(self.number_of_moves))
            print("spread x: {},{}".format(self.highest_x, self.lowest_x))
            print("spread y: {},{}".format(self.highest_y, self.lowest_y))
            spread = abs(self.highest_x - self.lowest_x) + abs(self.highest_y - self.lowest_y)
            print("spread: {}".format(spread))
            found_food = True
            utility.save_population_results(self.brain, self.number_of_moves, spread, found_food)
        # --------------- Reset -------------------
        self.canvas.after(8, self.update_loop)

# ==================================================================
#                         Game
# ==================================================================

class Game(tk.Tk):
    def __init__(self, player_x, player_y, player_size, food_x, food_y, tiles_wide):
        tk.Tk.__init__(self)
        self.center(self)
        player_size = player_size
        self.tiles_wide = tiles_wide
        self.board_width = self.tiles_wide * player_size
        self.canvas = tk.Canvas(self, width=self.board_width, height=self.board_width)
        self.canvas.pack(fill="both", expand=True)
        self.world_map = WorldMap(self.tiles_wide, player_x, player_y, food_x, food_y)
        self.player = Player(self.canvas, player_x, player_y, player_size, self.board_width, self.world_map)
        self.food = Food(self.canvas, food_x, food_y, player_size, self.world_map)
        # self.world = self.initialize_world()
        self.bind("<Key>", self.player.move_player)
        self.bind('<Escape>', self.program_close)

    def program_close(self, event):
        print(self.world_map)
        # master.withdraw() # if you want to bring it back
        sys.exit()  # if you want to exit the entire thing

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

# ==================================================================
# ==================================================================

def main():
    # generate_random_weights()
    player_x = 5
    player_y = 5
    player_size = 20
    food_x = 2
    food_y = 3
    tiles_wide = 10
    game = Game(player_x, player_y, player_size, food_x, food_y, tiles_wide)
    game.mainloop()

if __name__ == "__main__":
    main()

