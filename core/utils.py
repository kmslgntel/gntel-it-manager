import ipaddress
from .models import AuditLog


def log_action(request_or_actor, action, target_type, target_id='', detail=''):
    if hasattr(request_or_actor, 'user'):
        actor = request_or_actor.user.get_full_name() or request_or_actor.user.username
    else:
        actor = str(request_or_actor)
    AuditLog.objects.create(
        actor=actor,
        action=action,
        target_type=target_type,
        target_id=str(target_id),
        detail=detail,
    )


def ip_to_int(ip_str):
    try:
        return int(ipaddress.ip_address(ip_str))
    except ValueError:
        return 0
