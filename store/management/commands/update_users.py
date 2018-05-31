
"""
Make sure everyone in LDAP is included in the users table.

Call this with manage.py e.g.,
python manage.py update_users

The basic strategy here is to always have all employees at Janelia sitting in the
users table (inactivated).  Then Staff can go in and activate them, and
assign groups.  Active staff users can then log in with ldap.
"""

import sys
import uuid
import re
import json
from datetime import datetime

import requests
import ftfy
import ldap

from dateutil import parser
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.termcolors import colorize
from django.db.models import Q

from store.models import UserProfile, Department
from visitor_project_tracker.models import VisitingScientist


VERBOSITY = 0


THIRTY_DAYS_AGO = timezone.now() -  relativedelta(days=+30)

def get_all_users():         
     """Given an ldap connection, return all users.  Each user is a dictionary                                             
     with the following keys: 
     ['telephoneNumber', 'departmentNumber', 'loginShell', 'cn', 'uid', 'title',                                           
     'objectClass', 'uidNumber', 'description', 'jpegPhoto', 'roomNumber', 'gidNumber', 
     'gecos', 'sn', 'homeDirectory', 'mail', 'givenName', 'displayName', 'employeeNumber']                                 
     """
     ld_conn = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
     ld_conn.simple_bind_s()  
     basedn = "ou=people,dc=hhmi,dc=org"                                                                                   
     ldap_filter = "(|(uid=*))"
     results = ld_conn.search_s(basedn, ldap.SCOPE_SUBTREE, ldap_filter)
     #dn is a string like: 'cn=pinerog,ou=People,dc=janelia,dc=org'
     retlist = [entry for _, entry in results]
     ld_conn.unbind_s()       
     retlist.sort(key=lambda x: x['uid'])
     return retlist

def message(message, mtype):
    colors = {
        'error': 'red',
        'warning': 'yellow',
        'success': 'green',
        'info': 'blue',
    }

    color = colors[mtype]

    if mtype == 'error' or VERBOSITY >= 2:
        sys.stderr.write(colorize(message,fg=color))
    return

def user_debug(user_profile):
    """ log available user info
    user_profile: TimeMatrix.UserProfile object

    Needed for debugging recurring error notifications, which are quite common
    """
    user = user_profile.user
    debug_str = '\tDebug info: \n'
    debug_str += '\t User active: {0}, User_profile active:{1}'.format(user_profile.user.is_active, user_profile.is_active)
    if(user_profile.is_visitor):
        #try to print out project status, start_date, end_date, and department
        try:
            visitor = VisitingScientist.objects.using('vstar').get(
                (Q(last_name=user.last_name) & Q(first_name=user.first_name)) | Q(contact_email= user.email)
            )
            projects = visitor.projects.filter(Q(active=True) | (Q(date_end__gte=THIRTY_DAYS_AGO) & ~Q(status='AWAITINGREVIEW'))).order_by('date_end').reverse()
            #Q: print out all projects in this list?
            proj = projects[0]
            debug_str += "\tVSTAR project data: active: {0}, status: {1}, project date range: ({2}, {3}), department: {4}\n".format(
                proj.active, proj.status, proj.date_start, proj.date_end, proj.department_code)
        except:
            debug_str += "Unable to find visitor information in vstar\n"

    if(user_profile.employee_id):
        try:
            url = 'http://services.hhmi.org/IT/WD-hcm/wdworkerdetails/' + str(user_profile.employee_id)
            res = requests.get(url)
            workday_data = json.loads(res.content)[0]

            debug_str += '\tWORKDAY data: ' + str(workday_data) + '\n\n'
        except:
            debug_str += 'Error fetching workday data\n'

    message(debug_str, 'error')

#creates a lookup based on email address.
def create_ldap_lookup():
    lookup = {}
    users_list = get_all_users()

    for user in users_list:

        # if we have an employeed id that is a good lookup
        if 'employeeNumber' in user:
            lookup[user['employeeNumber'][0]] = user

        # email address can be used but employee id is better
        if 'mail' in user:
            lookup[user['mail'][0]] = user

        # can use firstname_lastname_department as that should be unique
        if 'givenName' in user and 'sn' in user and 'departmentNumber' in user:
            lookup[user['givenName'][0].decode('utf-8') + '_' + user['sn'][0].decode('utf-8') + '_' + user['departmentNumber'][0].decode('utf-8')] = user

        # can use firstname_lastname as a last_resort
        if 'givenName' in user and 'sn' in user:
            lookup[user['givenName'][0].decode('utf-8') + '_' + user['sn'][0].decode('utf-8')] = user

    return lookup


