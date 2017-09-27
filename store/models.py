"""
All data models for Media Store
"""

from django.db import models
#from django.contrib.admin.models import LogEntry
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import decimal
from datetime import datetime



# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(unique=True, max_length=6)
    account_code = models.IntegerField(null=True, blank=True)
    is_shared_resource = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

#   objects = ActiveDepartmentManager()
#   all_objects = models.Manager()

    def __unicode__(self):
        return self.number + " " + self.name
#	category = models.CharField(max_length=30,blank=True,null=True,choices = CATEGORY_CHOICES)
#note sure category choices should be the same but not sure if RM requires it to be the same?


    class Meta:
        ordering = ('number',)

"""class UserProfile(models.Model):
#   user = models.ForeignKey(User, related_name='user_profile')
#   department = models.ForeignKey(Department, blank=True, null=True)
#   alt_departments = models.ManyToManyField(Department, related_name='alt_departments', blank=True, null=True)
    hhmi_project_id = models.CharField(max_length=30, blank=True, null=True)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
#   manager = models.ForeignKey(User, related_name='user_manager', blank=True, null=True, on_delete=models.SET_NULL)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_janelia = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)

    skip_updates = models.BooleanField(default=False)


    is_privileged = models.BooleanField(default=False)


    offboard_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return str(self.user)

    def department_id_list(self):
        deparment_ids = [dept.id for dept in self.alt_departments.all()]
        deparment_ids.append(self.department_id)
        return deparment_ids

    def name(self):
        return self.last_name + ", " + self.first_name

    def manager_name(self):
        if self.manager:
            return ' '.join([self.manager.first_name, self.manager.last_name])
        return ''

    def has_job_privileges(self):
        return (self.user.is_superuser or
            (self.is_manager and self.department.number == '093098'))"""



class Vendor(models.Model):
    email_address = models.CharField(max_length=225, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

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
    notes = models.CharField(max_length=500, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    deposit = models.IntegerField(default=0, blank=True,null=True)
    minimum_amt = models.IntegerField(blank=True, null=True)
    part_num = models.CharField(max_length=20, blank=True, null=True)
    withdrawal = models.IntegerField(default=0, blank=True, null=True)
#    current_amt = deposit - withdrawal
    active = models.BooleanField(default=True, choices=BOOL_CHOICES)


    def __str__(self):
        return self.inventory_text


class Order(models.Model):
    #had to make null to migrate CHANGE LATER
#   submitter = models.ForeignKey(User, related_name='submitter')   #submitting order
#    requester = models.ForeignKey(User, related_name='requester')  #only use when billing other person
    department = models.ForeignKey(Department, blank=True, null=True)
    special_instructions = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(blank=True, null=True)
    date_submitted = models.DateField(blank=True, null=True)
    date_complete = models.DateField(blank=True, null=True)
    date_billed = models.DateField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    #had to set a default to migrate
    #make below an if statement if boolean is true and if boolean is false
    date_recurring_start = models.DateField(default=datetime.now, blank=True)
    date_recurring_stop = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=False, null=False, default='Complete',
        choices=(
            ('Submitted', 'Submitted'),
            ('In_Progress', 'In Progress'),
            ('Complete', 'Complete'),
            ('Canceled', 'Canceled'),
            )
    )
    
    def already_billed(self):
        if self.date_billed:
            return True
        return False
    def total(self):
        total = 0
    #not done with total
    def __unicode__(self):
        return 'Order for %s on %s (%s)' % (self.user, self.date_complete or self.date_submitted or self.date_created, self.status)
    def is_closed(self):
        return self.status.name == 'Complete'

class OrderLine(models.Model):
    order = models.ForeignKey(Order)
    description = models.TextField(blank=True)
    inventory = models.ForeignKey(Inventory, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=30, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def total(self):
        total = 0.00
        if self.cost and self.qty:
            total = round(decimal.Decimal(str(self.qty))*decimal.Decimal(str(self.cost)),2)
        return decimal.Decimal(total)
    class Meta:
        verbose_name_plural = 'order lines'
    def __unicode__(self):
        return u'%s' % self.pk
    

class Announcements(models.Model):
   text = models.TextField()
   show = models.BooleanField(default=False)

ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'

class SortHeaders:
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
