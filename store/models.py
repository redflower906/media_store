"""
All data models for Media Store
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import decimal
import datetime

# Create your models here.

class Service(models.Model):
	service_text = models.CharField(max_length=100)


class ServiceSubType(models.Model):
	servicesubtype_text = models.CharField(max_length=100)
	service = models.ForeignKey(Service,verbose_name="Service")
#	qty = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)


class Job(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(blank=False,null=False,default=True)
	service = models.ForeignKey(Service, blank=False,null=False)
	date_created = models.DateField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
#	job_class = models.CharField(max_length=30,blank=False)


"""
class WorkOrder(models.Model):
    bill_to = models.ManyToManyField('Department',through='WorkorderDepartmentRelationship', related_name='workorders', blank=False, null=True)
    job = models.ForeignKey(Job,blank=True,null=True)
    phase = models.ForeignKey(Phase,blank=True,null=True)
    submitter = models.ForeignKey(User,related_name='submitter')
    main_requestor = models.ForeignKey(User,related_name='main_requestor')
    department = models.ForeignKey(Department,blank=False,null=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=30,blank=False,null=False, default='Complete',
       choices=(
        ('Submitted','Submitted'),
        ('Assigned','Assigned'),
        ('In_Progress','In Progress'),
        ('Complete','Complete'),
        ('Canceled','Canceled'),
        ('Inquiry','Inquiry'),
       )
    )
    date_complete = models.DateField(blank=False)
    test_field = models.CharField(max_length=30,blank=True,null=True)
    job_manager_id = models.CharField(max_length=30,blank=True,null=True)
    date_promised = models.DateField(blank=True,null=True)
    date_revised = models.DateField(blank=True,null=True)
    date_submitted = models.DateField(blank=True,null=True)
    admin_code = models.CharField(max_length=30,blank=True)
    date_billed = models.DateField(blank=True,null=True)
    objects = WorkOrderManager()
    date_modified = models.DateTimeField(auto_now=True)
    # stores the id related to the reservation in resource scheduler.
    # this helps prevent the duplication of tickets and allows us to
    # easily link back to the other site.
    resource_scheduler_id = models.CharField(max_length=255, blank=True)

    def already_billed(self):
        if self.date_billed:
            return True
        return False

    def total(self):
        total = 0
        list = self.workorderline_set.all()
        for line in list:
            total += line.total()
        return total

    def performed_by(self):
        user = ''
        first_line = self.workorderline_set.first().performed_by

        if first_line:
            user = first_line.username

        return user

    def is_self_billing(self):
        if self.department in self.bill_to.all():
            return True
        return False

    def bill_to_dept_count(self):
        return self.workorderdepartmentrelationship_set.count()

    def reclass(self, new_data):
        original_id = self.id
        original_lines = self.workorderline_set.all()
        original_depts = self.workorderdepartmentrelationship_set.all()
        original_note = self.note

        # create a workorder to credit the original workorder departments.
        credit_wo = self
        credit_wo.pk = None
        credit_wo.date_complete = datetime.date.today()
        credit_wo.date_billed = None
        credit_wo.note = original_note + "\nReclass credit from workorder {0}".format(original_id)
        credit_wo.save()
        credit_id = credit_wo.id

        # restore the department relationships.
        for rel in original_depts:
            fields = WorkorderDepartmentRelationship._meta.get_all_field_names()
            new_rel = WorkorderDepartmentRelationship()
            # must ignore id or the original relationship will get overwritten
            ignored = ('workorder','id')
            for field in fields:
                if field in ignored:
                    continue
                setattr(new_rel, field, getattr(rel, field))

            new_rel.workorder_id = credit_wo.id
            new_rel.save()

        # create negative lines for each original line
        for line in original_lines:
            fields = WorkOrderLine._meta.get_all_field_names()
            new_line = WorkOrderLine()
            ignored = ('wo_id','id')
            for field in fields:
                if field in ignored:
                    continue
                setattr(new_line, field, getattr(line, field))
            new_line.wo_id = credit_wo
            new_line.cost = -new_line.cost
            new_line.save()

        # create a workorder to debit the new departments.
        debit_wo = self
        debit_wo.pk = None
        debit_wo.date_complete = datetime.date.today()
        debit_wo.date_billed = None
        debit_wo.note = original_note + "\nReclass debit from workorder {0}".format(original_id)
        debit_wo.save()
        debit_id = debit_wo.id

        # restore the lines for each original line
        for line in original_lines:
            new_line = line
            new_line.pk = None
            new_line.wo_id = debit_wo
            new_line.save()

        # create the new department relationships.
        for entry in new_data:
            if not entry['DELETE']:
                billing = WorkorderDepartmentRelationship(
                    workorder = debit_wo,
                    department_id = entry['new_dept'],
                    hhmi_project_id = entry['new_hhmi_project_id'],
                    percentage = entry['new_percentage']
                )
                billing.save()

        return(credit_id, debit_id)

    def __unicode__(self):
        return str(self.pk)

class WorkorderDepartmentRelationship(models.Model):
    workorder  = models.ForeignKey(WorkOrder, blank=False)
    department = models.ForeignKey(Department,blank=False)
    percentage = models.PositiveSmallIntegerField(default=100,blank=False)
    hhmi_project_id = models.CharField(max_length=255,blank=True,null=True)

    # some times we store the name of the person associated with the project id
    # this is no good for finace, so this function will strip it off it is present
    # and only return the 9 digit code.
    def short_hhmi_project_id(self):
        if self.hhmi_project_id:
            return self.hhmi_project_id.split(' ', 1)[0]
        else:
            return None

    def __unicode__(self):
        return str(self.pk)


class WorkOrderLine(models.Model):
    wo_id = models.ForeignKey(WorkOrder)
    description = models.TextField(blank=True)
    line_type = models.CharField(max_length=255)
    date_performed = models.DateField(blank=True, null=True)
    performed_by = models.ForeignKey(User,related_name='performed_by',blank=True,null=True)
    qty = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    unit = models.CharField(max_length=30,blank=True,null=True)
    cost = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    service = models.ForeignKey(Service,blank=True, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=30, null=True, choices = CATEGORY_CHOICES)
    def total(self):
        total = 0.00
        if self.cost and self.qty:
            total = round(decimal.Decimal(str(self.qty))*decimal.Decimal(str(self.cost)),2)
        return decimal.Decimal(total)

    def category_choices(self):
        return CATEGORY_CHOICES

    class Meta:
        verbose_name_plural = "work order lines"

    def __unicode__(self):
        return u'%s' % self.pk
        """




#	category = models.CharField(max_length=30,blank=True,null=True,choices = CATEGORY_CHOICES)
#note sure category choices should be the same but not sure if RM requires it to be the same?

# do we just copy this from Resource Matrix since we are trying to stay similar?