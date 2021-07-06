from ast import Str
import bottle, jinja2
from bottle import *
from bottle import jinja2_template as template
from mongoengine import connect, Document, ListField, StringField, URLField, IntField
import random
import json

TEMPLATE_PATH.append('./view')

class Users(Document):
    username = StringField(required=True, max_length=30)
    password = StringField(required=True, max_length=30)
    cookie = StringField()
    usernumber = IntField() #0-3までの数字で手番を管理する

class Turn():
    def __init__(self):
        self.value = 0
    def advance(self):
        self.value = (self.value + 1) % 4
        return self.value

try:
    connect(db='prosec', host='localhost', port=27017)
except:
    pass

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
            <a href="/login"><button>Login</botton></a>
            <a href="/signup"><button>Signup</button></a>
            '''

    user = Users(username=username, password=password)
    user.save()
    return '''
    <b>Registered</b><br>
    <a href="/login"><button>Go to Login</botton></a>
    <a href="/signup"><button>Go to SignUp</button></a>
    '''

@get('/test_game')
def login():
    return template('game.html', title='Test game.html Page')


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
            <a href="/game"><button>game</button></a>
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

# @get('/mypage')
# def mypage():
#     cookie_id = request.get_cookie('cookie_id', secret='key')
#     users = Users.objects(cookie=cookie_id)

#     if not bool(users) : # Cannnot find the cookie
#         return '''
#         <b>Not login error.</b><br>
#         <a href="/login"><button>Login</button></a>
#         <a href="/signup"><button>Signup</button></a>
#         '''
#     else :
#         user = users[0]
#         return template('mypage.html', title='MyPage', username=user.username)

@get('/game')
def game():
    cookie_id=request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)
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

@get('/waiting_room')
def waiting_room():
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
        return template('old_maid.html', title='WAITING ROOM', username=username)

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
        return template('home.html', title='HOME', username=username)

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
    run(host='0.0.0.0', port=8082, reloader=True, debug=True)