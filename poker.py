from calculations import monte_carlo
from poker_items import Deck, Hand


def main():
    deck = Deck()
    my_hand = Hand(name="Shaun")
    players = [my_hand, Hand(name="Bob"), Hand(name="Charlie")]

    for player in players:
        deck.add_player(player)

    opponent_count = len(players) - 1
    for _ in range(5):
        community_card = deck.draw_card()
        if community_card is None:
            raise RuntimeError("The deck ran out of cards")
        for player in players:
            player.add_card(community_card)

        win_probability, percentile = monte_carlo(my_hand, opponent_count, 1000)
        print(f"Win Probability: {win_probability[-1]:.3f}, Percentile: {percentile[-1]:.3f}")


if __name__ == "__main__":
    main()
