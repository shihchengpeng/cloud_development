import random
import numpy as np
import card
from collections import OrderedDict
import queue
import pprint


class Deck:
    def __init__(self,player_num):
        self.player_num = player_num
        self.cards =  card.Card().make_cards()

    def split_list(self):
        return np.array_split(self.cards,self.player_num)

    def cards_shuffle(self):
        random.shuffle(self.cards)

    def make_deck(self):
        self.cards_shuffle()
        return self.split_list()

    def check_type(self):
        print(type(self.cards))
        print(self.cards)



#ババ抜きクラス
class Old_maid():
    def __init__(self,player_num):
        self.hands = Deck(player_num).make_deck()
        self.players = [i for i in range(0, player_num)]
        self.player_queue = queue.Queue()
        for num in self.players:
            self.player_queue.put(num)
        self.garbage =[]
        self.delete_cards()
        self.dic = {key: val for key, val in zip(self.players, self.hands)}
        self.winplayers=[]


    #全プレイヤーの残りカード枚数の総和
    def get_all_num(self):
        num = 0
        for val in self.dic.values():
            num = num + len(val)
        return num

    #ゲーム終了かチェック
    def end_game(self):
        print("players_len: ",len(self.winplayers))
        if self.get_all_num() == 1:
            return 1
        elif len(self.winplayers) == 3:
            return 1
        else:
             return 0
    #どこかでタプルがリストに変わってるからタプルに戻す #あとでどこか探す
    def list2turple(self):
        news=[]
        for hand in self.hands:
            new = []
            for card in hand:
                newcard = tuple(card)
                new.append(newcard)
            news.append(new)
        self.hands = news

    #どこかでタプルがリストに変わってるからタプルに戻す #あとでどこか探す
    def list2turple_2(self):
        news=[]
        for key in self.dic:
            new = []
            for card in self.dic[key]:
                newcard = tuple(card)
                new.append(newcard)
            news.append(new)
            self.dic[key] =  news

    #全手札をソート
    def sort_hands(self):
        self.list2turple()
        new_hands =[]
        for hand in self.hands:
            new_hands.append(sorted(hand, key = lambda x:x[1]))
        self.hands = new_hands

    #全手札に対して2枚組のカードを捨てる
    def delete_cards(self):
        self.sort_hands()
        flag = 0
        new_hands=[]
        for hand in self.hands:
            new_hand = hand.copy()
            garbage = []
            for i in  range(len(hand)):
                if flag:
                    new_hand.remove(hand[i])
                    garbage.append(hand[i])
                    flag = 0
                    continue
                if i !=(len(hand)-1) and hand[i][1] == hand[i+1][1]:
                    new_hand.remove(hand[i])
                    garbage.append(hand[i])
                    flag = 1
            self.garbage.append(garbage)
            new_hands.append(new_hand)
        #return new_hands
        self.hands = new_hands

    #手札に対してソート
    def sort_hand(self,player):
        return sorted(self.dic[player], key = lambda x:x[1])

    #手札に対して被りを捨てる
    def delete_hand(self,player):
        flag = 0
        self.dic[player] = self.sort_hand(player)
        new_hand = self.dic[player].copy()
        hand = self.dic[player]
        garbage = []
        for i in  range(len(hand)):
            if flag:
                new_hand.remove(hand[i])
                garbage.append(hand[i])
                flag = 0
                continue
            if i !=(len(hand)-1) and hand[i][1] == hand[i+1][1]:
                new_hand.remove(hand[i])
                garbage.append(hand[i])
                flag = 1
        self.garbage.append(garbage)
        self.dic[player] =  new_hand

    #queue version 次の人から手札取得 toplayer,fromplayerはリスト,i = int型 iは取得する手札の場所
    def new_get_card_from_player(self, toplayer,fromplayer,i):
        print("選ばれたカード" + str(self.dic[fromplayer][i]))
        self.dic[toplayer].append(self.dic[fromplayer].pop(i))
        self.delete_hand(toplayer)


    #勝った人の確認
    def check_win(self):
        for key in self.dic :
            if self.dic[key] == []:
                self.winplayers.append(key)
        self.winplayers = list(OrderedDict.fromkeys(self.winplayers))

        self.players = list(set(self.players) - set(self.winplayers))


def main():
    old_maid = Old_maid(4)
    # 中身を確認
    to_player = old_maid.player_queue.get()
    from_player = old_maid.player_queue.get()
    #while not old_maid.player_queue.empty():
    while not old_maid.end_game():
        print("")
        print("to:"+ str(to_player) + " from :"+ str(from_player))
        from_len = len(old_maid.dic[from_player])
        if from_len!= 1:
            i =  random.randint(0,from_len-1)
        else:
            i = 0
        old_maid.new_get_card_from_player(to_player,from_player,i)

        print("################  after exchange  #######################################")
        pprint.pprint(old_maid.dic)
        old_maid.check_win()

        if (old_maid.end_game()):
            print("勝者順 : " + str(old_maid.winplayers))
            print("finish")
            break

        if old_maid.dic[to_player] != []:
            old_maid.player_queue.put(to_player)

        if old_maid.dic[from_player] != []:
            to_player = from_player
            from_player = old_maid.player_queue.get()
        else:
            to_player = old_maid.player_queue.get()
            from_player = old_maid.player_queue.get()











