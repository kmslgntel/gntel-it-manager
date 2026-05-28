from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator

from assets.models import IpAddress, Phone
from switches.models import Switch as SwitchModel
from inspection.models import Inspection
from accounts_work.models import AccountWork
from core.models import AuditLog


@login_required
def dashboard(request):
    now = timezone.now()
    this_ym = now.strftime('%Y-%m')

    ip_total = IpAddress.objects.count()
    ip_used = IpAddress.objects.filter(person__isnull=False).count()
    ip_free = ip_total - ip_used
    ip_usage_percent = round((ip_used / ip_total) * 100, 1) if ip_total else 0

    phone_total = Phone.objects.count()
    phone_used = Phone.objects.filter(person__isnull=False).count()
    phone_free = phone_total - phone_used

    switch_total = SwitchModel.objects.count()

    try:
        this_inspection = Inspection.objects.get(inspect_ym=this_ym)
        inspection_detail_count = this_inspection.details.count()
    except Inspection.DoesNotExist:
        this_inspection = None
        inspection_detail_count = 0

    recent_account_works = AccountWork.objects.order_by('-work_date', '-created_at')[:5]
    recent_logs = AuditLog.objects.order_by('-acted_at')[:10]

    return render(request, 'dashboard.html', {
        'ip_total': ip_total,
        'ip_used': ip_used,
        'ip_free': ip_free,
        'ip_usage_percent': ip_usage_percent,
        'phone_total': phone_total,
        'phone_used': phone_used,
        'phone_free': phone_free,
        'switch_total': switch_total,
        'this_inspection': this_inspection,
        'inspection_detail_count': inspection_detail_count,
        'this_ym': this_ym,
        'recent_account_works': recent_account_works,
        'recent_logs': recent_logs,
        'recent_log_count': len(recent_logs),
    })


@login_required
def auditlog_list(request):
    qs = AuditLog.objects.order_by('-acted_at')

    actor = request.GET.get('actor', '').strip()
    action = request.GET.get('action', '').strip()
    target_type = request.GET.get('target_type', '').strip()

    if actor:
        qs = qs.filter(actor__icontains=actor)
    if action:
        qs = qs.filter(action=action)
    if target_type:
        qs = qs.filter(target_type__icontains=target_type)

    paginator = Paginator(qs, 100)
    page_obj = paginator.get_page(request.GET.get('page'))

    action_choices = AuditLog.objects.values_list('action', flat=True).distinct().order_by('action')

    return render(request, 'core/auditlog_list.html', {
        'page_obj': page_obj,
        'actor': actor,
        'action': action,
        'target_type': target_type,
        'action_choices': action_choices,
    })
