"""
All data models for Media Store
"""

from django.db import models
# from django.db.models import prefetch_related
#from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.forms import ModelForm
from django.template import Context
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_auth_ldap.backend import LDAPBackend
import decimal
from datetime import datetime, date
from dateutil import relativedelta


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    number = models.CharField(unique=True, max_length=10)
    account_code = models.IntegerField(null=True, blank=True)
    is_shared_resource = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    #objects = ActiveDepartmentManager() #~FIX~ RM has this but I don't think MS needs it 
    # all_objects = models.Manager()

    def __str__(self):
        return self.number + " " + self.department_name

    class Meta:
        ordering = ('number',)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    department = models.ForeignKey(Department, blank=True, null=True)
#   alt_departments = models.ManyToManyField(Department, related_name='alt_departments', blank=True, null=True) #Jody said we probably don't need ~FIX~
    hhmi_project_id = models.CharField(max_length=30, blank=True, null=True) #needed for visitor projects
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
#   manager = models.ForeignKey(User, related_name='user_manager', blank=True, null=True, on_delete=models.SET_NULL) ~FIX~
    is_manager = models.BooleanField(default=False) #do we need? ~FIX~
    is_active = models.BooleanField(default=False)
    is_janelia = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)
    is_privileged = models.BooleanField(default=False)

# this is used to prevent updates from workday overriding the values that have
# been altered in ResourceMatrix. We need to do this for people who are in the
# wrong department for billing. eg: Pat Rivlin is in "093417 Fly Brain Imaging EM"
# but she should be billed to "093093 Electron Microscopy". This could be dangerous
# and we should probably limit which fields are ignored to department.
    skip_updates = models.BooleanField(default=False)
    offboard_date = models.DateField(blank=True, null=True)

    def name(self):
        return self.last_name + ", " + self.first_name


    def __str__(self):
        return str(self.user)

    def department_id_list(self):
        deparment_ids = [dept.id for dept in self.alt_departments.all()]
        deparment_ids.append(self.department_id)
        return deparment_ids

    def manager_name(self):
        if self.manager:
            return ' '.join([self.manager.first_name, self.manager.last_name])
        return ''

    def has_job_privileges(self):
        return (self.user.is_superuser or
            (self.is_manager and self.department.number == '093098'))

class UserFullName(User):
    class Meta:
        proxy = True
    
    def __str__(self):
        return self.get_full_name()

