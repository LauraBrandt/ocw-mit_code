import time
import random

##### Basic classes: Card, Deck, Hand (subclass of Deck), CardGame (just creates a shuffled deck) #####

class Card:
    suitList = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rankList = ["narf", "Ace", "2", "3", "4", "5", "6", "7",
                "8", "9", "10", "Jack", "Queen", "King"]
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank   
    def __str__(self):
        return (self.rankList[self.rank] + " of " +
                self.suitList[self.suit])
    def __cmp__(self,other):
        # check the suits
        if self.suit > other.suit: return 1
        if self.suit < other.suit: return -1
        # suits are the same... check ranks
        if self.rank == 1 and not other.rank ==1: return 1   # rank of the first and not the second is Ace
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        # ranks are the same... it's a tie
        return 0

class Deck:
    def __init__(self):
        #create standard 52-card deck
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
    def __str__(self):
        #name of card, for example "7 of Clubs" or "King of Hearts"
        s = ""
        for i in range(len(self.cards)):
            s = s + " "*i + str(self.cards[i]) + "\n"
        return s
    def shuffle(self):
        import random
        nCards = len(self.cards)
        for i in range(nCards):
            j = random.randrange(i, nCards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
    def removeCard(self,card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False
    def popCard(self):
        return self.cards.pop()
    def isEmpty(self):
        return (len(self.cards) == 0)
    def deal(self,hands,nCards=999):
        nHands = len(hands)
        for i in range(nCards):
            if self.isEmpty(): break
            card = self.popCard()
            hand = hands[i % nHands]
            hand.addCard(card)

class Hand(Deck):
    def __init__(self, name=""):
        self.cards = []
        self.name = name
    def __str__(self):
        s = "Hand " + self.name
        if self.isEmpty():
            return s + " is empty\n"
        else:
            return s + " contains: \n" + Deck.__str__(self)
    def addCard(self,card):
        self.cards.append(card)

class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

########## Old Maid ##########

class OldMaidHand(Hand):
    def removeMatches(self):
        count = 0
        originalCards = self.cards[:]
        for card in originalCards:
            match = Card(3 - card.suit, card.rank)
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                print "Hand %s: %s matches %s" % (self.name, card, match)
                count = count + 1
        return count

class OldMaidGame(CardGame):
    def play(self, names):
        #remove Queen of Clubs
        self.deck.removeCard(Card(0,12))

        #make a hand for each player
        self.hands = []
        for name in names:
            self.hands.append(OldMaidHand(name))

        #deal the cards
        self.deck.deal(self.hands)
        print "----------- Cards have been dealt."
        self.printHands()

        #remove initial matches
        numMatches = self.removeAllMatches()

        print "----------- Matches discarded, play begins"
        self.printHands()

        #play until all 50 cards are matched
        turn = 0
        numHands = len(self.hands)
        while numMatches < 25:
            numMatches += self.playOneTurn(turn)
            turn = (turn + 1) % numHands

        print "----------- Game is Over"
        self.printHands()

    def removeAllMatches(self):
        count = 0
        for hand in self.hands:
            count += hand.removeMatches()
        return count

    def printHands(self):
        for hand in self.hands:
            print hand
        
    def playOneTurn(self,i):
        if self.hands[i].isEmpty():
            return 0
        neighbor = self.findNeighbor(i)
        pickedCard = self.hands[neighbor].popCard()
        self.hands[i].addCard(pickedCard)
        print "Hand", self.hands[i].name, "picked", pickedCard
        count = self.hands[i].removeMatches()
        self.hands[i].shuffle()
        return count

    def findNeighbor(self,i):
        numHands = len(self.hands)
        for next in range(1,numHands):
            neighbor = (i + next) % numHands
            if not self.hands[neighbor].isEmpty():
                return neighbor

########## Go Fish ##########

class GoFishHand(Hand):
    def removeMatches(self):      
        i = 0
        while i < len(self.cards):
            card = self.cards[i]
            # pop out the card to check
            self.removeCard(card)
            # check that card against the rest of the cards for a match
            if not self.removeMatch(card):
                # if no match, put the card back where it came from
                self.cards.insert(i,card)
                i += 1           

    def removeMatch(self,card):
        # check the card against each of the cards in the hand
        # if it matches one of the cards in the hand, remove that card from the hand
        # Returns the card
        for myCard in self.cards:
            if myCard.rank == card.rank:
                self.cards.remove(myCard)
                print "Hand %s: %s matches %s" % (self.name, card, myCard)
                return card

    def findMatch(self,rank):
        for myCard in self.cards:
            if myCard.rank == rank:
                return myCard
            
class GoFishGame(CardGame):
    def play(self,names):
        # Give each player a hand
        self.hands = []
        for name in names:
            self.hands.append(GoFishHand(name))

        # Deal the cards
        nCards = 7*len(self.hands)
        self.deck.deal(self.hands,nCards)

        print "----------- Cards have been dealt."
        self.printHands()

        # Remove matches from each hand
        self.removeAllMatches()

        print "----------- Matches discarded, play begins"
        self.printHands()

        # Play until one person runs out of cards or the deck is empty
        numHands = len(self.hands)
        turn = 0
        while True:
            self.playOneTurn(turn)
            self.printHands()
            # When someone runs out of cards, the game is over
            if self.hands[turn].isEmpty():
                break
            # Go to the next player
            turn = (turn + 1) % numHands
            # If the deck is out of cards, the game is over
            if self.deck.isEmpty():
                break     
        if self.deck.isEmpty():
            print "----------- No cards left in the deck, game over."
        else: print "----------- Game is Over,", self.hands[turn].name, "wins!"

    def removeAllMatches(self):
        for hand in self.hands:
            hand.removeMatches()

    def printHands(self):
        print
        for hand in self.hands:
            print hand

    def playOneTurn(self,turn):
        currentPlayer = self.hands[turn]
        next = self.findNeighbor(turn)  # gives a number (index)
        neighbor = self.hands[next]  # the hand at that index
        # Select a card in the hand to try to match - the first card in the shuffled hand
        askCard = currentPlayer.cards[0]
        print currentPlayer.name + " asks " + neighbor.name + \
              ": Do you have any " + askCard.rankList[askCard.rank] + "'s?"
        # Does neighbor have this card?
        match = neighbor.findMatch(askCard.rank)
        if match:
            print neighbor.name, "does."
            # Remove card from neighbor's hand
            neighbor.removeCard(match)
            # Remove the matching card from the current player's hand
            currentPlayer.removeMatch(match)
        else:
            print neighbor.name, "doesn't."
            print "GO FISH!"
            print currentPlayer.name, "draws a card."
            # Draw a card
            newCard = self.deck.popCard()
            # If new card matches a card in the hand, remove the match;
            # otherwise, add the card to the hand
            if not currentPlayer.removeMatch(newCard):
                currentPlayer.addCard(newCard)

        currentPlayer.shuffle() # so not always asking for the same card
          
    def findLNeighbor(self,turn):
        # Returns the neighbor to the left
        numHands = len(self.hands)
        neighbor = (turn + 1) % numHands
        return neighbor

    def findNeighbor(self,turn):
        # Returns the player, not including current player, with the most cards
        numHands = len(self.hands)
        longest = []
        for next in range(1,numHands):
            test = (turn + next) % numHands
            if len(self.hands[test].cards) > len(longest):
                longest = self.hands[test].cards
                neighbor = test
        return neighbor

### Interactive Go Fish ###

class GoFishGame_Interactive(GoFishGame):
    def play(self):
        # Add players

        #get player name
        player = raw_input("Please enter your name:  ")
        #ask user how many opponents they want
        names = ["Mal","Kaylee","Zoe", "Wash", "River", "Simon", "Jayne", "Inara", "Book"]
        nOpponents = raw_input("How many people do you want to play against?  ")
        #make sure they enter an integer that is less than the number of names in the list
        while not nOpponents.isdigit() and nOpponents > 9:
            if nOpponents > 9:
                nOpponents = raw_input("Please choose a number less than 10.  ")
            else: nOpponents = raw_input("How many people do you want to play against?  ")
        #convert to an integer
        nOpponents = int(nOpponents)
        #select that many from a list of names and add them to a list
        self.names = random.sample(names, nOpponents)
        #add the user to the first spot in this list of players
        self.names.insert(0,player)
        #tell the user their opponents
        print "Players in this game: "
        for name in self.names:
            print name
        time.sleep(3)
        
        # Give each player a hand
        self.hands = []
        for name in self.names:
            self.hands.append(GoFishHand(name))
        
        # Deal the cards
        nCards = 7*len(self.hands)
        self.deck.deal(self.hands,nCards)

        print "----------- Cards have been dealt."
        self.printHands()
        time.sleep(2)
        
        # Remove matches from each hand
        self.removeAllMatches()

        print "----------- Matches discarded, play begins \n"

        # Play until one person runs out of cards or the deck is empty
        numHands = len(self.hands)
        turn = 0
        while True:
            if turn == 0:
                self.playUserTurn()
            else:
                self.playOneTurn(turn)
                print
            # When someone runs out of cards, the game is over          
            if self.hands[turn].isEmpty():
                break
            time.sleep(4)
            # Go to the next player
            turn = (turn + 1) % numHands
            # If the deck is out of cards, the game is over
            if self.deck.isEmpty():
                break
        if self.deck.isEmpty():
            print "----------- No cards left in the deck, game over."
        else: print "----------- Game is Over,", self.hands[turn].name, "wins!"

    def playUserTurn(self):
        self.printHands()
        currentPlayer = self.hands[0]

        # Choose neighbor (Hand)
        
        # Get user input for who to draw from
        neighborName = raw_input("Who do you want to take a card from?  ")
        neighborName = neighborName.capitalize()  # modify name to have initial capital
        #make sure user entered a valid player
        while neighborName not in self.names:
            neighborName = raw_input("Who do you want to take a card from?  ")
        #convert neighbor name to neighbor hand
        for i in range(len(self.hands)):
            if neighborName == self.hands[i].name:
                neighbor = self.hands[i]
                
        # Choose card to ask for (index)
        
        # Get user input for which card to ask about
        rank = raw_input("What card do you want to ask for?  ")
        rank = rank.capitalize()  # modify face card names to initial capital
        #make sure user entered a valid card rank
        rankList = currentPlayer.cards[0].rankList
        while rank not in rankList:
            rank = raw_input("What card do you want to ask for?  ")      
        #convert readable rank to rank index
        rankN = rankList.index(rank)
            
        print currentPlayer.name + " asks " + neighbor.name + \
              ": Do you have any " + rank + "'s?"

        # Does neighbor have this kind of card?
        match = neighbor.findMatch(rankN)
        # If they do...
        if match:
            print neighbor.name, "does."
            # Remove card from neighbor's hand
            neighbor.removeCard(match)
            # If card matches a card in the hand, remove the match;
            # otherwise, add the card to the hand
            if not currentPlayer.removeMatch(match):
                currentPlayer.addCard(match)
        # If they don't...
        else:
            print neighbor.name, "doesn't."
            print "GO FISH!"
            print currentPlayer.name, "draws a card."
            # Draw a card
            newCard = self.deck.popCard()
            print "You drew the", newCard
            # If new card matches a card in the hand, remove the match;
            # otherwise, add the card to the hand
            if not currentPlayer.removeMatch(newCard):
                currentPlayer.addCard(newCard)

        self.printHands()

    def printHands(self):
        print self.hands[0]
        for i in range(1,len(self.hands)):
            print self.hands[i].name, "has", len(self.hands[i].cards), "cards"
        print
        
## Testing...
players = ["Laura","Karen","Sarah", "Mom", "Dad"]
game = GoFishGame_Interactive()
game.play()

