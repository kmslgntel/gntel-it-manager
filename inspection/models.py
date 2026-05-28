from django.db import models


class Server(models.Model):
    """정기점검 대상 서버 마스터 — Excel 열 기준 9종"""
    COLLECT_CHOICES = [
        ('manual', '수동'),
        ('db-view', 'DB View'),
        ('winrm', 'WinRM'),
        ('ssh', 'SSH'),
        ('api', 'API'),
    ]
    name = models.CharField(max_length=50, unique=True)
    excel_label = models.CharField(max_length=50, blank=True)   # Excel 표시명 (C~K 열 고정값)
    hostname = models.CharField(max_length=100, blank=True)
    registered_ip = models.CharField(max_length=45, blank=True)
    os = models.CharField(max_length=50, blank=True)
    collect_method = models.CharField(max_length=20, choices=COLLECT_CHOICES, default='manual')
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.excel_label or self.name


class Inspection(models.Model):
    """월별 정기점검 헤더"""
    inspect_ym = models.CharField(max_length=7, unique=True)    # '2026-05'
    created_by = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)                      # 점검결과 특이사항 (C20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-inspect_ym']

    def __str__(self):
        return self.inspect_ym


class InspectionDetail(models.Model):
    """서버별 점검 항목 상세"""
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='details')
    server = models.ForeignKey(Server, on_delete=models.CASCADE)

    # IP 확인 (행4)
    ip_status = models.CharField(max_length=50, blank=True)
    ip_detected = models.CharField(max_length=45, blank=True)

    # 시스템 — Windows Event Log (행5)
    event_log_summary = models.TextField(blank=True)
    event_critical = models.IntegerField(null=True, blank=True)
    event_error = models.IntegerField(null=True, blank=True)
    event_warning = models.IntegerField(null=True, blank=True)

    # H/W (행6~9)
    cpu_total_ghz = models.FloatField(null=True, blank=True)
    cpu_usage_pct = models.FloatField(null=True, blank=True)
    ram_total_gb = models.FloatField(null=True, blank=True)
    ram_used_gb = models.FloatField(null=True, blank=True)
    disk_info_json = models.TextField(blank=True)               # JSON 배열: [{drive,total,used}]
    disk_health = models.CharField(max_length=100, blank=True)

    # Backup (행10)
    last_backup_date = models.DateField(null=True, blank=True)

    # 보안 업데이트 (행11~12)
    win_update_status = models.CharField(max_length=100, blank=True)
    v3_version = models.CharField(max_length=100, blank=True)

    # 계정 (행13~15) — AccountWork 집계값
    account_create_cnt = models.IntegerField(null=True, blank=True)
    account_change_cnt = models.IntegerField(null=True, blank=True)
    account_delete_cnt = models.IntegerField(null=True, blank=True)

    # IPS (행16)
    ips_block_cnt = models.IntegerField(null=True, blank=True)
    ips_attempt_cnt = models.IntegerField(null=True, blank=True)

    # 수신메일 (행17~19)
    mail_normal_cnt = models.IntegerField(null=True, blank=True)
    mail_spam_cnt = models.IntegerField(null=True, blank=True)
    mail_virus_cnt = models.IntegerField(null=True, blank=True)
    mail_ransom_cnt = models.IntegerField(null=True, blank=True)

    collected_at = models.DateTimeField(null=True, blank=True)
    is_auto_collected = models.BooleanField(default=False)

    class Meta:
        unique_together = ('inspection', 'server')

    def __str__(self):
        return f"{self.inspection.inspect_ym} - {self.server}"

    @property
    def mail_block_total(self):
        return (self.mail_spam_cnt or 0) + (self.mail_virus_cnt or 0) + (self.mail_ransom_cnt or 0)

    @property
    def mail_total(self):
        return (self.mail_normal_cnt or 0) + self.mail_block_total
