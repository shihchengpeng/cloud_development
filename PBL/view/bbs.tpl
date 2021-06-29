<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>Security Camp in Kyushu</title>
</head>
<body>
    <h2>こんにちは，<span id="hello-user">{{username}}</span>さん</h2><br />
    <h2>ここは，<span class="marked-font">みんなの掲示板</span>用のページです．</h2>
    <ol id="comment-list" style="margin:2em;">
        %for comment in comments:
            <li style="margin:2em; line-height:150%; border: solid 1px #ccc;">
                {{comment.username}} : {{comment.datetime}}<br />
                {{!comment.comment}}</li>
            <!-- disable escape for a purpose of cyberattack -->
        %end
    </ol>
    <form action="/bbs" method="post">
        <input type="hidden" name="token" value="a73+f*&t5" />
        <textarea name="comment" rows="5" cols="70" placeholder="何か書いてください"></textarea>
        <button type="submit">書き込む</button>
    </form>
    <a href="/mypage"><button>マイページに戻る</button></a>
    <a href="/login"><button>ログイン画面に戻る</button></a>
    <a href="/logout"><button>ログアウトする</button></a>
</body>
</html>

