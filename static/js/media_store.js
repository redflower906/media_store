

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
})