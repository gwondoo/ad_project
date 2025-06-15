from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def login_view(request):
    """사용자 로그인"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get("next") or 'index'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'common/login.html', context)


def logout_view(request):
    """사용자 로그아웃"""
    logout(request)
    return redirect('index')
