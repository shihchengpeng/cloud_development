const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const room = urlParams.get('roomPass');
var P1_arr = new Array();
var P2_arr = new Array();
var P3_arr = new Array();
var P4_arr = new Array();
var P1_HandNow = 0;
var P2_HandNow = 0;
var P3_HandNow = 0;
var P4_HandNow = 0;

//みんなの手札を設定する
function setCard(P1_card, P2_card, P3_card, P4_card){
    console.log("setCard");
    P1_HandNow = Object.keys(P1_card).length;
    P2_HandNow = Object.keys(P2_card).length;
    P3_HandNow = Object.keys(P3_card).length;
    P4_HandNow = Object.keys(P4_card).length;

    $('#handcard1').empty();
    $('#handcard2').empty();
    $('#handcard3').empty();
    $('#handcard4').empty();

    for(var i=0;i<P1_HandNow;i++)
    {
        var card = JSON.stringify(P1_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P1_card[i][1])[2]))
            card += JSON.stringify(P1_card[i][1])[2];
      
        card += JSON.stringify(P1_card[i][0])[1].toUpperCase() 

        //カードを配列に保存する
        P1_arr[i+1] = card;

        //カードの名前＋jpgをして、カードを表す
        card += ".jpg";
        $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+ (i+1) +'"> <div class="poker"> <img src="images/poker/'+card+'" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }

    for(var i=0;i<P2_HandNow;i++)
    {
        var card = JSON.stringify(P2_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P2_card[i][1])[2]))
            card += JSON.stringify(P2_card[i][1])[2];
      
        card += JSON.stringify(P2_card[i][0])[1].toUpperCase();

        //カードを配列に保存する
        P2_arr[i+1] = card;
        $('#handcard2').prepend('<div class="col-2 px-0" id="poker2_'+ (i+1) +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }
    
    for(var i=0;i<P3_HandNow;i++)
    {
        var card = JSON.stringify(P3_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P3_card[i][1])[2]))
            card += JSON.stringify(P3_card[i][1])[2];
      
        card += JSON.stringify(P3_card[i][0])[1].toUpperCase();

        //カードを配列に保存する
        P3_arr[i+1] = card;
        $('#handcard3').prepend('<div class="col-1 px-0" id="poker3_'+ (i+1) +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }

    for(var i=0;i<P4_HandNow;i++)
    {
        var card = JSON.stringify(P4_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P4_card[i][1])[2]))
            card += JSON.stringify(P4_card[i][1])[2];
      
        card += JSON.stringify(P4_card[i][0])[1].toUpperCase();

        //カードを配列に保存する
        P4_arr[i+1] = card;
        $('#handcard4').prepend('<div class="col-2 px-0" id="poker4_'+ (i+1) +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');  
    }
}

//引かれるカードの設定
function setDrag()
{
    if(P4_HandNow != 0)
    {
        for(var i=1;i<=P4_HandNow;i++)
        {
            $( "#poker4_"+i ).draggable({
                revert:'invalid'
            })
        }
    }
    else if(P3_HandNow != 0)
    {
        for(var i=1;i<=P3_HandNow;i++)
        {
            $( "#poker3_"+i ).draggable({
                revert:'invalid'
            })
        }
    }
    else if(P2_HandNow != 0)
    {
        for(var i=1;i<=P2_HandNow;i++)
        {
            $( "#poker2_"+i ).draggable({
                revert:'invalid'
            })
        }
    }
}

//どこにカードを置かれることを設定する
function setDrop(isMyTurn)
{
    console.log("isMyTurn: "+isMyTurn);
    if(isMyTurn == 1)
    {
        $( "#handcard1" ).droppable({
            disabled: false
        });
        $( "#handcard1" ).droppable({
            drop: function(event, ui){
                drawACard($(ui.draggable).get(0));
            }
        });

        console.log("set droppable");

        //時間内にカードを引かない場合、自動に引く(バグが起こる)
        var max=0;
        var from="";
        if(P4_HandNow!=0){
            max = P4_HandNow;
            from = '4';
        }
        else if(P3_HandNow!=0){
            max = P3_HandNow;
            from = '3';
        }
        else if(P2_HandNow!=0){
            max = P2_HandNow;
            from = '2';
        }
/*
        var myTimeout = setTimeout(function () {
            var index = getRandom(1,max);
            var randomCard = $("#poker"+from+"_"+index);
            console.log("randomDrop");
            drawACard(randomCard.get(0));
        }, 20000);
*/
    }   
}

