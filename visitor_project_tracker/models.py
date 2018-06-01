# -*- coding: utf-8 -*-

"""
TODO:

Future:
tie into FileMaker somehow? export for wiki?
reports

"""

import datetime
import random
import sys
import re
import base64,zlib,time

from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.files.base import ContentFile
from django.utils.encoding import smart_text, force_text
#We use templates to generate shipping forms for requests
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.db.models.signals import post_save
from django.contrib import messages


#----------- Main Tables -------------------------------------------------------

class User(models.Model):
    class Meta:
        db_table = 'auth_user'
    email = models.CharField("Email Address", max_length=255, blank=True)
    id = models.IntegerField(primary_key=True)


class TeamProject(models.Model):
    class Meta:
        #ordering = ('name',)
        db_table = 'tracker_teamproject'
        managed = False
    code = models.CharField("Project Code", max_length=20, blank=True)
    department_code = models.CharField("Department Number", max_length=20,
        blank=True, help_text="A Janelia department code such as 093060")
    comment = models.CharField(max_length=400, blank=True)

class OtherHost(models.Model):
    """Used for adding hosts that are not at Janelia"""
    class Meta:
        #ordering = ('name',)
        db_table = 'tracker_otherhost'
        managed = False

class VisitorProgramTitle(models.Model):
    class Meta:
        #ordering = ('name',)
        managed = False

