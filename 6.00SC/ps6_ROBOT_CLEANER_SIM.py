# Problem Set 6: Simulating robots

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty. True
    represents a clean tile, False a dirty one
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}
        for m in range(self.width):
            for n in range(self.height):
                self.tiles[(m,n)] = False
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        m = int(pos.x)
        n = int(pos.y)
        self.tiles[(m,n)] = True
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m,n)]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.tiles)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count = 0
        for elem in self.tiles.keys():
            if self.tiles[elem]:
                count += 1
        return count

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = self.width*random.random()
        y = self.height*random.random()
        return Position(x,y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if (0 <= pos.x < self.width) and (0 <= pos.y < self.height):
            return True
        else: return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.pos = self.room.getRandomPosition()
        self.dir = random.randrange(360)
        
        self.room.cleanTileAtPosition(self.pos)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_pos = self.pos.getNewPosition(self.dir, self.speed)
        if self.room.isPositionInRoom(new_pos):
            self.pos = new_pos
            self.room.cleanTileAtPosition(self.pos)
        else:
            self.dir = random.randrange(360)
            

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    totals_steps = []
    for trial in range(num_trials):
        #print "Trial", trial, ":",
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        numTilesNeededToFinish = min_coverage*room.getNumTiles()
        
        robots = []
        for num in range(num_robots):
            robots.append(robot_type(room, speed))

        timesteps = 0
        
        while room.getNumCleanedTiles() < numTilesNeededToFinish:
            #anim.update(room, robots)
            timesteps += 1
            for robot in robots:
                robot.updatePositionAndClean()
            #print timesteps, ":", room.getNumCleanedTiles()
        #print timesteps
        totals_steps.append(timesteps)
        #anim.done()
    #print totals_steps
    average = sum(totals_steps) / float(len(totals_steps))
    return average                              


# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    yvals = []
    for num in range(1,11):
        time = runSimulation(num, 1.0, 20, 20, 0.8, 100,
                  StandardRobot)
        yvals.append(time)
    xvals = range(1,11)
    #print xvals, yvals

    pylab.plot(xvals,yvals)
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Mean number of timesteps')
    pylab.title('Time needed to clean 80% of a 20x20 room')
    pylab.show()
    
#showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    widths = (20,25,40,50,80,100)
    heights = (20,16,10,8,5,4)
    xvals = []
    for i in range(len(widths)):
        xvals.append(float(widths[i])/heights[i])
    #print xvals
    
    yvals = []
    for i in range(len(widths)):
        time = runSimulation(2, 1.0, widths[i], heights[i], 0.8, 500,
                  StandardRobot)
        yvals.append(time)
    #print yvals
    pylab.plot(xvals,yvals)
    pylab.xlabel('Ratio of Room Width/Height')
    pylab.ylabel('Mean number of timesteps')
    pylab.title('Time needed to clean 80% of a room of varying sizes')
    pylab.show()
        

#showPlot2()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_pos = self.pos.getNewPosition(self.dir, self.speed)
        if self.room.isPositionInRoom(new_pos):
            self.pos = new_pos
            self.room.cleanTileAtPosition(self.pos)
        self.dir = random.randrange(360)


# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    xvals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    standard = []
    for i in range(len(xvals)):
        time = runSimulation(1, 1.0, 20, 20, xvals[i], 100, StandardRobot)
        standard.append(time)
    random = []
    for i in range(len(xvals)):
        time = runSimulation(1, 1.0, 20, 20, xvals[i], 100, RandomWalkRobot)
        random.append(time)
    #print standard, random
    pylab.plot(xvals, standard, 'r-', label="StandardRobot")
    pylab.plot(xvals, random, 'b-', label="RandomWalkRobot")
    pylab.xlabel('Fraction of Room to be Cleaned')
    pylab.ylabel('Mean time')
    pylab.legend(loc='upper left')
    pylab.title('Comparison of StandardRobot and RandomWalkRobot in a 20x20 room')
    pylab.show()
    
#showPlot3()

NUM_ROBOTS = 1
SPEED = 1.0
WIDTH = 10
HEIGHT = 10
MIN_COVERAGE = 0.75
NUM_TRIALS = 2
ROBOT_TYPE = RandomWalkRobot

print runSimulation(NUM_ROBOTS, SPEED, WIDTH, HEIGHT, MIN_COVERAGE, NUM_TRIALS, ROBOT_TYPE)
