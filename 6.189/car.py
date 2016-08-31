from graphics import *
from wheel import *

class Car:
    def __init__(self, wheel1_center, wheel2_center, radius, height):
        # create main rectangle of truck:
        midpoint = (wheel1_center.x + wheel2_center.x)/2.0
        x1 = midpoint - height
        y1 = wheel1_center.y - height
        x2 = midpoint + height
        y2 = wheel1_center.y
        self.rect_body = Rectangle(Point(x1, y1), Point(x2,y2))
        self.rect_body.setWidth(2)
        # create rectangle for cab of truck
        x1_c = x2 + 4
        y1_c = y2 - 0.6*height
        x2_c = x1_c + 0.6*height
        y2_c = y2
        self.rect_cab = Rectangle(Point(x1_c, y1_c), Point(x2_c, y2_c))
        self.rect_cab.setWidth(2)
        self.rect_cab.setFill("slate gray")
        # create first wheel
        self.tire1 = Wheel(wheel1_center, 0.6*radius, radius)
        # create second wheel
        self.tire2 = Wheel(wheel2_center, 0.6*radius, radius)
        
    def set_color(self, wheel_color, tire_color, body_color):
        self.tire1.set_color(wheel_color, tire_color)
        self.tire2.set_color(wheel_color, tire_color)
        self.rect_body.setFill(body_color)
        
    def draw(self, win):
        self.rect_body.draw(win)
        self.rect_cab.draw(win)
        self.tire1.draw(win)
        self.tire2.draw(win)
        
    def move(self, dx, dy):
        self.tire1.move(dx,dy)
        self.tire2.move(dx,dy)
        self.rect_cab.move(dx,dy)
        self.rect_body.move(dx,dy)
        
    def animate(self, win, dx, dy, moves):
        if moves>0:
            self.move(dx,dy)
            win.after(100, self.animate, win, dx, dy, moves-1)

def main():
    new_win = GraphWin("A Car", 600, 300)
            
    truck = Car(Point(50,100), Point(100,100), 15, 50)
    truck.set_color("red", "black", "blue")
    truck.draw(new_win)

    truck.animate(new_win, 2, 0, 100)
     
    new_win.mainloop()
    
main()