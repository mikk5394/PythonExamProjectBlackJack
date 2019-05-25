from blackjack import Deck, Player, Blackjack

deck = Deck()
deck.shuffle()
player = Player("Mikkel")
dealer = Player("dealer")
bj = Blackjack(player, dealer, deck)


while bj.game_running == True:
    bj.run_game()
    if bj.player.cash == 0:
        print("Your balance is 0 and you will have to rebuy to play again.")
    if input("Play again? Press any key to play or press q to quit! ") == "q":
        quit()
    else:
        bj.game_running = True
        player.hand = []
        dealer.hand = []