//user名前の色の設定
function setColor(isMyTurn)
{
    //console.log("isMyTurn: "+isMyTurn);
    if(isMyTurn == 1)
    {
        console.log(isMyTurn);
        $("#mySelf").css("color","red");
    }   
    else
    {
        $("#mySelf").css("color","black");
    }
}

//buttonの設定
function setBtn(isMyTurn)
{
    //console.log("isMyTurn: "+isMyTurn);
    if(isMyTurn == 1)
    {
        $("#giveUp").prop('disabled', false);
    }   
    else
    {
        $("#giveUp").prop('disabled', true);
    }
}

//sessionを更新して、setDropに行くの必要かをチェックする
function setSession(isMyTurn)
{
    //console.log("isMyTurn: "+isMyTurn);
    if(sessionStorage.getItem("lastDrop")!=isMyTurn && isMyTurn=="1")
    {
        console.log("go to setDrop");
        sessionStorage.setItem("lastDrop", isMyTurn);
        setDrop(isMyTurn);
    }
    else
    {
        sessionStorage.setItem("lastDrop", isMyTurn);
    }
}

//カードを引いた後の動きを設定する
function drawACard(index){
    //console.log(index);
    //console.log(typeof(index));

    //誰のカードを引くかを確認する
    var from_arr = new Array();
    if(P4_HandNow != 0)
    {
        from_arr = P4_arr;
    }
    else if(P3_HandNow != 0)
    {
        from_arr = P3_arr;
    }
    else if(P2_HandNow != 0)
    {
        from_arr = P2_arr;
    }

    console.log(index);
    console.log(typeof(index));

    //引かれたカードを削除する
    index.remove();
    newCard = from_arr[index.id.substr(index.id.length-1)]+ ".jpg";

    $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+(P1_HandNow+1)+'" style="display: inline"> <div class="poker"> <img src="images/poker/'+newCard+'" style="max-width: 120%; max-height: 120%"/> </div></div>');
    $( "#handcard1" ).droppable({
        disabled: true
    });

    sendDrawnCard(index);

    //pairになるかを検査
    var gotPair=0;
    for(var i=1;i<=P1_HandNow;i++)
    {
        if(P1_arr[i].length==from_arr[index.id.substr(index.id.length-1)].length)
            //alert(P1_arr[i].substring(0,P1_arr[i].length-1));
            //alert(P4_arr[index.id.substr(index.id.length-1)].substring(0,P4_arr[index.id.substr(index.id.length-1)].length-1));
            if(P1_arr[i].substring(0,P1_arr[i].length-1)==from_arr[index.id.substr(index.id.length-1)].substring(0,from_arr[index.id.substr(index.id.length-1)].length-1))
            {
                gotPair=1;
                break;
            }
    }

    if(gotPair==1)
    {
        setTimeout(function () {
            alert("Got Pair!");
            //location.reload(true);
        }, 1000);
        gotPair=0;
    }
}

//もらったカードをbackendに送る
function sendDrawnCard(index){
    $.post( "/game", {
        roomPass: room,
        giveUp: "",
        drawnCardID: index.id.substr(index.id.length-1)-1
    });
}

function giveUp(){
    $.post( "/game", {
        roomPass: room,
        giveUp:1,
        drawnCardID:""
    });
    window.location.href = "/loss?roomPass=" + room;
}


function discardACard(index){
    index.remove();
}

function getRandom(min,max){
    return Math.floor(Math.random()*(max-min+1))+min;
};

//ゲームの完了を確認
function checkEnd(endGame){
    if(endGame=="1" || endGame=="2")
    {
        console.log(endGame);
        if(P1_HandNow == 0 || endGame=="2")
        {
            console.log("P1win: "+P1_HandNow);
            window.location.href = "/win?roomPass=" + room;
        }
        else
        {
            console.log("P1loss: "+P1_HandNow);
            window.location.href = "/loss?roomPass=" + room;
        }
    }
}

//カード情報を更新する
function ajaxCall(){
  var req = new XMLHttpRequest();
  req.open('GET', '/game?roomPass='+room+'&times=1');
  req.onreadystatechange = function () {
    if (req.readyState === 4) {
        var jsonData = JSON.parse(req.responseText);
        setColor(JSON.parse(jsonData[4]));
        setCard(JSON.parse(jsonData[0]),JSON.parse(jsonData[1]),JSON.parse(jsonData[2]),JSON.parse(jsonData[3]));
        setDrag();
        setBtn(JSON.parse(jsonData[4]));
        setSession(JSON.parse(jsonData[4]))
        checkEnd(JSON.parse(jsonData[5]));
    }
  };
  req.send();
}