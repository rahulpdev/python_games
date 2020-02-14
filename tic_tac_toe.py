# Tic tac toe game to be played directly from terminal

from IPython.display import clear_output


# Print a tic-tac-toe board to the terminal
def display_board(prior_entries):
    clear_output(wait=True)
    
    empty_row = '     |     |   '
    split_row = '-'*17
    row_one = '{0:^5}|{1:^5}|{2:^5}'.format(prior_entries[1],prior_entries[2],prior_entries[3])
    row_two = '{0:^5}|{1:^5}|{2:^5}'.format(prior_entries[4],prior_entries[5],prior_entries[6])
    row_three = '{0:^5}|{1:^5}|{2:^5}'.format(prior_entries[7],prior_entries[8],prior_entries[9])
        
    board = [empty_row,row_one,empty_row,split_row,empty_row,row_two,empty_row,split_row,empty_row,row_three,empty_row]

    print('\n'.join(board))


# Permit two players to select a marker for the game 
def select_player_marker():
    print("Welcome to tic-tac-toe aka Noughts and Crosses!")

    marker = ''
    while marker != 'x' and marker != 'o':
        marker = input("Player 1, please select a marker 'X' or 'O':   ").lower()
    
    if marker == 'o':
        player_one_marker = 'O'
        player_two_marker = 'X'
    else:
        player_one_marker = 'X'
        player_two_marker = 'O'
    
    return 0, player_one_marker, player_two_marker


# Update entry on board if position is not taken and toggle player turn
def update_game_entry(current_entry, is_player_one, prior_entries, player_mark):
    if prior_entries[current_entry] == '':
        if is_player_one:
            prior_entries[current_entry] = player_mark[1]
        else:
            prior_entries[current_entry] = player_mark[2]
        is_player_one = not is_player_one
    else:
        print('This position has already been selected. Please try again!')
    
    return is_player_one, prior_entries


# Calculate when a game is won and which player is the winner
def check_game_win(prior_entries, player_mark):
    possible_wins = [[prior_entries[1],prior_entries[2],prior_entries[3]],
                     [prior_entries[4],prior_entries[5],prior_entries[6]],
                     [prior_entries[7],prior_entries[8],prior_entries[9]],
                     [prior_entries[1],prior_entries[4],prior_entries[7]],
                     [prior_entries[2],prior_entries[5],prior_entries[8]],
                     [prior_entries[3],prior_entries[6],prior_entries[9]],
                     [prior_entries[1],prior_entries[5],prior_entries[9]],
                     [prior_entries[3],prior_entries[5],prior_entries[7]]]    

    winner = None
    
    for i in range(1,3):
        if [player_mark[i] for number in range(1,4)] in possible_wins:
            winner = i
    
    return winner


def play_game(prior_entries, player_one=True, continue_game=True):
    player_markers = select_player_marker()
    
    while continue_game:
        display_board(prior_entries)
        print("\nPlayer 1 is '{}' and Player 2 is '{}'".format(player_markers[1], player_markers[2]))
        print("Enter 'end' at any time to exit the game")

        user_entry = input("Please enter a number between 1 and 9:   ")
        if user_entry in '123456789' and len(user_entry) == 1:
            current_game_status = update_game_entry(int(user_entry), player_one, prior_entries, player_markers)
            player_one = current_game_status[0]
            prior_entries = current_game_status[1]
            # Calculate when a game is won or if all possible entries are exhausted
            game_result = check_game_win(prior_entries, player_markers)
            if game_result != None or '' not in prior_entries:
                display_board(prior_entries)
                if game_result != None:
                    print("\nCongratulations Player {} you are the winner! Woo Hoo!!!".format(str(game_result)))
                else:
                    print("\nNeither player has won the game :-(")
                user_entry = input("Would you like to play again? 'Y' or 'end'   ")
                prior_entries = ['*','','','','','','','','','']
        # Terminate game
        if user_entry.lower() == 'end':
            continue_game = False
            print("\nThanks for playing with us today. We're sorry to see you go.\nCome back again soon!")


if __name__ == "__main__":
    new = ['*','','','','','','','','','']
    play_game(new)