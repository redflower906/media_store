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

    // $('.status_drop').off('click').click(function(){ //Once any element with class "status" is clicked
    //     if ($(this).find('koala').length) { // if class already has 'one', un-highlight
    //         console.log('off');
    //         // $(this).closest('.sdd').removeClass('sdd');
    //     } else {
    //         console.log('on');
    //         $(this).closest('.koala').addClass('sdd'); // Select the one clicked
    //     }
    // });
})

// $(document).ready(function(){
//     var array1 = 
//         $("select option:selected").map(function (i, el) { return $(el).val(); }).get();
//     console.log(arrayOfValues);
// });

var isEqual = function (value, other) {
    //Get value type
    var type = Object.prototype.toString.call(value);
    // Get length
    var valueLen = type ==='[object Array]' ? value.length : Object.keys(value).length;
    //compare two items
    var compare = function (item1, item2) {
        //Get the object type
        var itemType = Object.prototype.toString.call(item1);
        //If an object or array, compare recursively
        if (['[object Array]'], '[object Object]'.indexof(itemType) >= 0) {
            if (!isEqual(item1, item2)) return false;
        }
        //Otherwise do a simple comparison
        else {
            if(item1 !== item2) return false;
        }
    };
    // Compare properties
    if(type === '[object Array]') {
        for (var i = 0; i < valueLen; i++) {
            if (compare(value[i], other[i]) === false) return false;
        }
    } else {
        for (var key in value) {
            if(value.hasOwnProperty(key)) {
                if(compare (value[key], other[key]) === false) return false;
            }
        }
    }
    return true;
};

// $(function(){
//     var array1 = new Array();
//     // console.log(this);
//     $('select option:selected').each(function() {
//         array1.push($(this).val());
//     });
//     $('select').on('change', function(){
//         var array2 = new Array();
//         $('select option:selected').each(function() {
//             array2.push($(this).val());
//         });
//         console.log(array2);
//         console.log(array1);

//             for (var i = 0; i < array1.length; i++) {
//                 if (array1[i] != array2[i]) {
//                     console.log('not equal!');
//                     console.log(i, array1[i]);
//                     console.log(i, array2[i]);
//                     console.log(this);
//                     $(this).closest('koala').addClass('sdd');
//                 } else {
//                     console.log('equal!')
//                     // this is only referring to the current select. so if there is are any indices that match, it'll take off the .sdd of this,
//                     //regardless of whether the current index is the one that matches or not.
//                     //should I have it only check the current index of the array?
//                     if ($(this).parent('.sdd').length) { // if class already has 'one', un-highlight
//                         $(this).closest('.sdd').removeClass('sdd');
//                     }
//                 }
//             }
//     });
// });


//highlight clicked status
// $(function(){
//     $('.status_drop').off('click').change(function(){ //Once any element with class "status" is clicked
//         if ($(this).parent('.sdd').length) { // if class already has 'one', un-highlight
//             $(this).closest('.sdd').removeClass('sdd');
//         } else {
//             $(this).closest('tr.koala').addClass('sdd'); // Select the one clicked
//         }
//     });
// })

// //highlight clicked status
// $(document).ready(function(){
//     $('.status_drop').off('click').click(function(){ //Once any element with class "status" is clicked
//         if ($(this).parent('.sdd').length) { // if class already has 'one', un-highlight
//             console.log('hi');
//             $(this).closest('.sdd').removeClass('sdd');
//         } else {
//             console.log($(this).parent());
//             $(this).closest('tr.koala').addClass('sdd'); // Select the one clicked
//         }
//     });
// })

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

    document.getElementById("fname").onchange = function() {myFunction()};
    
    function myFunction() {
        var x = document.getElementById("fname");
        x.value = x.value.toUpperCase();
    }

function dataDump() {
    
}