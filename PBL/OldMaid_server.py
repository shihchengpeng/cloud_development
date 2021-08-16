from ast import Str
import bottle, jinja2
from bottle import *
from bottle import jinja2_template as template
from mongoengine import connect, Document, ListField, StringField, URLField, IntField, queryset
import random
import json
import deck_queue
import pprint

TEMPLATE_PATH.append('./view')

class Users(Document):
    username = StringField(required=True, max_length=30)
    password = StringField(required=True, max_length=30)
    cookie = StringField()
    usernumber = IntField() #0-3までの数字で手番を管理する

class Rooms(Document):
    password = StringField(required=True, max_length=30)
    discard = ListField()
    players = ListField()
    player_names = ListField()  # ルーム内のプレイヤー名を保持

class Turn():
    def __init__(self):
        self.value = 0
    def advance(self):
        self.value = (self.value + 1) % 4
        return self.value

try:
    connect(db='OldMaid', host='localhost', port=27017)
except:
    pass

@route('/js/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./view/js')

@route('/images/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./view/images')

@route('/css/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./view/css')

@get('/')
@get('/signup')
def index():
    return template('signup.html', title='Signup Page')

@post('/signup')
def register():
    username = request.forms.decode().get('username')
    password = request.forms.decode().get('password')

    for doc in Users.objects :
        if doc.username==username :
            return '''
            <b>This username already has been registered.</b><br>
            <a href="/login"><button>Login</button></a>
            <a href="/signup"><button>Signup</button></a>
            '''

    user = Users(username=username, password=password)
    user.save()
    return '''
    <b>Registered.</b><br>
    <a href="/login"><button>Go to Login</button></a>
    <a href="/signup"><button>Go to SignUp</button></a>
    '''

@get('/login')
def login():
    return template('login.html', title='Login Page')

@post('/login')
def login():
    username=request.forms.decode().get('username')
    password=request.forms.decode().get('password')

    for doc in Users.objects :
        if doc.username==username and doc.password==password :
            cookie_id = 'user('+str(username)+')'
            response.set_cookie('cookie_id', cookie_id, secret='key')
            doc.cookie = cookie_id
            #userにturnを割り当てる
            doc.save()
            return '''
            <b>Login Sucess. Hello, '''+username+'''..</b><br>
            <a href="/home"><button>home</button></a>
            <a href="/login"><button>Login</button></a>
            <a href="/signup"><button>Signup</button></a>
            <a href="/logout"><button>Logout</button></a>
            '''
    return '''
    <b>Error. Login Failed.</b>
    <a href = "/login"><button>Login</button></a>
    <a href = "/signup"><button>Signup</button></a>
    '''

@get('/logout')
def logout():
    response.delete_cookie('cookie_id')
    response.delete_cookie('username')
    redirect('/login')

