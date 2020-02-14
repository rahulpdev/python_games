# Multi player black jack game to be played directly from terminal

from IPython.display import clear_output
import random


# Create Card object
class Card():
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank.capitalize()} of {self.suit.capitalize()}"

    def value(self, deck):
        return deck.rank_scores[self.rank]


# Create Deck object
class Deck():
    
    def __init__(
        self, ranks=('2','3','4','5','6','7','8','9','jack','queen','king','ace'), 
        suits=('hearts','diamonds','clubs','spades'), 
        rank_scores={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'jack':10,'queen':10,'king':10,'ace':11}
    ):
        self.ranks = ranks
        self.suits = suits
        self.rank_scores = rank_scores
        self.cards = [Card(rank,suit) for suit in self.suits for rank in self.ranks]
        
    def __str__(self):
        return str(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal_card(self):
        return self.cards.pop()


# Create Hand object
class Hand():
    
    def __init__(self):
        self.cards = []
        self.score = 0
        
    # Add card to hand
    def add_card(self, card):
        self.cards.append(card)

    # Calculate hand score
    def calc_score(self, deck):
        self.score = sum([card.value(deck) for card in self.cards])
        for card in self.cards:
            if self.score > 21 and card.rank == deck.ranks[-1]:
                self.score -= 10


# Create Player object
class Player():
    
    def __init__(self, wallet=0, name='dealer'):
        self.name = name
        self.wallet = wallet
        self.bet = 0
        self.hand = []

    def __str__(self):
        return self.name.capitalize()


# Running total of bankroll over multiple games
    def bankroll(self, game_winnings):
        self.game_winnings = game_winnings
        self.wallet += self.game_winnings


# Create list of Players with names and bankrolls
def create_player_list():

    print("Welcome to the BlackJack table!")
    
# Enter number of Players on table
    while True:
        try:
            player_num = int(input("How many players are joining the table?:" + "\n"))
        except ValueError:
            continue
        else:
            break

# Create Players with name and bankroll
    players = []
    
    for number in range(player_num):
        player_name = input(f"Player {number+1}, what is your name?:" + "\n")
        while True:
            try:
                player_wallet = int(input(f"{player_name} what is your bankroll?:" + "\n"))
            except ValueError:
                print("Sorry I do not understand. Please try again.")
            else:
                player = Player(player_wallet, player_name)
                players.append(player)
                break
        
    return players


# Update table of Players to remove Players with zero bankroll
def check_bankroll(players):

    print(
        '\n'.join(
            [f"Sorry {player.name}, you have zero bankroll and must leave the table :-(" for player in players if player.wallet == 0]
        )
    )
    
    return [player for player in players if player.wallet > 0]


# Ask each Player on table for a game bet
def place_game_bets(players):
    
    print("Let's start a new game, place your bets!")
    
    for player in players:
        while True:
            try:
                game_bet = int(input(f"{player.name.capitalize()} how much do you want to bet?" + "\n"))
            except ValueError:
                print("Sorry I did not understand. Please try again.")
            else:
# Ensure Player's bet does not exceed their bankroll
                if game_bet > player.wallet:
                    print("Sorry you do not have enough chips to make that bet.")
                else:
                    player.bet = game_bet
                    break


# Deal two cards to each Player on table and two cards to the Dealer. Show only the first Dealer card.
def deal_hands(deck, players):
    
    print("\n" + "Let's deal a new hand!")
    
# Deal two cards to each Player
    for player in players:
        player.hand = Hand()
        
        for num in range(0,2):
            player.hand.add_card(deck.deal_card())
            print(f"{player} has {player.hand.cards[-1]}")
        
        player.hand.calc_score(deck)
    
    print("Do you want to Hit another card or Stand and play the Dealer's hand?" + "\n")

# Deal two cards to Dealer, only show the first card.
    dealer.hand = Hand()
    dealer.hand.add_card(deck.deal_card())
    print(f"{dealer} has {dealer.hand.cards[-1]}" + "\n")
    dealer.hand.add_card(deck.deal_card())
    dealer.hand.calc_score(deck)


# Ask the Player if they want to Hit or Stand.
# If the Player Hit's add a card to their hand. Bust the player if hand > 21 and lose their bet, else ask if they want to Hit or Stand again.
def play_hand(deck, player):
    
    while True:
        player_turn = input(f"{player} enter 'H' or 'S':  ").lower()
        
        if player_turn == 'h':
            player.hand.add_card(deck.deal_card())
            print(f"{player} has {player.hand.cards[-1]}")
            player.hand.calc_score(deck)
            if player.hand.score > 21:
                print("\n" + f"{player} Busts :-(")
                player.bankroll(-player.bet)
                break
        elif player_turn == 's':
            print("\n" + f"{player} is Standing :-|" + "\n")
            break
        else:
            continue


# Call play_hand function for each Player on table and remove all busted Players from the table for rest of game
def play_table(deck, players):

    for player in players:
        play_hand(deck, player)

    return [player for player in players if player.hand.score <= 21]


# Dealer must Hit while score < 17 and must Stand while score >= 17
def play_dealer(deck, players):
    
    print("It's the Dealer's turn to play!")
    print(f"{dealer} has {dealer.hand.cards[-1]}")

    while dealer.score < 17:
        dealer.hand.add_card(deck.deal_card())
        print(f"{dealer} has {dealer.hand.cards[-1]}")
        dealer.hand.calc_score(deck)
        

# Calculate game outcome and allocate bet wins and losses to standing Players on table
def standing_table_result(players):

    max_player_score = max([player.hand.score for player in players])
    
    if dealer.hand.score > 21:
        print("\n" + "Dealer Busts :-)" + "\n")
        
        for player in players:
            if player.hand.score == 21:
                player.bankroll(1.5*player.bet)
            else:
                player.bankroll(player.bet)
                
    else:
        print("")
        
        for player in players:
            if player.hand.score > dealer.hand.score:
                print(f"{player} Wins :-)")
                if player.hand.score == 21:
                    player.bankroll(1.5*player.bet)
                else:
                    player.bankroll(player.bet)
            elif player.hand.score == dealer.hand.score:
                print(f"{player} Ties :-) ~ :-(")
            else:
                print(f"{player} Loses :-(")
                player.bankroll(-player.bet)


# Inform all Players on table of their updated bankroll and ask if they want to play again.
def play_again(play, players):
    
    print("")
    
    for player in players:
        print(f"{player} your bankroll is {player.wallet}")
    
    while True:
        play_choice = input("\n" + "Enter 'Y' to play again or 'N' to end:  ").lower()
        if play_choice == 'n':
            return not play
        elif play_choice == 'y':
            return play
        

if __name__ == "__main__":
    play_next = True

    dealer = Player()

    player_list = create_player_list()

    while play_next:
        clear_output()
        game_deck = Deck()
        game_deck.shuffle()
        player_table = check_bankroll(player_list)
        if len(player_table) > 0:
            place_game_bets(player_table)
            deal_hands(game_deck, player_table)
            standing_players = play_table(game_deck, player_table)
            if len(standing_players) > 0:
                play_dealer(game_deck, standing_players)
                standing_table_result(standing_players)
            else:
                print("\n" + "Dealer Wins :-(" + "\n") 
            play_next = play_again(play_next, player_table)
        else:
            play_next = False
            
    print('Game Over')
