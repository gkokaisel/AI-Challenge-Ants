#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        self.unseen = []
        self.hills = []
        self.path = []
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use

    def do_turn(self, ants):
        orders = {}
        def do_move_direction(loc, direction):
            new_loc = ants.destination(loc, direction)
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False


        # track all moves, prevent collisions
        targets = {}
        def do_move_location(loc, dest):
            directions = ants.direction(loc, dest)
            for direction in directions:
                if do_move_direction(loc, direction):
                    targets[dest] = loc
                    return True
            return False

        # prevent stepping on own hill
        for hill_loc in ants.my_hills():
            orders[hill_loc] = None

        # find close food
        ant_dist = []
        for food_loc in ants.food():
            for ant_loc in ants.my_ants():
                dist = ants.distance(ant_loc, food_loc)
                ant_dist.append((dist, ant_loc, food_loc))
        ant_dist.sort()
        for dist, ant_loc, food_loc in ant_dist:
            if food_loc not in targets and ant_loc not in targets.values():
                do_move_location(ant_loc, food_loc)

        # attack hills
        for hill_loc, hill_owner in ants.enemy_hills():
            if hill_loc not in self.hills:
                self.hills.append(hill_loc)
        ant_dist = []
        for hill_loc in self.hills:
            for ant_loc in ants.my_ants():
                if ant_loc not in orders.values():
                    dist = ants.distance(ant_loc, hill_loc)
                    ant_dist.append((dist, ant_loc, hill_loc))
        ant_dist.sort()
        for dist, ant_loc, hill_loc in ant_dist:
            do_move_location(ant_loc, hill_loc)

        # explore unseen areas
        for loc in self.unseen[:]:
            if ants.visible(loc):
               self.unseen.remove(loc)
        for ant_loc in ants.my_ants():
             if ant_loc not in orders.values():
                unseen_dist = []
                for unseen_loc in self.unseen:
                    dist = ants.distance(ant_loc, unseen_loc)
                    unseen_dist.append((dist, unseen_loc))
                unseen_dist.sort()
                for dist, unseen_loc in unseen_dist:
                    if do_move_location(ant_loc, unseen_loc):
                       break

        # unblock own hill
        for hill_loc in ants.my_hills():
            if hill_loc in ants.my_ants() and hill_loc not in orders.values():
               for direction in ('s','e','w','n'):
                   if do_move_direction(hill_loc, direction):
                       break
    # A* algorithm for path finding implemented from code this site tutorial
    # http://codethissite.blogspot.com/2011/11/ai-challenge-pathfinding.html
    def aStar(start, target):
        closedList = set()
        openList = set()
        came_from = {}
        g_score = {}
        h_score = {}
        f_score = {}
        directions = list(AIM.keys())

        openList.add(start)
        g_score[start] = 0
        h_score[start] = ants.distance(start, target)
        f_score[start] = g_score[start] + h_score[start]

        while openList:
            current = min(f_score, key=f_score.get)
            if (current == target):
                self.PATH.append(start)
                trace_path(came_from, came_from[target])
                self.PATH.append(target)
                return self.PATH

            f_score.pop(current)
            openList.remove(current)
            closedList.add(current)

            for direction in directions:
                new_loc = ants.destination(current, direction)
                if (new_loc in closedList or not ants.passable(new_loc)):
                    continue
                new_g = g_score[current] + 1

                if new_loc not in openList:
                    openList.add(new_loc)
                    closer = True
                elif new_g < g_score[new_loc]:
                    closer = True
                else:
                    closer = False

                if closer == True:
                    came_from[new_loc] = current
                    g_score[new_loc] = new_g
                    h_score[new_loc] = ants.distance(new_loc, target)
                    f_score[new_loc] = g_score[new_loc] + h_score[new_loc]

                return None


    def trace_path(came_from, current_node):
        if current_node in came_from:
            trace_path(came_from, came_from[current_node])
            self.PATH.append(current_node)
            return

if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
