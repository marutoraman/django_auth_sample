python -m venv vnev
pip install django
django-admin startproject app .
python manage.py startapp my_app
python manage.py startapp users

settings.pyのINSTALLED_APPSに
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_app', # add
    'users' # add
]
```

python manage.py runserver

users/models.pyを以下の通りに編集
```
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
import ulid


class CustomUserManager(UserManager):
    '''
    Userを作成するための処理
    Userの項目が変更になっているので、こちらも変更の必要がある
    '''    
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, email=None, password=None, **extra_fields):
        '''
        一般ユーザーを作成する処理
        '''
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        '''
        管理者ユーザーを作成する処理
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    '''
    カスタムUser
    AbstractBaseUser: 標準のUserモデル
    ※AbstractUserというモデルもあり、これを継承することもできるが、柔軟性が低くなるため非推奨(項目を追加するのみ等の微小なカスタマイズの場合はOK)
    PermissionsMixin: 権限関連のモデル
    '''    
    
    '''
    必須項目
    '''
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False) # idは推測されずらく重複しないように、ulidを使用する
    email = models.EmailField(_('メールアドレス'), blank=False, unique=True, db_index=True) 
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    # UserManagerを指定
    objects = CustomUserManager()

    '''
    カスタマイズ項目 必要な項目は以下のように追加する
    '''
    nickname = models.CharField(_('ニックネーム'), max_length=32, blank=True)
    gender = models.IntegerField(_('性別'), blank=True, default=0)
    
    
    '''
    フィールド設定
    '''
    # emailの項目名を指定
    EMAIL_FIELD = 'email'
    # ログイン時にIDになる項目名を指定
    USERNAME_FIELD = 'email'
    # 必須入力とする項目名(USERNAME_FIELDに指定した項目は必ず指定する前提のため指定しない)
    REQUIRED_FIELDS = ['nickname', ]
    
    
    class Meta:
        '''
        テーブル定義(基本は変更しない)
        '''
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = "auth_user"

    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def get_full_name(self):
        return self.full_name


    def get_short_name(self):
        return self.full_name

```

settings.pyを以下を追記
```
AUTH_USER_MODEL = 'users.User'
```

管理者ユーザーを作成
python manage.py createsuperuser

python manage.py runserver 

以下にアクセスしてログインできればOK
http://127.0.0.1:8000/admin

Auth0設定
settings.py
INSTALLED_APPS に
'social_django',
を追加
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django', # add
    'my_app',
    'users'
]
 

```

Applications > Applications > Create Application
Name: 任意
Choose an application type: Regular Web Applications
Create
Django
Settings

Domain
Client ID
Client Secret
を控える

settings.py に以下を追記（Domain等は控えたものを入れる）
```
# Auth0
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = '<Domain>'
SOCIAL_AUTH_AUTH0_KEY = '<Client ID>'
SOCIAL_AUTH_AUTH0_SECRET = '<Client Secret>'

SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]

AUTHENTICATION_BACKENDS = {
    'users.auth0backend.Auth0',
    'django.contrib.auth.backends.ModelBackend'
}

SOCIAL_AUTH_URL_NAMESPACE = 'users:social'     

LOGIN_URL = 'users/login/auth0'
LOGIN_REDIRECT_URL = '/dashboard'

```

Application URIs > Allowed Callback URLs
http://127.0.0.1:8000/users/complete/auth0

Settings > General > Langurges > Default Language > Japansese
Save

