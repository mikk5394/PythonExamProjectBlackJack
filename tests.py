import unittest
from blackjack import Deck, Player, Blackjack, Card

#Unit tests:
    #Deck build
    #Player draw
    #Value calculation
    #Contains ace
    #Ace values
    #Blackjack
    #Check who won - multiple tests

class Test(unittest.TestCase):

    def test_deck(self):                        #This deck tests if the deck gets created correctly (len of the list is printed out to see if there's the correct amount of cards in it)
        deck = Deck()                           #The build method is called in the deck constructor so the deck is built at this point.
        self.assertTrue(len(deck.cards) == 52, "A deck must contain 52 cards from the beginning")  

    def test_draw(self):                        #This method tests if the player draws correctly. In the beginning the player should draw 2 cards and then 1 card each time onwards when the method is called.
        player = Player("Mikkel")               
        deck = Deck()                           
        player.draw(deck)                      
        self.assertTrue(len(player.hand) == 2, "The player should get 2 cards in the beginning of the first round") 
        player.draw(deck)
        self.assertTrue(len(player.hand) == 3, "If the player hits once after the first round he should have 3 cards in hand")  

    def test_value(self):                       #Tests my calc_val() method in my Player class. It calculates the value sum of the hand of the player
        player = Player("Mikkel")               
        player.hand.append(Card("Hearts", "Ace", 11))   
        player.hand.append(Card("Hearts", "King", 10))
        self.assertEqual(player.calc_val(), 21, "Total should be 21") #In this scenario it tests if the appended cards give a sum of 21 which they should do
                
    def test_contain_ace(self):                 #Checks if the Player holds an ace or not. Returns true if he does, false if he doesn't
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        self.assertTrue(player.contains_ace(), "Fails if there's no ace in hand")

    def test_ace_values(self):                  #Checks if the calc_val() method correctly recalculates the sum of the Players hand if there are multiple aces in the Players hand
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        player.hand.append(Card("Diamonds", "Ace", 11))
        self.assertEqual(player.calc_val(), 12, "If the player starts with 2 aces the value should be 12 and not 22") 
        player.hand.append(Card("Spades", "Ace", 11))
        self.assertEqual(player.calc_val(), 13, "Fails if the calc.val() doesn't correctly make the value 13") 

    def test_blackjack(self):
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        player.hand.append(Card("Diamonds", "Jack", 10))
        self.assertTrue(player.blackjack(), "Should return true since the player has a blackjack")
    
    def test_check_draw(self):                  #Testing if the game ends when there's a draw
        deck = Deck()
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        player.hand.append(Card("Spades", "Jack", 10))
        dealer = Player("dealer")
        dealer.hand.append(Card("Clubs", "Ace", 11))
        dealer.hand.append(Card("Diamonds", "Jack", 10))
        bj = Blackjack(player, dealer, deck)
        bj.check_who_won()
        self.assertFalse(bj.game_running, "Game should be over since the game drawed")

    def test_check_player_win(self):                  #Testing if the game ends if the player wins
        deck = Deck()
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        player.hand.append(Card("Spades", "Jack", 10))
        dealer = Player("dealer")
        dealer.hand.append(Card("Clubs", "Ace", 11))
        dealer.hand.append(Card("Diamonds", 5, 5))
        bj = Blackjack(player, dealer, deck)
        bj.check_who_won()
        self.assertFalse(bj.game_running, "Game should be over since the player won")
    
    def test_check_dealer_win(self):                  #Testing if the game ends if the dealer wins
        deck = Deck()
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        player.hand.append(Card("Spades", 2, 2))
        dealer = Player("dealer")
        dealer.hand.append(Card("Clubs", "Ace", 11))
        dealer.hand.append(Card("Diamonds", 7, 7))
        bj = Blackjack(player, dealer, deck)
        bj.check_who_won()
        self.assertFalse(bj.game_running, "Game should be over since the dealer won")

    def test_check_keeps_going(self):                  #Testing if the game keeps running even if the dealer has more value than the player (dealer has to keep hitting till he hits atleast 17)
        deck = Deck()
        player = Player("Mikkel")
        player.hand.append(Card("Hearts", "Ace", 11))
        player.hand.append(Card("Spades", 2, 2))
        dealer = Player("dealer")
        dealer.hand.append(Card("Clubs", "Ace", 11))
        dealer.hand.append(Card("Diamonds", 4, 4))
        bj = Blackjack(player, dealer, deck)
        bj.check_who_won()
        self.assertTrue(bj.game_running, "Game should keep running since the dealer hasn't hit atleast 17 value yet")


if __name__ == "__main__":
    unittest.main()
