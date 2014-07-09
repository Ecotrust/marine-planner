from social.backends.google import GooglePlusAuth


class CustomGooglePlusAuth(GooglePlusAuth):

    """P97 GPlus authentication backend"""
    name = 'google-plus'
    EXTRA_DATA = [
        ('id', 'user_id'),
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('access_type', 'access_type', True),
        ('code', 'code'),
        ('picture', 'picture')
    ]


    def get_user_details(self, response):
        """Return user details from Google API account"""
        if response.get('emails'):
            email = response['emails'][0]['value']
        elif response.get('email'):
            email = response['email']
        else:
            email = ''
        if email.endswith('pointnineseven.com'):
            is_staff = True
            is_superuser = True
        else:
            is_staff = False
            is_superuser = False
        return {'username': email.split('@', 1)[0],
                'email': email,
                'first_name': response.get('given_name'),
                'last_name': response.get('family_name'),
                'picture': response.get('picture'),
                'is_staff': is_staff,
                'is_superuser': is_superuser
                }
