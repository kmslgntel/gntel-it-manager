from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def switch_list(request):
    return render(request, 'switches/switch_list.html', {})


@login_required
def backup_list(request):
    return render(request, 'switches/switch_backups.html', {})
