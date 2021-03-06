"""
  User: Liujianhan
  Time: 14:21
  clubs (♣), diamonds (♦), hearts (♥), spades (♠)
  straight flush 8 > four of a kind 7 > full house 6 > flush 5
  > straight 4 > three of a kind 3 > two pair 2 > one pair 1 > high card 0
 """
import random

__author__ = 'liujianhan'


def poker(hands):
    """
    :param hands:
    :return: return the best hand: poker([hand,...]) => hand
    """
    return max(hands, key=hand_rank)


def hand_rank(hand):
    """
    :param hand:
    :return: return a value indicating the ranking of hand.
    """
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):  # straight flush
        return 8, max(ranks)
    elif kind(4, ranks):  # 4 of a kind
        return 7, kind(4, ranks), kind(1, ranks)
    elif kind(3, ranks) and kind(2, ranks):  # full house
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):  # flush
        return 5, ranks
    elif straight(ranks):  # straight
        return 4, ranks[0]
    elif kind(3, ranks):  # 3 of a kind
        return 3, kind(2, ranks), ranks
    elif two_pair(ranks):  # two pair
        return 2, two_pair(ranks), ranks
    elif kind(2, ranks):  # 2 of a kind
        return 1, kind(2, ranks), ranks
    else:  # high card
        return 0, ranks


def card_ranks(hand):
    """
    :param hand:
    :return: return a list of the ranks, sorted with higher first
    """
    ranks = ['--23456789TJQKA'.index(r) for r, _ in hand]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks


def straight(ranks):
    """
    :param ranks:
    :return: return true if the ordered ranks form a 5-card straight
    """
    # new = [r for r in range(ranks[0], len(ranks) + 1, -1)]
    # return True if ranks == new else False
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5


def flush(hand):
    """
    :param hand:
    :return: return true if all the cards have same suit
    """
    suits = [s for _, s in hand]
    return len(set(suits)) == 1


def kind(n, ranks):
    """
    :param n:
    :param ranks:
    :return: return the first rank that this hand has exactly n of.
    """
    for i in ranks:
        if ranks.count(i) == n:
            return i
    return None


def two_pair(ranks):
    """
    :param ranks:
    :return: return the two ranks as tuple:(highest, lowest) if there are two pair or None
    """
    pair = kind(2, ranks)
    low_pair = kind(2, list(reversed(ranks)))
    if pair and low_pair != pair:
        return pair, low_pair
    else:
        return None


def deal(num_hands, n=5, deck=[r + s for r in '23456789TJQKA' for s in 'SHDC']):
    """
    :param num_hands:
    :param n:
    :param deck:
    :return: shuffle the deck and deal out numbers n-card hands.
    """
    random.shuffle(deck)
    return [deck[n * i:n * (i + 1)] for i in range(num_hands)]


def hand_percentages(n=700 * 1000):
    """
    :param n:
    :return: sample n random hands and print a table of percentages for each type of hand
    """
    hand_names = ['Straight Flush: 0.0015 %',
                  'Four of a kind: 0.024 %',
                  'Full House: 0.140 %',
                  'Flush: 0.196 %',
                  'Straight: 0.39 %',
                  'Three of a kind: 2.11 %',
                  'Two pair: 4.75 %',
                  'Pair: 42.25 %',
                  'High Card: 50.11 %']
    counts = [0] * 9
    for i in range(n // 10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    counts.reverse()
    for i in (range(9)):
        print("%25s vs %6.4f %%" % (hand_names[i], 100. * counts[i] / n))


def test():
    # five of a kind with wild cards or multiple decks
    fk_5 = '5T 5C 5H 5D 5H'.split()
    # straight flush
    sf = '6C 7C 8C 9C TC'.split()
    sf_2 = '6D 7D 8D 9D TD'.split()
    # four of a kind
    fk = '9D 9H 9S 9C 7D'.split()
    # full house
    fh = 'TD TC TH 7C 7D'.split()
    # two pair
    tp = '5S 5D 9H 9C 6S'.split()
    # A-5 straight
    s1 = 'AS 2S 3S 4S 5C'.split()
    # 2-6 straight
    s2 = '2C 3C 4C 5S 6S'.split()
    # A high
    ah = 'AS 2S 3S 4S 6C'.split()
    # 7 high
    sh = '2S 3S 4S 6C 7D'.split()
    fk_ranks = card_ranks(fk)
    tp_ranks = card_ranks(tp)
    assert poker([s1, s2, ah, sh]) == [s2]
    assert poker([fk_5]) == [9, fk_5]
    assert poker([s1, ah, sh]) == [s1]
    assert kind(4, fk_ranks) == 9
    assert kind(3, fk_ranks) is None
    assert kind(2, fk_ranks) is None
    assert kind(1, fk_ranks) == 7
    assert two_pair(fk_ranks) is None
    assert two_pair(tp_ranks) == (9, 5)
    assert straight([9, 8, 7, 6, 5]) is True
    assert straight([9, 8, 8, 6, 5]) is False
    assert flush(sf) is True
    assert flush(fk) is False
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99 * [fh]) == [sf]
    assert poker([sf, sf_2]) == [sf, sf_2]
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    return 'test pass'


if __name__ == '__main__':
    test()
    # print(deal(3))
    # print(deal(4, 7))
    # hand_percentages(7000)
