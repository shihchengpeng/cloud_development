import random
import numpy as np
import card


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
        self.winplayers=[]
        self.garbage =[]
        self.sort_hands()
        self.delete_cards()

    def check_member(self):
        print(self.hands)
        print(self.garbage)
    """
    #各playerのカード枚数を確認する
    def check_hand(self):
        nums_list = []
        for hand in self.hands:
            num_list = []
            for i in hand:
                num_list.append(i[1])
            nums_list.append(num_list)

        return nums_list
    """
    #全プレイヤーの残りカード枚数の総和
    def get_all_num(self):
        num = 0
        for hand in self.hands:
            num = num + len(hand)
        return num

    #ゲーム終了かチェック
    def end_game(self):
        if self.get_all_num() == 1:
            return 1
        else:
             return 0

    #全手札をソート
    def sort_hands(self):
        self.list2turple()
        new_hands =[]
        for hand in self.hands:
            new_hands.append(sorted(hand, key = lambda x:x[1]))
        self.hands = new_hands

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

    #全手札に対して2枚組のカードを捨てる
    def delete_cards(self):
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

    #次の人から手札取得 toplayer,fromplayer,i = int型 iは取得する手札の場所
    def get_card_from_player(self, toplayer,fromplayer,i):
        print("選ばれたカード(deck.py get_card_from)" + str(self.hands[fromplayer][i]))
        #print(self.hands[fromplayer])
        self.hands[toplayer].append(self.hands[fromplayer].pop(i))
        self.sort_hands()
        self.delete_cards()

    #勝った人の確認
    def check_win(self):
        for i in range(len(self.hands)):
            if self.hands[i] == []:
                self.winplayers.append(i)
        
        #self.players = list(set(self.players) - set(self.winplayers))
        #print(self.players)
    
