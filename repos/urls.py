from django.urls import path

from .views import RepoList, IssueList, create_issue, change_due_date, change_state

app_name = 'repos'

urlpatterns = [
    path('', RepoList.as_view(), name='list'),
    path('<slug:name>/', IssueList.as_view(), name='issues'),
    path('<slug:name>/new/', create_issue, name='new_issue'),
    path('<slug:name>/<int:issue_id>/due_date/', change_due_date, name='change_due_date'),
    path('<slug:name>/<int:issue_id>/state/', change_state, name='change_state'),
]
