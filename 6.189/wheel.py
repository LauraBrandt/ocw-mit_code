from graphics import *

# class Point:
    # # A class that represents a 2D Point

    # def __init__(self, x, y):
        # # Initalization method, called when we create a Point. 
        # # Takes 2 arguments, x and y, that must be numbers

        # # Make 2 object attributes
        # self.x = x
        # self.y = y

    # def __str__(self):
        # # The point's string method. When you print an object,
        # #  the __str__ method is called
        # return "A Point at coordinates " + str((self.x, self.y))

    # def move_point(self, delta_x, delta_y):
        # # Moves this Point delta_x units in the x-direction
        # #  and delta_y units in the y direction.
        # # delta_x and delta_y must be numbers.
        # # Returns the new coordinates.
        # self.x += delta_x
        # self.y += delta_y
        # return (self.x, self.y)


class Wheel():

    def __init__(self, center, wheel_radius, tire_radius):
        self.tire_circle = Circle(center, tire_radius)
        self.wheel_circle = Circle(center, wheel_radius)

    def draw(self, win): 
        self.tire_circle.draw(win) 
        self.wheel_circle.draw(win) 

    def move(self, dx, dy): 
        self.tire_circle.move(dx, dy) 
        self.wheel_circle.move(dx, dy)

    def set_color(self, wheel_color, tire_color):
        self.tire_circle.setFill(tire_color) 
        self.wheel_circle.setFill(wheel_color)

    def undraw(self): 
        self.tire_circle .undraw() 
        self.wheel_circle .undraw() 

    def get_size(self):
        return self.tire_circle.getRadius()

    def get_center(self):
        return self.tire_circle.getCenter()
        
    def animate(self, win, dx, dy, n):
        if n>0:
            self.move(dx,dy)
            win.after(100, self.animate, win, dx, dy, n-1)


# Define a main function; if you want to display graphics, run main()
# after you load code into your interpreter
def main():
    # create a window with width = 700 and height = 500
    new_win = GraphWin('Wheel', 700, 500) 

    # What we'll need for the wheel...
    wheel_center = Point(200, 200) # The wheel center is a Point at (200, 200)
    tire_radius = 100  # The radius of the outer tire is 100

    # Make a wheel object
    new_wheel = Wheel(wheel_center, 0.6*tire_radius, tire_radius)

    # Set its color
    new_wheel.set_color('OrangeRed', 'black')

    # And finally, draw it 
    new_wheel.draw(new_win)
    
    # Make it move across the screen by 1 unit in the x dir 100 times
    new_wheel.animate(new_win, 2, 0, 100)

    # Run the window loop (must be the *last* line in your code)
    new_win.mainloop()

# Comment this call to main() when you import this code into
#  your car.py file - otherwise the Wheel will pop up when you
#  try to run your car code.
# main()
