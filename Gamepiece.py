# Gamepiece class object for Konane

class Gamepiece():
    def __init__(self, col, loc):
        self.color = col
        self.location = loc

    def get_color(self):
        print(self.color)

    def get_location(self):
        print(self.location)

    def move_location(self, new_loc):
        self.location = new_loc

    def removed(self):
        self.location = 'None'

temp = Gamepiece('black', 'a1')
temp.get_location()
temp.get_color()
temp.move_location('a3')
temp.get_location()
