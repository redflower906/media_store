//Properly Highlight Navbar Links
$(function() {
    $.each($('#navbar').find('li'), function() {
        $(this).toggleClass('active', 
            window.location.pathname.indexOf($(this).find('a').attr('href')) > -1);
    }); 
});

//hide / expand table children. had to change toggle_notes from id to class for click event to
//occur with all records
$(function(){
    $(".toggle_notes").off("click").click(function(e){
        // figure out the next line items class and show / hide it

        if ($(this).find('i.glyphicon-plus').length) {
            //add .length to see if an element exists in jquery
        $(this).closest('.koala').next().fadeIn();
        $(this).find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus')
        } else {
        $(this).closest('.koala').next().fadeOut();
        $(this).find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus')
        
        }
    });
})

//Search Function
$(function () { 
    (function ($) {
        //As you type in id=filter, it searches each character
        $('#filter').keyup(function () {
            //creates a regex to compare the typed values with values in table
            var rex = new RegExp($(this).val(), 'i');
            //hides every row in the table
            $('.searchable tr.koala').hide();
            //finds any instance of a minus glyph and changes it to a plus
            $('.searchable tr.koala').find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus')
            //closes all notes
            $('.searchable tr.koala').next().fadeOut();
            //searches each row for the regex and then shows it
            $('.searchable tr.koala').filter(function () {
                return rex.test($(this).text());
            }).show();
        });
    }(jQuery));
});

//datepicker function and disabling days before today/after 3 months
$(function() {
    $( "#id_order-date_recurring_start" ).datepicker({
        minDate: new Date(),
    });
    $( "#id_order-date_recurring_stop" ).datepicker({
        maxDate: "+3m",
    });        
});

//jquery datepicker to show/hide based on radio selection
$(function (){
    var radio = $('input:checked').attr('id');
    if (radio == 'id_order-is_recurring_0') {
        $('#datepicker').show();
        $('#datepicker').find('#id_order-date_recurring_start').prop('required', true);
        $('#datepicker').find('#id_order-date_recurring_stop').prop('required', true);
        $('#datepicker').find('#id_order-weeks').prop('required', true);


    }
    else{
        $('#datepicker').hide();
    }
    $('input[name="order-is_recurring"]:radio').change(
        function(){
            if (this.checked && this.value == 'True') {
                $('#datepicker').show();
                $('#datepicker').find('#id_order-date_recurring_start').prop('required', true);
                $('#datepicker').find('#id_order-date_recurring_stop').prop('required', true);
                $('#datepicker').find('#id_order-weeks').prop('required', true);
            }
            else {
                $('#datepicker').hide();
                $('#datepicker').find('#id_order-date_recurring_start').prop('required', false);
                $('#datepicker').find('#id_order-date_recurring_stop').prop('required', false);
                $('#datepicker').find('#id_order-weeks').prop('required', false);
            }
    });    
})

//Change maps depending on what floor is picked
$(function(){
    $('#id_order-location').on('change', function(e){
        var getVal = $('#id_order-location option:selected').val();
        var small = getVal.substr(0,2);
        $(this).removeClass();
        $(this).addClass(small)
        var image_modal = document.getElementById("img_map");
        var image_div = document.getElementById('img');
        console.log(image_div)
        if ($(this).closest('#id_order-location').hasClass('2W')){
            image_modal.src = "/static/images/2W.png" 
            image_div.src = "/static/images/2W.png"                         
        } else if ($(this).closest('#id_order-location').hasClass('2C')){
            image_modal.src = "/static/images/2C.png"      
            image_div.src = "/static/images/2C.png"                    
        } else if ($(this).closest('#id_order-location').hasClass('2E')){
            image_modal.src = "/static/images/2E.png" 
            image_div.src = "/static/images/2E.png" 
        } else if ($(this).closest('#id_order-location').hasClass('3E')){
            image_modal.src = "/static/images/3E.png" 
            image_div.src = "/static/images/3E.png" 
        } else if ($(this).closest('#id_order-location').hasClass('3C')){
            image_modal.src = "/static/images/3C.png" 
            image_div.src = "/static/images/3C.png" 
        } else{
            image_modal.src = "/static/images/3W.png" 
            image_div.src = "/static/images/3W.png" 
        }
    });
});

//Alert when editing a recurring order
function recurringAlert(){
    var recur = $('input:checked').attr('id');
    if (recur == 'id_order-is_recurring_0') {
        alert('Be aware that, if this order has been edited, any changes may not be implemented until the following week. Please email media facility with any questions.')
    }
}

//Change all orders tagged as complete to billed
function changeAllBill(){
    $('td.Complete').children().val('Billed');
};

//User cancel an order
$(function(){
    $('.cancelbtn').click(function(){
        $(this).parent().siblings('.status').children().val('Canceled');
    });
});



//Automatically choose department and project code based on requester
$(function(){
    $('#id_order-requester').change(function() {
        var optionSelected = $(this).find("option:selected");
        var valueSelected = optionSelected.val();
        var requester_name = optionSelected.text();
        $.ajax({
        url: '/ajax',
        data: {
            'id': valueSelected,
            'name': requester_name
        },
        dataType: 'json',
        success: function(data){
            if (data.r_id) {
                $("#id_order-department").val(data['d_id']).trigger("chosen:updated");

                if(data.p_id){
                    $("#id_order-project_code").val(data['up_id']).trigger("chosen:updated");
                }
                else{
                    $("#id_order-project_code").val('').trigger("chosen:updated");                    
                }
            }
            else{
                $("#id_order-department").val('').trigger("chosen:updated");
            }
        },
        });
    });
});

//remove readonly attribute if orderlines-0-inventory is 'custom order'
$(function(){
    $('#id_orderlines-0-inventory').change(function(){
        var inv = $('#id_orderlines-0-inventory').val();
        if ((inv == 1350) && $('#id_cost').hasClass('staff')){
            $('#id_orderlines-0-line_cost').removeAttr('readonly');
            console.log('inv = custom order');
        }
    })
    if ($('#id_cost').hasClass('staff')){
        $('#id_orderlines-0-line_cost').removeAttr('readonly');
        console.log('inv = custom order');
    }
})

//Remainder bottles/vials

function update_remainder(){
    $(function(){
        $('#bottle_i').on('input', function (evt){
            var bottle_ival = evt.target.value;
            console.log(bottle_ival);
            var bottle_cval = $('#bottle_i').parents('.bottle_i_td').siblings('#bottle_c').val();
            console.log(bottle_cval);
        })
    })
}