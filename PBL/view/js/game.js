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
        for(var i=1;i<=P1_HandNow;i++)
        {
            $( "#poker1_"+i ).draggable({
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


    $( function() { 
        var i=1;
        $( "#table" ).droppable({
            accept:"#poker1_"+i,
            drop: function(event, ui){
                discardACard($(ui.draggable).get(0));
            }
        });
    });
    
});

var P4_dic = new Array();
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
      
        card += JSON.stringify(P1_card[i][0])[1].toUpperCase() + ".jpg";
        $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+ (i+1) +'"> <div class="poker"> <img src="images/poker/'+card+'" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }

    for(var i=0;i<countP4;i++)
    {
        var card = JSON.stringify(P4_card[i][1])[1];

        if($.isNumeric(JSON.stringify(P4_card[i][1])[2]))
            card += JSON.stringify(P4_card[i][1])[2];
      
        card += JSON.stringify(P4_card[i][0])[1].toUpperCase();
        P4_dic[i+1] = card;
        $('#handcard4').prepend('<div class="col-2 px-0" id="poker4_'+ (i+1) +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');  
    }

    for(var i=0;i<P2_num;i++)
        $('#handcard2').prepend('<div class="col-2 px-0" id="poker2_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
    
    for(var i=0;i<P3_num;i++)
        $('#handcard3').prepend('<div class="col-1 px-0" id="poker3_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');

}

function drawACard(index){
    index.remove();
    newCard = P4_dic[index.id.substr(index.id.length-1)]+ ".jpg";
    P1_HandNow ++;
    P4_HandNow --;
    $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+P1_HandNow+'" style="display: inline"> <div class="poker"> <img src="images/poker/'+newCard+'" style="max-width: 120%; max-height: 120%"/> </div></div>');
    
    //alert();
    $.post( "/game", {
        getCardPlayer: 0,
        lossCardPlayer: 3,
        drawnCardID: index.id.substr(index.id.length-1)-1
    });
}

function discardACard(index){
    index.remove();
    P1_HandNow --;
}
