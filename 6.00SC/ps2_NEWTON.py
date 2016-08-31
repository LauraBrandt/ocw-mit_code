# 6.00 Problem Set 2
#
# Successive Approximation
#

def evaluate_poly(poly, x):
    """
    Computes the polynomial function for a given value x. Returns that value.

    Example:
    >>> poly = (0.0, 0.0, 5.0, 9.3, 7.0)    # f(x) = 7x^4 + 9.3x^3 + 5x^2
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 7(-13)^4 + 9.3(-13)^3 + 5(-13)^2
    180339.9

    poly: tuple of numbers, length > 0
    x: number
    returns: float
    """
    result = 0
    for i in range(len(poly)):
        term = poly[i] * x**i
        result += term

    return result

#poly = (0.0, 0.0, 5.0, 9.3, 7.0)
#print evaluate_poly(poly, -13.0)

def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function. If the
    derivative is 0, returns (0.0,).

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    # x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> print compute_deriv(poly)        # 4x^3 + 9x^2 + 35^x
    (0.0, 35.0, 9.0, 4.0)

    poly: tuple of numbers, length > 0
    returns: tuple of numbers
    """
    derivs = []
    for i in range(len(poly)):
        deriv = poly[i]*i
        derivs.append(deriv)
        #print result
        
    # Don't use the first term, because the derivative exponent (x**n) becomes x**(n-1)
    result = tuple(derivs[1:])
    return result
        
##poly = (-13.39, 0.0, 17.5, 3.0, 1.0)
##print compute_deriv(poly)

def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a tuple containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    #x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    (0.80679075379635201, 8.0)

    poly: tuple of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: tuple (float, int)
    """

    x = x_0

    deriv_poly = compute_deriv(poly)
    
    guess = evaluate_poly(poly, x)
    print guess

    num_iters = 1
    while not -epsilon<guess<epsilon:
        x = x - (evaluate_poly(poly, x)/evaluate_poly(deriv_poly, x))
        guess = evaluate_poly(poly, x)
        num_iters += 1
##        print "current guess for x = ", x
##        print "evaluation of current x is", guess
##        print "number of iterations:", num_iters

    return (x,num_iters)

poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    #x^4 + 3x^3 + 17.5x^2 - 13.39
x_0 = 0.1
epsilon = .0001
print compute_root(poly, x_0, epsilon)  # (0.80679075379635201, 8.0)
        
        
        

