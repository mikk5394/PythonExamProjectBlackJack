from blackjack import Deck, Player, Blackjack

#The classes are instantiated
deck = Deck()
deck.shuffle()
player = Player("Mikkel")
dealer = Player("dealer")
bj = Blackjack(player, dealer, deck)


while bj.game_running == True:                                          #A loop that keeps the game running untill the player decides he wants to quit
    bj.run_game()                                                       #The game is started
    if bj.player.cash == 0:
        print("Your balance is 0 and you will have to rebuy to play again.")
    if input("Play again? Press any key to play or press q to quit! ") == "q":   #If the player presses "q" the game stops - if not the game starts again  
        quit()
    else:                                                               #The else block resets the game
        bj.game_running = True                                          
        player.hand = []
        dealer.hand = []