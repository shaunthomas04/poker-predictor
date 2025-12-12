from collections import Counter
from itertools import combinations
import random

class Card:
    def __init__(self, suit, rank):
        rank_map = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
                    "J":11,"Q":12,"K":13,"A":14}
        self.suit = suit
        self.rank_str = rank
        self.rank = rank_map.get(rank, 0)
        self.is_community_card = True

    def __str__(self):
        return f"{self.rank_str} of {self.suit} ({self.rank})"

class Hand:
    def __init__(self, cards=None, name="Player"):
        self.cards = cards if cards else []
        self.name = name
        self.hand_worth = None

    def determine_hand_value(self):
        def is_straight_ranks(ranks):
            ranks = sorted(set(ranks))
            if set([14,2,3,4,5]).issubset(ranks):
                return True
            for i in range(len(ranks)-4):
                if ranks[i+4]-ranks[i]==4:
                    return True
            return False

        def evaluate_five(cards):
            rank_counts = Counter(card.rank for card in cards)
            counts = sorted(rank_counts.values(), reverse=True)
            ranks = sorted(rank_counts.keys(), reverse=True)
            suits = [card.suit for card in cards]
            is_flush = len(set(suits))==1
            straight = is_straight_ranks(ranks)

            if is_flush and straight:
                if set(ranks)=={10,11,12,13,14}:
                    return ("Royal Flush",10,ranks)
                return ("Straight Flush",9,[max(ranks)])
            if len(counts) >= 1 and counts[0]==4:
                quad = [r for r,cnt in rank_counts.items() if cnt==4][0]
                kicker = [r for r in ranks if r != quad][0]
                return ("Four of a Kind",8,[quad,kicker])
            if len(counts) >= 2 and counts[0]==3 and counts[1]==2:
                triple = [r for r,cnt in rank_counts.items() if cnt==3][0]
                pair = [r for r,cnt in rank_counts.items() if cnt==2][0]
                return ("Full House",7,[triple,pair])
            if is_flush:
                return ("Flush",6,sorted(ranks,reverse=True))
            if straight:
                return ("Straight",5,[max(ranks)])
            if len(counts) >= 1 and counts[0]==3:
                triple = [r for r,cnt in rank_counts.items() if cnt==3][0]
                kickers = sorted([r for r in ranks if r != triple], reverse=True)
                return ("Three of a Kind",4,[triple]+kickers)
            if len(counts) >= 2 and counts[0]==2 and counts[1]==2:
                pairs = sorted([r for r,cnt in rank_counts.items() if cnt==2], reverse=True)
                kicker = [r for r in ranks if r not in pairs][0]
                return ("Two Pair",3,pairs+[kicker])
            if len(counts) >= 1 and counts[0]==2:
                pair = [r for r,cnt in rank_counts.items() if cnt==2][0]
                kickers = sorted([r for r in ranks if r != pair], reverse=True)
                return ("One Pair",2,[pair]+kickers)
            return ("High Card",1,sorted(ranks,reverse=True))

        if len(self.cards) <= 5:
            return evaluate_five(self.cards)

        best = ("High Card",1,[])
        for combo in combinations(self.cards,5):
            result = evaluate_five(combo)
            if result[1] > best[1] or (result[1]==best[1] and result[2] > best[2]):
                best = result
        return best

    def add_card(self,new_card):
        self.cards.append(new_card)
        self.hand_worth = self.determine_hand_value()

    def get_community_cards(self):
        community_cards = []
        for card in self.cards:
            if card.is_community_card:
                community_cards.append(card)
        return community_cards

    def __str__(self):
        hand_str = f"{self.name}'s Hand:\n"
        for card in self.cards:
            hand_str += str(card) + "\n"
        name, rank, tie = self.determine_hand_value()
        display_rank = tie[0] if tie else rank
        hand_str += f"\nBest Hand: {name} (Rank: {display_rank}, Tie-breakers: {tie})"
        # hand_str += f"\nBest Hand: {name} (Rank: {rank}, Tie-breakers: {tie})"
        return hand_str

class Deck:
    def __init__(self):
        self.unknown_cards=[]
        for rank in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]:
            for suit in ["hearts","diamonds","clubs","spades"]:
                self.unknown_cards.append(Card(suit,rank))
        self.players=[]

    def draw_card(self):
        if not self.unknown_cards:
            return None
        return self.unknown_cards.pop(random.randrange(len(self.unknown_cards)))

    def add_player(self,player_hand):
        if len(self.unknown_cards) < 2:
            return
        self.players.append(player_hand)
        card = self.draw_card()
        card.is_community_card = False
        player_hand.add_card(card)
        card = self.draw_card()
        card.is_community_card = False
        player_hand.add_card(card)

    def update_cards(self):
        for player in self.players:
            player.add_card(self.draw_card())

    def remove_card(self, card):
        for c in self.unknown_cards:
            if c.suit == card.suit and c.rank_str == card.rank_str:
                self.unknown_cards.remove(c)
                return
