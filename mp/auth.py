from social.backends.open_id import OpenIdAuth


class P97OpenId(OpenIdAuth):

    """P97 OpenID authentication backend"""
    name = 'P97'
    URL = 'https://www.google.com/accounts/o8/id'

    def get_user_details(self, response):
        """Return user details from P97 Google account"""
        print self.data
        email = self.data.get('openid.ext1.value.email')
        last_name = self.data.get('openid.ext1.value.last_name')
        first_name = self.data.get('openid.ext1.value.first_name')
        username = email.split('@')[0]
        if email.endswith('pointnineseven.com'):
            is_staff = True
            is_superuser = True
        else:
            is_staff = False
            is_superuser = False

        return {'username': username,
                'email': email,
                'last_name': last_name,
                'first_name': first_name,
                'is_staff': is_staff,
                'is_superuser': is_superuser
                }
