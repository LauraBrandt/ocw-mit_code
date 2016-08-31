def printMultiples(n, max):
	m = 1
	while m<=max:
		print m*n, "\t",
		m += 1
	print "\n"

# printMultiples(2,11)
# printMultiples(5,11)

def printMultTable(max):
	n = 1
	while n<=max:
		printMultiples(n,max)
		n += 1

printMultTable(10)


	
