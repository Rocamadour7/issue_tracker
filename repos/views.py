from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from repos.models import Repo

from repos.utils import get_repos

decorators = [login_required, get_repos]


@method_decorator(decorators, name='dispatch')
class RepoList(ListView):
    model = Repo
