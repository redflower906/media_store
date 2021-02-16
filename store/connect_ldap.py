import os
import ldap
import logging

logger = logging.getLogger('default')

def connect_to_ldap():
        ld = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
        ld.simple_bind_s()
        basedn = "ou=Laboratories,ou=DepartmentsOnIntranet,ou=ApplicationRoles,dc=hhmi,dc=org"
        filter = "(|(ou=*))"
        results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
        #dn is a string like: 'cn=pinerog,ou=People,dc=janelia,dc=org'
        #we don't care about it
        retlist = [entry for dn,entry in results if entry.get('ou')]
        ld.unbind_s()
        retlist.sort(key=lambda x: x['ou'])
        return retlist

def get_graduate_details():
        ldap_results = connect_to_ldap()
        index = 0
        user_dict = {}
        for duser in ldap_results:
                grad_dict = {}
                if duser['ou'][0] == 'Laboratories':
                        pass
                else:
                        ou_var = duser['ou'][0]
                        desc = duser['description'][0]
                        ld = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
                        ld.simple_bind_s()
                        basedn = "ou="+str(ou_var)+",ou=Laboratories,ou=DepartmentsOnIntranet,ou=ApplicationRoles,dc=hhmi,dc=org"
                        filter = "(|(cn=jgs))"
                        results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
                        retlist = [entry for dn,entry in results if entry.get('cn')]
                        ld.unbind_s()
                        retlist.sort(key=lambda x: x['uniqueMember'])
                        if len(retlist) == 0:
                                pass
                        else:
                                user_query = retlist[0]['uniqueMember'][0]
                                ld2 = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
                                ld2.simple_bind_s()
                                basedn2 = str(user_query)
                                try:
                                        results2 = ld2.search_s(basedn2,ldap.SCOPE_SUBTREE)
                                        ld2.unbind_s()
                                except ldap.NO_SUCH_OBJECT:
                                        pass
                                if results2 == 'test':
                                        logging.info('get_graduate_details: no such object for {0}'.format(basedn2))
                                else:
                                        grad_dict['uid'] = results2[0][1]['uid']
                                        try:
                                                grad_dict['mail'] = results2[0][1]['mail']
                                        except:
                                                pass
                                        grad_dict['title'] = results2[0][1]['title']
                                        grad_dict['gidNumber'] = results2[0][1]['gidNumber']
                                        grad_dict['description'] = desc

                                        index += 1
                                        user_dict[index] = grad_dict
        return user_dict

def get_graduate_department(dict):
        grad_dict = {}
        for key,value in dict.items():
                for k,v in value.items():
                        if k == 'description':
                                description = v

                        if k == 'mail':
                                mail = v
                ld3 = ldap.initialize('ldap://ldap-vip1.int.janelia.org')
                ld3.simple_bind_s()
                basedn3 = "ou=people,dc=hhmi,dc=org"
                filter3 = "(|(description="+str(description)+"))"
                results3 = ld3.search_s(basedn3,ldap.SCOPE_SUBTREE,filter3)
                retlist3 = [entry for dn,entry in results3 if entry.get('employeeNumber')]
                ld3.unbind_s()
                retlist3.sort(key=lambda x: x['uid'])
                grad_dict['mail'] = mail
                grad_dict['department'] = retlist3[0]['gidNumber'][0]

grad_dictionary = get_graduate_details()
grad_department_dictionary = get_graduate_department(grad_dictionary)