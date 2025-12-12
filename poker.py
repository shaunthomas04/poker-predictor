from poker_items import Deck, Hand
from calculations import monte_carlo

deck = Deck()

# Create 3 players and give them cards
my_hand = Hand(name="Shaun")
player2 = Hand(name="Bob")
player3 = Hand(name="Charlie")
deck.add_player(my_hand)
print(my_hand)
deck.add_player(player2)
deck.add_player(player3)
opponent_count = len(deck.players) - 1


# #print all hands
# def print_hands(round_name):
#     print(f"\n=== {round_name} ===")
#     for player in deck.players:
#         print(f"{player.name}'s Hand:")
#         for card in player.cards:
#             print(f"  {card.rank_str} of {card.suit} ({card.rank})")
#         name, rank, tie = player.determine_hand_value()
#         print(f"Best Hand: {name} (Rank {rank}, Tie-breakers: {tie})\n")

# # Deal 5 community cards one by one
for i in range(5):
    new_card = deck.draw_card()
    for player in deck.players:
        player.add_card(new_card)
        print(player)

    # give out the probability at each stagen
    win_probability, percentile = monte_carlo(my_hand, opponent_count, 1000)
    print(f"Wind Probability: {win_probability}, Percentile: {percentile}")
    # print_hands(f"Community Card {i+1}")



