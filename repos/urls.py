from django.urls import path

from .views import RepoList, IssueList, create_issue

app_name = 'repos'

urlpatterns = [
    path('', RepoList.as_view(), name='list'),
    path('<slug:name>/', IssueList.as_view(), name='issues'),
    path('<slug:name>/new/', create_issue, name='new_issue'),
]
