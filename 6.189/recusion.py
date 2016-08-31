## 1. Write a function that takes in two numbers and recursively multiplies them together
def RecMult(x,y):
    if x == 0:
        return 0
    elif x == 1:
        return y
    else:
        return y + RecMult(x-1,y)
        
##print RecMult(0,5) # 0
##print RecMult(5,4) # 20
##print RecMult(3,0) # 0

## 2. Write a function that takes in a base and an exp and recursively computes base^exp.
def RecExp(base,exp):
    if exp == 0:
        return 1
    else:
        return base * RecExp(base, exp-1)

##print RecExp(0,5) # 0
##print RecExp(2,4)# 16
##print RecExp(3,0) # 1

## 3. Write a function using recursion to print numbers from n to 0.
def print_nums_rec(n):
    print n
    if n == 0:
        return
    elif n < 0:
        print_nums_rec(n+1)
    else:
        print_nums_rec(n-1)

##print_nums_rec(9)
##print_nums_rec(-9)
##print_nums_rec(0)

## 4. Write a function using recursion to print numbers from 0 to n.
def print_nums_rec_up(n):
    if n == 0:
        print n
    elif n<0:
        print_nums_rec_up(n+1)
        print n
    else:
        print_nums_rec_up(n-1)
        print n

##print_nums_rec_up(9)
##print_nums_rec_up(-9)
##print_nums_rec_up(0)

## 5. Write a function using recursion that takes in a string and returns a reversed copy of the string.
def RecReverse(string):
    if len(string) == 0:
        return ""
    else:
        #print string
        return string[-1] + RecReverse(string[:-1])

##print RecReverse("Laura") #aruaL
##print RecReverse("") # ""
##print RecReverse("A") # "A"

## 6. Write a function using recursion to check if a number n is prime
def RecIsPrime(m):
    def primeHelper(n, j):
        if j < 1:
            return None
        if j == 1:
            return True
        else:
            return n % j != 0 and primeHelper(n, j - 1)
    return primeHelper(m, m -1)

### Test:
##primes = []
##for n in range(20):
##    #print n, RecIsPrime(n)
##    if RecIsPrime(n):
##        primes.append(n)
##print primes # [2, 3, 5, 7, 11, 13, 17, 19]


## 7. Write a recursive function that takes in one argument n and computes Fn, the nth value of the Fibonacci sequence.
def RecFib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return RecFib(n-1) + RecFib(n-2)

#### Test:
##for n in range(10):
##    print RecFib(n), # 0 1 1 2 3 5 8 13 21 34          