LDAP_USERS = create_ldap_lookup()



def gen_pw():
    """Users can't be edited in the admin if password is empty so set a dummy one here
    It's safe because users are inactivated by default, and those that aren't default to
    their ldap password."""
    return uuid.uuid1()

def get_active_employees(emp_id=None):
    # use the requests library to fetch the json data from the workday API.
    url = 'http://services.hhmi.org/IT/WD-hcm/wdworkerdetails?includeTeams=false'
    if emp_id:
        url += str(emp_id)

    res = requests.get(url)
    type(res)
    employees = json.loads(res.content)
    #filter out employees that have termination dates previous to 30 days ago
    def should_be_active(emp):
        if not emp['TERMINATIONDATE']:
            return True
        term_date = datetime.strptime(emp['TERMINATIONDATE'], '%m/%d/%Y').replace(tzinfo=THIRTY_DAYS_AGO.tzinfo)
        return term_date.date() >= THIRTY_DAYS_AGO.date()

    return filter(should_be_active, employees)

def determine_username(emp):
    email = emp['EMAILADDRESS']

    uname = email.lower()[:30]

    # if janelia email address
    if re.search('janelia.hhmi.org$', email):
        # try to find the matching ldap account first by employee id
        if emp['EMPLOYEEID'] in LDAP_USERS:
            # if found try to get username
            ldap_account = LDAP_USERS[emp['EMPLOYEEID']]
            return ldap_account['uid'][0]
        # then by email address
        if emp['EMAILADDRESS'] in LDAP_USERS:
            ldap_account = LDAP_USERS[emp['EMAILADDRESS']]
            return ldap_account['uid'][0]

        emp_name = emp['FIRSTNAME'] + '_' + emp['LASTNAME']
        emp_name_dept = emp_name + '_' + emp['COSTCENTER']
        # then by name_department
        if emp_name_dept in LDAP_USERS:
            ldap_account = LDAP_USERS[emp_name_dept]
            return ldap_account['uid'][0]
        #then by name
        if emp_name in LDAP_USERS:
            ldap_account = LDAP_USERS[emp_name]
            return ldap_account['uid'][0]

        message("Couldn't find LDAP account for {FIRSTNAME} {LASTNAME} ({EMPLOYEEID})\n".format(**emp), 'warning')

    elif re.search('hhmi.org$', email):
        # try to find the matching ldap account first by employee id
        if emp['EMPLOYEEID'] in LDAP_USERS:
            # if found try to get username
            ldap_account = LDAP_USERS[emp['EMPLOYEEID']]
            return ldap_account['uid'][0]
        # then by email address
        if emp['EMAILADDRESS'] in LDAP_USERS:
            ldap_account = LDAP_USERS[emp['EMAILADDRESS']]
            return ldap_account['uid'][0]

        emp_name = emp['FIRSTNAME'] + '_' + emp['LASTNAME']
        emp_name_dept = emp_name + '_' + emp['COSTCENTER']
        # then by name_department
        if emp_name_dept in LDAP_USERS:
            ldap_account = LDAP_USERS[emp_name_dept]
            return ldap_account['uid'][0]
        # Don't bother trying just a name as there are too many people with the
        # same name. eg: Jose Rodriguez

    # cant use part before @ of email address because lots of people are "unknown@hhmi.org"
    # add first letter of first name to end of last name and lowercase.
    if not re.search('\w+', uname):
        uname = emp['LASTNAME'] + emp['FIRSTNAME'][:1] + emp['EMPLOYEEID']
        uname = re.sub("[^a-zA-Z0-9]","", uname)
    return uname.lower()[:30]

def get_manager(manager_id):
    try:
        manager_profile = UserProfile.objects.get(employee_id=manager_id)
        manager = manager_profile.user
    except:
        manager = None
    return manager

