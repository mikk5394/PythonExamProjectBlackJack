#This class contains all the functionality/classes for my game
import random                                                           #Using the random libary for the shuffle method, line 39 (to shuffle my deck)                                                                                                                                                                                                                                                                                              
import os                                                               #Using the os libary for the os.system("clear") method to clear the console and keep it clean (line 121 ect.)

class Card:                                                             #This class contains the definitions and rules for my cards
    
    def __init__(self, suit, type, value):                              #My Card constructor. Every card has to have a suit, a type and a value (a value for each card is needed for Blackjack to calculate who win, lose or if it's a draw)
        self.suit = suit                                                
        self.type = type                                                #Type can be jack, queen, 9 etc.
        self.value = value

    def show(self):                                                     #A method i use to print the type and the suit of a card                                                         
        print(f"{self.type} of {self.suit}")


class Deck:                                                             #This class contains the definitions and rules for my deck

    def __init__(self):                                                 #My Deck constructor. Every deck has to have a list of cards. When a Deck object is instantiated, the object gets an empty list assigned which is filled with cards (happens in the build method)    
       self.cards = []
       self.build()                                                     #Calls the method 2 lines below every time a new deck is instantiated
    
    def build(self):                                                    #This method fills the empty card array with cards    
        
        for s in ["Hearts", "Spades", "Clubs", "Diamonds"]:             #A loop which loops through the 4 suits - 13 cards are made for each suit in this loop body which amounts to a whole deck                 
            type = 2                                                    #A variable I use to start the type from 2 (since there is no card below 2 in Blackjack - Aces will be explained later)
            for v in range(2,11):                                       #This loop runs from 2 till 10 and construct a card in each iteration
                self.cards.append(Card(s, type, v))                     #Every new card is added to the cards array of the deck
                type += 1                                               #The type is incremented in each iteration so the next card goes 1 up
            self.cards.append(Card(s, "Jack", 10))                      #Since every type after 10 is not a number, I append the remaining 4 card individually as strings
            self.cards.append(Card(s, "Queen", 10))                     
            self.cards.append(Card(s, "King", 10))
            self.cards.append(Card(s, "Ace", 11))
    
    def show(self):                                                     #This method prints out the entire deck in the console. I used this method in the early phases of the program to see if the deck got constructed the right way and if the deck got shuffled correctly.
        for c in self.cards:                                            #Just a simple for loop whose body prints out every card in the deck
            c.show()

    def shuffle(self):                                                  #This method shuffles the entire deck
        random.shuffle(self.cards)                                      #Using the shuffle method to shuffle the cards array of the deck
    
    def drawCard(self):                                                 #This method returns a card and removes it from the deck
        return self.cards.pop()                                         #the pop function removes the last value of a list, if no index is passed as paramater, and returns that value


