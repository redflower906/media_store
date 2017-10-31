
var django = django || {};
django.formset = {};

django.formset.make_form = function ($formset, $form, params) {


    // Increase the number of total forms and sort the formset
    var $total_forms = $('#id_' + prefix + '-TOTAL_FORMS');
    $total_forms.val(parseInt($(form_element, $formset).length));
    django.formset.reprioritize_formset($formset)};
