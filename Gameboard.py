# 18x18 Gameboard class object for Konane

class Gameboard():
    def __init__(self, s):
        self.size = s
        self.board = [[1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2],
        [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1]]
        # empty = 0, black = 1, white = 2
        self.letter_number = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,
        'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17}

    def convert_location(self, loc):
        col = str(loc[:1])
        row = int(loc[1:])
        col = self.letter_number.get(col)
        row = 18 - row
        return col, row

    def get_value(self, loc):
        col, row = self.convert_location(loc)
        val = self.board[row][col]
        print(val)

    def change_value(self, loc, new_val):
        col, row = self.convert_location(loc)
        self.board[row][col] = new_val


temp = Gameboard(18)
temp.get_value('a18')
temp.change_value('a18', 0)
temp.get_value('a18')
