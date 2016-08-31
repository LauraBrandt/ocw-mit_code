from random import randrange
from string import *
from hangman_lib import *

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
# Import hangman words

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = split(line)
    print "  ", len(wordlist), "words loaded."
    print "Let's play a game of hangman!"
    print "Art created by sk\n"
    return wordlist

# actually load the dictionary of words and point to it with 
# the words_dict variable so that it can be accessed from anywhere
# in the program
words_dict = load_words()


# Run get_word() within your program to generate a random secret word
# by using a line like this within your program:
# secret_word = get_word()

def get_word():
    """
    Returns a random word from the word list
    """
    word=words_dict[randrange(0,len(words_dict))]
    return word

# end of helper code
# -----------------------------------


# CONSTANTS
# MAX_GUESSES = 6 # Must be 6 to use the ascii art

# GLOBAL VARIABLES 
secret_word = 'claptrap' 
letters_guessed = []
MAX_GUESSES = 0 # This will change by running the choose_level() function. If it is 6 (medium level), ascii art will display

def choose_level():
    ''' Updates the MAX_GUESSES global variable to 10, 6, or 4
        based on user input
    '''
    global MAX_GUESSES
    acceptable = ['easy', 'medium', 'hard', 'e', 'm', 'h']
    while True:
        inp = raw_input("Please choose a level - 'easy', 'medium', or 'hard': ")
        level = inp.lower()
        if level in acceptable:
            break
        else:
            print "Invalid input."  
    if level == 'easy' or level == 'e':
        MAX_GUESSES = 10
    elif level == 'medium' or level == 'm':
        MAX_GUESSES = 6
    elif level == 'hard' or level == 'h':
        MAX_GUESSES = 4
    
def word_guessed():
    '''
	Returns True if the player has successfully guessed the word,
    and False otherwise.
    '''
    global secret_word
    global letters_guessed
	
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def print_guessed():
    '''
    Returns the characters you have guessed in the secret word so far
    '''
    global secret_word
    global letters_guessed
    
    word_so_far = []
    for char in secret_word:
        if char in letters_guessed:
            word_so_far.append(char)
        else:
            word_so_far.append('-')
    return join(word_so_far,'')
    

def play_hangman():
    # Actually play the hangman game
    global secret_word
    global letters_guessed
    global MAX_GUESSES
    
    choose_level()
    
    guesses_left = MAX_GUESSES

    secret_word  = get_word()
    
    print "You have", guesses_left, "guesses remaining."
    
    while True:
        print "\nYour word is:", print_guessed()
        
        new_letter = raw_input("\nGuess a letter, or the full word if you think you know it: ")
        new_letter = new_letter.lower()
        #print "letter:", new_letter
        
        # Make sure the player didn't already guess it
        if new_letter in letters_guessed:
            print "You have already guessed that letter."
            continue
        else:
            letters_guessed.append(new_letter)
        #print "letters_guessed:", letters_guessed
        
        # Let's user guess the full word
        if new_letter == secret_word:
            print "Congratulations, you won!"
            print "The word was '" + secret_word + "'."
            break
            
        # Check if their guess is correct
        if new_letter not in secret_word:
            guesses_left -= 1
            print "Sorry, no " + new_letter + "'s!",
        else:
            print "Correct!",
        
        if MAX_GUESSES == 6:
            print
            print_hangman_image(MAX_GUESSES-guesses_left)
            print "Art created by sk\n"
            print
        
        if guesses_left == 1:   # Grammar
            print "You have", guesses_left, "guess remaining."
        else:
            print "You have", guesses_left, "guesses remaining."
        
        # Player lost
        if guesses_left == 0:
            print "Out of guesses, you lose!"
            print "The word was '" + secret_word + "'."
            break
        # Player won
        elif word_guessed():
            print "Congratulations, you won!"
            print "The word was '" + secret_word + "'."
            break
        
        print "So far you have guessed:", join(letters_guessed,',')

    return None

play_hangman()
