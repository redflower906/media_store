from django_auth_ldap import backend
from django.contrib.auth.models import User

class LDAPBackend(backend.LDAPBackend):

    def authenticate(self, username=None, password=None):

        user = backend.LDAPBackend.authenticate(self, username=username, password=password)


        if user:
            # TODO: add a step here that checks if a UserProfile object exists for this user.
            # if not, contact LDAP? and create one.
            pass

        return user