def get_department(deptid):
    try:
        dept = Department.all_objects.get(number=deptid)
    except:
        dept = Department()
        dept.number = deptid
        dept.save()
        message("Created department with id {0}\n".format(deptid),'warning')

    #make sure we are billing the correct department for Gerry
    if dept.number == 'CC51050':
        try:
            dept = Department.all_objects.get(number='CC50040')
        except:
            dept = Department()
            dept.number = 'CC50040'
            dept.save()
            message("Created department with id {0}\n".format(deptid),'warning')

    return dept



@transaction.atomic
def add_employee(emp, **kwargs):
    #fields available in the emp dict:
    # 'WORKERTYPE', 'LEGACYDEPTID', 'EMPLOYEEID', 'FIRSTNAME', 'LASTNAME', 'MGRLASTNAME', 'EMAILADDRESS', 'COSTCENTER', 'MGRFIRSTNAME', 'MGRID'
    is_manager = kwargs.get('manager', False)
    profile = None
    user    = None

    try:
        profile = UserProfile.objects.get(employee_id = emp['EMPLOYEEID'])
        user = profile.user
        message("Found employee with id {EMPLOYEEID}\n".format(**emp),'success')
    except:
        message("Couldn't find user profile with id: {EMPLOYEEID}\n".format(**emp),'warning')

    if not profile:
        try:
            user = User.objects.get(email=emp['EMAILADDRESS'])
            message("Found employee with email {EMAILADDRESS}\n".format(**emp),'success')
        except:
            message("Couldn't find user with email: {EMAILADDRESS}\n".format(**emp),'warning')

        if user:
            try:
                profile = user.user_profile.all()[0]
            except:
                profile = UserProfile()

    if not user and not profile:
        message("Creating a new user account for {0}, {1}\n".format(emp['PREFERREDFIRSTNAME'].encode('utf-8'), emp['PREFERREDLASTNAME'].encode('utf-8')), 'warning')
        user = User()
        profile = UserProfile()

    # update user details
    user.first_name = emp['PREFERREDFIRSTNAME'].encode('utf-8')
    user.last_name  = emp['PREFERREDLASTNAME'].encode('utf-8')
    user.email      = emp['EMAILADDRESS']
    user.username   = determine_username(emp)
    user.set_password(gen_pw())

    # determine if the user should still be active
    if emp['ACTIVEFLAG'] == 'Y':
        user.is_active  = True
    else:
        user.is_active  = False

    try:
        user.save()
        message("Updated user {0} {1} ({2})\n".format(user.first_name, user.last_name, emp['EMPLOYEEID']), 'success')
    except IntegrityError as e:
        message("Couldn't save user {0} {1} ({2}): {3} \n".format(user.first_name, user.last_name, emp['EMPLOYEEID'], e), 'error')
        return



    # update profile details
    profile.user          = user
    profile.email_address = user.email
    profile.employee_id   = emp['EMPLOYEEID']
    #profile.is_manager    = is_manager

    # we don't want to update these details if the skip_update flag has been
    # set for this employee.
    if not profile.skip_updates:
        profile.department    = get_department(emp['COSTCENTER'])
        #profile.manager       = get_manager(emp['MGRID'])
        profile.first_name    = user.first_name
        profile.last_name     = user.last_name
    else:
        message("Skipping profile updates for {0} {1}, skip_updates flag set on user profile.\n".format(user.first_name, user.last_name), 'warning')

    if is_manager:
        profile.is_privileged = True


    if emp['ACTIVEFLAG'] == 'Y':
        profile.is_active = True
    else:
        profile.is_active = False
        if emp['TERMINATIONDATE'] is not None:
            profile.offboard_date = parser.parse(emp['TERMINATIONDATE'])
        else:
            profile.offboard_date = None

    if emp['DEPARTMENTCITY'] == 'Ashburn':
        profile.is_janelia = True

    try:
        profile.save()
    except IntegrityError as e:
        message("Couldn't save user profile for {0} {1}: {2} \n".format(user.first_name, user.last_name, e), 'error')

    return

def get_visitor_billing_department(project):
    hosts = project.host.all()
    if hosts:
        # use the first host in the list.
        host = hosts[0]
        try:
            host_profile = UserProfile.objects.get(email_address=host.email)
            return host_profile.department.number, project.code
        except:
            message("Unable to locate host profile based on email address ({0}) from vstar\n".format(host.email), 'error')

    elif project.team_host:
        # then team_host
        return project.team_host.department_code, project.team_host.code.strip()

    message("Couldn't find a department for project {0}. VStar is missing a host or team host for this project.\n".format(project.id), 'error')
    return None, project.code

