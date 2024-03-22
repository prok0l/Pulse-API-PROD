from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, login, email, countryCode, isPublic,
                    password=None):
        if not email:
            return ValueError('Not Email')

        user = self.model(email=self.normalize_email(email))
        user.login = login
        user.email = email
        user.countryCode = countryCode
        user.isPublic = isPublic
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    login = models.CharField(max_length=30, unique=True, validators=[
        RegexValidator(
            regex=r'^(?!me$)[a-zA-Z0-9-]+$',
            message="Логин не удовлетворяет требованиям"
        )
    ])
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100, validators=[RegexValidator(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{6,100}$',
        message="Пароль не удовлетворяет требованиям"
    )])
    countryCode = models.CharField(max_length=2)
    isPublic = models.BooleanField()
    phone = models.CharField(max_length=20, blank=True, null=True,
                             validators=[RegexValidator(
                                 regex=r'^\+[\d]+$',
                                 message="Телефон не удовлетворяет требованиям"
                             )],
                             unique=True)
    image = models.URLField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = "users"

    USERNAME_FIELD = 'login'

    objects = UserManager()

    def __str__(self):
        return self.login
