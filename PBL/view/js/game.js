$(document).ready(function(){
    var card_num=3;
    for(var i=1;i<=card_num;i++){
        $('#handcard1').prepend('<div class="col-1 px-0" id="poker1_'+ i +'"> <div class="poker"> <img src="images/poker/joker.jpeg" style="max-width: 120%; max-height: 120%"/> </div></div>');
        $('#handcard2').prepend('<div class="col-2 px-0" id="poker2_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
        $('#handcard3').prepend('<div class="col-1 px-0" id="poker3_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
        $('#handcard4').prepend('<div class="col-2 px-0" id="poker4_'+ i +'"> <div class="poker"> <img src="images/card_back.png" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }

    $( function() {
        $( "#poker4_1, #poker4_2, #poker4_3, #poker4_4, #poker4_5" ).draggable({
            revert:'invalid'
        }) 
    });

    $( function() {
        $( "#poker1_1, #poker1_2, #poker1_3, #poker1_4, #poker1_5" ).draggable({
            revert:'invalid'
        })
    });

    $( function() {
        $( "#handcard1" ).droppable({
            drop: function(event, ui){
                drawACard($(ui.draggable).get(0));
            }
        });
    });

    $( function() {
        $( "#table" ).droppable({
            accept: "#poker1_1, #poker1_2, #poker1_3, #poker1_4, #poker1_5",
            drop: function(event, ui){
                discardACard($(ui.draggable).get(0));
            }
        });
    });


    function drawACard(b){
        b.remove();
        $('#handcard1').prepend('<div class="col-1 px-0" style="display: inline"> <div class="poker"> <img src="images/poker/joker.jpeg" style="max-width: 120%; max-height: 120%"/> </div></div>');
    }

    function discardACard(b){
        b.remove();
    }
});