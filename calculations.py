import random

from poker_items import Deck, Hand


def monte_carlo(current_hand, opponent_count, trial_count):
    if opponent_count < 0:
        raise ValueError("opponent_count cannot be negative")
    if trial_count <= 0:
        raise ValueError("trial_count must be greater than zero")

    stage_wins = [0, 0, 0, 0]
    stage_percentiles = [0.0, 0.0, 0.0, 0.0]
    stages = [0, 3, 4, 5]

    known_community = current_hand.get_community_cards()
    private_cards = current_hand.get_private_cards()
    if len(known_community) > 5:
        raise ValueError("A hand cannot contain more than five community cards")

    for _ in range(trial_count):
        deck = Deck()
        for card in current_hand.cards:
            deck.remove_card(card)

        players = []
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
        for index in range(opponent_count):
            opponent = Hand(name=f"{random.choice(names)} {index + 1}")
            deck.add_player(opponent)
            players.append(opponent)

        full_community = list(known_community)
        while len(full_community) < 5:
            card = deck.draw_card()
            if card is None:
                raise RuntimeError("The deck ran out of cards during simulation")
            full_community.append(card)

        for stage_index, community_count in enumerate(stages):
            stage_community = full_community[:community_count]
            user_score = Hand(cards=private_cards + stage_community).determine_hand_value()
            opponent_scores = [
                Hand(cards=opponent.cards + stage_community).determine_hand_value()
                for opponent in players
            ]

            better_count = sum(
                (score[1], score[2]) > (user_score[1], user_score[2])
                for score in opponent_scores
            )
            if better_count == 0:
                stage_wins[stage_index] += 1

            total_players = opponent_count + 1
            stage_percentiles[stage_index] += (total_players - better_count) / total_players

    win_probabilities = [wins / trial_count for wins in stage_wins]
    avg_percentiles = [total / trial_count for total in stage_percentiles]

    stage_names = ["Preflop", "Flop", "Turn", "River"]
    for name, win_probability, percentile in zip(stage_names, win_probabilities, avg_percentiles):
        print(f"{name} - Win Probability: {win_probability:.3f}, Percentile: {percentile:.3f}")

    print(f"\nFinal Win Probability: {win_probabilities[-1]:.3f}")
    print(f"Final Percentile: {avg_percentiles[-1]:.3f}")
    return win_probabilities, avg_percentiles
