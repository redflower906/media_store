from django import template
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
register = template.Library()

def table_header(context, headers):
    return {
        'headers': headers,
    }

register = template.Library()
register.inclusion_tag('store/table_header.html', takes_context=True)(table_header)

@register.filter()
def currency(amount):
    value = '$0.00'
    if (amount):
        value = locale.currency(amount, grouping=True)
    return value

@register.filter
def msgbootstrapconvert(tag):
    bootstrap_context_map = {
        'success': 'success',
        'error': 'danger'
    }
    return bootstrap_context_map[tag]


