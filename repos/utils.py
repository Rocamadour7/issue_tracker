import requests
from django.http import HttpResponseRedirect
from .models import Repo


def update_repos_decorator(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_social = user.social_auth.get(provider='github')
        access_token = user_social.extra_data['access_token']
        response = requests.get('https://api.github.com/user/repos',
                                headers={'Authorization': 'token {}'.format(access_token)})
        if response.status_code == 200:
            json_data = response.json()
            for data in json_data:
                name = data['name']
                repo, created = Repo.objects.get_or_create(user=user, name=name)
                repo.description = data['description']
                repo.language = data['language']
                repo.save()
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrapper
