class Card:
    def __init__(self):
        self.value = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.suits = ["spades", "hearts", "diamonds","clubs"]
        self.Joker = ("Joker",0)
        self.ref = {
                "Ace" :1,
                "Jack" :11,
                "Queen":12,
                "king": 13
            }

    def get_suit(self):
        return self.suits

    def get_value(self):
        return self.value

    def make_cards(self):
        cards = []
        for suit in self.suits:
            for i in self.value:
                cards.append((suit,i))
        
        cards.append(self.Joker)
        return cards 


#card = Card()
#print(len(card.make_cards()))