def get_visitor_details(emp):
    message("Looking up visitor {0.first_name} {0.last_name} in vstar\n".format(emp), 'info')
    department_code = None
    project_code = None
    # here is where we have the crazy logic to figure out who is going to get billed.
    # grab their first active project
    projects = emp.projects.filter(Q(active=True) | (Q(date_end__gte=THIRTY_DAYS_AGO) & ~Q(status='AWAITINGREVIEW'))).order_by('date_end').reverse()

    project = projects[0]
    # use that one to set the department code
    department_code = project.department_code

    # inactive projects have their department codes wiped in vstar, so only show message
    # for active projects. The department code will be set below for inactive projects
    if not department_code and project.active:
        message("No department code for {0.first_name} {0.last_name} in vstar\n".format(emp), 'error')

    # if there is more than one warn that we are going to use the one that expires last
    if not len(projects) == 1:
        message("There were more than one active projects for {0.first_name} {0.last_name} in vstar. Using the one with the furthest end date\n".format(emp), 'warning')

    project_code = project.code.strip()
    # if it is JVS000100 then grab the host lab and bill them by changing the department
    if project_code == 'JVS000100':
        department_code, project_code = get_visitor_billing_department(project)
    else:
        #  if project expired > 30 days ago get host lab and bill them
        if not project.active:
            if project.date_end > THIRTY_DAYS_AGO.date():
                department_code, project_code = get_visitor_billing_department(project)
    dept = None

    try:
        dept = Department.objects.get(legacy_number=department_code)
    except:
        try:
            dept = Department.objects.get(number=department_code)
        except:
            message("Can't find department code {1} in resourcematrix for user {0.first_name} {0.last_name} in vstar\n".format(emp, department_code), 'error')
    return dept, project_code

def add_visitor(emp, in_workday):
    # always ensure strings are always utf-8 encoded.
    emp.first_name = emp.first_name.encode('utf-8')
    emp.last_name = emp.last_name.encode('utf-8')

    dept, project = get_visitor_details(emp)
    profile = None
    user = None

    try:
        # check if we have an active user
        user = User.objects.get(first_name=emp.first_name, last_name=emp.last_name, is_active=True)
        user.first_name = user.first_name.encode('utf-8')
        user.last_name = user.last_name.encode('utf-8')
    except:
        try:
            # check if we have an inactive user
            user = User.objects.get(first_name=emp.first_name, last_name=emp.last_name)
            user.first_name = user.first_name.encode('utf-8')
            user.last_name = user.last_name.encode('utf-8')

            if user:
                # just throw a warning that the user is inactive and carry on
                message(u"Updating inactive visitor {0} {1}\n".format(user.first_name.decode('utf-8'), user.last_name.decode('utf-8')), 'warning')
        except:
            try:
                if emp.contact_email:
                    user = User.objects.get(email=emp.contact_email, is_active=True)
                else:
                    raise Exception('email was blank')
            except:
                username = emp.contact_email.lower()[:30]
                if not re.search('\w+', username):
                    username = "{0.last_name}_{0.first_name}".format(emp)
                    username.lower()[:30]

                user = User(
                    first_name = emp.first_name,
                    last_name  = emp.last_name,
                    username   = username,
                    email      = emp.contact_email
                )
                user.set_password(gen_pw())

    try:
        user.save()
        try:
            first_name = user.first_name
            if isinstance(first_name, str):
                first_name = ftfy.guess_bytes(first_name)[0]
            first_name = ftfy.fix_text(first_name)

            last_name = user.last_name
            if isinstance(last_name, str):
                last_name = ftfy.guess_bytes(last_name)[0]
            last_name = ftfy.fix_text(last_name)

            message(u"Updated visitor {0} {1}\n".format(first_name, last_name), 'success')
        except UnicodeDecodeError as e:
            message(u"Encountered error printing username for user {0}\n".format(user.id), 'error')
    except IntegrityError as e:
        message(u"Couldn't save visitor user {0} {1}: {2} \n".format(user.first_name, user.last_name, e), 'error')
        return

    # now we have a user object set up the profile
    profile = user.user_profile.first()

    # if they have an employeeid, make sure they are in the pool of users from workday that
    # are active or were terminated in the last 30 days
    if profile and profile.employee_id and profile.employee_id not in in_workday.keys():
        return

    # couldn't find a profile, so create one.
    elif not profile:
        profile = UserProfile(
             user = user,
             email_address = user.email,
             is_manager = False
        )

    if not profile.skip_updates:
        profile.department      = dept
        profile.hhmi_project_id = project
        profile.first_name      = user.first_name
        profile.last_name       = user.last_name
        profile.is_visitor      = True
        profile.is_active       = True
    else:
        message(u"Skipping Visitor updates for {0} {1}, skip_updates flag set on user profile.\n".format(user.first_name.decode('utf-8'), user.last_name.decode('utf-8')), 'warning')

    try:
        profile.save()
    except IntegrityError as e:
        message(u"Couldn't save visitor user profile for {0} {1}: {2} \n".format(user.first_name.decode('utf-8'), user.last_name.decode('utf-8'), e), 'error')

    return

