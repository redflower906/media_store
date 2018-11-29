from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from dateutil import relativedelta
from datetime import datetime, date
from store.models import Order

class Command(BaseCommand):
    def handle_noargs(self, **options):
        today = date.today()
        orders = Order.objects.all()
        for order in orders:
            if order.date_recurring_stop:
                today_to_stop = (order.date_recurring_stop - today).days

                if today_to_stop == 21:
                    number = 'three'
                if today_to_stop == 7:
                    number = 'one'

                if (today_to_stop == 21) or (today_to_stop == 7):
                    domain = 'mediastore.int.janelia.org/order/edit/{0}'.format(order.id)
                    subject,from_email,to = 'Recurring Media Store Order #{0} Ending Soon!'.format(order.id), 'mediafacility@janelia.hhmi.org', order.requester.user_profile.email_address 
                    context = Context({
                        'id': order.id,
                        'domain': domain,
                        'number': number,
                    })
                    m_plain = render_to_string('three_weeks.txt', context.flatten())
                    m_html = render_to_string('three_weeks.html', context.flatten())
                    email =EmailMultiAlternatives(
                    subject,
                    m_plain,
                    from_email,
                    [to],
                    cc=[order.submitter.user_profile.email_address],)
                    email.attach_alternative(m_html, "text/html")
                    email.send()
        subject,from_email,to = 'cron job successful!', 'harrisons1@janelia.hhmi.org', 'harrisons1@janelia.hhmi.org'
        m_plain = render_to_string('cron_successful.txt', context.flatten())
        email =EmailMultiAlternatives(
        subject,
        m_plain,
        from_email,
        [to],)
        email.send()
        return