class Vendor(models.Model):
    email_address = models.CharField(max_length=225, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    notes_ven = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.company

MEDIA_CHOICES = (
    #('','---------'),
    ('Agar','Agar'),
    ('Antibiotics','Antibiotics'),
    ('Cornmeal Food','Fly Food - Cornmeal'),
    ('Dextrose Food','Fly Food - Dextrose'),
    ('Power Food','Fly Food - Power'),
    ('Wurzburg Food','Fly Food - Wurzburg'),
    ('Liquid Media','Liquid Media'),
    ('Miscellaneous','Miscellaneous'),
    ('Solutions & Buffers','Solutions & Buffers'),
    ('Sylgard','Sylgard'),
)

class Inventory(models.Model):

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    class Meta:
        verbose_name_plural = 'Inventory'

    inventory_text = models.CharField(max_length=75)
    product = models.CharField(max_length=40, blank=True, null=True)
    media_type = models.CharField(max_length=30, blank=True, null=True, choices=MEDIA_CHOICES)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    container = models.CharField(max_length=50, blank=True, null=True)
    volume = models.CharField(max_length=15, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    notes_inv = models.CharField(max_length=500, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, blank=True, null=True)
    date_modified = models.DateField(auto_now_add=True)
    deposit = models.IntegerField(default=0, blank=True,null=True)
    minimum_amt = models.IntegerField(blank=True, null=True)
    withdrawal = models.IntegerField(default=0, blank=True, null=True)
#    current_amt = deposit - withdrawal
    active = models.BooleanField(default=True, choices=BOOL_CHOICES)


    def __unicode__(self):
        return self.inventory_text

    def __str__(self):
        return self.inventory_text

    def list_media_type(self):
        return self.media_type

class OrderManager(models.Manager):
    def preferred_order(self, *args, **kwargs):
        """Sort patterns by preferred order of Y then -- then N"""
        orders = self.get_queryset().filter(*args, **kwargs)
        orders = orders.annotate( custom_order=
            models.Case( 
                models.When(status='Submitted', then=models.Value(0)),
                models.When(status='In Progress', then=models.Value(1)),
                models.When(status='Complete', then=models.Value(2)),
                models.When(status='Billed', then=models.Value(3)),
                models.When(status='Problem', then=models.Value(4)),
                models.When(status='Canceled', then=models.Value(5)),
                models.When(status='Auto', then=models.Value(6)),
                default=models.Value(7),
                output_field=models.IntegerField(), )
            ).order_by('custom_order', 'date_recurring_stop')
        return orders

class Order(models.Model):
    #model field choices, extracted for easy reference
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
        ('Billed', 'Billed'),
        ('Problem', 'Problem'),
        ('Canceled', 'Canceled'),
        ('Auto', 'Auto'),
    )
    LOCATION_CHOICES =(
        ('2W.225', '2W.225 (4C)'),
        ('2W.227', '2W.227 (4C)'),
        ('2W.263', '2W.263 (4C)'),
        ('2W.265', '2W.265 (4C)'),
        ('2C.225', '2C.225 (4C)'),
        ('2C.227', '2C.227 (4C)'),
        ('2C.267', '2C.267 (4C)'),
        ('2C.277', '2C.277 (4C)'),
        ('2C ambient', 'Near 2C.243 (21C)'),
        ('2E.231', '2E.231 (4C)'),
        ('2E.233', '2E.233 (18C)'),
        ('2E.267', '2E.267 (4C)'),
        ('3W.228', '3W.228 (4C)'),
        ('3W.266', '3W.266 (4C)'),
        ('3C.226', '3C.226 (4C)'),
        ('3C.229', '3C.229 (18C)'),
        ('3C.265', '3C.265 (4C)'),
        ('3C.267', '3C.267 (4C)'),
        ('3C ambient', 'Near 3C.289 (21C)'),
        ('3E.265', '3E.265 (18C)'),
        ('3E.267', '3E.267 (4C)'),
    )
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.UserFullName, filename)

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    #had to make null to migrate CHANGE LATER
    notes_order = models.CharField(max_length=500, blank=True, null=True)
    submitter = models.ForeignKey(User, related_name='submitter', null=True)   #submitting order
    requester = models.ForeignKey(User, related_name='requester', null=True)  #only use when billing other person
    department = models.ForeignKey(Department, blank=False, null=False)
    special_instructions = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True, blank=True, null=True)
    date_submitted = models.DateField(blank=True, null=True) #is this the same as date_created? ~FIX~
    date_complete = models.DateField(blank=True, null=True)
    date_billed = models.DateField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    #had to set a default to migrate
    #make below an if statement if boolean is true and if boolean is false
    date_recurring_start = models.DateField(default=datetime.now, blank=True, null=True)
    date_recurring_stop = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=False, null=False,
        choices=LOCATION_CHOICES
    )
    status = models.CharField(max_length=30, blank=False, null=False, default='Submitted',
        choices=STATUS_CHOICES
    )
    doc = models.FileField(upload_to='/documents', null=True, blank=True)
    # doc = models.FileField(upload_to='/groups/sciserv/home/coffmans', null=True, blank=True)
    days_since_bill = models.IntegerField(blank=True, null=True)
    objects = OrderManager()

    def already_billed(self):
        if self.date_billed:
            return True
        return False

    def order_total(self):
        total = 0
        list = self.orderline_set.all()
        for line in list:
            total += line.total()
        return total

    def __unicode__(self):
        return 'Order for %s on %s (%s)' % (self.user, self.date_complete or self.date_submitted or self.date_created, self.status)

    def is_closed(self):
        return self.status.name == 'Complete'
        ##DO WE NEED THIS?? ~FIX~

class OrderLine(models.Model):
    order = models.ForeignKey(Order, blank=False, null=False)
    # description = models.TextField(blank=True) #Where is this being used??~FIX~
    inventory = models.ForeignKey(Inventory, blank=False, null=False)
    qty = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    # unit = models.CharField(max_length=30, blank=True,
    #                         null=True)  # DO WE NEED THIS?? this was considered container but we don't need that within the orderline
    # shouldn't this be the same as Inventory cost? do we need it? 
    line_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)

    def total(self):
        total = 0.00
        if self.inventory.cost and self.qty:
            total = round(decimal.Decimal(str(self.qty))*decimal.Decimal(str(self.inventory.cost)),2)
        return decimal.Decimal(total)

    class Meta:
        verbose_name_plural = 'order lines'

    def __unicode__(self):
        return u'%s' % self.pk

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        try:
            self.inventory
        except Inventory.DoesNotExist:
            raise ValidationError(
                {'inventory': ('Please select an inventory item.')})
        if self.total() <= decimal.Decimal(0):
            raise ValidationError('Order line must have quantity and cost > 0')
    

class Announcements(models.Model):
   text = models.TextField()
   show = models.BooleanField(default=False)

ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'

