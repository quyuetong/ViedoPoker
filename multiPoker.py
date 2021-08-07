from tkinter import *
from tkinter import messagebox
import cards


class MultiVideoPoker:
    def __init__(self):
        self.deck = cards.Hand()
        self.cardsImage = [[], [], []]
        self.hand = []
        self.isStart = True
        self.inGameProcess = False
        self.isOver = False
        self.credits = 300
        self.defaultbet = 5
        self.bet = 5
        self.GraphicUI()

    # Control action for deal button
    def buttonControl(self):
        if self.isOver:
            self.newGame()
        elif not self.inGameProcess:
            self.processBet()
        elif self.inGameProcess:
            self.evaluateHand()

    # Control mouse click to flip cards player want to change.
    # If a card on first line is labeled to change, the card on other lines should do same.
    def flip(self, event):
        if not self.inGameProcess:
            return
        if event.widget.isFlipped:
            event.widget.isFlipped = False
            event.widget.configure(image=event.widget.cardimage)
            for i in range(len(self.cardsImage[0])):
                if self.cardsImage[0][i] == event.widget:
                    self.cardsImage[1][i].isFlipped = False
                    self.cardsImage[2][i].isFlipped = False
                    self.cardsImage[1][i].configure(image=self.cardsImage[1][i].cardimage)
                    self.cardsImage[2][i].configure(image=self.cardsImage[2][i].cardimage)
        else:
            event.widget.isFlipped = True
            event.widget.configure(image=self.backImgFile)
            for i in range(len(self.cardsImage[0])):
                if self.cardsImage[0][i] == event.widget:
                    self.cardsImage[1][i].isFlipped = True
                    self.cardsImage[2][i].isFlipped = True
                    self.cardsImage[1][i].configure(image=self.backImgFile)
                    self.cardsImage[2][i].configure(image=self.backImgFile)

    # Init a new game, reset credits, default bet etc.
    def newGame(self):
        for subImg in self.cardsImage:
            for image in subImg:
                image.configure(image=self.backImgFile)
                image.isFlipped = True
        self.isOver = False
        self.inGameProcess = False
        self.credits = 300
        self.defaultbet = 5
        self.bet = 5
        self.updateCredits()
        self.bet_amt_fld.configure(state=NORMAL)
        self.bet_str.set(str(self.defaultbet))
        self.button.configure(text='Deal')
        self.status_label.configure(text='Click Deal to Play.')

    # Process bet,  prevent invalid bet.
    def processBet(self):
        b_str = self.bet_str.get()
        try:
            self.bet = int(b_str)
        except ValueError:
            self.invalidBet("Invalid bet!", "The bet must be an integer!")
            return
        if self.bet * 3 > self.credits:
            self.invalidBet("Invalid bet!", "You credits is not enough to bet that amount!")
            return
        elif self.bet < 1:
            self.invalidBet("Invalid bet!!", "The bet can only be positive number!")
            return

        self.hand = self.deck.newHand()
        self.showCardImg()
        self.credits -= self.bet * 3
        self.updateCredits()
        self.button.configure(text="Exchange/skip")
        self.status_label.configure(text="Choose cards from main line to exchange by " + "clicking on them.")
        self.line1_status.configure(text='Good Luck!')
        self.line2_status.configure(text='Good Luck!')
        self.line3_status.configure(text='Good Luck!')
        self.bet_amt_fld.configure(state=DISABLED)
        self.inGameProcess = True

    # Display card image.
    def showCardImg(self):
        for i in range(3):
            for cardimg, card in zip(self.cardsImage[i], self.hand[i]):
                cardfile = 'cards/%s' % card.getImageName()
                img = PhotoImage(file=cardfile)
                cardimg.configure(image=img)
                cardimg.cardimage = img
                cardimg.isFlipped = False

    def invalidBet(self, title, message):
        messagebox.showerror(title, message)
        self.bet = self.defaultbet
        self.bet_str.set(str(self.defaultbet))

    def updateCredits(self):
        txt_str = "${0:}".format(self.credits)
        self.credits_amt_label.configure(text=txt_str)

    # This method control action when player change card and evaluate hand.
    def evaluateHand(self):
        ex = []

        # Check which card player wants to change and add it position in change list.
        for i in range(len(self.cardsImage[0])):
            if self.cardsImage[0][i].isFlipped:
                ex.append(i)

        self.hand = self.deck.exchangeHand(ex)
        self.showCardImg()
        result = self.deck.evaluate(self.bet)
        winnings = result[0]

        # Display result message.
        if winnings:
            self.credits += winnings
            win_str = 'You highest hand is ' + result[1] + '. '
            win_str += "Total pays ${0:}!".format(winnings)
            self.updateCredits()
        else:
            win_str = ''
            win_str += "Oops, You got nothing in this turn!"
            if self.credits < 3:
                win_str += " :( Game Over!"
                self.isOver = True

        # Display result for each line.
        line1_str = result[3][1]
        line1_str += " Line 1 pays you ${0:}".format(result[3][0] * self.bet) if result[3][0] > 0 else ''
        line2_str = result[4][1]
        line2_str += " Line 2 pays you ${0:}".format(result[4][0] * self.bet) if result[4][0] > 0 else ''
        line3_str = result[2][1]
        line3_str += " Line 3 pays you ${0:}".format(result[2][0] * self.bet) if result[2][0] > 0 else ''

        self.status_label.configure(text=win_str)
        self.line1_status.configure(text=line1_str)
        self.line2_status.configure(text=line2_str)
        self.line3_status.configure(text=line3_str)

        # If player's credit lower than 3, start a new game.
        if self.isOver:
            self.button.configure(text="New game")
        else:
            self.button.configure(text="Deal again")
            self.bet_amt_fld.configure(state=NORMAL)

        # Change default bet to last bet amount if credits is enough.
        # Otherwise set to the highest amount related to current credits.
        self.defaultbet = self.bet if self.bet * 3 <= self.credits else int(self.credits / 3)
        self.bet_str.set(str(self.defaultbet))
        self.inGameProcess = False
        self.hand = []

    # GUI configuration
    def GraphicUI(self):
        self.root = Tk()
        self.root.title('MultiPoker')
        self.backImgFile = PhotoImage(file="cards/back.gif")

        pay_rate = Button(self.root, text="Click to check pays rate.", command=self.payRate)
        pay_rate.grid(row=0, column=1, columnspan=3, pady=5, ipadx=10, ipady=10, sticky=W + E)

        self.status_label = Label(self.root, bd=1, relief=SUNKEN,
                                  text="Multiple Video Poker! " + "Click 'Deal' to play!")
        self.status_label.grid(row=1, column=0, columnspan=5, padx=10, pady=10,
                               ipadx=10, ipady=10, sticky=W + E + S + N)

        for i in range(5):
            card = Label(self.root, image=self.backImgFile)
            card.grid(row=6, column=i, padx=15, pady=10)
            card.bind("<Button-1>", self.flip)
            card.isFlipped = True
            self.cardsImage[0].append(card)
        for i in range(2):
            row = 2 + i * 2
            for j in range(5):
                card = Label(self.root, image=self.backImgFile)
                card.grid(row=row, column=j, padx=15, pady=10)
                card.isFlipped = True
                self.cardsImage[i+1].append(card)

        self.line1_status = Label(self.root, bd=1, relief=SUNKEN, text='')
        self.line1_status.grid(row=3, column=0, columnspan=5, sticky=W + E)

        self.line2_status = Label(self.root, bd=1, relief=SUNKEN, text='')
        self.line2_status.grid(row=5, column=0, columnspan=5, sticky=W + E)

        self.line3_status = Label(self.root, bd=1, relief=SUNKEN, text='')
        self.line3_status.grid(row=7, column=0, columnspan=5, sticky=W + E)

        self.credits_label = Label(self.root, text="Credits ($):")
        self.credits_label.grid(row=8, column=0, padx=10, pady=2, sticky=W)

        self.credits_amt_label = Label(self.root, text="")
        self.credits_amt_label.grid(row=8, column=1, columnspan=2, padx=10, pady=2, sticky=W)

        self.bet_label = Label(self.root, text="Each line bet ($):")
        self.bet_label.grid(row=9, column=0, padx=10, pady=2, sticky=W)
        self.updateCredits()
        self.bet_str = StringVar()
        self.bet_str.set(str(self.defaultbet))

        self.bet_amt_fld = Entry(self.root, textvariable=self.bet_str)
        self.bet_amt_fld.grid(row=9, column=1, columnspan=2, padx=10, pady=2, sticky=W)

        self.button = Button(self.root, text="Deal", command=self.buttonControl)
        self.button.grid(row=8, column=3, rowspan=2, columnspan=2, sticky=W + E + S + N, padx=10)

        empty_label = Label(self.root, text="")
        empty_label.grid(row=10, column=0, columnspan=5, pady=10)

    # Pay rate table GUI
    def payRate(self):
        payRate = Toplevel(self.root)
        payRate.transient(self.root)
        rate = {1: "Jacks or Higher", 2: "Two Pair", 3: "Three of a Kind",
                   4: "Straight", 6: "Flush", 9: "Full House", 25: "Four of a Kind",
                   50: "Straight Flush", 800: "Royal Flush"}
        row = 1
        for i in sorted(rate.keys(), reverse=True):
            label = Label(payRate, text=rate[i])
            label.grid(row=row, column=1, columnspan=2, sticky=W)
            label = Label(payRate, text="1 : %d" % i)
            label.grid(row=row, column=3, sticky=E)
            row += 1
        label = Label(payRate, text='')
        label.grid(row=1, column=0, padx=20)
        label = Label(payRate, text='')
        label.grid(row=1, column=4, padx=20)
        label = Label(payRate, text='')
        label.grid(row=0, column=0, pady=10)
        label = Label(payRate, text='')
        label.grid(row=10, column=0, pady=10)
        payRate.title("Pays Rate Info")
        payRate.parent = self.root
        payRate.geometry("+{0}+{1}".format(self.root.winfo_rootx() + 150, self.root.winfo_rooty() + 150))
        payRate.focus_set()
        payRate.grab_set()
        payRate.mainloop()

if __name__ == '__main__':
    game = MultiVideoPoker()
    mainloop()
