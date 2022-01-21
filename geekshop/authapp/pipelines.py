from collections import OrderedDict
from datetime import datetime, date, timedelta
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden, AuthException

from authapp.models import UserProfile


# bdate
# sex
# about
# photo

def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(OrderedDict(
                              fields=','.join(('first_name', 'bdate', 'sex', 'about', 'personal', 'photo_200')),
                              access_token=response['access_token'], v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]

    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE

    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = (date.today() - bdate) // timedelta(days=365.2425)
    # age = timezone.now().date().year - bdate.year
    user.age = age

    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_200']:
        photo_200_link = data['photo_200']
        photo_response = requests.get(photo_200_link)
        path_photo_200 = f'users_image/{user.pk}.jpg'
        with open(f'media/{path_photo_200}', 'wb') as photo_200:
            photo_200.write(photo_response.content)
        user.image = path_photo_200

    if data['personal'].get('langs'):
        user.userprofile.langs = data['personal']['langs'][0] if len(data['personal']['langs'][0]) > 0 else 'EN'

    if data['first_name']:
        user.username = data['first_name']

    user.save()
