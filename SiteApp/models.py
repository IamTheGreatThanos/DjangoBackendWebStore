import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """
        Создает и возвращает пользователя с правами
        суперпользователя (администратора).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = None
    # email = models.EmailField(
    #     validators=[validators.validate_email],
    #     unique=True,
    #     blank=False,
    #     default=''
    # )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()
    # Сообщает Django, что класс UserManager, определенный выше,
    # должен управлять объектами этого типа.
    objects = UserManager()

    def __str__(self):
        return self.username

    def displayID(self):
        # return ', '.join([genre.name for genre in self.genre.all()[:3]])
        return 'User ID: ' + str(self.pk)

    displayID.short_description = 'ID'

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        # return self._generate_jwt_token()

        return self.create_auth_token()

    # @receiver(post_save, sender=User)
    def create_auth_token(self, instance=None, created=False, **kwargs):
        token, _ = Token.objects.get_or_create(user=self)
        return token.key

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=1024, null=True)
    price = models.IntegerField(null=True)
    image = models.CharField(max_length=255, default='https://tracerproducts.com/wp-content/uploads/2019/12/Product-Image-Coming-Soon.jpg')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=2)
    in_stock = models.BooleanField(null=True, default=False)
    code = models.CharField(max_length=255, null=True, default='XXXXXX')
    rating = models.FloatField(null=True, default=5.0)


