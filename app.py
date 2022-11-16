import random  # used for shuffling deck
import time  # used for making the gameplay loop seem a little more realistic


class Shoe:  # FINISHED I THINK!?!!
    # lists to use to create a deck, capitalized since they are constants
    SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    VALS = ['Ace', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', 'Jack', 'Queen', 'King']

    # initialize new deck to empty, but allow number of decks in shoe to be changed
    def __init__(self, decks):
        self.cards = []
        self.decks = decks

    # enables checking of remaining cards in shoe so we can reshuffle under a threshold (like real blackjack)
    def __len__(self):
        return len(self.cards)

    # empty current deck
    def new_shoe(self):
        self.cards = []

    # generate instances of card class for each suit,value pair 8 times (like real blackjack shoe)
    # this triply nested loop is a little gross but I can't think of a better way
    def generate_shoe(self):
        # underscore used to denote unused variable, I just need to loop over the number of decks
        for _ in range(self.decks):
            for suit in self.SUITS:
                for val in self.VALS:
                    self.cards.append(Card(val, suit))

    # I was looking for a module that would randomize a list and found that random had a shuffle method! Perfect use case
    # this allows me to pop the end of the shoe so I don't have to do something like generate a randint using max value of length of shoe
    def shuffle_shoe(self):
        print('\nShuffling decks...\n')
        random.shuffle(self.cards)
        time.sleep(4)
        print('Decks shuffled! Play on!\n')
        time.sleep(1)

    # shoe will be regenerated if not enough cards remain to make the game more consistent
    @property
    def reshuffle_threshold(self):
        return self.decks - (self.decks // 2)


class Card:  # FINISHED I THINK!?!?!??!?!?!?!
    # each instance of a card has a value and a suit
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit

    # thought using this magic method to print out the card details would be a good way to do it? might be overkill
    def __str__(self):
        return f"{self.val} of {self.suit}"

    @property
    def card_val(self):
        # allows use of face cards instead of just values
        if self.val in ['Jack', 'Queen', 'King']:
            return 10
        # I don't know how to make aces value of 1 if the player is going to bust
        # decided to subtract 10 for each ace from hand_score if hand_score is over 12
        # this subtraction is done when the hand_score is evaluated
        if self.val == 'Ace':
            return 1
        # all other cards just regular value
        else:
            return int(self.val)


class Player:  # idk what im doing
    # what methods and attributes have to be the same between players?
    # all players start with empty hand
    # need to know number of aces in each hand
    # need to know value of each hand
    # need to know if hand is busted
    # need to be able to reveal hand
    # need to be able to reset hand

    # defaults to empty hand
    def __init__(self):
        self.hand = []

    # clears hand (called on new round)
    def new_hand(self):
        self.hand = []

    @property
    def hand_value(self):
        # sum is so much better than JavaScripts reduce for getting the sum of a list/array
        hand_val = sum([card.card_val for card in self.hand])
        # if hand_val is over 12 and isn't 21, aces need to drop to their other value of 1
        # done by subtracting 10 for each ace
        num_aces = 0
        for card in self.hand:
            if card.val == "Ace":
                num_aces += 1
        if hand_val == 21:
            return hand_val
        elif hand_val < 12:
            for _ in range(num_aces):
                hand_val += 10
        return hand_val

    @property
    def busted(self):
        # if hand value over 21 need to return True so we can cause player to lose
        if self.hand_value > 21:
            return True


class Dealer(Player):  # i still dont know whats happening
    def __init__(self):
        super().__init__()

    # hide_first_card allows me to hide the dealers first card when the player is still hitting (like real blackjack)
    def show_hand(self, hide_first_card=True):
        if hide_first_card:
            print('\n***')
            print(self.hand[1])
            print(
                f"\nDealer's current hand is worth: {self.hand[1].card_val}...?\n")
        else:
            for card in self.hand:
                print(card)
            print(f"Dealer's current hand is worth: {self.hand_value}\n")


class Human(Player):  # same situation as dealer class
    def __init__(self, chip_count, bet_amt=0, turn=True):
        super().__init__()
        self.chip_count = chip_count
        self.bet_amt = bet_amt
        self.turn = turn

    def show_hand(self):
        for card in self.hand:
            print(card)
        print(f"\nYour current hand is worth: {self.hand_value}\n")

    def new_bet(self):
        user_bet = input(
            f'You have {self.chip_count} chips.\nHow much would you like to wager on this hand?\n')
        try:
            user_bet = int(user_bet)
            if user_bet > self.chip_count:
                print("You can't bet more chips than you have.")
                self.new_bet()
            else:
                self.chip_count -= user_bet
                self.bet_amt = user_bet
        except:
            print('Try betting a number.')
            self.new_bet()

    # add getter and setter for bet/chip count


class Game:  # making the gameplay loop has me completely lost
    # holds all logic that drives the game

    # need list of all players to loop through
    # need info about current deck
    # need to know what the human bet
    # need to know whose turn it is

    # passing here seems weird, not sure what needs to be stored in each game instance
    def __init__(self):
        pass

    # need to deal 2 cards to all players at first from a new deck
    def new_deal(self, shoe, players):
        if len(shoe) < shoe.reshuffle_threshold:
            shoe.new_shoe()
            shoe.generate_shoe()
            shoe.shuffle_shoe()
        for _ in range(2):
            time.sleep(1)
            for player in players:
                player.hand.append(shoe.cards.pop())

    def end_game(self, player):
        if isinstance(player, Human):
            player.chip_count += 2 * player.bet_amt
            print(
                f"Player wins!\n{player.bet_amt * 2} chips have been added to your pile.\nYou now have {player.chip_count} chips.")
            player.bet_amt = 0

        if isinstance(player, Dealer):
            print('You lose!\nThe house always wins!')

    def draw_game(self, player):
        if isinstance(player, Human):
            print(
                f"Draw! You didn't win, but you also didn't lose!\nHere are your {player.bet_amt} chips back.")
            player.chip_count += player.bet_amt

    # player must be able to choose to hit or stand (how to add split and double down?)
    def hit_or_stand(self, shoe, player):
        choices = ['h', 'hit', 's', 'stand']
        user_choice = input("(H)it | (S)tand?\n").lower()
        if user_choice not in choices:
            print('Invalid choice.')
            self.hit_or_stand(shoe, player)
        elif user_choice == 'h' or user_choice == 'hit':
            self.hit(shoe, player)
        elif user_choice == 's' or user_choice == 'stand':
            print(
                f'Player chose to stand with {player.hand_value}')
            player.turn = False

    # players need to be able to hit (add card to players hand)
    def hit(self, shoe, player):
        self.check_busted(player)
        if isinstance(player, Dealer):
            time.sleep(1)
            player.hand.append(shoe.cards.pop())
            player.show_hand(False)
        if isinstance(player, Human):
            time.sleep(1)
            player.hand.append(shoe.cards.pop())
            player.show_hand()

    # need to check if players win/draw/busted after each hit

    def check_busted(self, player):
        if player.busted:
            if isinstance(player, Dealer):
                self.end_game(player)
            if isinstance(player, Human):
                self.end_game(player)
                player.turn = False

    # need to be able to check human hand_value vs dealer hand_value

    def compare_hand_values(self, human, dealer):
        if human.hand_value > dealer.hand_value:
            self.end_game(human)
        if human.hand_value < dealer.hand_value:
            self.end_game(dealer)
        if human.hand_value == dealer.hand_value:
            self.draw_game(human)

    # need to call new_hand for dealer and human
    def new_hands(self, players):
        for player in players:
            player.new_hand()

    # need to ask human to play again
    def choose_play_again(self):
        choices = ['y', 'yes', 'n', 'no']
        while True:
            user_choice = input(
                '\nDo you want to play again? (Y)es | (N)o\n').lower()
            if user_choice not in choices:
                print('Invalid option.')
            elif user_choice == 'y' or user_choice == 'yes':
                return True
            elif user_choice == 'n' or user_choice == 'no':
                print('\n\nThanks for playing!\n')
                return False

    def new_game(self):
        # need to establish new_game loop logic
        # new game setup
        human = Human(250)
        dealer = Dealer()
        curr_shoe = Shoe(8)
        curr_shoe.generate_shoe()
        curr_shoe.shuffle_shoe()

        playing = True
        while playing:

            if human.chip_count == 0:
                print("\n\nLooks like you're out of chips! Come back another time!\n")
                break

            human.new_bet()

            self.new_deal(curr_shoe, [human, dealer])
            dealer.show_hand()
            human.show_hand()

            while human.turn:
                self.hit_or_stand(curr_shoe, human)

            if not human.busted:
                dealer.show_hand(False)

                while not human.turn:
                    if dealer.hand_value < 17:
                        print('Dealer hits...')
                        time.sleep(1)
                        self.hit(curr_shoe, dealer)
                        time.sleep(1)
                    if dealer.hand_value >= 17 and not dealer.busted:
                        print("Dealer stands.\n")
                        break
                    if dealer.busted:
                        self.end_game(human)
                        break
                if not dealer.busted:
                    self.compare_hand_values(human, dealer)

            if not self.choose_play_again():
                playing = False

            human.turn = True
            self.new_hands([human, dealer])


def main():
    new_game = Game()
    new_game.new_game()


main()
