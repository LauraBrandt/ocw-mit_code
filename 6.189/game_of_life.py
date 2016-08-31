from graphics import *
import random

## Written by Sarina Canelake & Kelly Casteel, August 2010
## Revised January 2011

############################################################
# GLOBAL VARIABLES
############################################################
    
BLOCK_SIZE = 30
BLOCK_OUTLINE_WIDTH = 2
BOARD_WIDTH = 20
BOARD_HEIGHT = 20

DELAY = 500 # ms
COLOR = 'black'

neighbor_test_blocklist = [(0,0), (1,1)]
toad_blocklist = [(4,4), (3,5), (3,6), (5,7), (6,5), (6,6)]
beacon_blocklist = [(2,3), (2,4), (3,3), (3,4), (4,5), (4,6), (5,5), (5,6)]
glider_blocklist = [(1,2), (2,3), (3,1), (3,2), (3,3)]
pulsar_blocklist = [(2,4), (2,5), (2,6), (4,2), (4,7), (5,2), (5,7),
                    (6,2), (6,7), (7,4), (7,5), (7,6), (9,4), (9,5), (9,6),
                    (10,7), (11,7), (12,7), (10,2), (11,2), (12,2), (14,4),
                    (14,5), (14,6), (4,9), (5,9), (6,9), (10,9), (11,9),
                    (12,9), (7,10), (7,11), (7,12), (9,10), (9,11), (9,12),
                    (2,10), (2,11), (2,12), (14,10), (14,11), (14,12),
                    (4,14), (5,14), (6,14), (10,14), (11,14), (12,14)]
# for diehard, make board at least 25x25, might need to change block size
diehard_blocklist = [(5,7), (6,7), (6,8), (10,8), (11,8), (12,8), (11,6)]

############################################################
# TEST CODE (don't worry about understanding this section)
############################################################

def test_neighbors(board):
    '''
    Code to test the board.get_block_neighbor function
    '''
    for block in board.block_list.values():
        neighbors = board.get_block_neighbors(block)
        ncoords = [neighbor.get_coords() for neighbor in neighbors]
        if block.get_coords() == (0,0):
            zeroneighs = [(0,1), (1,1), (1,0)]
            for n in ncoords:
                if n not in zeroneighs:
                    print "Testing block at (0,0)"
                    print "Got", ncoords
                    print "Expected", zeroneighs
                    return False

            for neighbor in neighbors:
                if neighbor.get_coords() == (1, 1):
                    if neighbor.is_live() == False:
                        print "Testing block at (0, 0)..."
                        print "My neighbor at (1, 1) should be live; it is not."
                        print "Did you return my actual neighbors, or create new copies of them?"
                        print "FAIL: get_block_neighbors() should NOT return new Blocks!"
                        return False

        elif block.get_coords() == (1,1):
            oneneighs = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1),(2,2)]
            for n in ncoords:
                if n not in oneneighs:
                    print "Testing block at (1,1)"
                    print "Got", ncoords
                    print "Expected", oneneighs
                    return False
            for n in oneneighs:
                if n not in ncoords:
                    print "Testing block at (1,1)"
                    print "Got", ncoords
                    print "Expected", oneneighs
                    return False
    print "Passed neighbor test"
    return True


