from datetime import datetime, timedelta
from secrets import token_urlsafe

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from boogie import rules
from boogie.apps.users.models import AbstractUser
from boogie.rest import rest_api
from .manager import UserManager


@rest_api(['id', 'name'])
class User(AbstractUser):
    """
    Default user model for EJ platform.
    """

    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=('Your e-mail address')
    )

    objects = UserManager()

    @property
    def username(self):
        return self.email.replace('@', '__')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    @property
    def profile(self):
        profile = rules.get_value('auth.profile')
        return profile(self)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class PasswordResetToken(TimeStampedModel):
    """
    Expiring token for password recovery.
    """
    url = models.CharField(
        _('User token'),
        max_length=50,
        unique=True,
    )
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )

    @property
    def is_expired(self):
        time_now = datetime.now(timezone.utc)
        return (time_now - self.created).total_seconds() > 600

    def generate_token(self):
        self.url = token_urlsafe(30)


def generate_token(user):
    token = PasswordResetToken(user=user)
    token.generate_token()
    token.save()
    return token


def clean_expired_tokens():
    """
    Clean up used and expired tokens.
    """
    threshold = datetime.now(timezone.utc) - timedelta(seconds=600)
    expired = PasswordResetToken.objects.filter(created__lte=threshold)
    used = PasswordResetToken.objects.filter(is_used=True)
    (used | expired).delete()
