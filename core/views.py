from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    user = request.user.social_auth.get(provider='github')
    access_token = user.extra_data['access_token']
    context = {'access_token': access_token}
    return render(request, 'core/home.html', context=context)