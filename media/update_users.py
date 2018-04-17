"""
Make sure everyone in LDAP is included in the users table.

Call this with manage.py e.g.,
python manage.py update_users

The basic strategy here is to always have all employees at Janelia sitting in the 
users table (inactivated).  Then Staff can go in and activate them, and 
assign groups.  Active staff users can then log in with ldap.
"""

import sys
sys.path.append('/SlackerTracker') #assumes we're running from DjangoProjects/VisitorProjectTracker
import datetime
import uuid

from update_LDAP import get_all_users

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group,User

def gen_pw():
    """Users can't be edited in the admin if password is empty so set a dummy one here
    It's safe because users are inactivated by default, and those that aren't default to
    their ldap password."""
    return uuid.uuid1()

def map_attrs_to_user(u, dattrs):
    u.username = dattrs['uid'][0]
    u.is_active = True
    #u.is_staff = True
    u.first_name = dattrs.get('givenName',[''])[0]
    u.last_name = dattrs.get('sn',[''])[0]
    u.email = dattrs.get('mail',[''])[0]
    u.set_password(gen_pw())
    u.save() #save so a profile gets created if it doesn't already exist

class Command(BaseCommand):
    args = ''
    help = 'Make sure everyone in LDAP is included in the users and user profile tables.'

    def handle(self, *args, **options):

        #get_all_users() returns all users.  Each user is a dictionary
        #with the following keys:
        #['telephoneNumber', 'departmentNumber', 'loginShell', 'cn', 'uid', 'title', 
        #'objectClass', 'uidNumber', 'description', 'jpegPhoto', 'roomNumber', 'gidNumber', 
        #'gecos', 'sn', 'homeDirectory', 'mail', 'givenName', 'displayName', 'employeeNumber'] 
        all_ldap_users = get_all_users()

        #Update or create users to match LDAP
        for duser in all_ldap_users:
            matches = User.objects.filter(username=duser['uid'][0])
            if len(matches)==1:
                user = matches[0]
            elif len(matches)== 0:
                user = User()
                self.stdout.write("Creating new user record for %s\n" % duser['uid'][0])
            else:
                raise CommandError('Found duplicate user %s\n' % duser['uid'][0])
            map_attrs_to_user(user,duser)

        #Find anyone not in LDAP and deactivate them
        #Skip for now
        #current_users_in_ldap = set([u['uid'][0] for u in all_ldap_users])
        #for user in User.objects.all():
        #    if not user.username in current_users_in_ldap:
        #        user.is_active = False
        #        user.save()
        #        self.stdout.write("Marked user %s as non active!\n" % user.username)

        self.stdout.write('Successfully updated users!\n')