class VisitingScientist(models.Model):
    """Stores all scientist information.  FYI: More than 1 scientist can be on a project
    and 1 scientist can have multiple projects. """
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=50, blank=True,
        choices=(
            ('HHMIINVESTIGATOR','HHMI Investigator'),
            ('HHMIEARLYCAREERSCIENTIST','HHMI Early Career Scientist'),
            ('PRINCIPALINVESTIGATOR','Principal Investigator'),
            ('POSTDOCTORALFELLOW','Postdoctoral Fellow'),
            ('GRADUATESTUDENT','Graduate Student'),
            ('UNDERGRADUATESTUDENT','Undergraduate Student'),
            ('OTHER','Other (specify)'),
        )
    )
    title_if_other = models.CharField(max_length=100, blank=True,
        help_text="Enter title here is it is not one of the choices")
    visitor_program_title = models.ForeignKey(VisitorProgramTitle, blank=True, null=True)
    appointment_start_date = models.DateField(blank=True, null=True)
    appointment_end_date = models.DateField(blank=True, null=True)
    contact_email = models.EmailField(blank=True,)
    contact_phone = models.CharField(max_length=50, blank=True,)
    institute = models.CharField("Institution", max_length=500, blank=True)
    address_1 = models.CharField(max_length=35, blank=True)
    address_2 = models.CharField(max_length=35, blank=True, 
        help_text="Suite Number, Mail Stop, Department")
    city_state_zip = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=20, choices=(('MALE','Male'),('FEMALE','Female')), blank=True)
    emergency_contact_name = models.CharField(max_length=500, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    emergency_contact_phone = models.CharField(max_length=100, blank=True)
    CV = models.FileField(blank=True, upload_to='uploads')
    notes = models.TextField(blank=True)
    class Meta:
        db_table = 'tracker_visitingscientist'
        managed = False
        ordering = ['last_name','first_name']

    def hhmi_designation(self):
        if self.visitor_program_title and self.visitor_program_title.name.upper().startswith('HHMI/JRC'):
            return 'HHMI'
        elif self.title == 'HHMIINVESTIGATOR':
            return 'HHMI'
        else:
            return 'NON-HHMI'

    def display_title(self):
        if self.title=='OTHER':
            return self.title_if_other
        else:
            return self.title

    def short_name(self):
        ret_str = self.first_name + ' ' + self.last_name
        ret_str = latin1_to_ascii(ret_str)
        return force_text(ret_str)

    def __unicode__(self):
        str_inst = ' (%s)' % self.institute if self.institute else ''
        ret_str = self.first_name + ' ' + self.last_name + str_inst
        #Django admin has a bug where it breaks when it tries to log a change 
        #and there's a non ascii character in the content.  As a workaround 
        #we replace any non-ascii characters with the closest ascii char we
        #can find and then convert it back to unicode.
        #If you upgrade Django you can try running without this. The umlaut is
        #a good test case
        ret_str = latin1_to_ascii(ret_str)
        return force_text(ret_str)

    def str_w_cv(self):
        """Conditionally hyperlink name is CV is available"""
        str_cv = (' <a href="%s">CV</a>' % self.CV.url) if self.CV else ''        
        if self.CV:
            return "<a href='%s'>%s</a>" % (self.CV.url, str(self))
        else:
            return str(self)


class Project(models.Model):
    """Stores a project or a renewal record.  Both information submitted and administrative
    info such as budget and codes."""

    def default_deadline():
        return datetime.date.today() + datetime.timedelta(days=7)


    #Admin
    code = models.CharField("Project Code", max_length=20, blank=True) #ideally this would be unique unless blank, but can't do it in django?
    host = models.ManyToManyField(User,
            blank=True,
            help_text="Which Janelia lab heads are hosting this project")
    team_host = models.ForeignKey(TeamProject,
            blank=True,
            null=True,
            verbose_name="Team Project Host",
        help_text="(Optional) Is a team project hosting this project?")
    other_host = models.ForeignKey(OtherHost, blank=True, null=True, verbose_name="Other Host",
        help_text="(Optional) If host is not a current Janelia employee use this.")
    department_code = models.CharField("Department Number", max_length=20, 
        blank=True, help_text="A Janelia department code such as 093060")
    programmatic = models.BooleanField(blank=True)
    status = models.CharField(max_length=20, default='AWAITINGREVIEW',
        choices=(
            ('AWAITINGREVIEW','Awaiting Review'),
            ('PENDING','Pending'),
            ('STARTED','Started'),
            ('COMPLETED','Completed'),
            ('REJECTED','Rejected'),
            ('WITHDRAWN','Withdrawn'),
        )
    )
    active = models.BooleanField(blank=True, default=True, help_text="Uncheck when this project is no longer active")
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    overview_benefits = models.TextField(blank=True)
    overview_costs = models.TextField(blank=True)
    deadline_operations_reviews = models.DateField(blank=True, null=True, 
        help_text="Default deadline to use for operations reviews",
        default=default_deadline)
    deadline_labhead_reviews = models.DateField(blank=True, null=True, 
        help_text="Default deadline to use for scientific reviews",
        default=default_deadline)
    seminar_location = models.CharField(max_length=100, blank=True)
    seminar_datetime = models.DateTimeField(blank=True, null=True)

    #Budget
    budget_personnel = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_shared_resources = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_supplies = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_travel = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_housing = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_IT = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_equipment_non_capital = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_other = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    budget_equipment_capital = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    #Resources
    resources_personnel = models.TextField(blank=True,)
    resources_lab_space = models.TextField(blank=True,)
    resources_shared_resources = models.TextField(blank=True,)
    resources_safety_animals = models.TextField(blank=True,)
    resources_lab_supplies = models.TextField(blank=True,)
    resources_travel = models.TextField(blank=True,)
    resources_housing = models.TextField(blank=True,)
    resources_IT = models.TextField("Resources IT", blank=True,)
    resources_equipment_non_capital = models.TextField(blank=True,)
    resources_equipment_capital = models.TextField(blank=True,)
    resources_other = models.TextField(blank=True,)
    resources_comments = models.TextField(blank=True,)

    publication_plan = models.TextField(blank=True,)

    #From submitted paper forms
    proposed_title = models.CharField(max_length=200)
    application_form = models.FileField("Submitted Application", blank=True, upload_to='uploads',
        help_text="Uploading an application form will prepopulate the fields below after saving (if they are empty.) "
        "If this is a renewal please set the 'Renewal of' field below BEFORE adding the application. "
        "(or make sure the prhase 'renew' is in the file name.)")
    scientist = models.ManyToManyField(VisitingScientist, related_name='projects')
    proposed_problem = models.TextField(blank=True,)
    proposed_solution = models.TextField(blank=True,)
    proposed_outcome = models.TextField(blank=True,)
    proposed_time_frame = models.TextField(blank=True,)
    proposed_collaboration = models.TextField(blank=True,)
    proposed_appropriateness = models.TextField(blank=True,)
    # -- for renewals    
    renewal_of = models.ForeignKey('self', blank=True, null=True)
    progress = models.TextField("Summary of progress", blank=True, help_text="for renewals")
    work_done_at_janelia = models.TextField("Description of work done at Janelia", blank=True, help_text="for renewals")
    work_done_at_vistitors_institution = models.TextField("Description of work done at the visitor's institution(s)", blank=True, help_text="for renewals")
    scope = models.TextField(blank=True, help_text="for renewals")

    class Meta:
        db_table = 'tracker_project'
        managed = False
        ordering = ['code','id',]

    def __unicode__(self):
        str_code = '(%s) - ' % self.code if self.code else ''
        ret_str = str_code + self.proposed_title
        ret_str = latin1_to_ascii(ret_str)
        return force_text(ret_str)

    def export_in_word_url(self):
        if self.id:
            url = '/projectdetail/%s/' % self.id
            return url
        else:
            return "?"
    def word_export(self):
        if self.id:
            return "<a href='%s'>Export to Word Document</a>" % (self.export_in_word_url(),)
        else:
            return "?"
    word_export.allow_tags = True
    word_export.short_description = "Printable Report"

    def scientists_w_cv(self):
        """Show all scientists on this project as a string"""
        return ', '.join([s.str_w_cv() for s in self.scientist.all()])

    def scientists(self):
        """Show all scientists on this project as a string"""
        return ', '.join([str(s) for s in self.scientist.all()])

    @staticmethod
    def format_hosts(all_hosts, other_host, team_host):
        hosts = [str(s) for s in all_hosts]
        if other_host:
            hosts.append(other_host)
        str_hosts = ', '.join([str(s) for s in hosts])
        if team_host:
            result = "Team Host: %s" % team_host.name
            if str_hosts:
                result += " / Other Hosts: %s" % str_hosts
        else:
            result = str_hosts
        return result

    def hosts(self):
        """Show all hosts on this project as a string"""
        return Project.format_hosts(self.host.all(), self.other_host, self.team_host)

    def reviews(self):
        """Show many reviews have been completed vs pending"""
        completed = self.review_set.filter(status='COMPLETED').count()
        pending = self.review_set.filter(status='AWAITINGREVIEW').count()
        return "%s out of %s completed" % (completed, completed + pending) 

    def subtotal_excl_personnel(self):
        return sum([
            #self.budget_personnel or 0,
            self.budget_shared_resources or 0,
            self.budget_supplies or 0,
            self.budget_travel or 0,
            self.budget_housing or 0,
            self.budget_IT or 0,
            self.budget_equipment_non_capital or 0,
            self.budget_other or 0,
        ])
    def subtotal_excl_personnel_str(self):
        return format(self.subtotal_excl_personnel(),'2c')
    subtotal_excl_personnel_str.short_description = 'Subtotal (Excluding Personnel)'
    def total_excl_personnel(self): 
        return self.subtotal_excl_personnel() + (self.budget_equipment_capital or 0)
    def total_excl_personnel_str(self):
        return format(self.total_excl_personnel(),'2c')
    total_excl_personnel_str.short_description = 'Total (Excluding Personnel)'
    def subtotal(self):
        return sum([
            self.budget_personnel or 0,
            self.budget_shared_resources or 0,
            self.budget_supplies or 0,
            self.budget_travel or 0,
            self.budget_housing or 0,
            self.budget_IT or 0,
            self.budget_equipment_non_capital or 0,
            self.budget_other or 0,
        ])
    def subtotal_str(self):
        return format(self.subtotal(),'2c')
    subtotal_str.short_description = 'Subtotal (Including Personnel)'
    def total(self):
        return self.subtotal() + (self.budget_equipment_capital or 0)
    def total_str(self):
        return format(self.total(),'2c')
    total_str.short_description = 'Total (Including Personnel)'
