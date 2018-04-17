function add_row(data, table_id, template_id, mngmt_total_id, form_id){

  if (!table_id){
    table_id='order_table';
    template_id = 'order-line-form';
    mngmt_total_id = 'id_orderlines-TOTAL_FORMS';
    form_id = 'order_form';
  }

  var count =  $('#' + table_id +' tbody').children().length;
  var template = $('#' + template_id +'').html();
  var compiled = Handlebars.compile(template);
  data['id'] = count;
  var html = compiled(data);
  $('#' + table_id +' tbody').append(html);
  $('#' + mngmt_total_id).attr('value', count + 1);
  $('#' + form_id).trigger('rescan.areYouSure');
  return count;//return the row id
}

$('#add_order_line').on('click', function() {
    add_row([])
    $("#order_table .chosen-select:last").chosen({'disable_search_threshold': 10, 'enable_split_word_search': false, 'search_contains': true });
});

//make sure the checkboxes that are present on initial page load also get the hide functionality
$('#order_table').on('change', 'tbody input[type=checkbox]', function() {
  //TODO: possibly replace with undo link.
  if ($(this).prop('checked')) {
    $(this).parent().parent().addClass('deleted');
  } else {
    $(this).parent().parent().removeClass('deleted');
  }
});

$('#order_table, #dept_cost_assign').on('change', 'thead input[type=checkbox]', function() {
  //TODO: possibly replace with undo link.
  if ($(this).prop('checked')) {
    $('#order_table, #dept_cost_assign').find('input[name$="DELETE"]').prop('checked', true).trigger('change')
  } else {
    $('#order_table, #dept_cost_assign').find('input[name$="DELETE"]').prop('checked', false).trigger('change')
  }
});

function getCookie(name){
    var cookieValue = null;
    if(document.cookie && document.cookie != ''){
        var cookies = document.cookie.split(';');
        for(var i = 0; i<cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            if(cookie.substring(0, name.length +1) == (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
}



var updateTotals = function() {
    var total = 0;
    var lines = $('#order_table tbody tr');

    lines.each(function(line) {
        if (!$(this).find('input[type=checkbox]').prop('checked')) {
            var qty = parseFloat($(this).find('line_qty').val());
            var cost = parseFloat($(this).find('line_cost').val());
            var line_total = 0;
            if (fixed) {
                line_total = fixed;
            } else if (cost && qty) {
                line_total = cost * qty;
            }
            total += line_total;
            var as_currency = line_total.toLocaleString('en_US', {style: 'currency', currency: 'USD' });
            $(this).find('.line_total').text(as_currency);
        }
    });
    $('.aggregate_total').text(total.toLocaleString('en_US', {style: 'currency', currency: 'USD' });
});