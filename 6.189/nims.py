def play_nims(pile, max_stones):
    '''
    An interactive two-person game; also known as Stones.
    @param pile: the number of stones in the pile to start
    @param max_stones: the maximum number of stones you can take on one turn
    '''

    # Make sure that the parameters pile and max_stones are valid
    if not isinstance(pile, int) or not isinstance(max_stones,int):
        return "Parameters must be integers"
    if max_stones > pile:
        return "max_stones must be less than the stones in the pile"

    print "There are", pile, "stones in the pile."
    print "You can take at most", max_stones, "stones."
    print

    player = "Player 1"

    # Play game until there are no more stones in the pile
    while pile > 0:
        # Get player's input, check that it's valid
        while True:
            print player, "-",
            inp = raw_input("How may stones do you want to take? ")
            try:
                stones = int(inp)
            except:
                print "That is not a valid number"
                continue
            if 0 < stones <= max_stones:	# Check that it's a valid number of stones
                pile -= stones
                break
            else:
                print "You can't take that many stones"

        if pile < max_stones:	# Player can't take more that what's left in the pile
            max_stones = pile

        # Print current status
        if pile == 1:	# Grammar
            print "There is", pile, "stone left"
        else:
            print "There are", pile, "stones left"

        # Alternate players
        if pile != 0:   # Don't switch once the game is over
            if player == "Player 1":
                player = "Player 2"
            else:
                player = "Player 1"

    print       
    print "Game over,", player, "wins!"

play_nims(20,5)
