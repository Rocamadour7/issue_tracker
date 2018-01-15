import requests
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Repo, Issue


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
                description = data['description']
                language = data['language']
                defaults = {'description': description, 'language': language}
                Repo.objects.get_or_create(user=user, name=name, defaults=defaults)
        return func(request, *args, **kwargs)
    return wrapper


def update_issues_decorator(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        repo_name = kwargs.get('name')
        response = requests.get('https://api.github.com/repos/{}/{}/issues'.format(user.username, repo_name))
        if response.status_code == 200:
            repo = Repo.objects.get(user=user, name=repo_name)
            json_data = response.json()
            for data in json_data:
                title = data['title']
                body = data['body']
                author = data['user']['login']
                state = data['state'][0]
                created_at = data['created_at']
                defaults = {'body': body, 'author': author, 'state': state, 'created_at': created_at}
                Issue.objects.get_or_create(repo=repo, title=title, defaults=defaults)
        return func(request, *args, **kwargs)
    return wrapper


def check_due_dates_decorator(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        repo_name = kwargs.get('name')
        try:
            repo = get_object_or_404(Repo, user=user, name=repo_name)
        except (KeyError, Repo.DoesNotExist):
            pass
        else:
            issue_list = repo.issue_set.all()
            for issue in issue_list:
                if issue.due_date:
                    delta = issue.due_date - timezone.now()
                    if delta.days < 0 and not (issue.state != 'r' or issue.state != 'p'):
                        issue.state = 's'
                        issue.save()
                    elif delta.days > 0 and not (issue.state != 'r' or issue.state != 'p'):
                        issue.state = 'o'
                        issue.save()
        finally:
            return func(request, *args, **kwargs)
    return wrapper


def check_if_date_is_valid(date):
    delta = date - timezone.now()
    if delta.days > 0:
        return True
    else:
        return False