class Player:                                                           #This class contains the definitions and rules for the players (the dealer is also made from this class, since they share almost all of the same functionality)

    def __init__(self, name):                                           #My Player constructor. Every player in this game (or dealer) has:
        self.name = name                                                #a name,
        self.hand = []                                                  #a hand with cards (which is a list containing card objects),
        #self.value = 0
        if self.name != "dealer":                                                 
            self.cash = 0                                               #a variable to track the balance of the player. Only gets assigned if the player isn't a dealer

    def draw(self, deck):                                               #My draw method which assign card(s) to the hand of the player or dealer
        if len(self.hand) == 0 and self.name != "dealer":               #An if statement that checks wether the game has just started or not (if it's the first round, the player has to draw 2 cards and the dealer has to draw 1). If the hand of the player is empty, the game has just started. Dealers are not supposed to draw 2 cards in the beginning so they are excluded
            while len(self.hand) < 2:                                   #The loop keeps running untill the player has 2 cards
                self.hand.append(deck.drawCard())                       #Appends a card to the hand of the player (only players will ever get inside this loop)
        else:
            self.hand.append(deck.drawCard())                           #If it isn't the first round of the game, only one card is drawn everytime this method is called

    def calc_val(self):                                                 #This method calculates the total value of the Player hand
        value = 0                                                       #A local variable to hold the value (which is returned at the end of the method)

        for v in self.hand:                                             #This loop gets the value of each card in the Player hand and add them to the value variable
            value += v.value                                            #The value of each card is added to the current value at that moment
        
        if value > 21 and self.contains_ace() == True:                  #The body of this if statement solves the "ace issue" (Example: If you draw 2 aces in the beginning you want the value to be 12 and not 22)
                                                                        #This if statement is only accessed if the value of the Player is over 21 and if the Player has > 1 ace on his hand, because in this scenario, the value of the ace or aces should to be set to 1 so the Player doesn't lose
            amountOfAces = 0                                            #This local variable is made to hold the amount of aces in the Players hand 

            for c in self.hand:                                         #This loop iterates through every card in the Players hand and checks the type of each card
                if c.type == "Ace":                                     #Checks if the card is an ace
                    amountOfAces += 1                                   #If the card is an ace the amountOfAces variable is incremented by 1
                    c.value = 1                                         #Then the value of the ace is set to 1. 

            value = 0                                                   #The value is reset so the value can be recounted with the new ace value(s)
            for v in self.hand:                                         #The next 2 lines are the same as line 64 and 65
                value += v.value

            if amountOfAces > 1 and value <= 11:                        #In case the player draws 2x aces in the beginning the value should be 12 and not 22 
                for i in range(len(self.hand)):                         #A loop that iterates an integer for the amount of cards in the Players hand. This integer is used to check indexes on the next line
                    if self.hand[i].type == "Ace" and self.hand[i].value == 1:  #This if statement checks if the card at the given index (index number is the integer variable from the for loop) is an ace or not, and if the ace has a value of 1.
                        self.hand[i].value = 11                         #If the above if statement is true, the value of the ace is set to 11.
                        break                                           #Only the value of one of the aces has to be set to 11 so the loop breaks if that happens (there is never a scenario where you will want to have 2x aces set to 11, since that will give you a minimum value of 22 which makes you lose)    
       
            value = 0                                                   #The value is reset so the value can be recounted with the new ace value     
            for v in self.hand:
                value += v.value

        return value                                                    #The value is then returned

    def showhand(self):                                                 #This method prints out the Players hand
        for c in self.hand:                                             
            c.show()                                                
    
    def discard(self):                                                  #This method discards the last index of the Player-hand list. I never use this method but I thought I would at some point when I made it.
        return self.hand.pop()                                          

    def contains_ace(self):                                             #This method checks if the hand of the Player contains an ace or not    
        for c in self.hand:                                                 
            if c.type == "Ace":                                         #Compares the type of the card at that moment to "Ace" and returns true if the if-statement is true
                return True
    
    def blackjack(self):                                                #This method checks if the Player has a blackjac or not.
        if len(self.hand) == 2:                                         #A blackjack can only occur with 2 cards which is why this if statement exists
            if (self.hand[0].type == "Ace" and self.hand[1].type == "Jack") or (self.hand[0].type == "Jack" and self.hand[1].type == "Ace"): #The types of the two cards are checked and if they together make a blackjack, true is returned
                return True


