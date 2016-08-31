from graphics import *
import math

#########################################################################################
## CLOCK CLASS
#########################################################################################
class Clock:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.ampm = 'AM'
               
    def am_pm(self):
        seconds = self.convertToSeconds()
        if 86400<seconds<90000:  # between 12:00 midnight and 1:00 am
            self.ampm = 'AM'
        elif seconds >= 43200: # after 12:00 noon
           self.ampm = 'PM'
        else:
            self.ampm = 'AM'
                        
    def convertToSeconds(self):
        seconds = self.hour*3600+self.minute*60+self.second
        return seconds
        
    def convertToTime(self, seconds):
        self.hour = seconds//3600
        self.minute = (seconds%3600)//60
        self.second = seconds%60
        
    def update(self):
        seconds = self.convertToSeconds()
        seconds += 1
        # Roll over back to the beginning
        if seconds >= 90000:    # 25:00
            seconds = 3600     # 1:00 am
        self.convertToTime(seconds) 
                               
#########################################################################################
## DIGITAL CLOCK
#########################################################################################      
        
class DigitalClock(Clock):
    def __init__(self, hour=0, minute=0, second=0, pos_ul=Point(5,5)):
        Clock.__init__(self,hour, minute, second)
        self.pos = pos_ul
                 
    def __str__(self): 
        self.am_pm()
        if self.hour>12:
            hour = self.hour-12
        else:
            hour = self.hour
        return "%2d:%02d:%02d %s" % (hour, self.minute, self.second, self.ampm)
            
    def drawFace(self, win):
        # Create a background rectangle for the text to be displayed on
        self.background = Rectangle(Point(self.pos.x,self.pos.y), Point(self.pos.x+200,self.pos.y+100))
        self.background.setWidth(5)
        self.background.setFill("light steel blue")
        self.background.draw(win)
    
    def drawTime(self, win):
        self.display = Text(Point(self.pos.x+100, self.pos.y+50), self)
        self.display.setSize(23)
        self.display.setStyle('bold')
        self.display.setFace('times roman')
        self.display.draw(win)
        
    def draw(self, win):
        self.drawFace(win)
        self.drawTime(win)
        
    def tick(self, win):
        self.update()
        self.display.setText(self)
        win.after(1000, self.tick, win)

#########################################################################################
## ANALOG CLOCK
#########################################################################################      
 
class AnalogClock(Clock):
    def __init__(self, hour=0, minute=0, second=0, center=Point(150,150)):
        Clock.__init__(self, hour, minute, second)
        self.center = center
        self.radius = 100
    
    def drawFace(self, win):
        # Draw the circle
        self.face = Circle(self.center, self.radius)
        self.face.setFill("light steel blue")
        self.face.setWidth(4)
        self.face.draw(win)
        center = Circle(self.center, 2)
        center.setFill('black')
        center.draw(win)
        # Draw ticks and numbers for each hour
        for n in range(12):
            # calculate position on the circle
            angle = n*(2*math.pi)/12
            p_outer = Point(self.center.x + (self.radius*math.cos(angle)),
                            self.center.y + (self.radius*math.sin(angle)))
            p_inner = Point(self.center.x + (0.9*self.radius*math.cos(angle)),
                            self.center.y + (0.9*self.radius*math.sin(angle)))
            # draw the ticks
            line = Line(p_outer,p_inner)
            line.setWidth(2)
            line.draw(win)
            # draw a number 
            text_pos = Point(self.center.x + (0.8*self.radius*math.cos(angle)),
                self.center.y + (0.8*self.radius*math.sin(angle)))
            text = str((n+3)%12) # get the right number at the right position
            if text == '0':
                text = '12'
            hour = Text(text_pos, text)
            hour.draw(win)
        # Draw ticks at each minute
        for n in range(60):
            # calculate position on the circle
            angle = n*(2*math.pi)/60
            p_outer = Point(self.center.x + (self.radius*math.cos(angle)),
                self.center.y + (self.radius*math.sin(angle)))
            p_inner = Point(self.center.x + (0.93*self.radius*math.cos(angle)),
                self.center.y + (0.93*self.radius*math.sin(angle)))
            # draw the ticks
            line = Line(p_inner,p_outer)
            line.draw(win)
            
    def drawHands(self, win):
        #pass
        # Draw hour hand
        angle = ((self.hour-3)%12) * 2*math.pi/12
        angle += (self.minute/60.0)*(2*math.pi/12) # add in a fractional part so the hour hand has intermediate positions
        x = self.center.x + 0.5*self.radius*math.cos(angle)
        y = self.center.y + 0.5*self.radius*math.sin(angle)
        p_outer = Point(x,y)
        self.hour_hand = Line(self.center,p_outer)
        self.hour_hand.setWidth(2)
        self.hour_hand.draw(win)
        # Draw minute hand
        angle = (self.minute-15) * 2*math.pi/60
        x = self.center.x + 0.67*self.radius*math.cos(angle)
        y = self.center.y + 0.67*self.radius*math.sin(angle)
        p_outer = Point(x,y)
        self.minute_hand = Line(self.center,p_outer)
        self.minute_hand.setWidth(2)
        self.minute_hand.draw(win)        
        # Draw second hand
        angle = ((self.second-15)%60) * 2*math.pi/60
        x = self.center.x + 0.67*self.radius*math.cos(angle)
        y = self.center.y + 0.67*self.radius*math.sin(angle)
        p_outer = Point(x,y)
        self.second_hand = Line(self.center,p_outer)
        self.second_hand.draw(win)
        
    def undrawHands(self):
        self.hour_hand.undraw()
        self.minute_hand.undraw()
        self.second_hand.undraw()
        
    def tick(self, win):
        self.update()
        self.undrawHands()
        self.drawHands(win)
        win.after(1000,self.tick,win)
        
