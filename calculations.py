import random
from poker_items import Hand, Deck

def monte_carlo(current_hand, opponent_count, trial_count):
    # win counts and sum of percentiles for each stage
    stage_wins = [0, 0, 0, 0]
    stage_percentiles = [0, 0, 0, 0]

    stages = [0, 3, 4, 5]  # preflop, flop, turn, river

    for sim in range(trial_count):
        deck = Deck()
        # remove known cards from deck
        for card in current_hand.cards:
            deck.remove_card(card)

        community_cards = current_hand.get_community_cards()
        for card in community_cards:
            deck.remove_card(card)

        # create opponents
        players = []
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
        for _ in range(opponent_count):
            opp = Hand(name=random.choice(names))
            deck.add_player(opp)
            players.append(opp)

        # fill remaining community cards for this trial
        full_community = community_cards.copy()
        while len(full_community) < 5:
            full_community.append(deck.draw_card())

        # evaluate hands at each stage
        for stage_index, num_community in enumerate(stages):
            stage_community = full_community[:num_community]

            temp_user_hand = Hand(cards=current_hand.cards + stage_community)
            user_score = temp_user_hand.determine_hand_value()

            temp_opp_scores = []
            for opp in players:
                temp_opp_hand = Hand(cards=opp.cards + stage_community)
                temp_opp_scores.append(temp_opp_hand.determine_hand_value())

            # check if user has best hand
            win = True
            better_count = 0
            for opp_score in temp_opp_scores:
                if opp_score[1] > user_score[1] or (
                    opp_score[1] == user_score[1] and opp_score[2] > user_score[2]
                ):
                    win = False
                    better_count += 1

            if win:
                stage_wins[stage_index] += 1

            # approximate percentile
            percentile = (opponent_count - better_count) / opponent_count
            stage_percentiles[stage_index] += percentile

    # convert counts to probabilities and average percentiles
    win_probabilities = [count / trial_count for count in stage_wins]
    avg_percentiles = [total / trial_count for total in stage_percentiles]

    # print stage-by-stage results
    stage_names = ["Preflop", "Flop", "Turn", "River"]
    for i in range(4):
        print(f"{stage_names[i]} - Win Probability: {win_probabilities[i]:.3f}, "
              f"Percentile: {avg_percentiles[i]:.3f}")

    # print final results
    final_win = win_probabilities[-1]
    final_percentile = avg_percentiles[-1]
    print(f"\nFinal Win Probability: {final_win:.3f}")
    print(f"Final Percentile: {final_percentile:.3f}")

    return win_probabilities, avg_percentiles