class Blackjack:                                                        #My Blackjack class which contains all the functionality and rules for the game itself

    def __init__(self, player, dealer, deck):                           #My Blackjack constructor. Every game in my version has to have a:
        self.player = player                                            #a player,
        self.dealer = dealer                                            #a dealer,
        self.deck = deck                                                #a deck to play with
        self.game_running = True                                        #a boolean which shows if the game is running or not
        self.player_bet = 0                                             #a variable that holds the bet of the player

    def run_game(self):                                                 #This method contains the while loop which is responsible for running a single game of blackjack. When this method is called the game is started

        os.system("clear")                                              #Clears the console when the game is started for convenience purposes
        print("Welcome to Python-Blackjack!")   
        
        self.player.draw(self.deck)                                     #The player is assigned 2 cards 
        self.dealer.draw(self.deck)                                     #The dealer is given a card 

        while self.player.cash == 0:                                    #This user will prompt the user to buy in but it will only happen if the player is broke or if the game just started.          
            try:
                self.player.cash = int(input("How much do you wish to buy in for? "))   #The player is asked how much he/she wants to buy in for
                if type(self.player.cash) == int:                       #Breaks the loop if input above is an integer, else the loop runs again
                    break
            except:
                print("Input has to be a number!")                      #Tells the user that the input has to be a number

        while True:                                                     #This while loop will prompt the user for a bet
            try:
                self.player_bet = int(input(f"How much do you wish to bet? Your balance is {self.player.cash}! "))   #The player is asked how much he/she wants to bet.
                if type(self.player_bet) == int and (self.player.cash - self.player_bet >= 0):  #This if-statement makes sure that the player has enough money to make the bet he/she wishes - if not the player is asked to bet again
                    self.player.cash -= self.player_bet
                    break
            except:
                print("Input has to be a number and you can't go below your balance!")

        self.update()                                                   #The board is drawn and the game has begun. Method is explained on line 152
        while self.game_running == True:                                #The game runs as long as the game_running boolean is true
            self.check_who_won()                                        #This method is explained on line 189. It checks if theres a winner, loser or if the game is a draw. If any of the 3 scenarios occur the game_running boolean will be set to False and the game stops (No code in the method below is executed if the boolean is False) 
            self.choice_player()                                        #This method is explained on line 169. 
            if self.game_running == False:                              #If the game is over the loop stops - if not the board is updated
                break
            self.update()                                               #Update happens here

    def update(self):                                                   #This method is responsible for updating the board each time a change has been made that is visible (such as hand, total value ect.)
        os.system("clear")                                              #This method is really handy as it clears the console everytime update() is called which makes the game look nice and manageable
                                                                        #The next 13 lines is pretty self explanatory. It's how the game looks in the console :-)
        print()
        print("Hand of the dealer:")
        self.dealer.showhand()                                      
        print()
        print(f"Dealer total: {self.dealer.calc_val()}. Total cards: {len(self.dealer.hand)}")
        print("================================")
        print(f"Player total: {self.player.calc_val()}. Total cards: {len(self.player.hand)}")
        print()
        print("Hand of the player:")
        self.player.showhand()
        print()
        print(f"Balance: {self.player.cash} - your bet for this game is: {self.player_bet}")
        print()

    def choice_player(self):                                            #This method is responsible for giving the player the choice between hitting or standing. This method is also responsible for checking if the player overdraws or not.
                                                                        #Nothing will happen in this method if the game_running boolean is false.    
        if self.player.calc_val() <= 21 and self.game_running == True:  #If the value of the players hand is 21 or below he will get access to 2 options: hit or stand. This will obviously only happen if the game is still running
            print(f"{self.player.name} your value is {self.player.calc_val()}. Press 1 to hit and 2 to stand.")
            while True:
                if input() == "1":                                      #If the input is 1, the player hits and draws a card
                    self.player.draw(self.deck)
                    break                                               #The loop breaks when the player is given a card (the board is then updated, see line 150 and if the player haven't overdrawn or lost, he will get these 2 options again. This will keep happening till the game has ended)
                elif input() == "2":                                    #If the input is 2, the player stands and the dealer draws till he hits atleast 17.
                    while self.dealer.calc_val() < 17 and self.dealer.calc_val() < 22:   #The code block in this loop makes the dealer keep drawing untill he gets atleast 17 value. If the dealer ends above 21 value he loses
                        self.dealer.draw(self.deck)
                    if self.dealer.calc_val() == self.player.calc_val() and self.dealer.calc_val() < 17:   #This if-statement makes the dealer draw a card if he has the same value as the player, and if the value is under 17. This is done to find a winner. The rules require the dealer to stand if is between 17 and 21 value
                        self.dealer.draw(self.deck)
                    break
        elif self.game_running == True:                                 #This elif will only get executed if the player has overdrawn
            print(f"You overdrew and lost {self.player_bet}!")          
            self.game_running = False                                   #If the player overdraws the game is over


    def check_who_won(self):                                            #This method check all the different situations that can happen in the game and act according to what situation is present in the current game
        sumD = self.dealer.calc_val()                                   #The value of the dealer gets assigned to a local variable for convenience sake
        sumP = self.player.calc_val()                                   #Same with the player

        if sumD > sumP and sumD < 22 and len(self.dealer.hand) > 1 and sumD > 16:   #If this is true, the dealer has won. Notice that the statement checks if the dealer has more than 1 card, as you can't win with a single card in Blackjack.
            if self.dealer.blackjack() == True:                                     #If the dealer hits a blackjack a different print messaged is shown
                print(f"The dealer hit a blackjack and the player lost {self.player_bet}!")
                self.game_running = False
            else:
                print(f"The dealer won and the player lost {self.player_bet}!")
                self.game_running = False
        elif sumD > 21 or (sumD < sumP and sumP > sumD and len(self.dealer.hand) > 1):  #If this is true, the player has won. Reverse scenario of the if statement above
            if self.player.blackjack() == True:
                print(f"The player hit a blackjack and won {self.player.bet * 2}! Original bet was {self.player_bet}")   #If the player hits a blackjack a different print messaged is shown
                self.player.cash += (self.player_bet * 2)                               #The new balance of the player gets updated
                self.game_running = False                                               #The boolean gets set to false since the game is over
            else:
                print(f"The player won {self.player_bet * 2}! Original bet was {self.player_bet}")
                self.player.cash += (self.player_bet * 2)
                self.game_running = False
        elif sumP == 21 and sumD == 21:                                                 #This elif makes sure that it can't be a draw if either the player or the dealer has a blackjack (Since a blackjack beats 21)                         
            if self.player.blackjack() == True and self.dealer.blackjack() == False:
                print(f"The player hit a blackjack and won {self.player.bet * 2}! Original bet was {self.player_bet}")
                self.player.cash += (self.player_bet * 2)
            elif self.player.blackjack() == False and self.dealer.blackjack() == True:
                print(f"The dealer hit a blackjack and the player lost {self.player_bet}!")
        elif sumP == sumD and sumD > 16:                                                #Checks if it's a draw
            print(f"Game is a tie! Original bet from the player ({self.player_bet}) refunded!")
            self.player.cash += self.player_bet
            self.game_running = False