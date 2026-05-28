from django.db import models


class AccountWork(models.Model):
    """계정 작업 내역 — 정기점검 계정 건수 집계에도 사용"""
    SYSTEM_CHOICES = [
        ('groupware', '그룹웨어'),
        ('erp', 'ERP'),
        ('fileserver-account', '파일서버 계정'),
        ('fileserver-folder', '파일서버 폴더'),
        ('firewall', '방화벽'),
    ]
    WORK_CHOICES = [
        ('add', '추가'),
        ('delete', '삭제'),
        ('leave', '퇴사처리'),
        ('permission', '권한변경'),
        ('folder-create', '폴더 생성'),
        ('folder-rename', '폴더명 변경'),
    ]

    work_date = models.DateField()
    system_type = models.CharField(max_length=30, choices=SYSTEM_CHOICES)
    work_type = models.CharField(max_length=30, choices=WORK_CHOICES)
    operator = models.CharField(max_length=50)
    target = models.CharField(max_length=100)
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['work_date']),
            models.Index(fields=['system_type']),
            models.Index(fields=['work_type']),
            models.Index(fields=['operator']),
            models.Index(fields=['target']),
        ]
        ordering = ['-work_date', '-created_at']

    def __str__(self):
        return (f"{self.work_date} | {self.get_system_type_display()} | "
                f"{self.get_work_type_display()} | {self.target}")
