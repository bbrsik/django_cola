from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import Profile


@csrf_exempt
def render_login(request):
    if request.user.is_authenticated:
        return redirect('/message/chats/')
    login_failed = request.session.get('login_failed', False)
    if login_failed:
        messages.error(request, 'Wrong username or password')
        del request.session['login_failed']
    return render(request, 'render_login.html', {'login_failed': login_failed})


@csrf_exempt
def render_signup(request):
    if request.user.is_authenticated:
        return redirect('/message/chats/')
    signup_failed = request.session.get('signup_failed', False)
    if signup_failed:
        messages.error(request, 'User already exists')
        del request.session['signup_failed']
    return render(request, 'render_signup.html', {'signup_failed': signup_failed})


def render_display_profile(request):
    pass


def render_edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('/user/login/')
    profile = Profile.objects.get(user=request.user)

    edit_failed = request.session.get('edit_failed', False)
    if edit_failed:
        messages.error(request, 'Password verification failed')
        del request.session['edit_failed']

    edit_succeeded = request.session.get('edit_succeeded', False)
    if edit_succeeded:
        messages.success(request, 'Profile updated successfully')
        del request.session['edit_succeeded']

    context = {
        'first_name': profile.first_name or '',
        'last_name': profile.last_name or '',
        'middle_name': profile.middle_name or '',
        'birthdate': str(profile.birthdate) or '',
        'current_location': profile.current_location or '',
        'picture': profile.picture,
        'edit_failed': edit_failed,
        'edit_succeeded': edit_succeeded,
    }
    return render(request, 'render_profile.html', context=context)

