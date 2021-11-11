"""
Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        visited.clear()
        distance_field = [[self._grid_height * self._grid_width 
                           for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        type_map = {HUMAN: self._human_list, ZOMBIE: self._zombie_list}
        boundary = poc_queue.Queue()
        for entity in type_map[entity_type]:
            boundary.enqueue(entity)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbor_cells = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbor_cells:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        next_human_pos = []
        for human in self._human_list:
            #By default, we stay in the same place
            max_distance = zombie_distance_field[human[0]][human[1]]
            best_move = [human]
            poss_human_moves = self.eight_neighbors(human[0], human[1])
            for move in poss_human_moves:
                if self.is_empty(move[0], move[1]):
                    potential_distance = zombie_distance_field[move[0]][move[1]]
                    if potential_distance > max_distance:
                        max_distance = potential_distance
                        best_move = [move]
                    elif zombie_distance_field[move[0]][move[1]] == max_distance:
                        best_move.append(move)
            next_move = random.choice(best_move)
            next_human_pos.append((next_move[0], next_move[1]))
        self._human_list = next_human_pos

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        next_zombie_pos = []
        for zombie in self._zombie_list:
            #By default, we stay in the same place
            min_distance = human_distance_field[zombie[0]][zombie[1]]
            best_move = [zombie]
            poss_zombie_moves = self.four_neighbors(zombie[0], zombie[1])
            for move in poss_zombie_moves:
                if self.is_empty(move[0], move[1]):
                    potential_distance = human_distance_field[move[0]][move[1]]
                    if potential_distance < min_distance:
                        min_distance = potential_distance
                        best_move = [move]
                    elif human_distance_field[move[0]][move[1]] == min_distance:
                        best_move.append(move)
            next_move = random.choice(best_move)
            next_zombie_pos.append((next_move[0], next_move[1]))
        self._zombie_list = next_zombie_pos

poc_zombie_gui.run_gui(Apocalypse(30, 40))

