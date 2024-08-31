from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_detail(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Include user information to display first_name and last_name
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'userprofiles/profile_detail.html', context)

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save Profile form
            profile = form.save(commit=False)
            # Save user first_name and last_name
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()
            profile.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'userprofiles/profile_edit.html', {'form': form})
