from django.contrib import admin

from repos.models import Repo, Issue

admin.site.register(Repo)
admin.site.register(Issue)
