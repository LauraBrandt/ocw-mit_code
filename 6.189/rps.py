p1 = raw_input("Player 1? ")
p2 = raw_input("Player 2? ")

p1 = p1.lower()
p2 = p2.lower()

if p1 == "rock":
	if p2 == "scissors":
		print "Player 1 wins!"
	elif p2 == "paper":
		print "Player 2 wins!"
	elif p2 == "rock":
		print "It's a tie!"
	else:
		print "Player 2 - Not a valid entry"
elif p1 == "paper":
	if p2 == "scissors":
		print "Player 2 wins!"
	elif p2 == "rock":
		print "Player 1 wins!"
	elif p2 == "paper":
		print "It's a tie!"
	else:
		print "Player 2 - Not a valid entry"
elif p1 == "scissors":
	if p2 == "paper":
		print "Player 1 wins!"
	elif p2 == "rock":
		print "Player 2 wins!"
	elif p2 == "scissors":
		print "It's a tie!"
	else:
		print "Player 2 - Not a valid entry"
else: print "Player 1 - Not a valid entry"
