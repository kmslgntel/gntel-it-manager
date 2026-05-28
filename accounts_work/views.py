from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def accountwork_list(request):
    return render(request, 'accounts_work/accountwork_list.html', {})
