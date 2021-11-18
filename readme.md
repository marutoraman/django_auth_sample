```
python -m venv vnev  
```
```
pip install django
```
```
django-admin startproject app .
```

```
python manage.py startapp my_app
```

```
python manage.py startapp users
```

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

～中略～

LANGUAGE_CODE = 'ja-jp' 

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False
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

Branding > Unicersal Login > Customization
Company Logo
Primary Color
PAge Background Color
を自由に設定

デフォルトではパスワードの要求強度が強いので、必要に応じて以下を設定変更
Authentication > Database > Username-Password-Authentication > Password Policy > Password Strength
下から２番目　（８文字以上ならOK）
Save Changes


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
LOGOUT_URL = "/"

```

Application URIs > Allowed Callback URLs
http://127.0.0.1:8000/users/complete/auth0

Application URIs > Allowed Logout URLs
http://127.0.0.1:8000/

save

Settings > General > Langurges > Default Language > Japansese
Save

app/urls.py を以下のように編集
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('my_app/', include('my_app.urls')),
]
```

users/urls.py を以下通りに作成
```
app_name = "users"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    path('logout', logout_auth0, name="logout"),
]
```

users/views.py を以下のように記述
```
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from app.settings import LOGOUT_URL


def logout_auth0(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri(LOGOUT_URL)})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
```


users/auth0backend.pyを以下の通り作成
```
from urllib import request
from jose import jwt
from social_core.backends.oauth import BaseOAuth2


class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('picture', 'picture'),
        ('email', 'email')
    ]

    def authorization_url(self):
        return 'https://' + self.setting('DOMAIN') + '/authorize'

    def access_token_url(self):
        return 'https://' + self.setting('DOMAIN') + '/oauth/token'

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        id_token = response.get('id_token')
        jwks = request.urlopen('https://' + self.setting('DOMAIN') + '/.well-known/jwks.json')
        issuer = 'https://' + self.setting('DOMAIN') + '/'
        audience = self.setting('KEY')  # CLIENT_ID
        payload = jwt.decode(id_token, jwks.read(), algorithms=['RS256'], audience=audience, issuer=issuer)
        return {'username': payload['nickname'],
                'full_name': payload['name'],
                'picture': payload['picture'],
                'user_id': payload['sub'],
                'email': payload['email'],
                'email_verified': payload['email_verified']}

```

templatesを作成
templatesフォルダを作成、その配下にmy_appフォルダを作成

ログインページ(トップページ)
templates/index.html

```
<html>
<head>
</head>
<body>
    <p>トップページ</p>
    <a href="{% url 'users:login' %}auth0">ログイン</a>
</body>
</html>
```

ログイン後ページ
templates/my_app/dashboard.html
```
<html>
<head>
</head>
<body>
    <p>[ログイン中です] email: {{ user.email }}</p>
    <a href="{% url 'users:logout' %}">ログアウト</a>
</body>
</html>
```

ログイン要求ページ
templates/login_required.html
```
<html>
<head>
</head>
<body>
    <p>ログインが必要なページです。ログインしてください。</p>
    <a href="{% url 'users:login' %}auth0">ログイン</a>
</body>
</html>
```


```
settings.py のTEMPLATEDに以下を記述
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")], # この行をそのままコピー
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

ログインしていないと表示できないようにする

app/middleware.py を以下の通りに作成
```
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin 

class AuthMiddleware(MiddlewareMixin): 
    def process_response(self, request, response):
        '''
        認証系処理
        '''
        # トップ画面、ログイン処理画面はスルー
        if request.path == "/" or request.path.find("auth0") >= 1 or request.path == "/login_required" or request.path.find("logout") >= 1:
            return response
        
        # ログインしていない場合はログイン要求ページにリダイレクト
        if not request.user.is_authenticated: 
            return HttpResponseRedirect('/login_required') 
        
        return response

```

settings.py のMIDDLEWARE に以下の通りに追記
```

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.AuthMiddleware' # add
]
```