#########################################################################################
## RUN
#########################################################################################      

def getTime():
    '''Returns a tuple of the current time: (hour,minute,second)'''
    import datetime
    current_time = datetime.datetime.now().time()
    hour = int(current_time.hour)
    minute = int(current_time.minute)
    second = int(current_time.second)
    return (hour, minute, second)

def runDigital(win):
    time = getTime()
    clock = DigitalClock(time[0], time[1], time[2])
    clock.draw(win)
    clock.tick(win)

def runAnalog(win):
    time = getTime()
    clock = AnalogClock(time[0], time[1], time[2])
    clock.drawFace(win)
    clock.drawHands(win)
    clock.tick(win)

def whichClock():
    '''Displays a window with two buttons, labelled 'Analog Clock' and 'Digital Clock' 
        Once the user clicks one of those two buttons, return a string, 
        either 'Analog' or 'Digital'
    '''
    choice_win = GraphWin("Clock",300,250)

    # Format the question at the top
    question = Text(Point(150,30), "Please choose the type of clock to display:")
    question.setSize(10)
    question.setStyle('bold')
    question.draw(choice_win)

    # Format the first button (analog)
    opt1 = Rectangle(Point(60,65),Point(240,115))
    opt1.setFill('LightSteelBlue3')
    opt1.setOutline('LightSteelBlue2')
    opt1.setWidth(4)
    text1 = Text(Point(150,90), "Analog Clock")

    # Format the second button (digital)
    opt2 = Rectangle(Point(60,150),Point(240,200))
    opt2.setFill('LightSteelBlue3')
    opt2.setOutline('LightSteelBlue2')
    opt2.setWidth(4)
    text2 = Text(Point(150, 175), "Digital Clock")

    # Draw the two buttons
    opt1.draw(choice_win)
    text1.draw(choice_win)
    opt2.draw(choice_win)
    text2.draw(choice_win)

    while True:
        # Let user click one of the two buttons
        choice = choice_win.getMouse()
        # Calculate which choice was clicked
        if 60<choice.x<240:
            if 65<choice.y<115:
                choice_win.close()
                return 'Analog'
            elif 150<choice.y<200:
                choice_win.close()
                return 'Digital' 
                
    
def main(): 
    type = whichClock()
    
    if type == 'Digital':
        clock_win = GraphWin("%s Clock" % type, 205, 105)
        runDigital(clock_win)
    elif type == 'Analog':
        clock_win = GraphWin("%s Clock" % type, 300, 300)
        runAnalog(clock_win)
    else:
        return None
    clock_win.mainloop()
    
main()





