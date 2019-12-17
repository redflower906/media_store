
/**
* Register listeners and add ids to a new orderline row.
* Called by django formset after a new row is added
* @param {object} row - jquery-wrapped row element
*/
function register_row(row){
    var prefix = build_prefix(row.find('input')[0].name)
    var media_select = $('#' + prefix + 'mediatype')
    var inventory_select = $('#id_' + prefix + 'inventory')
    //register listeners to changes in the dropdowns
    // media_select.change(populate_inventory)
    inventory_select.change(populate_vol_and_containers)

    //add django formset-style ids to container and vol p tags,
    //since django-inline-formset won't handle the rownum properly
    row.find('.inv_container p').attr('id', prefix + 'container')
    row.find('.inv_vol p').attr('id', prefix + 'vol')
    // //register a listener to changes in the qty value without touchspin
    // $('#id_' + prefix + 'qty').change('input', handle_qty_update)
    // console.log('prefix', prefix)
}


/**
* Run cleanup tasks when a row is removed
* Called by django formset
* @param {object} row - jquery-wrapped row element
*/
function deregister_row(row){
    update_total()
}

/**
* Media type select handler. Populates the inventory dropdown
* @param {js event} e - event object for media type select change
*/


/**
* Inventory select handler. Fills out form with inventory data
* @param {js event} e - event object for inventory select change
*/
function populate_vol_and_containers(e){
    // fill in the note and container fields for 
    var id = $(e.target).val()
    var prefix = build_prefix(e.target.name)
    if(id){
        var item = find_invdetails(id)
        $('#' + prefix + 'container').text(item.container)
        $('#' + prefix + 'vol').text(item.vol)
        //add cost and quantity
        //set quantity to 1 if 0/empty
        var cur_quantity = $('#id_' + prefix + 'qty').val()
        if (cur_quantity === "0" || cur_quantity === "") {
            $('#id_' + prefix + 'qty').val(1)
            cur_quantity = $('#id_' + prefix + 'qty').val()
        }

        $('#id_' + prefix + 'line_cost').val(calc_cost(cur_quantity, item.cost))
    }
    else{
        //clear container, vol, qty, and cost
        $('#' + prefix + 'container').text('-------')
        $('#' + prefix + 'vol').text('-------')
        $('#id_' + prefix + 'qty').val(0)
        $('#id_' + prefix + 'line_cost').val(0)
    }
    update_total()
}

/**
* qty change handler. Updates line total
* @param {js event} e - event object for qty input
*/
// old version without touchspin
// function handle_qty_update(e){
//     var prefix = build_prefix(e.target.name)
//     var cur_quantity=e.target.value
//     var inventory_id = ($('#id_' + prefix + 'inventory').val())
//     // only update costs/totals if the user has selected an item
//     if(inventory_id){
//         var item = find_invdetails(inventory_id)
//         $('#id_' + prefix + 'line_cost').val(calc_cost(cur_quantity, item.cost))
//         update_total()
//     }
// }

function handle_qty_update(invItem, qtyVal){
    var prefix = build_prefix_buttons(invItem);
    var cur_quantity = qtyVal;
    var inventory_id = invItem.val();
    // only update costs/totals if the user has selected an item
    if(inventory_id){
        var item = find_invdetails(inventory_id)
        $('#' + prefix + 'line_cost').val(calc_cost(cur_quantity, item.cost));
        update_total();
    }

}

/**
 * Find inventory details in the inventory_groups map, given an inventory id
 * @param {string} id - the database id of the inventory object
 */
function find_invdetails(inv_id) {
    return $.grep(
        //flatten the groups into one list
        $.map(inventory_groups, function (vals) { return vals }),
        //then find the item
        function (item) { return item.id == inv_id }
    )[0]
}

/**
 * Utility to get the django form prefix from the given form element id
 * @param {id} id - form element id
 */
function build_prefix(id) {
    id_parts = id.split('-')
    return id_parts[0] + '-' + id_parts[1] + '-'
}

function build_prefix_buttons(invItem) {
    id_parts = invItem.attr('id').split('-')
    return id_parts[0] + '-' + id_parts[1] + '-'
}

/**
 * Utility to calculate line costs OR MAYBE THIS IS WHAT NEEDS TO CHANGE TO MANUALLY OVERRIDE LINE COSTS ~FIX~
 * @param {string} qty - qty field value
 * @param {string} cost - cost field value
 */
function calc_cost(qty, cost){
    if(qty==='' || qty===null){
        return 0
    }    
    return  (qty * parseFloat(cost)).toFixed(2)

}

/**
 * Utility to calculate the order total
 */
function update_total(){
    var total = 0;
    $('input.line_cost').map(function (__, costel) {
        var val = parseFloat($(costel).val() || '0')
        if(val === null || val === ''){
            val = 0
        }
        total += val
    });
    $('p.aggregate_total').text('$' + total.toFixed(2))
}