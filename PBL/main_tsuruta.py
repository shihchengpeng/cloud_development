from ast import Str
import bottle, jinja2
from bottle import *
from bottle import jinja2_template as template
from jinja2 import Markup
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
    member = IntField()
    discard = ListField()
    players = ListField()

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
    cookie_id=request.get_cookie('cookie_id', secret='key')
    #roomPass=request.query.decode().get('roomPass')
    roomPass='aaa' #/gameにアクセスするときにroomPassが必要です(一旦'aaa'にしています)
    users = Users.objects(cookie=cookie_id)
    print("This is GET")
    print("roomPass = ", roomPass)

    if cookie_id==None or (not bool(users)) : # Cannot find the cookie
        return '''
        <b>Not login Error.</b>
        <a href="/mypage"><button>Go to My page</button></a>
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else :
        #ゲーム側の処理
        #cardsをゲーム側から受け取る
        old_maid.sort_hands()
        old_maid.delete_cards()

        #json_discard = json.dumps(old_maid.garbage)
        #json_players = json.dumps(old_maid.hands)

        P1_card = old_maid.dic[0]
        P2_num = len(old_maid.dic[1])
        P3_num = len(old_maid.dic[2])
        P4_card = old_maid.dic[3]

        username = users[0].username

        for doc in Rooms.objects:
            print("password: "+doc.password)

        for doc in Rooms.objects:
            if doc.password==roomPass: #部屋検索
                doc.discard=old_maid.garbage
                doc.players= list(old_maid.dic.values())
                #doc.players=old_maid.dic
                
                print(doc.discard)
                print(doc.players)
                pprint.pprint(old_maid.dic)
                doc.save()
                #return json.dumps(cards)
                #discard=json.dumps(old_maid.garbage)
                #players=json.dumps(old_maid.hands)

                #return template('game.html')
                return template('game.html', title='OLD MAID', username=username, P1_card=Markup(json.dumps(P1_card)), P2_num=P2_num, P3_num=P3_num, P4_card=Markup(json.dumps(P4_card)))

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
    usernumber = int(request.forms['getCardPlayer']);
    
    print(usernumber)
    print(turn.value)

    if cookie_id==None or (not bool(users)) :
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    elif usernumber==turn.value:
        username = users[0].username
        #クライアントからjson形式のデータを受け取る
        lossCardPlayer = int(request.forms['lossCardPlayer']);
        cards = int(request.forms['drawnCardID']);
        turn.advance()
        #print(old_maid.hands)  
        #pprint.pprint(old_maid.dic)
        old_maid.new_get_card_from_player(usernumber, lossCardPlayer, cards);
        #print(old_maid.hands)　変わっていない
        #pprint.pprint(old_maid.dic)　変わった
        return redirect('/game')
    elif usernumber!=turn.value:
        username = users[0].username
        #print(username)
        #return turn.value
        return template('game.html', title='OLD_MAID', username=users[0].username, turn=turn.value)

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
            room = Rooms(password=roomPass, member=1)
            room.save()
            
            myroom = Rooms.objects(password=roomPass)
            Users.objects(username= users[0].username).update_one(
                set__usernumber = str(myroom[0].member),
                upsert = False)
            print(myroom[0].member)

            return template('standby.html', roomPass=roomPass, username=users[0].username)
            # return template('standby.html', roomPass=roomPass, username=users[0].username, member=room[0].member)
        elif mode == 'join':
            for doc in Rooms.objects :
                if doc.password==roomPass : # そのroomPassの部屋があるか判定
                    if int(doc.member)<4 : # 部屋が4人未満か判定
                        doc.update(inc__member=1) #doc.memberをインクリメント
                        doc.save()
                        myroom = Rooms.objects(password=roomPass)
                        Users.objects(username= users[0].username).update_one(
                            set__usernumber = str(myroom[0].member),
                            upsert = False)
                        print(myroom[0].member)
                        return template('standby.html', roomPass=roomPass, username=users[0].username)
                        # return template('standby.html', roomPass=roomPass, username=users[0].username, member=room[0].member)
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
    #roomPass=request.query.decode().get('roomPass')
    roomPass='aaa' #/winにアクセスするときにroomPassが必要です(一旦'aaa'にしています)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        for doc in Rooms.objects:
            if doc.password==roomPass:
                doc.delete()
        return template('win.html', title='WIN')

@get('/loss')
def loss():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)
    #roomPass=request.query.decode().get('roomPass')
    roomPass='aaa' #/lossにアクセスするときにroomPassが必要です(一旦'aaa'にしています)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        for doc in Rooms.objects:
            if doc.password==roomPass:
                doc.delete()
        return template('loss.html', title='LOSE')


if __name__ == '__main__':
    turn = Turn()
    #old_maid = deck.Old_maid(4)
    old_maid = deck_queue.Old_maid(4)
    run(host='0.0.0.0', port=8082, reloader=True, debug=True)