import deck, player
import  random
if __name__ == '__main__':
    old_maid = deck.Old_maid(4)
    #print("各プレイヤーの手札")
    #print(*old_maid.hands, sep='\n')
    while(not len(old_maid.players)== 1):
        print("                     ")
        print("new round")
        print("                     ")
        for now_pl in old_maid.players:
            #print("debug")
            print("                     ")
            print("                     ")
            print("total_player" + str(old_maid.players))
            print("now_pl :"+ str(now_pl))
            #print(*old_maid.hands, sep='\n')
            if now_pl == old_maid.players[-1]:
                print("to last from first")
                len_next = len(old_maid.hands[old_maid.players[0]])
                if len_next ==1:
                    old_maid.get_card_from_player(now_pl,old_maid.players[0],0)
                else:
                    print(len_next)
                    old_maid.get_card_from_player(now_pl,old_maid.players[0],random.randint(0,len_next-1))
            else:
                print(old_maid.players[now_pl+1])
                if len(old_maid.hands[old_maid.players[now_pl+1]]) == 1:
                    old_maid.get_card_from_player(now_pl,now_pl+1,0)
                else:
                    old_maid.get_card_from_player(now_pl,now_pl+1,len(old_maid.hands[old_maid.players[now_pl+1]])-1)


            print(*old_maid.hands, sep='\n')
            #print("##########################################################################################")
            old_maid.check_win()
            if (old_maid.end_game()):
                print(old_maid.winplayers)
                print("finish")
                break

            