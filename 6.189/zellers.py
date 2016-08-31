def zellers(month, day, year):
    '''Given a date, returns the day of the week that day fell on.
        month is a string ('January'-'December'),
        day is a 2-digit number,
        year is a 4-digit number'''
    
    month_dict = {'february': 12, 'october': 8, 'march': 1, 'august': 6,
                  'may': 3, 'december': 10, 'june': 4, 'september': 7,
                  'april': 2, 'january': 11, 'july': 5, 'november': 9                  }
    days_dict = {0:"Sunday",1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",
                 5:"Friday",6:"Saturday"}
    
    #split up the year into the century and the year of that century
    #(first 2 and last 2 digits)
    century = year/100
    year = year%100

    #get number of month
    month = month.lower()
    month = month_dict[month]
    #because the new year starts in March
    if month >10:  #Jan or Feb
        year -= 1

    # compute values for Zeller's algorithm
    W = (13*month - 1) / 5
    X = year/4
    Y = century/4
    Z = W + X + Y + day + year - 2*century
    R = Z%7    # this is the day of the week, where 0 is Sunday, ..., 6 is Saturday

    # convert R to a day:
    day_of_week = days_dict[R]
    return day_of_week


### Test Cases for zellers (should all be True)
##print zellers("March", 10, 1940) == "Sunday"
##print zellers("March",13,1986) == "Thursday"
##print zellers ("November", 9, 2013) == "Saturday"
##print zellers("February", 20, 2014) == "Thursday"
##print zellers("January", 1, 2014) == "Wednesday"



def zellers_interactive():
    ''' Asks for the user's birthday and name,
        and returns the day of the week on which they were born '''
 
    # Get the input and check the data makes sense
    name = raw_input("Enter name: ")

    bad_data = True
    while bad_data:
        dob = raw_input("Enter date of birth (MMDDYYYY): ")
        try:
            int(dob)
        except ValueError:
            print "Invalid date. Make sure to enter the date as a number in the form MMDDYYYY"
            continue
        if len(dob) == 8:
            num_month = int(dob[0:2])
            date = int(dob[2:4])
            year = int(dob[4:])

            if 1<=num_month<=12 and 1<=date<=31:
                bad_data = False
            else:
                print "Invalid date."
        else:
            print "Invalid date. Make sure to enter the date in the form MMDDYYYY"

    # Get the name of the month
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
     6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
     11: "November", 12: "December"}  
    month = months[num_month]

           
    # Find the birth day of the week
    day = zellers(month, date, year)

    # Print out the result
    print name + " was born on a " + day + "."


zellers_interactive()