@get('/game')
def game():
    times=request.query.times
    cookie_id=request.get_cookie('cookie_id', secret='key')
    roomPass=request.query.roomPass
    # roomPass='aaa' #/gameにアクセスするときにroomPassが必要です(一旦'aaa'にしています)
    users = Users.objects(cookie=cookie_id)
    print("This is GET")
    print("roomPass = ", roomPass)
    print("end_game: ",old_maid.end_game())
    #print("times = ",times)

    if cookie_id==None or (not bool(users)) : # Cannot find the cookie
        return '''
        <b>Not login Error.</b>
        <a href="/home"><button>Home</button></a>
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else :
        #ゲーム側の処理
        #cardsをゲーム側から受け取る
        old_maid.sort_hands()
        old_maid.delete_cards()

        #get user
        thisUser = users[0].usernumber
        print("usernumber: "+ str(thisUser))

        #userによって、playerのカードを分配する 
        P1_card = old_maid.dic[thisUser]
        P2_card = old_maid.dic[thisUser+1] if thisUser+1<4 else old_maid.dic[(thisUser+1)%4]
        P3_card = old_maid.dic[thisUser+2] if thisUser+2<4 else old_maid.dic[(thisUser+2)%4]
        P4_card = old_maid.dic[thisUser+3] if thisUser+3<4 else old_maid.dic[(thisUser+3)%4]

        #このuserは既に勝った、自分のターンをパス
        if old_maid.dic[thisUser] == [] and thisUser == turn.value:
            print("Turn: ",turn.value)
            turn.advance()

        #自分のターンを確認する
        isMyTurn = 1 if thisUser == turn.value else 0
        print("Turn: " +str(turn.value))
        print(isMyTurn)

        username = []
        giveUp = 0
        end_game = 0

        for doc in Rooms.objects:
            if doc.password==roomPass: #部屋検索
                #doc.discard=old_maid.garbage
                if old_maid.end_game() == 1:
                    for card in doc.players:
                        if ["giveUp",-1] in card:
                            giveUp = 1
                    if giveUp == 1 :
                        end_game = 2
                    else:
                        end_game = 1

                if end_game != 2:
                    doc.players= list(old_maid.dic.values())
                doc.save()

                print("docP: ",doc.players)
                pprint.pprint(old_maid.dic)

                #userによって、usernameという配列が違い
                size = 0
                i = thisUser
                while size<4:
                    if i >3:
                        i %= 4
                    username.append(doc.player_names[i])
                    size += 1
                    i += 1
                #print("username",username)

                #始めのアクセス
                if times == '0':
                    #json.dumpsを使って、listからjson strにする
                    return template('game.html', title='OLD MAID', username=username, P1_card=json.dumps(P1_card), P2_card=json.dumps(P2_card), P3_card=json.dumps(P3_card), P4_card=json.dumps(P4_card),isMyTurn=isMyTurn)
                
                #ajaxの回答
                elif times == '1':
                    newHand = {"0": json.dumps(P1_card), "1": json.dumps(P2_card), "2": json.dumps(P3_card), "3": json.dumps(P4_card), "4":isMyTurn, "5": end_game}
                    print(type(newHand))
                    res = bottle.HTTPResponse(body=newHand, status=200)
                    res.set_header("Content-Type", "application/json")

                    return res

        return '''
        <b>This roomPass is not registered.</b><br>
        <a href="/login"><button>Login</button></a>
        <a href="/home"><button>Home</button></a>
        '''

@post('/game')
def game():
    print("This is POST")
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)
    roomPass=str(request.forms['roomPass'])
    print(roomPass)
    #usernumber = int(request.forms['getCardPlayer']);
    
    print(users[0].usernumber)
    print(turn.value)

    if cookie_id==None or (not bool(users)) :
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    elif users[0].usernumber==turn.value:
        #give up
        print("giveUp: ",request.forms['giveUp'])
        if request.forms['giveUp'] != "":
            giveUp_players = [[],[],[],[]]
            Rooms.objects(password=roomPass).update_one(
                players = giveUp_players,
                upsert = False)
            #old_maid.winplayers.clear()

            print(old_maid.players)

            for doc in Rooms.objects:
                if doc.password==roomPass:
                    for players in old_maid.players:
                        if players != users[0].usernumber:
                            old_maid.winplayers.append(players)
                        else:
                            doc.players[players].append(["giveUp",-1])    
                    doc.save()

                print(doc.players)

        #postからのカードIDを受ける
        elif request.forms['drawnCardID'] != "":

            #誰のカードを引くかを決める
            lossCardPlayer = users[0].usernumber-1 if users[0].usernumber-1>=0 else (users[0].usernumber-1)%4
            print(len(old_maid.dic[lossCardPlayer]))
            if len(old_maid.dic[lossCardPlayer]) == 0:
                lossCardPlayer = users[0].usernumber-2 if users[0].usernumber-2>=0 else (users[0].usernumber-2)%4
            if len(old_maid.dic[lossCardPlayer]) == 0:
                lossCardPlayer = users[0].usernumber-3 if users[0].usernumber-3>=0 else (users[0].usernumber-3)%4

            cards = int(request.forms['drawnCardID']);
            old_maid.new_get_card_from_player(users[0].usernumber, lossCardPlayer, cards)
            old_maid.check_win()

        turn.advance()
        return redirect('/game?roomPass='+roomPass)

@get('/standby')
def standby():
    return """不正な画面遷移です"""

@post('/standby')
def standby():
    roomPass=request.forms.decode().get('roomPass')
    mode = request.forms.decode().get('roomType')
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        if mode == 'create':
            for doc in Rooms.objects :
                # 既にデータベースがある場合には警告
                print(doc)
                if doc.password==roomPass :
                    return '''
                    <b>This roomPass already has registered.</b><br>
                    <a href="/login"><button>Login</button></a>
                    <a href="/home"><button>Home</button></a>
                    '''
            # データベースにルームを作る
            room = Rooms(password=roomPass, player_names=[users[0].username])
            room.save()

            #users.usernumberを設定する
            myroom = Rooms.objects(password=roomPass)
            Users.objects(username= users[0].username).update_one(
                set__usernumber = len(myroom[0].player_names)-1,
                upsert = False)
            print(len(myroom[0].player_names))

            return template('standby.html', roomPass=roomPass, username=users[0].username, players=room.player_names)
        elif mode == 'join':
            for doc in Rooms.objects :
                if doc.password==roomPass : # そのroomPassの部屋があるか判定
                    if len(doc.player_names)<4 : # 部屋が4人未満か判定
                        doc.player_names.append(users[0].username) # プレイヤー名を追加
                        doc.save()

                        #users.usernumberを設定する
                        myroom = Rooms.objects(password=roomPass)
                        Users.objects(username= users[0].username).update_one(
                                set__usernumber = len(myroom[0].player_names)-1,
                                upsert = False)
                        print(len(myroom[0].player_names))

                        return template('standby.html', roomPass=roomPass, username=users[0].username, players=doc.player_names)
                    else :
                        return '''
                        <b>This roomPass is full.</b><br>
                        <a href="/login"><button>Login</button></a>
                        <a href="/home"><button>Home</button></a>
                        '''
            # なかったら警告
            return '''
            <b>This roomPass is not registered.</b><br>
            <a href="/login"><button>Login</button></a>
            <a href="/home"><button>Home</button></a>
            '''
        elif mode == 'exit':
            for doc in Rooms.objects :
                if doc.password==roomPass:
                    name_list = list(doc.player_names)
                    # バグで名前が複数ある場合に対応
                    while users[0].username in name_list:
                        name_list.remove(users[0].username)
                    doc.player_names = name_list
                    doc.save()
        elif mode == 'check':
            body = {}
            for doc in Rooms.objects :
                if doc.password==roomPass:
                    print(len(doc.player_names))
                    for i, player_name in enumerate(doc.player_names):
                        body[str(i)] = player_name
            r = bottle.HTTPResponse(body=body, status=200)
            r.set_header("Content-Type", "application/json")
            print("check")
            return r
        elif mode == 'reload':
            for doc in Rooms.objects :
                if doc.password==roomPass :
                    print("reload")
                    return template('standby.html', roomPass=roomPass, username=users[0].username, players=doc.player_names)

# @post('/home')
# def home():
#     cookie_id = request.get_cookie('cookie_id', secret='key')
#     users = Users.objects(cookie=cookie_id)
#     roomPass = request.forms.decode().get('roomPass')

#     if cookie_id==None or (not bool(users)) : 
#         return '''
#         <b>Not login Error.</b>'
#         <a href="/login"><button>Login</button></a>
#         <a href="/signup"><button>Signup</button></a>
#         <a href="/logout"><button>Logout</button></a>
#         '''
#     else:
#         for doc in Rooms.objects :
#             if doc.password==roomPass:
#                 name_list = list(doc.player_names)
#                 # バグで名前が複数ある場合に対応
#                 while users[0].username in name_list:
#                     name_list.remove(users[0].username)
#                 doc.player_names = name_list
#                 doc.save()
                
