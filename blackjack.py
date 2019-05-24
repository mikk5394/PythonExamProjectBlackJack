import random
import os

class Card:
    
    def __init__(self, suit, type, value):
        self.suit = suit
        self.type = type
        self.value = value

    def show(self):
        print(f"{self.type} of {self.suit}")


class Deck:

    def __init__(self):
       self.cards = []
       self.build()
    
    def build(self):
        
        for s in ["Hearts", "Spades", "Clubs", "Diamonds"]:
            type = 2
            for v in range(2,11):
                self.cards.append(Card(s, type, v))
                type += 1
            self.cards.append(Card(s, "Jack", 10))
            self.cards.append(Card(s, "Queen", 10))
            self.cards.append(Card(s, "King", 10))
            self.cards.append(Card(s, "Ace", 11))
    
    def show(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def drawCard(self):
        return self.cards.pop()


class Player:

    #When the game starts the player decides how much to buy in for.
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.value = 0
        self.cash = 0


    #In blackjack the player starts with 2 cards
    def draw(self, deck):
        if len(self.hand) == 0 and self.name != "dealer":
            while len(self.hand) < 2:
                self.hand.append(deck.drawCard())
        else:
            self.hand.append(deck.drawCard())   

    def calc_val(self):
        value = 0

        for v in self.hand:
            value += v.value
        
        if value > 21 and self.contains_ace() == True:

            amountOfAces = 0

            for c in self.hand:
                if c.type == "Ace":
                    amountOfAces += 1
                    c.value = 1

            value = 0
            for v in self.hand:
                value += v.value

            if amountOfAces > 1 and value <= 11:                                #In case the player draws 2x aces in the beginning the value is 12 and not 1 or 22
                for i in range(len(self.hand)):
                    if self.hand[i].type == "Ace" and self.hand[i].value == 1:
                        self.hand[i].value = 11
                        break
       
            value = 0
            for v in self.hand:
                value += v.value

        return value

    def showhand(self):
        for c in self.hand:
            c.show()
    
    def discard(self):
        return self.hand.pop()

    def contains_ace(self):
        for c in self.hand:
            if c.type == "Ace":
                return True
    
    def blackjack(self):
        if len(self.hand) == 2:
            if (self.hand[0].type == "Ace" and self.hand[1].type == "Jack") or (self.hand[0].type == "Jack" and self.hand[1].type == "Ace"):
                return True


class Blackjack:

    def __init__(self, player, dealer, deck):
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.game_running = True
        self.player_bet = 0

    def update(self):
        os.system("clear")

        print()
        print("Hand of the dealer:")
        self.dealer.showhand()
        print()

        print(f"Dealer total: {dealer.calc_val()}. Total cards: {len(self.dealer.hand)}")

        print("================================")

        print(f"Player total: {player.calc_val()}. Total cards: {len(self.player.hand)}")
        
        print()
        print("Hand of the player:")
        self.player.showhand()
        print()
        print(f"Balance: {self.player.cash - self.player_bet} - your bet for this game is: {self.player_bet}")
        print()

    def choice_player(self):

        self.check_who_won()
        if self.player.calc_val() <= 21 and self.game_running == True:
            print(f"{self.player.name} your value is {self.player.calc_val()}. Press 1 to hit and 2 to stand.")
            while True:
                if input() == "1":                       
                    self.player.draw(self.deck)
                    break
                elif input() == "2":
                    while self.dealer.calc_val() < 17 and self.dealer.calc_val() < 22:
                        self.dealer.draw(self.deck)
                    if self.dealer.calc_val() == self.player.calc_val() and self.dealer.calc_val() < 17:
                        self.dealer.draw(self.deck)
                    break
        elif self.game_running == True:
            print(f"You overdrew and lost {self.player_bet}!")
            self.player.cash -= self.player_bet
            self.game_running = False


    def check_who_won(self):
        sumD = self.dealer.calc_val()
        sumP = self.player.calc_val()

        if sumD > sumP and sumD < 22 and len(self.dealer.hand) > 1 and sumD > 16:
            if self.dealer.blackjack() == True:
                print(f"The dealer hit a blackjack and the player lost {self.player_bet}!")
                self.player.cash -= self.player_bet
                self.game_running = False
            else:
                print(f"The dealer won and the player lost {self.player_bet}!")
                self.player.cash -= self.player_bet
                self.game_running = False
        elif sumD > 21 or (sumD < sumP and sumP > sumD and len(self.dealer.hand) > 1):
            if self.player.blackjack() == True:
                self.player.cash = (self.player_bet * 2)
                print(f"The player hit a blackjack and won {self.player.bet * 2}! Original bet was {self.player_bet}")
                self.player.cash += (self.player_bet * 2)
                self.game_running = False
            else:
                self.player.cash = (self.player_bet * 2)
                print(f"The player won {self.player_bet * 2}! Original bet was {self.player_bet}")
                self.player.cash += (self.player_bet * 2)
                self.game_running = False
        elif sumP == 21 and sumD == 21:
            if self.player.blackjack() == True and self.dealer.blackjack() == False:
                print(f"The player hit a blackjack and won {self.player.bet * 2}! Original bet was {self.player_bet}")
                self.player.cash += (self.player_bet * 2)
            elif self.player.blackjack() == False and self.dealer.blackjack() == True:
                print(f"The dealer hit a blackjack and the player lost {self.player_bet}!")
                self.player.cash -= self.player_bet
            else: 
                print(f"Game is a tie! Original bet from the player ({self.player_bet}) refunded!")
                self.player.cash += self.player_bet
        elif sumP == sumD and sumD > 16:
            print(f"Game is a tie! Original bet from the player ({self.player_bet}) refunded!")
            self.player.cash += self.player_bet
            self.game_running = False

    def run_game(self):

        os.system("clear")
        print("Welcome to Python-Blackjack!")
        
        self.player.draw(self.deck)
        self.dealer.draw(self.deck) 

        while True:
            try:
                self.player_bet = int(input(f"How much do you wish to bet? Your balance is {self.player.cash}! "))
                if type(self.player_bet) == int and (self.player.cash - self.player_bet >= 0):
                    break
            except:
                print("Input has to be a number and you can't go below your balance!")

        self.update()
        while self.game_running == True:
            self.choice_player()
            if self.game_running == False:
                continue
            self.update()
            

deck = Deck()
deck.shuffle()
player = Player("Mikkel")
dealer = Player("dealer")
bj = Blackjack(player, dealer, deck)

while True:
    try:
        bj.player.cash = int(input("How much do you wish to buy in for? "))
        if type(bj.player.cash) == int:
            break
    except:
        print("Input has to be a number!")

while True:
    bj.run_game()
    if bj.player.cash == 0:
        print("Your balance is 0, game over!")
        quit()
    if input("Play again? Press any key to play or press q to quit! ") == "qs":
        quit()
    else:
        
        bj.game_running = True
        bj.player_bet = 0
        player.hand = []
        dealer.hand = []