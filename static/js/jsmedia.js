function add_item_line(data){
    var count =  $('#item_line_table tbody').children().length;
    var template = $('#item-line-form').html();
    var compiled = Handlebars.compile(template);
    data['id'] = count;
    var html = compiled(data);
    $('#item_line_table tbody').append(html);
    $('#id_SingleItem_set-TOTAL_FORMS').attr('value', count + 1);
    $("#item_line_table .chosen-select:last").chosen({'disable_search_threshold': 10, 'enable_split_word_search': false, 'search_contains': true });
  }
  
  $('#add_item_line').on('click', add_item_line);