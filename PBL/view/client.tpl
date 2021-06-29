<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <title>Security Camp in Kyushu</title>
</head>
<body>
    <h2>こんにちは，<span id="hello-user">{{username}}</span>さん</h2><br />
    <h2>ここは，<span class="marked-font">ババ抜き</span>用のページです．</h2>
    <ol id="card-list" style="margin:2em;">
        %for card in mycards:
            <li style="margin:2em; line-height:150%; border: solid 1px #ccc;">
                {{card.markname}} : {{card.marknum}}<br></li>
            <!-- disable escape for a purpose of cyberattack -->
        %end
    </ol>
    <form action="/game" method="post">
        <input type="hidden" name="token" value="a73+f*&t5" />
	<select name="select">
	%for card in cards:
	<option value={{card.id}}>{{card.id}}</option><br />
	%end
	</select>
        <button type="submit">書き込む</button>
    </form>
    <a href="/mypage"><button>マイページに戻る</button></a>
    <a href="/login"><button>ログイン画面に戻る</button></a>
    <a href="/logout"><button>ログアウトする</button></a>
</body>
</html>

