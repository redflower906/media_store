// function add_item_line(data){
//     var count =  $('#item_line_table tbody').children().length;
//     var template = $('#item-line-form').html();
//     var compiled = Handlebars.compile(template);
//     data['id'] = count;
//     var html = compiled(data);
//     $('#item_line_table tbody').append(html);
//     $('#id_SingleItem_set-TOTAL_FORMS').attr('value', count + 1);
//     $("#item_line_table .chosen-select:last").chosen({'disable_search_threshold': 10, 'enable_split_word_search': false, 'search_contains': true });
//   }
  
//   $('#add_item_line').on('click', add_item_line);

//Properly Highlight Navbar Links
$(document).ready(function() {
    $.each($('#navbar').find('li'), function() {
        $(this).toggleClass('active', 
            window.location.pathname.indexOf($(this).find('a').attr('href')) > -1);
    }); 
});

//hide / expand table children. had to change toggle_notes from id to class for click event to
//occur with all records
$(document).ready(function(){
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
$(document).ready(function () { 
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

    document.getElementById("fname").onchange = function() {myFunction()};
    
    function myFunction() {
        var x = document.getElementById("fname");
        x.value = x.value.toUpperCase();
    }