class SortHeaders(models.Model):
    """
    Handles generation of an argument for the Django ORM's
    ``order_by`` method and generation of table headers which reflect
    the currently selected sort, based on defined table headers with
    matching sort criteria.

    Based in part on the Django Admin application's ``ChangeList``
    functionality.
    """
    def __init__(self, request, headers, default_order_field=None,
            default_order_type='asc', additional_params=None):
        """
        request
            The request currently being processed - the current sort
            order field and type are determined based on GET
            parameters.

        headers
            A list of two-tuples of header text and matching ordering
            criteria for use with the Django ORM's ``order_by``
            method. A criterion of ``None`` indicates that a header
            is not sortable.

        default_order_field
            The index of the header definition to be used for default
            ordering and when an invalid or non-sortable header is
            specified in GET parameters. If not specified, the index
            of the first sortable header will be used.

        default_order_type
            The default type of ordering used - must be one of
            ``'asc`` or ``'desc'``.

        additional_params:
            Query parameters which should always appear in sort links,
            specified as a dictionary mapping parameter names to
            values. For example, this might contain the current page
            number if you're sorting a paginated list of items.
        """
        if default_order_field is None:
            for i, (header, query_lookup) in enumerate(headers):
                if query_lookup is not None:
                    default_order_field = i
                    break
        if default_order_field is None:
            raise AttributeError('No default_order_field was specified and none of the header definitions given were sortable.')
        if default_order_type not in ('asc', 'desc'):
            raise AttributeError('If given, default_order_type must be one of \'asc\' or \'desc\'.')
        if additional_params is None: additional_params = {}

        self.header_defs = headers
        self.additional_params = additional_params
        self.order_field, self.order_type = default_order_field, default_order_type

        # Determine order field and order type for the current request
        params = dict(request.GET.items())
        if ORDER_VAR in params:
            try:
                new_order_field = int(params[ORDER_VAR])
                if headers[new_order_field][1] is not None:
                    self.order_field = new_order_field
            except (IndexError, ValueError):
                pass # Use the default
        if ORDER_TYPE_VAR in params and params[ORDER_TYPE_VAR] in ('asc', 'desc'):
            self.order_type = params[ORDER_TYPE_VAR]

    def headers(self):
        """
        Generates dicts containing header and sort link details for
        all defined headers.
        """
        for i, (header, order_criterion) in enumerate(self.header_defs):
            th_classes = []
            new_order_type = 'asc'
            if i == self.order_field:
                th_classes.append('sorted %sending' % self.order_type)
                new_order_type = {'asc': 'desc', 'desc': 'asc'}[self.order_type]
            yield {
                'text': header,
                'sortable': order_criterion is not None,
                'url': self.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}),
                'class_attr': (th_classes and '%s' % ' '.join(th_classes) or 'unsorted'),
            }

    def get_query_string(self, params):
        """
        Creates a query string from the given dictionary of
        parameters, including any additonal parameters which should
        always be present.
        """
        params.update(self.additional_params)
        return '?%s' % '&amp;'.join(['%s=%s' % (param, value) \
                                     for param, value in params.items()])

    def get_order_by(self):
        """
        Creates an ordering criterion based on the current order
        field and order type, for use with the Django ORM's
        ``order_by`` method.
        """
        return '%s%s' % (
            self.order_type == 'desc' and '-' or '',
            self.header_defs[self.order_field][1],
        )

@receiver(pre_save, sender=Order)
def status_email(sender, instance, *args, **kwargs):
    if instance.status == 'Complete':
        context = Context({
            'id': instance.id,
            'location': instance.location,
        })        
        m_plain = render_to_string('complete_email.txt', context.flatten())
        m_html = render_to_string('complete_email.html', context.flatten())

        send_mail(
            'Order #{0} Complete'.format(instance.id),
            m_plain,
            'mediafacility@janelia.hhmi.org',
            [instance.submitter.user_profile.email_address], #change email to requester after testing ~FIX~
            fail_silently=False,
            html_message=m_html,
        )

        if instance.is_recurring == True:
            order = Order.objects.get(pk=instance.id)
            ol = Order.prefetch_related('orderline_set').get(pk=instance.id)
            order.id = None
            order.pk = None
            order.save()
            order.orderline.set(ol)
        # messages.success(request, 'Order #{0} has been completed'.format(instance.id)) can't get request within a signal. find something better ~FIX~

    instance.date_complete = date.today()

    if instance.status == 'Billed':
        today = date.today()
        nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()
        lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)

        if today >= nextbill:
            nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=1)
            lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()

        instance.date_billed = today
        instance.days_since_bill = (today-lastbill).days
    ##elif instance.status == 'Canceled':
        ##DO WE NEED TO SEND AN EMAIL FOR CANCELED? PROBLEM? WOULD THESE EMAILS BE SENT BEFORE? ~FIX~
