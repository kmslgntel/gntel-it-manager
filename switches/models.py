from django.db import models


class Rack(models.Model):
    """RCK_INF — 렉"""
    legacy_rack_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Switch(models.Model):
    """SWT_INF — 스위치"""
    legacy_switch_id = models.IntegerField(unique=True)
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='switches')
    ip = models.GenericIPAddressField()                         # SWITCH_IP
    sort_order = models.IntegerField(default=0)                 # SWITCH_SORT
    vendor = models.CharField(max_length=30, default='juniper')
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['rack__name', 'sort_order']

    def __str__(self):
        rack_name = self.rack.name if self.rack else '-'
        return f"{rack_name} / {self.ip}"


class SwitchPort(models.Model):
    """SWT_PRT_MD_INF + PRT_CNC_LCT_INF 통합 — 포트 모드/위치"""
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='ports')
    interface = models.CharField(max_length=50)                 # ge-0/0/0.0
    port_mode = models.CharField(max_length=20, blank=True)     # trunk/access
    area_number = models.CharField(max_length=100, blank=True)  # 아웃렛 (IP+포트 설명 포함 가능)
    port_number = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('switch', 'interface')
        ordering = ['switch', 'interface']

    def __str__(self):
        return f"{self.switch.ip} - {self.interface}"


class SwitchMacEntry(models.Model):
    """ETH_SWT_INF — 포트별 학습 MAC"""
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='mac_entries')
    interface = models.CharField(max_length=50)
    vlan = models.CharField(max_length=20, blank=True)
    mac = models.CharField(max_length=20, db_index=True)
    entry_type = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=20, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['mac']),
            models.Index(fields=['switch', 'interface']),
        ]

    def __str__(self):
        return f"{self.mac} @ {self.switch.ip}/{self.interface}"


class SwitchConfigBackup(models.Model):
    """SWT_CNF_BCK + SWT_BCK_INF 통합 — 스위치 설정 백업"""
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='backups')
    config_data = models.TextField(blank=True)
    status = models.CharField(max_length=20, blank=True)        # Access / Failed
    backup_date = models.CharField(max_length=20, blank=True)   # YYYY-MM-DD
    backup_time = models.CharField(max_length=20, blank=True)   # HH:MM:SS
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['switch', 'backup_date', 'backup_time']),
            models.Index(fields=['backup_date', 'backup_time']),
        ]
        ordering = ['-backup_date', '-backup_time']

    def __str__(self):
        return f"{self.switch.ip} - {self.backup_date} {self.backup_time}"
