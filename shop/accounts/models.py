from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import datetime

class AuthUserManager(BaseUserManager):

    @classmethod
    def normalize_phone(cls, phone, country_code=None):
        phone = phone.strip().lower()
        #try:
        #    import phonenumbers
        #    phone_number = phonenumbers.parse(phone, country_code)
        #    phone = phonenumbers.format_number(
        #        phone_number, phonenumbers.PhoneNumberFormat.E164)
        #except ImportError:
        #    pass


        return phone

    def _create_user(self, name, password,
                     is_staff, is_superuser, **extra_fields):
        # email_or_phone = name
        # if not email_or_phone:
        #     raise ValueError('The given email_or_phone must be set')
        #
        # if "@" in email_or_phone:
        #     email_or_phone = self.normalize_email(email_or_phone)
        #     username, email, phone = (email_or_phone, email_or_phone, '')
        # else:
        #     phone = self.normalize_phone(
        #         email_or_phone)
        #     username, email, phone = (email_or_phone, '', email_or_phone)
        username = name
        now = timezone.now()
        first_name = extra_fields.pop("first_name", '')
        last_name = extra_fields.pop("last_name", '')
        sex = extra_fields.pop("sex", '')
        phone = extra_fields.pop("phone", '')
        email = extra_fields.pop("email", '')
        #activationextra_fields_key = extra_fields.pop("activation_key", '')
        #key_expires = extra_fields.pop("key_expires", '')
        is_active = extra_fields.pop("is_active", True)
        print(username, password, extra_fields)
        user = self.model(
            username=username,
            email=email,
            phone=phone,
            first_name = first_name,
            last_name = last_name,
            sex =sex,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,




            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        print(username, password, extra_fields)
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username,  password, **extra_fields):
        return self._create_user( username, password, True, True,
                                 **extra_fields)


class AbstractAuthUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'), max_length=255, unique=True, db_index=True,
        help_text=_('Required. 255 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[validators.RegexValidator(
            r'^[\w.@+-]+$', _(
                'Enter a valid username. '
                'This value may contain only letters, numbers '
                'and @/./+/-/_ characters.'
            ), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    email = models.EmailField(_('email'), max_length=254, blank=True,unique=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True,unique=True)
    first_name = models.CharField(_('first_name'), max_length=255, blank=True)
    last_name = models.CharField(_('last_name'), max_length=255, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    sex = models.CharField(_('sex'),max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    activation_key = models.CharField(_('activation_key'),max_length=40, blank=True,null=True)
    key_expires = models.DateTimeField(_('key_expires joined'),blank=True,null=True)
    objects = AuthUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """ Return the full name for the user."""
        return self.username

    def get_short_name(self):
        """ Return the short name for the user."""
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username

class AuthUser(AbstractAuthUser):

    class Meta(AbstractAuthUser.Meta):
            swappable = 'AUTH_USER_MODEL'


