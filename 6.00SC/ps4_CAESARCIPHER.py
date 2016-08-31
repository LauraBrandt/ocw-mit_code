# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "ps4_words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
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
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("ps4_fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    assert isinstance(shift, int), 'Shift is not an integer'
    assert shift > -27 and shift < 27, 'Shift %s is not between -27 and 27' % shift
        
    coder = {}
    lower = 'abcdefghijklmnopqrstuvwxyz '
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    length = 27
    # add shifted values for lowercase letters and space
    for i in range(length):
        new_index = (i+shift) % length
        coder[lower[i]] = lower[new_index]
    # add shifted values for uppercase letters, not including space
    for i in range(length-1):
        new_index = (i+shift) % length
        coder[upper[i]] = upper[new_index]
    return coder


def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    return build_coder(shift)

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    return build_coder(-shift)

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    string = ""
    for char in text:
        string += coder.get(char, char)
    return string

##code = apply_coder('hello!', build_encoder(3))  # Should give 'khoor!'
##original = apply_coder('khoor!', build_decoder(3)) # Should give 'hello!'
##print "encoded text:", code
##print "decoded text:", original

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    # Shift is cyclic through the 26 letters plus space
    shift = shift % 27
    
    return apply_coder(text, build_encoder(shift))

##code = apply_shift('This is a test.', -29)  # Should return 'Apq hq hiham a.'
##decode = apply_shift('Apq hq hiham a.', 19) # Should return 'This is a test.'
##print code
##print decode
   
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    # Initialize best values
    best_shift = 0
    most_words = 0
    
    for shift in range(27):    
        # Get the possible string, and count how many real words appear in that string
        poss_string = apply_shift(text, -shift)
        num_words = count_real_words(wordlist, poss_string)
        
        # Check if the number of real words is the most so far, and if it is, keep track of it
        if num_words > most_words:
            most_words = num_words
            best_shift = shift
    return best_shift

def count_real_words(wordlist,text):
    ''' Counts the number of words in a text that are real words

    text: string
    wordlist: list (of strings)
    returns: int
    '''
    count = 0

    words = text.split()
    for word in words:
        if is_word(wordlist, word):
            count += 1
            
    return count
   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    for elem in shifts:
        start = elem[0]
        shift = elem[1]
        text = text[:start] + apply_shift(text[start:], shift)
    return text

##print apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])

#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    return find_best_shifts_rec(wordlist, text, 0)

##text = 'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'       
##shifts = find_best_shifts(wordlist, text)
##print decrypt_multilayer(text, shifts)
###print find_best_shifts(wordlist, 'JufYkaolfapxQdrnzjfkdslafrpfdvpmEurrb?')
##string = random_scrambled(wordlist, 5)
##print string
##shifts = find_best_shifts(wordlist, string)
##result = decrypt_multilayer(string, shifts)
##print result

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """

    ### NOT DONE - steps 4-7, 9, 2.###
    result = []
    for poss_shift in range(27):
        #print "current shift value", poss_shift
        #print "current list", result
        s = text[:start] + apply_shift(text[start:], poss_shift)
        #print s
        word_break = string.find(s, ' ', start)
        #print word_break
        if word_break == -1:
            #print "last word"
            if is_word(wordlist, s[start:]):
                #print "the last word is a word"
                result += [(start, poss_shift)]
                #print result
                return result
        else:
            if is_word(wordlist, s[start:word_break]):
                #print "it's a word"
                result += [(start, poss_shift)]
                #print result
                #print "...entering recursion..."
                shifts = find_best_shifts_rec(wordlist, s, word_break+1)
                #print "...exiting recursion layer..."
                if shifts:
                    #print "recursion returned a result"
                    result += shifts
                    #print result
                    return result
                else:
                    result.pop()
                
    return None

##s = random_scrambled(wordlist, 3)
##print s
##shifts = find_best_shifts_rec(wordlist, s,0)
##print shifts
##print apply_shifts(s, shifts)

##s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18),
##                                                          (12, 16)])
##print s
##shifts = find_best_shifts(wordlist, s)
##print shifts
##print apply_shifts(s, shifts)


def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    fable = get_fable_string()
    shifts = find_best_shifts(wordlist, fable)
    return apply_shifts(fable, shifts)

print decrypt_fable()

    
##An Ingenious Man who had built a flying machine invited a great concourse
##of people to see it go up. at the appointed moment, everything being ready,
##he boarded the car and turned on the power. the machine immediately broke
##through the massive substructure upon which it was builded, and sank out of
##sight into the earth, the aeronaut springing out a rely in time to save
##himself. "well," said he, "i have done enough to demonstrate the correctness
##of my details. the defects," he added, with a add hat the ruined brick work,
##"are merely a sic and fundamental." upon this assurance the people came ox
##ward with subscriptions to build a second machine


