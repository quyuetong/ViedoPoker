import random

# create map to locate card image file.
valueFileMap = [0, 1, 49, 45, 41, 37, 33, 29, 25, 21, 17, 13, 9, 5]
suitMap = {'c': 0, 's': 1, 'h': 2, 'd': 3}


# Card class
class Card:
    def __init__(self, card):
        self.value = card[0]
        self.suit = card[1]

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit


# DrawnCard class
class DrawnCard(Card):
    def __init__(self, card):
        Card.__init__(self, card)
        self.fileName = '%s.gif' % str(valueFileMap[self.value] + suitMap[self.suit])

    def getImageName(self):
        return self.fileName


# Deck class
class Deck:
    def __init__(self):
        self.deck = list()
        for suit in 'hcds':
            for value in range(1, 14):
                self.deck.append([value, suit])
        random.shuffle(self.deck)
        self.discard = list()

# This method drew a random card.
    def deal(self):
        card = self.deck.pop()
        self.discard.append(card)
        return card

    def shuffle(self):
        self.deck.extend(self.discard)
        self.discard = []
        random.shuffle(self.deck)

# This method use to ensure cards on the 2nd and 3rd line same to 1st line when player first deal.
    def dealTaget(self, card):
        for i in range(len(self.deck)):
            if self.deck[i] == card:
                self.discard.append(card)
                self.deck.pop(i)
                break


# Player hand class
class Hand:
    def __init__(self):
        self.deck = []
        for i in range(3):
            newdeck = Deck()
            self.deck.append(newdeck)
        self.hand = [[], [], []]

    def newHand(self):
        for i in range(3):
            self.deck[i].shuffle()
            self.hand[i] = []
        for i in range(5):
            # Drew a random card on 1st line, and then get same card on 2nd and 3rd line.
            deal = self.deck[0].deal()
            self.deck[1].dealTaget(deal)
            self.deck[2].dealTaget(deal)
            for j in range(3):
                card = DrawnCard(deal)
                self.hand[j].append(card)
        return self.hand

    # Change card.
    def exchangeHand(self, indexList):
        for i in indexList:
            for j in range(3):
                card = DrawnCard(self.deck[j].deal())
                self.hand[j][i] = card
        return self.hand

    # Evaluate hand and return winning information.
    def evaluate(self, bet):
        first_hand = self.evaluateHelper(self.hand[0])
        second_hand = self.evaluateHelper(self.hand[1])
        third_hand = self.evaluateHelper(self.hand[2])
        highest_win = max(first_hand[0], second_hand[0], third_hand[0])
        win_str = {0: '', 1: "Jacks or Higher", 2: "Two Pair", 3: "Three of a Kind",
                   4: "Straight", 6: "Flush", 9: "Full House", 25: "Four of a Kind",
                   50: "Straight Flush", 800: "Royal Flush"}
        total_win = (first_hand[0] + second_hand[0] + third_hand[0]) * bet
        return total_win, win_str[highest_win], first_hand, second_hand, third_hand

    # Evaluate hand from higher to lower.
    def evaluateHelper(self, hand):
        values = list()
        suits = list()
        for card in hand:
            values.append(card.getValue())
            suits.append(card.getSuit())
        values.sort()
        isFlush = self.isFlush(suits)
        isStraight = self.isStraight(values)
        if isFlush and isStraight:
            if isStraight > 1:
                return 800, "Wooooooooo! Royal Flush!"
            else:
                return 50, "That's pretty cool! Straight Flush!"
        elif self.fourOfAKind(values):
            return 25, "Nice hand! Four of a Kind!"
        elif self.fullHouse(values):
            return 9, "Nice hand! Full House!"
        elif isFlush:
            return 6, "Flush!"
        elif isStraight:
            return 4, "Straight!"
        elif self.threeOfAKind(values):
            return 3, "Three of a Kind!"
        elif self. twoPairs(values[:]):
            return 2, "Two pairs!"
        elif self.JackOrHigher(values):
            return 1, "Jack or Higher!"
        else:
            return 0, "Oops :("

    def isFlush(self, suits):
        for i in range(1, len(suits)):
            if suits[i] != suits[i-1]:
                return False
        return True

    def isStraight(self, values):
        highStraight = [1, 10, 11, 12, 13]
        if values == highStraight:
            return 2
        elif values[4] - values[3] == values[3] - values[2] == values[2] - values[1] == values[1] - values[0] == 1:
            return 1
        else:
            return 0

    def fourOfAKind(self, values):
        if values[0] == values[3] or values[1] == values[4]:
            return True
        else:
            return False

    def fullHouse(self, values):
        if (values[0] == values[1] and values[2] == values[4]) \
                or (values[0] == values[2] and values[3] == values[4]):
            return True
        else:
            return False

    def threeOfAKind(self, values):
        if values[0] == values[1] == values[2]:
            return True
        elif values[1] == values[2] == values[3]:
            return True
        elif values[2] == values[3] == values[4]:
            return True
        else:
            return False

    def twoPairs(self, values):
        size = 0
        for i in range(len(values)):
            if values[i] != values[size]:
                size += 1
                values[size] = values[i]
        if size == 2:
            return True
        else:
            return False

    def JackOrHigher(self, values):
        pre = 0
        for value in values:
            if value == pre and (value > 10 or value == 1):
                return True
            pre = value
        return False
