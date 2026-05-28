from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ip_list(request):
    return render(request, 'assets/ip_list.html', {})


@login_required
def phone_list(request):
    return render(request, 'assets/phone_list.html', {})
