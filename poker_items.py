from collections import Counter
from itertools import combinations
import random


RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["hearts", "diamonds", "clubs", "spades"]
RANK_VALUES = {rank: value for value, rank in enumerate(RANKS, start=2)}


class Card:
    def __init__(self, suit, rank):
        if suit not in SUITS:
            raise ValueError(f"Unknown suit: {suit}")
        if rank not in RANK_VALUES:
            raise ValueError(f"Unknown rank: {rank}")

        self.suit = suit
        self.rank_str = rank
        self.rank = RANK_VALUES[rank]
        self.is_community_card = True

    def __str__(self):
        return f"{self.rank_str} of {self.suit} ({self.rank})"


class Hand:
    def __init__(self, cards=None, name="Player"):
        self.cards = list(cards) if cards else []
        self.name = name
        self.hand_worth = None

    @staticmethod
    def _straight_high(ranks):
        unique_ranks = set(ranks)
        if {14, 2, 3, 4, 5}.issubset(unique_ranks):
            return 5

        consecutive = sorted(unique_ranks)
        for index in range(len(consecutive) - 4):
            window = consecutive[index:index + 5]
            if window[-1] - window[0] == 4:
                return window[-1]
        return None

    @classmethod
    def _evaluate_five(cls, cards):
        rank_counts = Counter(card.rank for card in cards)
        counts = sorted(rank_counts.values(), reverse=True)
        ranks = sorted(rank_counts, reverse=True)
        is_flush = len({card.suit for card in cards}) == 1
        straight_high = cls._straight_high(ranks)

        if is_flush and straight_high:
            if straight_high == 14 and set(ranks) == {10, 11, 12, 13, 14}:
                return ("Royal Flush", 10, [14])
            return ("Straight Flush", 9, [straight_high])

        if counts and counts[0] == 4:
            quad = max(rank for rank, count in rank_counts.items() if count == 4)
            kicker = max(rank for rank in ranks if rank != quad)
            return ("Four of a Kind", 8, [quad, kicker])

        triples = sorted((rank for rank, count in rank_counts.items() if count == 3), reverse=True)
        pairs = sorted((rank for rank, count in rank_counts.items() if count == 2), reverse=True)
        if triples and (pairs or len(triples) > 1):
            pair = pairs[0] if pairs else triples[1]
            return ("Full House", 7, [triples[0], pair])

        if is_flush:
            return ("Flush", 6, ranks)
        if straight_high:
            return ("Straight", 5, [straight_high])

        if triples:
            triple = triples[0]
            kickers = sorted((rank for rank in ranks if rank != triple), reverse=True)
            return ("Three of a Kind", 4, [triple] + kickers)

        if len(pairs) >= 2:
            kicker = max(rank for rank in ranks if rank not in pairs)
            return ("Two Pair", 3, pairs[:2] + [kicker])

        if pairs:
            pair = pairs[0]
            kickers = sorted((rank for rank in ranks if rank != pair), reverse=True)
            return ("One Pair", 2, [pair] + kickers)

        return ("High Card", 1, ranks)

    def determine_hand_value(self):
        if not self.cards:
            return ("High Card", 1, [])

        if len(self.cards) <= 5:
            return self._evaluate_five(self.cards)

        best = ("High Card", 1, [])
        for combo in combinations(self.cards, 5):
            result = self._evaluate_five(combo)
            if (result[1], result[2]) > (best[1], best[2]):
                best = result
        return best

    def add_card(self, new_card):
        if new_card is None:
            raise ValueError("Cannot add an empty card")
        self.cards.append(new_card)
        self.hand_worth = self.determine_hand_value()

    def get_community_cards(self):
        return [card for card in self.cards if card.is_community_card]

    def get_private_cards(self):
        return [card for card in self.cards if not card.is_community_card]

    def __str__(self):
        hand_str = f"{self.name}'s Hand:\n"
        hand_str += "\n".join(str(card) for card in self.cards)
        name, rank, tie = self.determine_hand_value()
        hand_str += f"\n\nBest Hand: {name} (Rank: {rank}, Tie-breakers: {tie})"
        return hand_str


class Deck:
    def __init__(self):
        self.unknown_cards = [Card(suit, rank) for rank in RANKS for suit in SUITS]
        self.players = []

    def draw_card(self):
        if not self.unknown_cards:
            return None
        return self.unknown_cards.pop(random.randrange(len(self.unknown_cards)))

    def add_player(self, player_hand):
        if len(self.unknown_cards) < 2:
            raise ValueError("Not enough cards to deal a player")
        self.players.append(player_hand)
        for _ in range(2):
            card = self.draw_card()
            card.is_community_card = False
            player_hand.add_card(card)

    def update_cards(self):
        for player in self.players:
            player.add_card(self.draw_card())

    def remove_card(self, card):
        for index, unknown_card in enumerate(self.unknown_cards):
            if (unknown_card.suit, unknown_card.rank_str) == (card.suit, card.rank_str):
                self.unknown_cards.pop(index)
                return True
        return False
