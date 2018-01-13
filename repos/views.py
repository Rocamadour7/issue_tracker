from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from repos.models import Repo

from repos.utils import update_repos_decorator

decorators = [login_required, update_repos_decorator]


@method_decorator(decorators, name='dispatch')
class RepoList(ListView):
    model = Repo
    template_name = 'repos/index.html'

    def get_queryset(self):
        return Repo.objects.filter(user=self.request.user.id)
