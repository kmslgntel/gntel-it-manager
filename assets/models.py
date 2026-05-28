from django.db import models


class Company(models.Model):
    """CPY_INF — 회사"""
    code = models.CharField(max_length=20, unique=True)   # COCD
    name = models.CharField(max_length=100)               # CPY_NAME

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    """DPT_INF — 부서"""
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)   # DEPT_CODE
    name = models.CharField(max_length=100)               # DEPT_NAME
    name_en = models.CharField(max_length=100, blank=True)
    high_dept_code = models.CharField(max_length=20, blank=True)
    step = models.IntegerField(null=True, blank=True)
    view_order = models.IntegerField(null=True, blank=True)
    use_yn = models.CharField(max_length=1, default='Y')

    class Meta:
        ordering = ['view_order', 'name']

    def __str__(self):
        return self.name


class Person(models.Model):
    """USR_INF + OTH_INF 통합 — 임직원/기타 사용자"""
    PERSON_TYPE_CHOICES = [('employee', '임직원'), ('other', '기타')]

    person_type = models.CharField(max_length=10, choices=PERSON_TYPE_CHOICES)
    legacy_id = models.CharField(max_length=50, db_index=True)  # USER_ID / OTHER_ID
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)         # GRADE_NM
    emp_no = models.CharField(max_length=50, blank=True)        # EMP_NO
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=50, blank=True)
    hp = models.CharField(max_length=50, blank=True)
    use_yn = models.CharField(max_length=1, default='Y')
    resign_dt = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ('person_type', 'legacy_id')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_person_type_display()})"

    @property
    def is_active(self):
        return self.use_yn == 'Y'


class IpGroup(models.Model):
    """IP_GRP_INF + GRP_INF + IP_PRN_INF 통합 — IP 그룹"""
    legacy_group_id = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100, blank=True)  # IP_PRN_INF 평탄화
    is_phone_group = models.BooleanField(default=False)          # GRP_INF 구분

    class Meta:
        ordering = ['parent_name', 'name']

    def __str__(self):
        if self.parent_name:
            return f"{self.parent_name} / {self.name}"
        return self.name


class IpAddress(models.Model):
    """IP_MNG — IP 할당 정보"""
    ip = models.GenericIPAddressField()
    ip_int = models.BigIntegerField(db_index=True)              # 정렬/원본 IP_ID 보존
    group = models.ForeignKey(IpGroup, on_delete=models.SET_NULL, null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['ip_int']

    def __str__(self):
        return self.ip

    @property
    def is_assigned(self):
        return self.person_id is not None


class NetworkDevice(models.Model):
    """NTWR_DVCS_INF — IPScan 수집 장비 정보"""
    ip_address = models.ForeignKey(IpAddress, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.CharField(max_length=45, blank=True)
    mac = models.CharField(max_length=20, blank=True, db_index=True)
    hostname = models.CharField(max_length=100, blank=True)     # HNAME
    division = models.CharField(max_length=100, blank=True)
    scan_user = models.CharField(max_length=100, blank=True)    # USER
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ip} ({self.mac})"


class Phone(models.Model):
    """PHN_MNG — 내선/전화번호"""
    phone_id = models.CharField(max_length=20, unique=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.ForeignKey(IpAddress, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['phone_id']

    def __str__(self):
        return self.phone_id

    @property
    def is_assigned(self):
        return self.person_id is not None
