import string

VOWELS = ['a', 'e', 'i', 'o', 'u']

def find_first_vowel(word):
	# returns the index of the first vowel in the string word
	i = 0
	for char in word:
		if char in VOWELS:
			return i
		i = i+1
	return -1

## Test cases	
# print find_first_vowel("image") # 0
# print find_first_vowel("boot") # 1
# print find_first_vowel("this") # 2
# print find_first_vowel("string") # 3

def move_punct_end(word):
	# moves all non-letter characters to the end of the word
	index = 0
	for char in word:
		if char not in string.lowercase and char != "-": 	# punctuation or special characters
			index = string.find(word, char, index, len(word))
			word = word[:index] + word[index+1:] + word[index]	 # move character to the end
		#print "char:", char, "/ index:", index, "/ word:", word
	return word

# print move_punct_end("b!!an,g?")  # bang!!,?
		
def pig_latin(word):
        # word is a string to convert to pig-latin
	word = word.lower()
	break_point = find_first_vowel(word)
	
	if break_point == 0:		# word starts with a vowel
		new_word = word + "-hay"
	elif word[0:2] == 'qu':		# special case
		new_word = word[2:] + '-' + word[0:2] + 'ay'
	else:
		new_word = word[break_point:] + "-" + word[:break_point] + "ay"
	# deal with punctuation or other characters
	new_word = move_punct_end(new_word)
	return new_word 

## Test cases
# print pig_latin("image")  # image-hay
# print pig_latin("boot")  # oot-bay
# print pig_latin("this")  # is-thay
# print pig_latin("string")  # ing-stray
# print pig_latin("queen")  # een-quay

	
def pig_latin_sentence(phrase):
	# phrase contains only words and spaces (no other characters)
	converted_phrase = ''
	lowercase = phrase.lower()
	word_list = lowercase.split()
	for word in word_list:
		converted_phrase += pig_latin(word) + ' '
	return converted_phrase
	
## Test cases:
# phrase1 = "Hello there how are you today"
# phrase2 = "Now consider the tortoise"
# print pig_latin_sentence(phrase1)
# print pig_latin_sentence(phrase2)
	
def pig_latin_converter():
	# asks for user input, then converts that phrase to pig latin
	while True:
		phrase = raw_input("What phrase would you like to convert? (type 'quit' to end)\n> ")
		if phrase.lower() == 'quit':
			print "You have chosen to quit the program"
			return
		print pig_latin_sentence(phrase)
		print
	
pig_latin_converter()
