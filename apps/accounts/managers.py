from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    '''
    Authenticate case-insensitive usernames
    '''

    def get_by_natural_key(self, username):
        '''
        It is called from the default AUTHENTICATION_BACKEND (ModelBackend)
        to authenticate a guest against its username:
        user = UserModel._default_manager.get_by_natural_key(username)
        '''
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})
