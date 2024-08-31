from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from moviesearch.models import Bookmark, Movie

@login_required
def profile_detail(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'userprofiles/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'userprofiles/profile_edit.html', {'form': form})
