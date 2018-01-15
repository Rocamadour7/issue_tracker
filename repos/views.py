from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from repos.utils import *

repo_list_decorators = [login_required, update_repos_decorator]


@method_decorator(repo_list_decorators, name='dispatch')
class RepoList(ListView):
    model = Repo
    template_name = 'repos/repos_index.html'

    def get_queryset(self):
        return self.request.user.repo_set.all()


issue_list_decorators = [login_required, update_issues_decorator, check_due_dates_decorator]


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


@login_required
def create_issue(request, name):
    try:
        repo = get_object_or_404(Repo, user=request.user, name=name)
        title = request.POST['title']
        body = request.POST['body']
        created_at = timezone.now()
        raw_due_date = request.POST['due_date']
        due_date = timezone.datetime.strptime(raw_due_date, '%Y-%m-%dT%H:%M')
        due_date = timezone.make_aware(due_date)
        is_due_date_valid = check_if_date_is_valid(due_date)
        if is_due_date_valid:
            issue = repo.issue_set.create(title=title,
                                          body=body,
                                          author=request.user.username,
                                          created_at=created_at,
                                          due_date=due_date)
            issue.save()
    except(KeyError, Repo.DoesNotExist):
        return redirect('repos:issues', name=name, error_message='Invalid Issue data.')
    else:
        return redirect('repos:issues', name=name)


@login_required
def change_due_date(request, name, issue_id):
    try:
        issue = get_object_or_404(Issue, id=issue_id)
        raw_due_date = request.POST['due_date']
        due_date = timezone.datetime.strptime(raw_due_date, '%Y-%m-%dT%H:%M')
        due_date = timezone.make_aware(due_date)
        is_due_date_valid = check_if_date_is_valid(due_date)
        if is_due_date_valid:
            issue.due_date = due_date
            issue.save()
    except(KeyError, Issue.DoesNotExist):
        return redirect('repos:issues', name=name, error_message='Invalid due date.')
    else:
        return redirect('repos:issues', name=name)


@login_required
def change_state(request, name, issue_id):
    try:
        issue = get_object_or_404(Issue, id=issue_id)
        new_state = request.POST['state']
        print(issue.title)
        issue.state = new_state
        issue.save()
    except(KeyError, Issue.DoesNotExist):
        return redirect('repos:issues', name=name, error_message='Something went wrong.')
    else:
        return redirect('repos:issues', name=name)
