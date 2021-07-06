import bottle, jinja2
from bottle import *
from bottle import jinja2_template as template

TEMPLATE_PATH.append('./view')
PORT=8086


class Users():
    def __init__(self, name, password):
        self.username = name
        self.password = password

#　本番はこっち
# class Users(Document):
#     username = StringField(required=True, max_length=30)
#     password = StringField(required=True, max_length=30)
#     cookie   = StringField()
#     session  = StringField()


testUser = Users("T1", "test")

@get('/')
def home():
    # isLogin = ログインしていたらTrue, name = Users.username
    # ログインしているかの判定が欲しいです
    return template('home.html', isLogin=True, name=testUser.username)

@post('/standby')
def standby():
    roomPass=request.forms.decode().get('roomPass')
    # mode = 'join' or 'create' ルームを作ったのか，参加しているのかで処理を変える
    mode = request.forms.decode().get('roomType')

    if mode == 'create':
        # データベースにルームを作る
        pass
    elif mode == 'join':
        # そのroomPassの部屋があるか，ないか判定

        # あったらデータベースのルームにその人を追加して　return template('standby.html', roomPass=roomPass, users = testUser.username)

        # なかったら警告
        pass
    return template('standby.html', roomPass=roomPass, users = testUser.username)
    
run(host='0.0.0.0', port=PORT)