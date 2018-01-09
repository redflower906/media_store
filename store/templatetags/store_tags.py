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

@register.filter(name='addcss')
def addcss(field, css):
       return field.as_widget(attrs={"class":css})