# def cleanup_missing_user_profiles():
#     # get all the user objects.
#     users = User.objects.all().prefetch_related('user_profile')
#     # loop over them and figure out which ones don't have a matching profile
#     for user in users:
#         if len(user.user_profile.all()) < 1:
#             wo_count = WorkOrder.objects.filter(Q(submitter=user) | Q(main_requestor=user)).count()

#             if wo_count < 1:
#                 # delete that user if they don't have associated workorders
#                 message("Removed user: {0} with no profile.\n".format(user.username), 'warning')
#                 user.delete()
#             else:
#                 message("Can't remove {0} with no profile, because they are associated with {1} workorders.\n".format(user.username, wo_count), 'error')

#     return

def deactivate_users_missing_from_workday(all_employees, in_workday):

    # get all the User Profiles
    user_profiles = UserProfile.objects.all().order_by('last_name')

    for profile in user_profiles:
        if profile.employee_id and not profile.employee_id in in_workday:
            if profile.is_active is True or profile.user.is_active is True:
                profile.is_active = False
                profile.save()
                profile.user.is_active = False
                profile.user.save()
                message(u"Employee {0.first_name}, {0.last_name} ({0.employee_id}) not active in workday within the last 30 days. Marked inactive.\n".format(profile), 'error')
                user_debug(profile)
    return in_workday



class Command(BaseCommand):
    """Grab all employees from workday API and update user profiles"""
    args = '<employeeid>'
    help = 'Grab all employees from workday API and update user profiles'

    def handle(self, *args, **options):
        global VERBOSITY
        VERBOSITY = int(options['verbosity'])

        emp_id = None

        if args:
            emp_id = args[0]

        # get an array of dicts each containing the following details
        #'WORKERTYPE', 'LEGACYDEPTID', 'EMPLOYEEID', 'FIRSTNAME', 'LASTNAME', 'MGRLASTNAME',
        #'EMAILADDRESS', 'COSTCENTER', 'MGRFIRSTNAME', 'MGRID'}
        all_employees = get_active_employees(emp_id=emp_id)
        # build a lookup dict of the users in workday that should be active in ResourceMatrix
        in_workday = {}
        for emp in all_employees:
            in_workday[emp['EMPLOYEEID']] = True

        if not emp_id:
            deactivate_users_missing_from_workday(all_employees, in_workday)
            # cleanup_missing_user_profiles()

        managers = {}


        for emp in all_employees:
            if emp['MGRID']:
                managers[emp['MGRID']] = 1

        for emp in all_employees:
            if emp['EMPLOYEEID'] in managers:
                add_employee(emp, manager=True)

        for emp in all_employees:
            if emp['EMPLOYEEID'] not in managers:
                add_employee(emp)

        if not emp_id:
            visiting_scientists = VisitingScientist.objects.using('vstar').filter(
                Q(projects__active=True) | (Q(projects__date_end__gte=THIRTY_DAYS_AGO) & ~Q(projects__status='AWAITINGREVIEW'))).distinct()


            for emp in visiting_scientists:
                add_visitor(emp, in_workday)

        return
