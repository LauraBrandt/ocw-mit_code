from ps3a_WORDGAME import *
import time
from ps3_perm import *


def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    print "Computer is thinking..."
    
    # Find all possible permutations of the length of the hand or less
    # that are also valid words
    poss_words = []
    hand_length = calculate_handlen(hand)
    for n in range(hand_length, 0, -1):
        permutations = get_perms(hand, n)
        for word in permutations:
            if word in word_list:
                poss_words.append(word)
    # Choose the word worth the most points and return it
    highest = 0
    best_word = None
    if len(poss_words) == 0:
        return None
    else:
        for word in poss_words:
            score = get_word_score(word, HAND_SIZE)
            if score > highest:
                highest = score
                best_word = word
    return best_word

### Test:       
##word_list = load_words()
##hand = deal_hand(HAND_SIZE)
##display_hand(hand)
##print comp_choose_word(hand, word_list)

def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:
    1) The hand is displayed.
    2) The computer chooses a word using comp_choose_words(hand, word_dict).
    3) After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.
    4) The sum of the word scores is displayed when the hand finishes.
    5) The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    total_score = 0

    finished = False
    while not finished:
        print
        print "Current hand: ",
        display_hand(hand)
        
        word = comp_choose_word(hand, word_list)

        # If there are no possible words left with the current hand,
        # the game is over
        if word == None:
            finished = True
            print "There are no more possible words."
            continue
        
        word_score = get_word_score(word, HAND_SIZE)
        total_score += word_score
        hand = update_hand(hand, word)
        
        print "'" + word + "' earned " + str(word_score) + " points. Total: " + str(total_score)

    print "\nTotal score for this hand: ", total_score
    print
    return total_score
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    prompt1 = "Please enter: \n'n' to start a new hand, \n'r' to replay the last hand, or \n'e' to exit \n>  "
    prompt2 = "Please press 'u' if you would like to play this hand, or 'c' to let the computer play: "
    hand = None
    while True:
        choice = raw_input(prompt1).lower()

        if choice == 'e':
            break
        elif choice == 'n':
            hand = deal_hand(HAND_SIZE)
        elif choice == 'r':
            if not hand:
                print "*Sorry, no current hand yet. Press 'n' to play a new hand.*"
                continue
        else:
            print "Not a valid choice. Please try again."  

        player = raw_input(prompt2).lower()
        if player == 'u':
            play_hand(hand, word_list)
        elif player == 'c':
            comp_play_hand(hand, word_list)
        else:
            print "I'm sorry, that is not a valid choice."
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
