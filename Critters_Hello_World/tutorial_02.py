import pygame, sys
import constants
import os
# from random import randint

"""
=======================================================
                   class Tile
=======================================================
"""
class Tile:
    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.contents = contents

    # --------------------------------------------------------------------------

    def draw(self, surface):
        tile_color = constants.UGLY_PINK
        color_selected = False
        if self.contents == "m":
            tile_color = constants.DARKGREY
            color_selected = True
            # print("There are mountains! {} and they are color: {}".format(self.contents, constants.DARKGREY))
        if self.contents == ".":
            tile_color = constants.GREEN
            color_selected = True
        if self.contents == "c":
            tile_color = constants.GREEN
            color_selected = True
        if self.contents == "f":
            tile_color = constants.DARKGREEN
            color_selected = True
        if self.contents == "p":
            tile_color = constants.BLUE
            color_selected = True
        if color_selected == True:
            # print("DRAWING {}".format(tile_color))
            myrect = pygame.Rect(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
            pygame.draw.rect(surface, tile_color, myrect)

    # --------------------------------------------------------------------------

    def list_to_string(self, mylist):
        mystring = ""
        for item in mylist:
            mystring = "{} {}".format(mystring, item.return_string())
        return mystring

    # --------------------------------------------------------------------------

    def print_string(self):
        return self.return_string()

    # --------------------------------------------------------------------------

    def return_string(self):
        return "{}-{}-{} || ".format(self.x, self.y, self.contents)

    # --------------------------------------------------------------------------

    def debug_print(self):
        print("{}-{}-{} || ".format(self.x, self.y, self.contents))

"""
=======================================================
                   class Food
=======================================================
"""

"""
=======================================================
                   class Player
=======================================================
"""

class Player:

    # face_direction = ['up', 'down', 'right', 'left', 'upper_right', 'upper_left', 'lower_right', 'lower_left']
    img = "/Users/BigBlue/Documents/Programming/images/player_characters/"
    actions = "look_forward, move_forward, eat, turn_right, turn_left"
    player_up = os.path.join(img, "dog01-up.png")
    player_down = os.path.join(img, "dog01-down.png")
    player_right = os.path.join(img, "dog01-right.png")
    player_left = os.path.join(img, "dog01-left.png")

    def __init__(self):
        # super().__init__(x, y, contents)
        self.facing_direction = 'up'
        self.take_action = "look_forward"
        self.food_ahead = False
        self.food_on_this_tile = False
        self.next_tiles = []
        self.this_tile = Tile(-1, -1, "")
        self.energy = 100
        self.image_up = pygame.image.load(self.player_up).convert_alpha()
        self.image_down = pygame.image.load(self.player_down).convert_alpha()
        self.image_right = pygame.image.load(self.player_right).convert_alpha()
        self.image_left = pygame.image.load(self.player_left).convert_alpha()
        # self.image.set_alpha(128)
        self.rect = self.image_up.get_rect()

    def re_init_vars(self):
        self.food_ahead = False
        self.food_on_this_tile = False

    def decide_how_to_act(self):
        # print("next tiles: {}".format(len(self.next_tiles)))
        if len(self.next_tiles) == 0:
            # print("len(next_tiles) = 0")
            print("POSSIBLE ERROR!!!! Player.decide_how_to_act(): len(next_tiles) == 0.")
        else:
            if self.food_on_this_tile == True:
                self.take_action = "eat"
                self.eat_helper()
                print("debugging (decide how to act): ate on tile {},{}".format(self.x, self.y))
            elif self.food_ahead == True:
                self.take_action = "move_forward"

    def critter_take_action(self):
        if self.take_action == "move_forward":
            if self.facing_direction == "up":
                self.move_up()
        if self.take_action == "eat":
            self.eat_helper()

    def eat_helper(self):
        print("CRITTER IS EATING!!!")
        self.energy += constants.FOOD_ENERGY
        # print("energy: {}".format(self.energy))

    def eat(self, myMap):
        this_tile = myMap.get_tile(self.x, self.y)
        # this_tile.debug_print()
        if this_tile.contents == "f":
            self.eat_helper()

    def look_ahead(self, myMap):
        print("----- look_head (begin) ------")
        mystring = Tile(-1, -1, "").list_to_string(self.next_tiles)
        print("next_tiles: {}".format(mystring))
        print("this tile: {}".format(self.this_tile.return_string()))
        print("food ahead: {}".format(self.food_ahead))
        print("food on this tile: {}".format(self.food_on_this_tile))
        # -------------------------------------
        temp_tiles = []
        if self.facing_direction == "up":
            print("squares, up")
            myrow = myMap.get_row(self.x)
            for tile in myrow:
                if tile.y < self.y:
                    # tile.debug_print()
                    temp_tiles.append(tile)
        if self.facing_direction == "down":
            print("squares, down")
            myrow = myMap.get_row(self.x)
            for tile in myrow:
                if tile.y > self.y:
                    # tile.debug_print()
                    temp_tiles.append(tile)
        if self.facing_direction == "right":
            # keep x constant and decrease x
            # mytile = myMap.get_tile(self.x, self.y-1)
            mycolumn = myMap.get_column(self.y)
            print("squares, left and right")
            for tile in mycolumn:
                if tile.x > self.x:
                    # tile.debug_print()
                    temp_tiles.append(tile)
        if self.facing_direction == "left":
            # keep x constant and decrease x
            # mytile = myMap.get_tile(self.x, self.y-1)
            mycolumn = myMap.get_column(self.y)
            print("squares, left and right")
            for tile in mycolumn:
                if tile.x < self.x:
                    # tile.debug_print()
                    temp_tiles.append(tile)
        self.next_tiles = temp_tiles
        mystring = [i.print_string() for i in self.next_tiles]
        # print("DEBUGGING: next_tiles: {}".format(mystring))
        self.this_tile = myMap.get_tile(self.x, self.y)

        # --------------------------------------------------
        self.food_ahead = False
        for mytile in self.next_tiles:
            if mytile.contents == "f":
                self.food_ahead = True

        # Is there food on the tile I'm standing on?
        self.food_on_this_tile = False
        if self.this_tile.contents == "f":
            self.food_on_this_tile = True
        # -------------------------------------
        print("---------------------------------")
        mystring = Tile(-1, -1, "").list_to_string(self.next_tiles)
        print("next_tiles: {}".format(mystring))
        print("this tile: {}".format(self.this_tile.return_string()))
        print("food ahead: {}".format(self.food_ahead))
        print("food on this tile: {}".format(self.food_on_this_tile))
        print("----- look_head (end) ------")
        return temp_tiles

    def move_down(self):
        dy = self.y
        dy += 1
        # get tile
        # x, y, color = aWorld.get_tile(temp, self.y)
        if self.y >= constants.NUMBER_OF_BLOCKS_HIGH-1:
            print("Cannot move down.")
            return ""
        else:
            self.y = dy
        # print("critter's x, y: {},{}".format(self.x, self.y))
        # debug print
        #next_tile = mymap.get_tile(self.x, self.y)

    def move_up(self):
        dy = self.y
        dy += -1
        if self.y <= 0:
            print("Cannot move up.")
        else:
            self.y = dy

    def move_right(self):
        dx = self.x
        dx += 1
        if self.x >= constants.NUMBER_OF_BLOCKS_WIDE-1:
            print("Cannot move right.")
        else:
            self.x = dx

    def move_left(self):
        dx = self.x
        dx += -1
        if self.x <= 0:
            print("Cannot move left.")
        else:
            self.x = dx

    def draw(self, surface):
        self.rect.topleft = [self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT]
        if self.facing_direction == "up":
            surface.blit(self.image_up, self.rect)
            # print("drawing image up")
        if self.facing_direction == "down":
            surface.blit(self.image_down, self.rect)
            # print("drawing image down")
        if self.facing_direction == "right":
            surface.blit(self.image_right, self.rect)
            # print("drawing image right")
        if self.facing_direction == "left":
            surface.blit(self.image_left, self.rect)
            # print("drawing image left")

        # myrect = pygame.Rect(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
        # pygame.draw.rect(surface, constants.RED, myrect)

    def draw_tile(self, x, y, ):
        pass

    def move(self):
        pass

    def examine_world(self):
        # is the player surrounded by two or more "x" tiles?
        pass

    def print_brain(self):
        mystring = ""
        for item in self.next_tiles:
            mystring += item.return_string()
        print("=============== Player.print_brain() BEGIN ==================")
        print("energy: {}".format(self.energy))
        print("x, y: {},{}".format(self.x, self.y))
        print("facing direction: {}".format(self.facing_direction))
        print("food ahead: {}".format(self.food_ahead))
        print("food on this tile: {}".format(self.food_on_this_tile))
        print("take action: {}".format(self.take_action))
        print("-----------------------------------------------------------")
        print("next tiles: {}".format(mystring))
        print("this tile: {}".format(self.this_tile.return_string()))
        print("=============== Player.print_brain() END ==================")

    def debug_print_stats(self):
        print("=============== Player.debug_print() BEGIN ==================")
        print("energy: {}".format(self.energy))
        print("x, y: {},{}".format(self.x, self.y))
        print("facing direction: {}".format(self.facing_direction))
        print("food ahead: {}".format(self.food_ahead))
        print("food on this tile: {}".format(self.food_on_this_tile))
        print("take action: {}".format(self.take_action))
        print("=============== Player.debug_print() END ==================")

# *******************************************************
# *******************************************************

def get_tile_color(tile_contents):
    tile_color = constants.GOLD
    if tile_contents == "m":
        tile_color = constants.DARKGREY
    if tile_contents == ".":
        tile_color = constants.GREEN
    if tile_contents == "p":
        tile_color = constants.BLUE
    if tile_contents == "c":
        tile_color = constants.RED
    if tile_contents == "f":
        tile_color = constants.DARKGREEN
    return tile_color


"""
=======================================================
                   class Map
=======================================================
"""
class Map:
    def __init__(self, mapfile):
        # self.world_map = self._read_map(mapfile)
        self.world_map = self._read_map(mapfile)
        # self.debug_print()

    def _read_map(self, mapfile):
        worldMap = []
        temp_map = []
        with open(mapfile, 'r') as f:
            temp_map = f.readlines()
        temp_map = [line.strip() for line in temp_map]
        for j, tile in enumerate(temp_map):
            newrow = []
            for i, tile_contents in enumerate(tile):
                newtile = Tile(i, j, tile_contents)
                newrow.append(newtile)
            worldMap.append(newrow)
        return worldMap

    def get_column(self, column_num):
        return self.world_map[column_num]

    def get_row(self, row_num):
        temp_row = []
        for row in self.world_map:
            for j in range(len(row)):
                if j == row_num:
                    temp_row.append(row[j])
        return temp_row

    def get_tile(self, x, y):
        # print("---- In Map.get_tile. x: {}, y: {}".format(x, y))
        myrow = self.world_map[y]
        mytile = myrow[x]
        # for item in myrow:
            # item.debug_print()
        # print("---- leaving get_tile -----")
        return mytile

    # def _read_map(self, mapfile):
    #     with open(mapfile, 'r') as f:
    #         world_map = f.readlines()
    #     world_map = [line.strip() for line in world_map]
    #     print(world_map)
    #     return (world_map)

    def draw_map(self, surface):
        for tiles in self.world_map:
            for a_tile in tiles:
                # print(a_tile.debug_print())
                a_tile.draw(surface)

    def draw_grid(self, surface):
        for i in range(constants.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * constants.BLOCK_HEIGHT)
            new_width = round(i * constants.BLOCK_WIDTH)
            pygame.draw.line(surface, constants.BLACK, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
            pygame.draw.line(surface, constants.BLACK, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)

    def player_starting_coords(self):
        for j, tile in enumerate(self.world_map):
            for i, tile_contents in enumerate(tile):
                # print("{},{}: {}".format(i, j, tile_contents))
                # print("tile contents: {}".format(tile_contents.contents))
                if tile_contents.contents == "c":
                    return i, j
        return -1, -1

    def debug_print(self):
        for row in self.world_map:
            for tile in row:
                tile.debug_print()

"""
=======================================================
                   class Game
=======================================================
"""

class Game:

    def __init__(self, mapfilename, player, surface):
        self.myMap = Map(mapfilename)
        self.player = player
        self.player.x, self.player.y = self.myMap.player_starting_coords()
        self.surface = surface
        pygame.init()
        pygame.display.set_caption(constants.TITLE)
        self.surface.fill(constants.UGLY_PINK)


    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_DOWN:
                        self.player.facing_direction = "down"
                        self.player.move_down()
                    if event.key == pygame.K_UP:
                        self.player.facing_direction = "up"
                        self.player.move_up()
                    if event.key == pygame.K_RIGHT:
                        self.player.facing_direction = "right"
                        self.player.move_right()
                    if event.key == pygame.K_LEFT:
                        self.player.facing_direction = "left"
                        self.player.move_left()
                    if event.key == pygame.K_w:
                        self.player.facing_direction = "up"
                        self.player.look_ahead(self.myMap)
                    if event.key == pygame.K_s:
                        self.player.facing_direction = "down"
                        self.player.look_ahead(self.myMap)
                    if event.key == pygame.K_d:
                        self.player.facing_direction = "right"
                        self.player.look_ahead(self.myMap)
                    if event.key == pygame.K_a:
                        self.player.facing_direction = "left"
                        self.player.look_ahead(self.myMap)
                    if event.key == pygame.K_y:
                        self.player.print_brain()
                    if event.key == pygame.K_t:
                        # print("BRAIN (before)")
                        # self.player.print_brain()
                        # ---------------
                        self.player.critter_take_action()
                        self.player.look_ahead(self.myMap)
                        self.player.decide_how_to_act()
                        # ---------------
                        # print("BRAIN (after)")
                        # self.player.print_brain()
                        # self.player.re_init_vars()
                    if event.key == pygame.K_e:
                        print("e was pressed")
                        self.player.eat(self.myMap)

            self.myMap.draw_map(self.surface)
            self.myMap.draw_grid(self.surface)
            self.player.draw(self.surface)
            fpsTime = pygame.time.Clock().tick(10)
            pygame.display.update()


# ==============================================================
# ==============================================================

def main():
    surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    contents = "."
    myplayer = Player()
    mygame = Game(constants.MAPFILE, myplayer, surface)
    mygame.game_loop()

if __name__=="__main__":
    main()
