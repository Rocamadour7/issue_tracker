from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from repos.models import Repo, Issue

from repos.utils import update_repos_decorator, update_issues_decorator

repo_list_decorators = [login_required, update_repos_decorator]


@method_decorator(repo_list_decorators, name='dispatch')
class RepoList(ListView):
    model = Repo
    template_name = 'repos/repos_index.html'

    def get_queryset(self):
        return self.request.user.repo_set.all()


issue_list_decorators = [login_required, update_issues_decorator]


@method_decorator(issue_list_decorators, name='dispatch')
class IssueList(ListView):
    template_name = 'repos/issues_index.html'
    context_object_name = 'issue_list'

    def get_queryset(self):
        name = self.kwargs.get('name')
        issue_list = self.request.user.repo_set.get(name=name).issue_set.all()
        return issue_list

    def get_context_data(self, **kwargs):
        context = super(IssueList, self).get_context_data(**kwargs)
        context['repo_name'] = self.kwargs.get('name')
        return context


def create_issue(request, name):
    return HttpResponseRedirect(reverse('repos:issues', args=(name,)))
