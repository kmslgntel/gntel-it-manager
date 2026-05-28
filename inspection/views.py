from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def inspection_list(request):
    return render(request, 'inspection/inspection_list.html', {})
