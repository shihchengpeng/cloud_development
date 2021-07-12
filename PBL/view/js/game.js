$(document).ready(function(){
    $( function() {
        for(var i=1;i<=P4_HandNow;i++)
        {
            $( "#poker4_"+i ).draggable({
            revert:'invalid'
        })
        }
    });

    $( function() {
        $( "#handcard1" ).droppable({
            drop: function(event, ui){
                drawACard($(ui.draggable).get(0));
            }
        });
    });

});

var P4_arr = new Array();
var P1_arr = new Array();
var P1_HandNow = 0;
var P4_HandNow = 0;

function setCard(P1_card, P2_num, P3_num, P4_card){
    var countP1 = Object.keys(P1_card).length;
    var countP4 = Object.keys(P4_card).length;
    P1_HandNow = countP1;
    P4_HandNow = countP4;

    for(var i=0;i<countP1;i++)
    {
        var card = JSON.stringify(P1_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P1_card[i][1])[2]))
            card += JSON.stringify(P1_card[i][1])[2];
      
        card += JSON.stringify(P1_card[i][0])[1].toUpperCase() 
        P1_arr[i+1] = card;
        card += ".jpg";
        $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+ (i+1) +'"> <div class="poker"> <img src="images/poker/'+card+'" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }

    for(var i=0;i<countP4;i++)
    {
        var card = JSON.stringify(P4_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P4_card[i][1])[2]))
            card += JSON.stringify(P4_card[i][1])[2];
      
        card += JSON.stringify(P4_card[i][0])[1].toUpperCase();
        P4_arr[i+1] = card;
        $('#handcard4').prepend('<div class="col-2 px-0" id="poker4_'+ (i+1) +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');  
    }

    for(var i=0;i<P2_num;i++)
        $('#handcard2').prepend('<div class="col-2 px-0" id="poker2_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
    
    for(var i=0;i<P3_num;i++)
        $('#handcard3').prepend('<div class="col-1 px-0" id="poker3_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');

}

function drawACard(index){
    index.remove();
    newCard = P4_arr[index.id.substr(index.id.length-1)]+ ".jpg";

    $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+(P1_HandNow+1)+'" style="display: inline"> <div class="poker"> <img src="images/poker/'+newCard+'" style="max-width: 120%; max-height: 120%"/> </div></div>');
    $( "#handcard1" ).droppable({
        disabled: true
    });

    $.post( "/game", {
        getCardPlayer: 0,
        lossCardPlayer: 3,
        drawnCardID: index.id.substr(index.id.length-1)-1
    });

    var gotPair=0;
    for(var i=1;i<P1_HandNow;i++)
    {
        if(P1_arr[i].length==P4_arr[index.id.substr(index.id.length-1)].length)
            //alert(P1_arr[i].substring(0,P1_arr[i].length-1));
            //alert(P4_arr[index.id.substr(index.id.length-1)].substring(0,P4_arr[index.id.substr(index.id.length-1)].length-1));
            if(P1_arr[i].substring(0,P1_arr[i].length-1)==P4_arr[index.id.substr(index.id.length-1)].substring(0,P4_arr[index.id.substr(index.id.length-1)].length-1))
            {
                gotPair=1;
                break;
            }
    }

    if(gotPair==1)
    {
        setTimeout(function () {
            alert("Got Pair!");
            location.reload(true);
        }, 500);
    }
}

function discardACard(index){
    index.remove();
}
