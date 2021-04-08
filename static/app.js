$(document).ready(function(){
    var manualinterval;
    $('.manualbutton').mousedown(function() {
          element = $(this);
          manualRoll($(element).data('roller'), $(element).data('direction'), 0.5);
          manualinterval = setInterval(function(){ manualRoll($(element).data('roller'), $(element).data('direction'), 0.5);} , 700);
    }).mouseup(function() {
          clearInterval(manualinterval);
    });
    $('.manualbuttonprecise').mousedown(function() {
          element = $(this);
          manualRoll($(element).data('roller'), $(element).data('direction'), 0.1);
          manualinterval = setInterval(function(){ manualRoll($(element).data('roller'), $(element).data('direction'), 0.5);} , 300);
    }).mouseup(function() {
          clearInterval(manualinterval);
    });

    var settinginterval;
    $('.setroller').mousedown(function() {
          element = $(this);
          setRoll($(element).data('roller'), $(element).data('direction'), 0.5);
          settinginterval = setInterval(function(){setRoll($(element).data('roller'), $(element).data('direction'), 0.5);} , 700);
    }).mouseup(function() {
          clearInterval(settinginterval);
    });
    $('.setrollerprecise').mousedown(function() {
          element = $(this);
          setRoll($(element).data('roller'), $(element).data('direction'), 0.1);
          settinginterval = setInterval(function(){setRoll($(element).data('roller'), $(element).data('direction'), 0.5);} , 300);
    }).mouseup(function() {
          clearInterval(settinginterval);
    });
    
    $('.runprogram').click(function(){
        console.log('running')
        $('.runprogram').each(function(){
            $(this).attr('disabled', true);
        });
        $.post('/runprogram', {'id':$(this).data('program_id')}, function(){
            $('.runprogram').each(function(){
                $(this).attr('disabled', false);
            });
        });
    });

});


function manualRoll(roller, direction, time) {
    console.log(roller);
    console.log(direction);
    $.post('/trigger_curtain', {'action': 'push_direction','roller': roller, 'direction': direction, 'time': time});
}

function setRoll(roller, direction, time) {

    $.post('/trigger_curtain', {'action': 'push_direction','roller': roller, 'direction': direction, 'time': time});
    if (roller == 'bottom'){
        if (direction == 'down'){
            cv = parseFloat($('#bottomcounter').val());
            if (cv  - time < 0 ){
                cv = 0;
            }
            else{
                cv = (parseFloat($('#bottomcounter').val()) - parseFloat(time));
            }
            $('#bottomcounter').val(cv);
        }
        if (direction == 'up'){
            $('#bottomcounter').val(parseFloat($('#bottomcounter').val()) + parseFloat(time));
        }
    }

    if (roller == 'top'){
        if (direction == 'up'){
            cv = parseFloat($('#topcounter').val());
            if (cv  - time < 0 ){
                cv = 0;
            }
            else{
                cv = (parseFloat($('#topcounter').val()) - parseFloat(time));
            }
            $('#topcounter').val(cv);
        }
        if (direction == 'down'){
            $('#topcounter').val(parseFloat($('#topcounter').val()) + parseFloat(time));
        }
    }

}


