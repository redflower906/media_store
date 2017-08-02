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

  $(document).ready(function() {
    $.each($('#navbar').find('li'), function() {
        $(this).toggleClass('active', 
            window.location.pathname.indexOf($(this).find('a').attr('href')) > -1);
    }); 
});

// var $makeActive = false;
// $('#activate').on('click', 'a', function() {
//    $makeActive = !($makeActive);
//     console.log($makeActive);
// });

// var $makeInactive = true;
// $('#inactivate').on('click', 'a', function() {
//    $makeInactive = !($makeInactive);
//     console.log($makeInactive);
// });

function updateActivation(){
    var data = {'active': active};
    $.post(URL, data, function(response){
        if(response === 'success'){ console.log(data); }
        else{ console.log('Error! :('); }
    });
}
$(document).ready(function(){
    $('#activate').click(function(){
        active = true;
        updateActivation();
    });
    $('#inactivate').click(function(){
        active = false;
        updateActivation();
    });
});