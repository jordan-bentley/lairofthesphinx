import pygame

"""
Code created by Jordan Bentley and David Battoe for CSC 236 Final Projects
"Cave Explorer"
"""

class SubMap():

    def __init__(self, mapp):
        """
                :param pos: Must be a tuple with integers in this format (x, y)
                :param mapp: Must be a nested list of rows
                :param dim: Must be tuple with integers in the format of (x, y)
                :return: None
                """
        self.mapp = mapp  # Gives a map of the area
        self.row = (len(mapp)-2)  # Sets the row position
        self.col = 1  # Sets the column position
        self.pos = (self.row, self.col)  # Sets self.pos to a tuple to the current row, current col
        self.treas_num = 0
        self.check = False
        self.valid = True


    def get_pos(self):
        """
        pre: None
        :return: Updated self.pos
        """
        self.pos = (self.col, self.row)  # Resets the self.pos using the current values of the row and col
        return self.pos  # Returns the updated self.pos

    def get_surroundings(self):
        """
        This method checks the area around the Explorer and sets the surroundings to variables.
        The 'if' statement will check for Treasure in these locations. If found, it calls the self.get_treasure method
        :return: The variables self.n, self.e, self.w, self.s are filled with the corresponding items.
        """
        self.n = self.mapp[self.row - 1][self.col]  # Returns the value 'north'
        self.e = self.mapp[self.row][self.col + 1]  # Returns the value 'east'
        self.w = self.mapp[self.row][self.col - 1]  # Returns the value 'west'
        self.s = self.mapp[self.row + 1][self.col]  # Returns the value 'south'

    def north(self):

        self.get_surroundings()
        if self.n == '.':  # If the value to the 'North' is a valid path i.e. a '.'
            self.row -= 1  # Sets the Explorers location to that of the '.'
            self.mapp[self.row][self.col] = 'm'  # Moves the 'm' in mapp
            self.mapp[self.row + 1][self.col] = ','  # Leaves a 'breadcrumb' to tell the Explorer that they have been here
            self.valid = True
        elif self.n == ",":
            self.row -= 1  # Sets the Explorers location to that of the '.'
            self.mapp[self.row][self.col] = 'm'  # Moves the 'm' in mapp to match the Explorers location
            self.mapp[self.row + 1][self.col] = ','  # Leaves a 'breadcrumb' to tell the Explorer that they have been here
            self.valid = True
        else:
            self.valid = False

    def east(self):
        self.get_surroundings()
        if self.e == '.':  # Else if the value to the East is a valid path i.e. a '.'
            self.col += 1
            self.mapp[self.row][self.col] = 'm'
            self.mapp[self.row][self.col - 1] = ','
            self.valid = True
        elif self.e == ',':  # Else if the value to the East is a valid path i.e. a '.'
            self.col += 1
            self.mapp[self.row][self.col] = 'm'
            self.mapp[self.row][self.col - 1] = ','
            self.valid = True
        else:
            self.valid = False

    def west(self):
        self.get_surroundings()
        if self.check == True:
            self.treas_turt.undo()
            self.check = False
        if self.w == '.':  # Else if the value to the West is a valid path i.e. a '.'
            self.col -= 1
            self.mapp[self.row][self.col] = 'm'
            self.mapp[self.row][self.col + 1] = ','
            self.valid = True
        elif self.w == ',':  # Else if the value to the West is a valid path i.e. a '.'
            self.col -= 1
            self.mapp[self.row][self.col] = 'm'
            self.mapp[self.row][self.col + 1] = ','
            self.valid = True
        else:
            self.valid = False

    def south(self):
        self.get_surroundings()
        if self.s == '.':  # Else if the value to the South is a valid path i.e. a '.'
            self.row += 1
            self.mapp[self.row][self.col] = 'm'
            self.mapp[self.row - 1][self.col] = ','
            self.valid = True
        elif self.s == ',':  # Else if the value to the South is a valid path i.e. a '.'
            self.row += 1
            self.mapp[self.row][self.col] = 'm'
            self.mapp[self.row - 1][self.col] = ','
            self.valid = True
        else:
            self.valid = False


    def print_curr_mapp(self):
        for line in self.mapp:
            print line
            print "\n"

    def undo(self):
        if self.check == True:
            self.treas_turt.undo()
            self.treas_turt.undo()
            self.check = False