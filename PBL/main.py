from mongoengine import connect, Document, ListField, StringField, URLField
import datetime
from bottle import *

PORT=8086

# Modles class #####################################################################
class Users(Document):
    username = StringField(required=True, max_length=30)
    password = StringField(required=True, max_length=30)
    cookie   = StringField()
    session  = StringField()

class Comments(Document):
    username  = StringField(max_length=30)
    comment   = StringField()
    datetime  = StringField()

try:
    connect(db='prosec', host='localhost', port=27017)
except:
    pass

# Controller #######################################################################
@hook('before_request')
def before():
    response.headers['Access-Control-Allow-Origin'] = '*'

@hook('after_request')
def after():
    pass

@get('/')
@get('/signup')
def index():
    return template('signup')

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

@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text"/>
            Password: <input name="password" type="password"/><br>
            <input value="Login" type="submit"/>
        </form>
        <a href="/signup"><button>Go to Signup Page</botton></a>
    '''

@post('/login')
def login():
    username=request.forms.decode().get('username')
    password=request.forms.decode().get('password')

    for doc in Users.objects :
        if doc.username==username and doc.password==password :
            cookie_id = 'user('+str(username)+')'
            response.set_cookie('cookie_id', cookie_id, secret='key')
            doc.cookie = cookie_id
            doc.save()
            return '''
            <b>Login Sucess. Hello, '''+username+'''..</b><br>
            <a href="/mypage"><button>MyPage</botton></a>
            <a href="/login"><button>Login</botton></a>
            <a href="/signup"><button>Signup</botton></a>
            <a href="/logout"><button>Logout</botton></a>
            '''
    return '''
    <b>Error.</b>'
    <a href="/login"><button>Login</botton></a>
    <a href="/signup"><button>Signup</button></a>
    <a href="/logout"><button>Logout</button></a>
    '''

@get('/logout')
def logout():
    response.delete_cookie('cookie_id')
    response.delete_cookie('username')
    redirect('/login')

@get('/mypage')
def mypage():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)

    if not bool(users) : # Cannnot find the cookie
        return '''
        <b>Not login error.</b><br>
        <a href="/login"><button>Login</botton></a>
        <a href="/signup"><button>Signup</button></a>
        '''
    else :
        user = users[0]
        return '''
        <b>Hello, '''+user.username+'''..</b>
        <a href="/bbs"><button>Go to BBS</button></a>
        <a href="/login"><button>Go to Login</botton></a>
        <a href="/signup"><button>Go to Signup</botton></a>
        <a href="/logout"><button>Go to Logout</botton></a>
        '''

@get('/bbs')
def bbs():
    cookie_id=request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)
    if cookie_id==None or (not bool(users)) : # Cannot find the cookie
        return '''
        <b>Not login Error.</b>
        <a href="/mypage"><button>Go to My page</button></a>
        <a href="/login"><button>Login</botton></a>
        <a href="/signup"><button>Signup</button></a> 
        <a href="/logout"><button>Logout</button></a>
        '''
    else :
        user = users[0]
        username = user.username
        comments = Comments.objects
        return template('bbs', username=username, comments=comments)

@post('/bbs')
def bbs():
    cookie_id = request.get_cookie('cookie_id', secret='key')
    users = Users.objects(cookie=cookie_id)

    if cookie_id==None or (not bool(users)) : 
        return '''
        <b>Not login Error.</b>'
        <a href="/login"><button>Login</botton></a>
        <a href="/signup"><button>Signup</button></a> 
        <a href="/logout"><button>Logout</button></a>
        '''
    else:
        username = users[0].username
        comment = request.forms.decode().get('comment')    
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        comments = Comments(username=username, comment=comment, datetime=now)
        comments.save()

    return redirect('/bbs')
        
@get('/contact')
def contact():
    return html%'''
    <form action="/contact" method="post">
    貴方のメールアドレス: <input name="address" type="text"/><br>
    <textarea name="comment" rows="5" cols="70" placeholder="連絡事項を書いてください">
    </textarea>
    <button type="submit">書き込む</button>
    </form>
    '''

@post('/contact')
def contact():
    address = request.forms.decode().get('address')
    comment = request.forms.decode().get('comment')
    import os
    os.system('/bin/echo "'+comment+'" | /usr/sbin/sendmail -f '+address+' pi@localhost')
    return html%'''
        <b>正常に送信されました</b>
        <a href="/mypage"><button>Go to MyPage</button></a>
    '''

# Main routines #####################################################################
run(host='0.0.0.0', port=PORT)
