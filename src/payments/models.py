from typing import List, Optional

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class UserPaymentAbs(TimeStampedModel):

    class Meta:
        abstract = True

    STANDARD = 'STANDARD'
    PREMIUM = 'PREMIUM'
    ENTERPRISE = 'ENTERPRISE'

    CUSTOMER_TYPE_CHOICES = (
        (STANDARD, 'Standard'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPE_CHOICES, null=True, default=None)


class UserPaymentStatus(UserPaymentAbs):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    CANCELED = 'CANCELED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (SUCCESS, 'SUCCESS'),
        (CANCELED, 'CANCELED'),
        (REJECTED, 'REJECTED'),
    )
    stripe_checkout_id = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=PENDING)
    history = HistoricalRecords()


class UserPayment(UserPaymentAbs):
    history = HistoricalRecords()

    @classmethod
    def get_premium_site_access_list(cls, user_id) -> List[str]:
        return list(set([p.site_name for p in cls.objects.filter(user=user_id)]))

    @classmethod
    def get_by_current_user_and_site(cls, user_id, site_name: str) -> Optional['UserPayment']:
        return cls.objects.filter(user=user_id, site_name=site_name).first()
