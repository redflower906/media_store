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

//Datatables.net jquery library settings
// $(document).ready(function() {
//     console.log(InventoryItem)
// });    
// $(document).ready(function() {
//     // console.log(InventoryItems);
//     $('#inventory_table').DataTable( {
//         "order": [[ 0, "asc" ]],
//         stateSave: false,
//         "paging": false,
//         "dom": 'flrti',
//         "columns": [
//             null,
//             null,
//             null,
//             null,
//             { "type": "checked-in" },
//             { "sorting": false },
//             // "className": 'details-control',
//             // "orderable": false,
//             // "data": null,
//             // "defaultContent": ''
//             // "render": function () {
//             //     return '<i class="glyphicon glyphicon-plus" aria-hidden="true"></i>';
//             // },
//           ]

//     } );
// });

//     //Allows boolean sort for inventory table
//     jQuery.fn.dataTableExt.oSort['checked-in-asc']  = function(a,b) {
//         var a_sort = parseInt($(a).data("sort"));
//         var b_sort =  parseInt($(b).data("sort"));
//         return ((a_sort < b_sort) ? -1 : ((a_sort > b_sort) ?  1 : 0));
//     };

//     jQuery.fn.dataTableExt.oSort['checked-in-desc'] = function(a,b) {
//         var a_sort = parseInt($(a).data("sort"));
//         var b_sort =  parseInt($(b).data("sort"));
//         return ((a_sort < b_sort) ?  1 : ((a_sort > b_sort) ? -1 : 0));
//     };

//     // Add event listener for opening and closing details
//     $('#inventory_table tbody').on('click', 'td.details-control', function () {
//         var tr = $(this).closest('tr');
//         var tdi = tr.find("i.glyphicon");
//         var row = table.row(tr);

//         if (row.child.isShown()) {
//         // This row is already open - close it
//             row.child.hide();
//             tr.removeClass('shown');
//             tdi.first().removeClass('glyphicon glyphicon-minus');
//             tdi.first().addClass('glyphicon glyphicon-plus');
//         }
//         else {
//         // Open this row
//             row.child(format(row.data())).show();
//             tr.addClass('shown');
//             tdi.first().removeClass('glyphicon glyphicon-plus');
//             tdi.first().addClass('glyphicon glyphicon-minus');
//         }
//     });

//     table.on("user-select", function (e, dt, type, cell, originalEvent) {
//         if ($(cell.node()).hasClass("details-control")) {
//             e.preventDefault();
//             }
//         });
//     });

//    function format(d){
       
//         // `d` is the original data object for the row
//         // need to call d function
//         // need to reference details-control in formatting
//         return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
//             '<tr>' +
//                 '<td>notes:</td>' +
//                 '<td>' + d.notes + '</td>' +
//             '</tr>' +
//         '</table>';  
        
//    }

//hide / expand table children. had to change toggle_notes from id to class for click event to
//occur with all records
$(document).ready(function(){
    $(".toggle_notes").click(function(){
        // figure out the next line items class and show / hide it
        console.log($(this).find('i.glyphicon-plus').length)
        if ($(this).find('i.glyphicon-plus').length) {
            //add .length to see if an element exists in jquery
            console.log('true', $(this))
        $(this).closest('.koala').next().fadeIn();
        $(this).find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus')
        } else {
            console.log('false', $(this))
        $(this).closest('.koala').next().fadeOut();
        $(this).find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus')
        
        }
    });
})

$(document).ready(function () { 
        (function ($) {
            $('#filter').keyup(function () {
                var rex = new RegExp($(this).val(), 'i');
                $('.searchable tr.koala').hide();
                $('.searchable tr.koala').find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus')
                $('.searchable tr.koala').next().fadeOut();
                $('.searchable tr.koala').filter(function () {
                    return rex.test($(this).text());
                }).show();
            });
        }(jQuery));
    });