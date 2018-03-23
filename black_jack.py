# -*- coding: utf-8 -*-
import random


class Player(object):

    def __init__(self):
        self.cards = []
        self.a_11 = 0
        self.a_1 = 0
        self.other = 0

    @property
    def points(self):
        # 真正分數
        return self.a_11 * 11 + self.a_1 * 1 + self.other

    @property
    def min_points(self):
        # A 都換成 1 不代表真正分數，只是決定是否 < 17 再拿牌
        return (self.a_11 + self.a_1) * 1 + self.other

    def add_card(self, card):
        self.cards += [card]
        if card == "A":
            self.a_11 += 1
        elif card in ["J", "Q", "K"]:
            self.other += {
                "J": 11,
                "Q": 12,
                "K": 13
            }[card]
        else:
            self.other += int(card)
        self._balance()

    def _balance(self):
        if self.points > 21 and self.a_11 != 0:
            # 你只需改變數量，呼叫 points 時會去計算現在的分數，遞迴直到 分數低於 21 或是 全部的 Ａ 都換成 1
            self.a_11 -= 1
            self.a_1 += 1
            # 遞迴
            self._balance()


# 可以手動設定發牌內容的發牌機
class CardGenerator(object):

    def __init__(self, my_card_list):
        self.cards = my_card_list
        self.card_count = 52

    def get_card(self):
        return self.cards.pop(0)


# 隨機發牌機
class RandomCardGenerator(object):

    def __init__(self):
        self.cards = list("A23456789JQK" * 4) + ["10", "10", "10", "10"]  # '10' 有兩個字元不能用前面方法轉陣列
        self.card_count = 52

    def get_card(self):
        random_index = random.randint(1, len(self.cards))
        return self.cards.pop(random_index - 1)  # index 從 0 開始


def play(players, card_generator):
    # 我們會同時發給所有人到兩張，檢查第一人即可
    if len(players[0].cards) <= 2:
        for player in players:
            player.add_card(card_generator.get_card())
    else:
        if all([player.min_points > 17 for player in players]):
            # 遊戲結束條件，所有玩家都大於 17 不用再發牌，也可以設計成某一位穩贏就結束(寫出來會很醜)
            return
        else:
            for player in players:
                if player.min_points <= 17:
                    player.add_card(card_generator.get_card())
    # 繼續下一輪 遞迴
    return play(players, card_generator)


if __name__ == '__main__':
    # Test game
    test_card_lists = [
        ["A", "A", "A", "A", "K", "2"],

        ["A", "5", "A", "J"],
        ["5", "A", "A", "J"],
        ["A", "A", "5", "J"],

        ["A", "A", "K", "2", "6"],
        ["K", "A", "A", "2", "6"],
        ["A", "K", "A", "2", "6"],

    ]
    for card_list in test_card_lists:
        print "發牌順序 {}".format(card_list)
        p1 = Player()
        card_generator = CardGenerator(card_list)
        play([p1], card_generator)
        print "Player 1 拿著牌 {}， 點數是 {}".format(p1.cards, p1.points)
        print "-" * 60

    print "=" * 60

    # Real game, you can add player
    p1 = Player()
    p2 = Player()
    players = [p1, p2]
    card_generator = RandomCardGenerator()
    play(players, card_generator)
    for i, player in enumerate(players):
        print "Player {} 拿著牌 {}， 點數是 {}".format(i, player.cards, player.points)
