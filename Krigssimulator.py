from random import randint
import plotly.plotly as py
import plotly
import plotly.graph_objs as go

#Simple class holding value, type and a compare function
#Type is not really necessary, but makes the printed results look a bit better
class Card:

    def __init__(self, value, type):
        self.value = value
        self.type = type

    #returns 0 for same value (triggers a war), 1 if higher than the other card and -1 if lower
    def compare(self, card):
        diff = self.value - card.value
        return 0 if diff == 0 else diff/abs(diff)

    def __str__(self):
        return str(self.value) + " of " + str(self.type)

    __repr__ = __str__


#Used for both the initial deck and the collection of cards each player has
#self.deck is the remaining cards in a player's deck before they need to shuffle
#self.received is the cards a player has won since they last shuffled
class Deck:

    def __init__(self, player, judge):
        self.judge = judge
        self.deck = []
        self.received = []
        if not player:
            for i in range(4):
                for j in range(13):
                    self.deck.append(Card(j, i))

    #For each suit (0-4), display the remainding cards in the deck followed by the cards in received
    def printDeck(self):
        output = ""
        for i in range(4):
            output += "\n" + str(i)+ ": "
            thisLine = ""
            for card in self.deck:
                if card.type == i:
                    thisLine += str(card.value) + ", " #thisLine created so that received-info can be right-aligned

            output += thisLine + " " * (50-len(thisLine)) + "("
            for card in self.received:
                if card.type == i:
                    output += str(card.value) + ", "
            output += ")"

        output += "\nNext card: " + str(self.deck[0]) if self.deck else "none"
        print(output)

    #Used before dealing the cards, as well as when received becomes the real deck
    def shuffle(self):
        newDeck = []
        while len(self.deck) > 0:
            newDeck.append(self.deck.pop(randint(0, len(self.deck)-1)))
        self.deck = newDeck

    def receive(self, cards):
        self.received += cards

    #Return the card on the top of the deck, as well as checking if a player has lost or needs to shuffle their received cards
    def showCard(self):

        if not self.received and not self.deck:
            print("----------------\nI'm out of cards!!\n----------------")
            self.judge.playerLost(self)
            return
        elif not self.deck:
            self.reset()
            #print("Had to reset")
        card = self.deck.pop(0)
        return card

    def reset(self):
        self.deck = self.received
        self.shuffle()
        self.received = []

#Keeps track of the players and results
#self.pot is whichever cards are currently being played for. Normally the two in play, but larger if a war is happening
class Judge:

    def __init__(self):
        self.player1 = Deck(True, self) #initially empty
        self.player2 = Deck(True, self) #initially empty
        self.pot = []
        deck = Deck(False, self)
        deck.shuffle()
        for i in range(len(deck.deck)):
            receiver = self.player1 if i % 2== 0 else self.player2
            receiver.receive([deck.deck.pop()])
        self.player1.reset()
        self.player2.reset()
        self.gameOver = False

    def playerLost(self, player):
        print("Game over, player " + str(1 if player == self.player1 else 2) + " is out!")
        self.gameOver = True

    def doRound(self):

        card1 = self.player1.showCard()
        card2 = self.player2.showCard()
        winner = None

        #gameOver is true if one player tries to show a card with no more remaining
        if self.gameOver:
            return

        result = card1.compare(card2)
        self.pot += [card1, card2]

        #if draw, add 3 cards from each deck to the pot, then do the next round
        if(result == 0):
            #print("War started")
            for i in range(3):
                self.pot += [self.player1.showCard(), self.player2.showCard()]
            #print("================\nWAR   " + str(self.pot) + "\n===============")
            self.doRound()
        else:
            if(result == 1):
                winner = self.player1
            elif(result == -1):
                winner = self.player2

            winner.receive(self.pot)
            self.pot = []

    def showPlayers(self):
        print("Player 1:")
        self.player1.printDeck()
        print("\nPlayer 2:")
        self.player2.printDeck()
        print("----------------------------------")


judge = Judge()
counter = 0
total = 0
totalWithoutNoEnds = 0
rounds = 100000
maxRound = 0
noEnd = 0
roundResults = []
threshold = 10000

#Plays a set amount of games, and finds average game length, number of infinite games and longest game
for i in range(rounds):

    while not judge.gameOver:
        #judge.showPlayers()
        judge.doRound()
        counter += 1
        if(counter >= threshold):
            judge.showPlayers()
            print("No end in sight")
            judge.showPlayers()
            judge.gameOver = True
            noEnd += 1
            totalWithoutNoEnds -= counter
    total += counter
    roundResults.append(counter)
    totalWithoutNoEnds += counter
    if(counter < threshold):
        maxRound = max(maxRound, counter)
    print("Game nr. " + str(i) + " took " + str(counter) + " rounds")
    counter = 0
    judge = Judge()

print("Took " + str(total/rounds) + " (" + str(totalWithoutNoEnds/rounds) + " without infinite games)" + " rounds on average. Max round was "
      + str(maxRound) + ". " + str(noEnd) + " round" + ("" if noEnd == 1 else "s") + " with no end. ")
print(roundResults)


#Following is the code that extracts the data, sorts it into groupings and displays it in a bar graph
occurrences = {}
grouping = 25

for i in roundResults:
    i = i - i%grouping
    if(i in occurrences):
        occurrences[i] += 1
    else:
        occurrences[i] = 1
print(occurrences)
print(len(occurrences))

barGraphArray = []
for i in range(rounds):
    if not i in occurrences:
        barGraphArray.append(0)
    else:
        barGraphArray.append(occurrences[i])
plotly.tools.set_credentials_file(username='Sprekasus', api_key='RgsONdK4bRKMQxLEFMuh')
data = [go.Bar(
            x=[x for x in range(0, max(roundResults), grouping)],
            y=barGraphArray[::grouping]
    )]
print(data)
py.plot(data, filename='basic-bar')





















