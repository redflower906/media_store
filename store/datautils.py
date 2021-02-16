import ldap
from django.db import transaction, connections
from VisitorProjectTracker.models import TeamProject, VisitingScientist

def connect_to_ldap(): #get employee_number from ldap
    ld = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
    ld.simple_bind_s()
    basedn = "ou=people,dc=hhmi,dc=org"
    filter = "(|(uid=*))"
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
    retlist = [entry for dn,entry in results if entry.get('employeeNumber')]
    ld.unbind_s()
    retlist.sort(key=lambda x: x['uid'])
    return retlist

def get_entry(last_name, first_name):
    user = None
    ld = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
    ld.simple_bind_s()
    basedn = "ou=people,dc=hhmi,dc=org"
    filter = "(&(sn={0})(givenName={1}))".format(last_name,first_name)
    attrs = ['sn', 'uid', 'employeeNumber', 'givenName', 'departmentNumber']
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter, attrs)
    retlist = [entry for dn,entry in results if entry.get('employeeNumber')]
    ld.unbind_s()
    if len(retlist) > 0:
        user = retlist[0]
    return user

def connect_to_ldap_mail(): #connect to ldap mail
    ld = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
    ld.simple_bind_s()
    basedn = "ou=people,dc=hhmi,dc=org"
    filter = "(|(uid=*))"
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
    retlist = [entry for dn,entry in results if entry.get('mail')]
    ld.unbind_s()
    retlist.sort(key=lambda x: x['mail'])
    return retlist

def get_visiting_scientist(last_name=None, first_name=None): #connect to vStar to get all of the project codes, first_name,last_name
    row_list = []

    scientists = VisitingScientist.objects.using('vstar').filter(projects__active=True).prefetch_related('projects').order_by('last_name').distinct()

    if first_name and last_name:
        scientists = scientists.filter(last_name=last_name, first_name=first_name)

    for scientist in scientists:
        for project in scientist.projects.filter(active=True):
            row_list.append({
                'last_name': unicode(scientist.last_name).encode("utf-8"),
                'first_name': unicode(scientist.last_name).encode("utf-8"),
                'code': project.code
            })

    return row_list	 #return a list of visiting scientist project codes


def get_project_team(dept_code=None): #connect to vStar to get all of the team projects codes that are active
    row_list = []

    projects = TeamProject.objects.using('vstar').order_by('code').only('code','department_code').distinct()

    if dept_code:
        projects = projects.filter(department_code=dept_code)

    for project in projects:
        row_list.append({
            'department_code': project.department_code,
            'code': project.code
        })

    return row_list #return a list of project team project codes
