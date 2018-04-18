
"""
Run this twice daily to refresh table that holds a list of 
employees.
"""

import os
import ldap
import MySQLdb
import ldif
import sys
import logging

logger = logging.getLogger('default')
# Use execfile instead of import, because we don't want all the Django junk to try to run
# Assumes we're in the tools directory

def get_all_users():
    """Given an ldap connection, return all users.  Each user is a dictionary
    with the following keys:
    ['telephoneNumber', 'departmentNumber', 'loginShell', 'cn', 'uid', 'title', 
    'objectClass', 'uidNumber', 'description', 'jpegPhoto', 'roomNumber', 'gidNumber', 
    'gecos', 'sn', 'homeDirectory', 'mail', 'givenName', 'displayName', 'employeeNumber'] 
    """
    ld = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
    ld.simple_bind_s()
    basedn = "ou=people,dc=hhmi,dc=org"
    filter = "(|(uid=*))"
    #Other sample filters
    #filter = "(|(uid=" + user + "*)(mail=" + user + "*))"
    #filter = "(|(description=Facilities - Security*))"
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
    #dn is a string like: 'cn=pinerog,ou=People,dc=janelia,dc=org'
    #we don't care about it
    retlist = [entry for dn,entry in results]
    ld.unbind_s()
    retlist.sort(key=lambda x: x['uid'])
    return retlist


def get_all_AD_users():
    """Given an ldap connection, return all users.  Each user is a dictionary
    with the following keys:
    ['telephoneNumber', 'departmentNumber', 'loginShell', 'cn', 'uid', 'title', 
    'objectClass', 'uidNumber', 'description', 'jpegPhoto', 'roomNumber', 'gidNumber', 
    'gecos', 'sn', 'homeDirectory', 'mail', 'givenName', 'displayName', 'employeeNumber'] 
    """
    ldif_writer = ldif.LDIFWriter(sys.stdout)
    ld = ldap.initialize('ldap://172.19.15.120')
    ldap_username = 'nycek@janelia.hhmi.org'
    ldap_password = 'Binky2000!'
    ld.simple_bind_s(ldap_username,ldap_password)
    if ld.simple_bind_s():
	logger.info('LDAP connected')
    basedn = "ou=people,dc=hhmi,dc=org"
    #filter = "(|(uid=*))"
    #filter = "(cn=*)"
    #Other sample filters
    #filter = "(|(uid=" + user + "*)(mail=" + user + "*))"
    #filter = "(|(description=Facilities - Security*))"
    results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,"(cn=*)")
    for dn,entry in results:
	ldif_writer.unparse(dn,entry)

    #dn is a string like: 'cn=pinerog,ou=People,dc=janelia,dc=org'
    #we don't care about it
    #retlist = [ldif_writer.unparse(dn,entry) for dn,entry in results]
    ld.unbind_s()
    #retlist.sort(key=lambda x: x['uid'])

