from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from dateutil import relativedelta
from datetime import datetime, date
from store.models import Order


def recur_end_email():
    today = date.today()
    orders = Order.objects.all()
    for order in orders:
        if order.date_recurring_stop:
            today_to_stop = (order.date_recurring_stop - today).days
            print(today_to_stop)
            if today_to_stop == 21:
                print('second if worked') 
                domain = 'mediastore.int.janelia.org/order/edit/{0}'.format(order.id)
                subject,from_email,to = 'Order #{0} Submitted'.format(order.id), 'mediafacility@janelia.hhmi.org', order.requester.email
                context = Context({
                    'id': order.id,
                    'domain': domain,
                })
                m_plain = render_to_string('three_weeks.txt', context.flatten())
                m_html = render_to_string('three_weeks.html', context.flatten())
                email =EmailMultiAlternatives(
                subject,
                m_plain,
                from_email,
                [to],
                cc=[order.submitter.user_profile.email_address], #add mediafacility email here ~FIX~
                )
                email.attach_alternative(m_html, "text/html")
                email.send()
