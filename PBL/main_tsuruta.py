from ast import Str
import bottle, jinja2
from bottle import *
from bottle import jinja2_template as template
from mongoengine import connect, Document, ListField, StringField, URLField, IntField, ReferenceField
import random
import json
import deck_queue

TEMPLATE_PATH.append('./view')

class Users(Document):
    username = StringField(required=True, max_length=30)
    password = StringField(required=True, max_length=30)
    cookie = StringField()
    usernumber = IntField() #0-3までの数字で手番を管理する

class Cards(Document):
    suits = StringField()
    value = StringField()

class Rooms(Document):
    password = StringField(required=True, max_length=30)
    discard = ListField(ReferenceField(Cards))
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
            print(username)#test
            print(password)
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
    room = Rooms.objects(password=roomPass)
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
        discard = old_maid.garbage
        players = old_maid.hands
        print(discard)
        print(players)
        #データベースにdiscardとplayersを格納できなくて困っています
        room = Rooms(discard=discard, players=players)
        room.save
        
        cards = old_maid.hands
        json_cards = json.dumps(old_maid.hands)
        username = users[0].username
        #return json.dumps(cards)
        return template('game.html', title='OLD MAID')
        #return template('game.html', title='OLD MAID', username=username, card=json.dumps(cards))

@post('/game')
def game():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)

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
        cards = json.loads(json_cards)
        turn.advance()
        return redirect('/game')
    elif usernumber!=turn.value:
        username = Users[0].username
        #return turn.value
        return template('game.html', title='OLD_MAID', username=username, turn=turn.value)

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
                if doc.password==roomPass :
                    return '''
                    <b>This roomPass already has registered.</b><br>
                    <a href="/login"><button>Login</button></a>
                    <a href="/home"><button>Home</button></a>
                    '''
            # データベースにルームを作る
            room = Rooms(password=roomPass)
            room.save()
            return template('standby.html', roomPass=roomPass, username=users[0].username)
        elif mode == 'join':
            # そのroomPassの部屋があるか，ないか判定
            for doc in Rooms.objects :
                if doc.password==roomPass :
                    return template('standby.html', roomPass=roomPass, username=users[0].username)
                else :
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

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</button></a>
        <a href="/signup"><button>Signup</button></a>
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        return template('win.html', title='WIN')

@get('/loss')
def loss():
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
        return template('loss.html', title='LOSE')


if __name__ == '__main__':
    turn = Turn()
    #old_maid = deck.Old_maid(4)
    old_maid = deck_queue.Old_maid(4)
    run(host='0.0.0.0', port=8082, reloader=True, debug=True)