#         return template('home.html', isLogin=True, name=users[0].username)

@get('/home')
def home():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        return template('home.html', isLogin=True, name=users[0].username)

@get('/win')
def win():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)
    roomPass=request.query.decode().get('roomPass')
    print(roomPass)
    #roomPass='aaa' #/winにアクセスするときにroomPassが必要です(一旦'aaa'にしています)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        winner = ""
        loser = ""
        for doc in Rooms.objects:
            if doc.password==roomPass:
                for idx, players in enumerate(old_maid.winplayers):
                    if idx == 2:
                        winner += doc.player_names[players]
                    else:
                        winner += doc.player_names[players] + ','
                for idx, players in enumerate(doc.players):
                    if players != []:
                        loser = doc.player_names[idx]
        print(winner)
        print(loser)

                #doc.delete()
                #playAgain = "/game?"+roomPass+"&times=0"
        return template('win.html', title='WIN', winner=winner, loser=loser)

@get('/loss')
def loss():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)
    roomPass=request.query.decode().get('roomPass')
    #roomPass='aaa' #/lossにアクセスするときにroomPassが必要です(一旦'aaa'にしています)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        winner = ""
        loser = ""
        for doc in Rooms.objects:
            if doc.password==roomPass:
                for idx, players in enumerate(old_maid.winplayers):
                    if idx == 2:
                        winner += doc.player_names[players]
                    else:
                        winner += doc.player_names[players] + ','
                for idx, players in enumerate(doc.players):
                    if players != []:
                        loser = doc.player_names[idx]
        print(winner)
        print(loser)

                #doc.delete()
        return template('loss.html', title='LOSE', winner=winner, loser=loser)


if __name__ == '__main__':
    turn = Turn()
    old_maid = deck_queue.Old_maid(4)
    run(host='0.0.0.0', port=8082, reloader=True, debug=True, server='paste')