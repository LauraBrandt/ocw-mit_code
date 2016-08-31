from graphics import *
import random
import copy

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the Tetris board in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y

        # Convert from squares on the grid of the board to pixels:
        # Point(0,0) is the top left square
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        # Modify block appearance
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise            
        '''
        return board.can_move(self.x+dx, self.y+dy)
        
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ## A boolean to indicate if a shape shifts rotation direction or not.
        ## Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        '''returns the list of blocks
        '''
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape, i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)
            
    def undraw(self):
        ''' Undraws each block from the canvas
        '''
        for block in self.blocks:
            block.undraw()

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if all of them can, and False otherwise           
        '''
        for block in self.blocks:
            if not block.can_move(board,dx,dy):
                return False
        return True
    
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            returns the current rotation direction
        '''
        return self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated. 
            Returns True if each block can move to the new position
            after rotation, False otherwise
        '''
        # Get rotation direction
        rot_dir = self.rotation_dir
        # Center about which shape rotates
        center_x = self.center_block.x
        center_y = self.center_block.y
        for block in self.blocks:
            # Calculate new position of block after rotation
            x = center_x - rot_dir*center_y + rot_dir*block.y
            y = center_y + rot_dir*center_x - rot_dir*block.x
            # Check if the block can move to that position
            if not board.can_move(x,y):
                return False
        return True

    def rotate(self, board):
        ''' Parameters: board - type: Board object           
        '''    
        # Rotation direction
        rot_dir = self.rotation_dir
        # Center of rotation
        center_x = self.center_block.x
        center_y = self.center_block.y
        for block in self.blocks:
            # Calculate position after rotation
            x = center_x - rot_dir*center_y + rot_dir*block.y
            y = center_y + rot_dir*center_x - rot_dir*block.x
            # Move each block to its new position
            block.move(x-block.x, y-block.y)

        # Pieces that shift rotation direction (I, S, Z) do so after a successful rotation.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1
        

############################################################
# ALL SHAPE CLASSES
############################################################
 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')        
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')        
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return 

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1

class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]

class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      

############################################################
# BOARD CLASS
############################################################

