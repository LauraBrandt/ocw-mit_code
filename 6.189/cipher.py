## Encrypts a phrase using the Caeser cipher

## Get phrase to encode and shift value
phrase = raw_input("Please enter the phrase you would like to encode: ")
while True:
	shift = raw_input("Enter the number you would like to shift by: ")
	try: 
		shift = int(shift)
		break
	except:
		print "Please enter an integer value."

## Shift each alphabetic character in a cyclical manner. Leave the other characters as they are.
for char in phrase:
	num = ord(char)
	if num in range(65,91):
		#print "old:", num
		num = ((num-65 + shift)%(91-65)) + 65
		new_char = chr(num)
		#print "new:", num
	elif num in range(97,123):
		#print "old:", num
		num = ((num-97 + shift)%(123-97)) + 97
		new_char = chr(num)
		#print "new:", num
	else: new_char = char	
	# print new_char
	phrase += new_char
# print phrase, len(phrase)
phrase = phrase[len(phrase)/2:]

## Print result
print "The encoded phrase is", phrase