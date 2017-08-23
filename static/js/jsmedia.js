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

//Does nothing right now
// $(".search_dt").html($(".dataTables_filter"));

$(document).ready(function() {
    $('#inventory_table').DataTable( {
        "order": [[ 0, "asc" ]],
        stateSave: false,
        "paging": false,
        "dom": 'flrti',
        "columns": [
            null,
            null,
            null,
            null,
            { "type": "checked-in" },
            { "sorting": false },
          ]
    } );
} );

//Allows boolean sort for inventory table
jQuery.fn.dataTableExt.oSort['checked-in-asc']  = function(a,b) {
	var a_sort = parseInt($(a).data("sort"));
	var b_sort =  parseInt($(b).data("sort"));
	return ((a_sort < b_sort) ? -1 : ((a_sort > b_sort) ?  1 : 0));
};

jQuery.fn.dataTableExt.oSort['checked-in-desc'] = function(a,b) {
	var a_sort = parseInt($(a).data("sort"));
	var b_sort =  parseInt($(b).data("sort"));
	return ((a_sort < b_sort) ?  1 : ((a_sort > b_sort) ? -1 : 0));
};

