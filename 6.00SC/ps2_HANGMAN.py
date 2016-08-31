# Laura Brandt
# 2/13/14
# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "ps2_words.txt"

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
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

def play_hangman():
    '''Plays a game of hangman'''
    
    # Actually load the dictionary of words and point to it with 
    # the wordlist variable
    wordlist = load_words()

    # Choose the word to be guessed
    word = choose_word(wordlist)

    # Start a list that keeps track of the letters guessed so far
    guessed_so_far = []

    # Initialize number of lives (guesses) left
    lives = 8

    print '----------------------------------------------------'
    print 'Welcome to Hangman!'
    print 'I am thinking of a word that is', len(word), 'letters long.'
    print

    # Play game until either the player guesses the word or runs out of lives 
    while not is_won(word, guessed_so_far) and lives > 0:
        # Give the player all the current information
        print "The word is: ", display_word(word, guessed_so_far)
        print "You have", lives, "guesses left."
        if len(guessed_so_far) == 0:
            print "You have not guessed any letters yet."
        else:
            print "So far, you have guessed:", guessed_so_far

        # Player chooses a letter
        guess = get_player_letter(guessed_so_far)
            
        # Add their letter to the list of guessed letters
        guessed_so_far += [guess]

        print '----------------------------------------------------'
        # If guess is correct, add the letter in the correct spot(s) in 'display.
        # If not, subtract a life
        if guess in word:
            print "Good guess!"
        else:
            print "Sorry! No " + guess + "'s"
            lives -= 1
            
    print '\n----------------------------------------------------'
    # Tell the player either that they won or that they lost
    if lives == 0:
        print "You lose! The word was '" + word + "'"
    else:
        print "You got it! The word was '" + word + "'"

def display_word(word, letters_guessed):
    ''' word - type: string
        letters_guessed - type: list

        Returns the word to display -
        if the letter is in the list of letters guessed, prints the letter
        otherwise, prints a line '_'
    '''
    string = ''
    for char in word:
        if char in letters_guessed:
            string += char + ' '
        else:
            string += '_ '
    return string

def get_player_letter(letters_guessed):
    ''' Asks player to guess a letter.
        Verifies that the input is acceptable,
        then returns the letter (lowercase)
    '''
    prompt = "Guess a letter: "
    while True:
        letter = raw_input(prompt)
        letter = letter.lower()
        if letter not in string.ascii_lowercase:
            print "That's not a letter!"
        elif letter in letters_guessed:
            print "You've already guessed", letter
            prompt = "Guess another letter:  "
        else:
            return letter

def is_won(word, letters_guessed):
    ''' word - type: str
        letters_guessed - type: list

        In Hangman, checks if the player has guessed all the letters in a word
        Returns True if so, False otherwise
    '''
    for char in word:
        if char not in letters_guessed:
            return False
    return True
    
play_hangman()