class Board():
    ''' Board class: it represents the Tetris board in the middle, 
        and information about the game (score, piece preview, instructions)
        on the sides

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    side_width - type:int - width of each of the columns on the side
                            of the game board, where the score and piece preview are drawn
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
                    score_object - type:Text object - text that shows the current score
                                    (to be displayed to the side of the game board)
                    level_object - type:Text object - text that shows the current level
                                    (to be displayed to the side of the game board)
                    rows_object - type:Text object - text that shows the number of completed rows
                                    (to be displayed to the side of the game board)
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.side_width = 6
        
        self.is_game_over = False
        
        # Initialize text objects that will display the score, level, and rows completed
        self.score_object = Text(Point(0,0), "0")
        self.level_object = Text(Point(0,0), "0")
        self.rows_object = Text(Point(0,0), "0")
        
        self.new_shape = Shape([Point(0,0)],'black')

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, (self.width+2*self.side_width) * Block.BLOCK_SIZE,
                                        (self.height) * Block.BLOCK_SIZE)
        self.canvas.setBackground('light steel blue')       
       
        self.draw_permanent_shapes()
        
        ### Check board width (for testing only, do not use in final version!)
        # for x in range(self.width+self.side_width*2):
            # block = Block(Point(x,0), "green")
            # block.draw(self.canvas)
        
        # create an empty dictionary with tuples (x,y) as the keys and Blocks as values
        # currently we have no shapes on the board
        self.grid = {}
        
               
    def draw_permanent_shapes(self):
        ''' Creates and draws the non-playable parts of the board
        '''
        # color the playing space differently
        board_space = Rectangle(Point(self.side_width*Block.BLOCK_SIZE, 0),
                                Point((self.side_width+self.width)*Block.BLOCK_SIZE+2*Block.OUTLINE_WIDTH, 
                                       self.height*Block.BLOCK_SIZE+2*Block.OUTLINE_WIDTH))
        board_space.setFill('black')
        board_space.draw(self.canvas)
        
        # write the directions on the screen
        directions = ["Left arrow: move left",
                      "Right arrow: move right",
                      "Down arrow: move down",
                      "Up arrow: rotate",
                      "Space bar: drop to bottom",
                      "P: pause game"]
        x = (self.side_width+self.width+(self.side_width/2))*Block.BLOCK_SIZE
        y = 11*Block.BLOCK_SIZE
        for i in range(len(directions)):
            dir = Text(Point(x,y), directions[i])
            dir.setSize(int(0.3*Block.BLOCK_SIZE))  
            dir.setStyle('bold')
            dir.draw(self.canvas)
            y += 0.7*Block.BLOCK_SIZE
            
        # create space to show block preview
        # text
        center = Point((self.width+self.side_width+2.3)*Block.BLOCK_SIZE,
                        Block.BLOCK_SIZE*1.7)
        preview = Text(center, "Next Block: ")
        preview.setSize(int(0.4*Block.BLOCK_SIZE))
        preview.setStyle('bold')
        preview.draw(self.canvas)
        # rectangle
        p1 = Point((self.side_width + self.width + 0.7)*Block.BLOCK_SIZE, 
                    2.5*Block.BLOCK_SIZE)
        p2 = Point((self.side_width + self.width + self.side_width - 0.5)*Block.BLOCK_SIZE, 
                    6.5*Block.BLOCK_SIZE)
        prev_window = Rectangle(p1,p2)
        prev_window.setFill('gray20')
        prev_window.draw(self.canvas)
        
        # create spaces to show level, completed lines, and score
        texts = ["Level:", "Lines: ", "Score: "]
        x = 1.5*Block.BLOCK_SIZE
        y = 2*Block.BLOCK_SIZE
        for i in range(len(texts)):
            text = Text(Point(x,y), texts[i])
            text.setSize(int(0.4*Block.BLOCK_SIZE))
            text.setStyle('bold')
            p1 = Point(x-0.8*Block.BLOCK_SIZE, y+0.7*Block.BLOCK_SIZE)
            p2 = Point(x+3.5*Block.BLOCK_SIZE, y+2*Block.BLOCK_SIZE)
            window = Rectangle(p1,p2)
            window.setFill('gray20')
            text.draw(self.canvas)
            window.draw(self.canvas)
            y += 4*Block.BLOCK_SIZE
        
        
    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            Checks if it is ok to move to square x,y
        '''
        # x,y within the board boundaries
        if x in range(self.side_width,self.width+self.side_width) and y in range(self.height):
            # not already a block at that position
            if (x,y) not in self.grid:
                return True
        return False

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid
        '''
        blocks = shape.get_blocks()
        for block in blocks:
            self.grid[(block.x,block.y)] = block

    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y          
        '''
        # Each block in the row on the game board
        for x in range(self.side_width, self.width+self.side_width):
            # Undraw the block and remove it from the grid
            block = self.grid[(x,y)]
            block.undraw()
            del self.grid[(x,y)]
    
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is one square that is not occupied, return False
            otherwise return True            
        '''
        # Check each block in one row in the gameboard area
        for x in range(self.side_width,self.width+self.side_width):
            if (x,y) not in self.grid:
                return False
        return True
            
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            for each block from row y_start to the top, 
            move the block down one square
        '''   
        # Each column in the game board area
        for x in range(self.side_width,self.width+self.side_width):
            # Each row from y_start to top
            for y in range(y_start,-1,-1):
                if (x,y) in self.grid:
                    block = self.grid[(x,y)]
                    # undraw block and remove from grid
                    self.grid[(x,y)].undraw()
                    del self.grid[(x,y)]
                    # move block down one row
                    block.move(0,1)
                    # redraw block and add it to grid at new position
                    self.grid[(x,block.y)] = block
                    block.draw(self.canvas)
            
    def remove_complete_rows(self):
        ''' Return value: type: int - number of completed rows
        
            removes all the complete rows
        '''
        num_rows = 0
        for y in range(0,self.height):
            if self.is_row_complete(y):
                num_rows += 1
                self.delete_row(y)
                self.move_down_rows(y-1)
        return num_rows
        
    def draw_score(self, score):
        ''' Draws the score to the score box on the canvas, 
        '''
        self.score_object.undraw()
        self.score_object = Text(Point(2.85*Block.BLOCK_SIZE,11.35*Block.BLOCK_SIZE), str(score))
        self.score_object.setTextColor('white')
        self.score_object.setSize(int(0.5*Block.BLOCK_SIZE))
        self.score_object.draw(self.canvas)
        
    def draw_level(self, level):
        ''' Draws the level to the level box on the canvas
        '''
        self.level_object.undraw()
        self.level_object = Text(Point(2.85*Block.BLOCK_SIZE,3.35*Block.BLOCK_SIZE), str(level))
        self.level_object.setTextColor('white')
        self.level_object.setSize(int(0.5*Block.BLOCK_SIZE))
        self.level_object.draw(self.canvas)
        
    def draw_rows_complete(self, rows):
        ''' Draws the number of completed rows to the lines box on the canvas
        '''
        self.rows_object.undraw()
        self.rows_object = Text(Point(2.85*Block.BLOCK_SIZE,7.35*Block.BLOCK_SIZE), str(rows))
        self.rows_object.setTextColor('white')
        self.rows_object.setSize(int(0.5*Block.BLOCK_SIZE))
        self.rows_object.draw(self.canvas)
        
    def piece_preview(self, shape):
        ''' Parameters: shape - type: Shape
        
            Draws the a copy of the shape onto the board 
            within the rectangle on the side bar to show the next shape
        '''
        self.new_shape.undraw()
        self.new_shape = copy.deepcopy(shape)
        self.new_shape.move(self.side_width/2 + self.width/2, 3)
        self.new_shape.draw(self.canvas)
        
    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            and make all of the blocks fall off the bottom of the screen
        '''      
        self.is_game_over = True
        
        # Create text
        x = ((self.width+2*self.side_width)*Block.BLOCK_SIZE)/2
        y = (self.height*Block.BLOCK_SIZE)*0.25
        message = Text(Point(x, y), 
                       'Game\nOver!')
        message.setSize(Block.BLOCK_SIZE)
        message.setTextColor('red')
        # Create background rectangle for text to be drawn into
        background = Rectangle(Point(x-3*Block.BLOCK_SIZE,y-2*Block.BLOCK_SIZE),
                               Point(x+3*Block.BLOCK_SIZE, y+2*Block.BLOCK_SIZE))
        background.setFill('old lace')
        # Draw message
        background.draw(self.canvas)
        message.draw(self.canvas)
        # Animate blocks falling off the screen
        self.blocks_fall_off(self.canvas, self.height)
                               
    def blocks_fall_off(self, win, moves):
        ''' Parameters: win - type: CanvasFrame 
                        moves - type: int - number of rows on the screen
                        
            animates each row moving down until it falls off the bottom of the window
        '''
        if moves>0:
            self.move_down_rows(self.height-1)
            win.after(100, self.blocks_fall_off, win, moves-1)  


############################################################
# TETRIS CLASS
############################################################

class Tetris():
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
            paused - type:bool - indicates if the game is paused
            pause_message - type:Text object - displays a message saying that the game is paused
            score - type: int - the current score
            level - type: int - the current level
            rows_complete - type: int - the total number of completed rows
            next_shape - type:Shape - the piece to appear after the current shape
    '''
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        
        self.paused = False
        self.pause_message = Text(Point(
                                (self.board.width+self.board.side_width*2)*Block.BLOCK_SIZE/2,
                                 self.board.height*Block.BLOCK_SIZE*.305),
                                "Game is Paused\nPress 'P' to Resume")
        self.pause_message.setTextColor('grey')
                        
        self.delay = 1000 #ms
        self.score = 0
        self.level = 0
        self.rows_complete = 0
        
        self.update_score(0)
        self.update_level()
        self.board.draw_rows_complete(self.rows_complete)

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape and the shape to come after it to a random new shape
        self.current_shape = self.create_new_shape()
        self.next_shape = self.create_new_shape()

        # Draw the current_shape on the board 
        self.board.draw_shape(self.current_shape)
        self.board.piece_preview(self.next_shape)

        # Animate the shape
        self.animate_shape()


    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        choice = random.choice(self.SHAPES)
        shape = choice(Point(int((self.BOARD_WIDTH+2*self.board.side_width)/2), 0))
        return shape
    
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        # only animates if the game is not paused and is not over
        if not self.board.is_game_over:
            if self.paused == False:
                self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
            
    def update_score(self, rows_completed):
        ''' increases the score depending on how many rows were completed, 
            and redraws the new score on the board
        '''
        if rows_completed == 1:
            self.score += 100
        elif rows_completed == 2:
            self.score += 300            
        elif rows_completed == 3:
            self.score += 400
        elif rows_completed == 4:
            self.score += 600
        elif rows_completed > 4:
            self.score += 600
            self.update_score(rows_completed-4)
        self.board.draw_score(self.score)
    
    def update_level(self):
        '''updates the level based on the score,
            rewrites the current level on the board, 
            and increases the speed 
        '''
        self.level = (self.score / 1100) + 1
        self.board.draw_level(self.level)
        self.delay = (10-self.level)*100
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Check if shape can be moved in the direction specified.
            If it can, move the shape and return True, if not return False
            
            If the direction was 'Down', and the shape cannot move down, 
            update the board and initialize a new shape,
            or if there's no more space, end the game            
        '''
        coords = self.DIRECTION[direction]
        # check if shape can move in that direction, and move it if it can
        if self.current_shape.can_move(self.board,coords[0],coords[1]):
            self.current_shape.move(coords[0],coords[1])
            return True
        # if it tried to move down but couldn't...
        elif direction == 'Down':
            # add the shape to the grid of the board
            self.board.add_shape(self.current_shape)
            # remove the completed rows and count how many rows were completed
            num_rows = self.board.remove_complete_rows()
            # add that to the running total of number of rows completed, and write it to the board
            self.rows_complete += num_rows
            self.board.draw_rows_complete(self.rows_complete)
            # update the current score and level based on the rows removed
            self.update_score(num_rows)
            self.update_level()
            # create a new random shape and draw it on the board, if possible
            self.current_shape = self.next_shape
            self.next_shape = self.create_new_shape()
            self.board.piece_preview(self.next_shape)
            if not self.board.draw_shape(self.current_shape):
                self.board.game_over()            
        return False

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        ''' 
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            
            if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape will rotate.
                
            if the user presses the 'p' key, the game will pause                
        '''
        key = event.keysym
        if not self.board.is_game_over:
            if key == 'p' or key == 'P':
                if self.paused == False:
                    self.paused = True
                    self.pause_message.draw(self.board.canvas)
                elif self.paused == True:
                    self.paused = False
                    self.pause_message.undraw()
            if self.paused == False:
                if key == 'Up':
                    self.do_rotate()
                elif key == 'Left' or key == 'Right' or key == 'Down':
                    self.do_move(key)
                elif key == 'space':
                    keep_going = True
                    while keep_going == True:
                        keep_going = self.do_move('Down')

       
################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