############################################################
# BLOCK CLASS (Read through and understand this part!)
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the board
        in terms of the square grid
    '''

    def __init__(self, pos, color):
        '''
        pos: a Point object specifing the (x, y) square of the Block (NOT in pixels!)
        color: a string specifing the color of the block (eg 'blue' or 'purple')
        '''
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*BLOCK_SIZE,
                   pos.y*BLOCK_SIZE)
        p2 = Point(p1.x + BLOCK_SIZE, p1.y + BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(BLOCK_OUTLINE_WIDTH)
        self.setFill(color)
        self.status = 'dead'
        self.new_status = 'None'
        
    def get_coords(self):
        return (self.x, self.y)

    def set_live(self, canvas):
        '''
        Sets the block status to 'live' and draws it on the grid.
        Be sure to do this on the canvas!
        '''
        if self.status=='dead':
          self.status = 'live'
          self.draw(canvas)

    def set_dead(self):
        '''
        Sets the block status to 'dead' and undraws it from the grid.
        '''
        if self.status=='live':
          self.status = 'dead'
          self.undraw()

    def is_live(self):
        '''
        Returns True if the block is currently 'live'. Returns False otherwise.
        '''
        if self.status == 'live':
            return True
        return False

    def reset_status(self, canvas):
        '''
        Sets the new_status to be the current status
        '''
        if self.new_status=='dead':
            self.set_dead()
        elif self.new_status=='live':
            self.set_live(canvas)
        

###########################################################
# BOARD CLASS (Read through and understand this part!)
###########################################################

class Board(object):
    ''' Board class: it represents the Game of Life board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the blocks will be drawn
                    block_list - type:Dictionary - stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        # self.delay is the number of ms between each simulation. Change to be
        # shorter or longer if you wish!
        self.delay = DELAY

        # create a canvas to draw the blocks on
        self.canvas = CanvasFrame(win, self.width * BLOCK_SIZE,
                                       self.height * BLOCK_SIZE)
        self.canvas.setBackground('white')

        # initialize grid lines
        for x in range(1,self.width):
            self.draw_gridline(Point(x, 0), Point(x, self.height))

        for y in range(1,self.height):
            self.draw_gridline(Point(0, y), Point(self.width, y))

        # initialize a block for each square of the board,
        # stored in a dictionary (key:value is (x,y):Block)
        self.block_list = {}
        for x in range(self.width):
            for y in range(self.height):
                self.block_list[(x,y)] = Block(Point(x,y), COLOR) 

    def draw_gridline(self, startp, endp):
        ''' Parameters: startp - a Point of where to start the gridline
                        endp - a Point of where to end the gridline
            Draws two straight 1 pixel lines next to each other, to create
            a nice looking grid on the canvas.
        '''
        line = Line(Point(startp.x*BLOCK_SIZE, startp.y*BLOCK_SIZE), \
                    Point(endp.x*BLOCK_SIZE, endp.y*BLOCK_SIZE))
        line.draw(self.canvas)
        
        line = Line(Point(startp.x*BLOCK_SIZE-1, startp.y*BLOCK_SIZE-1), \
                    Point(endp.x*BLOCK_SIZE-1, endp.y*BLOCK_SIZE-1))
        line.draw(self.canvas)


    def random_seed(self, percentage):
        ''' Parameters: percentage - a number between 0 and 1 representing the
                                     percentage of the board to be filled with
                                     blocks
            This method activates the specified percentage of blocks randomly.
        '''
        for block in self.block_list.values():
            if random.random() < percentage:
                block.set_live(self.canvas)

    def seed(self, block_coords):
        '''
        Seeds the board with a certain configuration.
        Takes in a list of (x, y) tuples representing block coordinates,
        and activates the blocks corresponding to those coordinates.
        '''
        for block in block_coords:
            self.block_list[block].set_live(self.canvas)
   
    def get_block_neighbors(self, block):
        '''
        Given a Block object, returns a list of neighboring blocks.
        '''
        coords = []
        neighbors = []
        for x in range(block.x-1,block.x+2):
            for y in range(block.y-1,block.y+2):
                coords.append((x,y))
        coords.remove((block.x,block.y))
        for coord in coords:
            if coord in self.block_list:
                neighbors.append(self.block_list[coord])
        return neighbors   
            
    def simulate(self):
        ''' Executes one turn of Conways Game of Life using the
            rules of the game       
        '''
        for block in self.block_list.values():
            # Count how many of the block's neighbors are live
            live_neighs = self.count_live_neighbors(block)
            # Set the new status based on the rules of the game
            if block.status == "dead":
                if live_neighs == 3:
                    block.new_status = "live"
                else:
                    block.new_status = "dead"
            elif block.status == "live":
                if live_neighs > 3:
                    block.new_status = "dead"
                elif live_neighs==2 or live_neighs==3:
                    block.new_status = "live"
                else:   # fewer than 2 live neighbors
                    block.new_status = "dead"
                    
        # Change all the current statuses to the new statuses
        for block in self.block_list.values():
            # print block.x, block.y, block.new_status
            block.reset_status(self.canvas)
            # print "status set to", block.status
                      
    def count_live_neighbors(self,block):
        ''' Returns the number of surrounding blocks that are 'live'
        '''
        neighbors = self.get_block_neighbors(block)
        # Count how many live neighbors:
        num_neighs = 0
        for neighbor in neighbors:
            if neighbor.is_live():
                num_neighs +=1
        # print "> (%d,%d), %d" % (block.x,block.y,num_neighs)
        return num_neighs

    def animate(self):
        '''
        Animates the Game of Life, calling "simulate"
        once every second
        '''
        self.simulate()
        self.win.after(self.delay, self.animate)



################################################################
# RUNNING THE SIMULATION
################################################################

if __name__ == '__main__':    
    # Initalize board
    win = Window("Conway's Game of Life")
    board = Board(win, BOARD_WIDTH, BOARD_HEIGHT)

    # board.random_seed(.15)
    board.seed(pulsar_blocklist)

    win.after(500, board.animate)
    
    win.mainloop()
                
