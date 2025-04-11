import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from utils.models import TimestampModel


class CommonUser(TimestampModel):
    common_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    join_type = models.CharField(max_length=10)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class UserInfo(TimestampModel):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    common_user = models.OneToOneField(CommonUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10)
    birthday = models.DateField(null=True, blank=True)

    interest = ArrayField(
        models.CharField(max_length=50), default=list, blank=True
    )
    purpose_subscription = ArrayField(
        models.CharField(max_length=50), default=list, blank=True
    )
    route = ArrayField(
        models.CharField(max_length=50), default=list, blank=True
    )
    wish_work_place = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.common_user.email})"


class CompanyInfo(TimestampModel):
    company_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    common_user = models.OneToOneField(CommonUser, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=50)
    establishment = models.DateField()
    company_address = models.CharField(max_length=100)
    business_registration_number = models.CharField(max_length=20)
    company_introduction = models.TextField()
    certificate_image = models.URLField()

    ceo_name = models.CharField(max_length=20)
    manager_name = models.CharField(max_length=30)
    manager_phone_number = models.CharField(max_length=30)
    manager_email = models.EmailField(max_length=50)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
