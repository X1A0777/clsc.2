"""
Django 项目的主配置文件
包含了项目的所有全局设置
"""

from pathlib import Path
import os

# 构建项目根目录的绝对路径
# BASE_DIR 指向包含 manage.py 的目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全设置
# SECURITY WARNING: 在生产环境中要保密密钥
SECRET_KEY = 'your-secret-key-here'  # 用于加密签名，session等

# SECURITY WARNING: 生产环境中要设置为 False
DEBUG = True  # 调试模式开关

# 允许访问的主机列表
ALLOWED_HOSTS = [
    'xjy.pythonanywhere.com',  # PythonAnywhere 域名
    'localhost',               # 本地开发服务器
    '127.0.0.1'               # 本地 IP
]

# 安装的应用列表
INSTALLED_APPS = [
    'django.contrib.admin',        # 管理后台
    'django.contrib.auth',         # 认证系统
    'django.contrib.contenttypes', # 内容类型框架
    'django.contrib.sessions',     # 会话框架
    'django.contrib.messages',     # 消息框架
    'django.contrib.staticfiles',  # 静态文件管理
    'cars.apps.CarsConfig',       # 汽车应用
]

# 中间件设置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware',   # 会话中间件
    'django.middleware.common.CommonMiddleware',              # 通用中间件
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF 保护
    'django.contrib.auth.middleware.AuthenticationMiddleware',# 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',   # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 点击劫持保护
]

# 项目的 URL 配置文件路径
ROOT_URLCONF = 'car_collection.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 模板引擎
        'DIRS': [BASE_DIR / 'templates'],    # 模板目录列表
        'APP_DIRS': True,                    # 是否在应用中查找模板
        'OPTIONS': {
            'context_processors': [          # 上下文处理器
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用的路径
WSGI_APPLICATION = 'car_collection.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',        # 数据库引擎
        'NAME': BASE_DIR / 'db.sqlite3',              # 数据库文件路径
    }
}

# 密码验证设置
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化设置
LANGUAGE_CODE = 'zh-hans'    # 使用中文
TIME_ZONE = 'Asia/Shanghai'  # 使用中国时区
USE_I18N = True             # 启用国际化
USE_TZ = True              # 启用时区支持

# 静态文件设置 (CSS, JavaScript, Images)
STATIC_URL = 'static/'      # 静态文件 URL 前缀
STATIC_ROOT = BASE_DIR / 'staticfiles'  # 收集的静态文件存储目录
STATICFILES_DIRS = [        # 额外的静态文件目录
    BASE_DIR / 'static',
]

# 媒体文件设置
MEDIA_URL = 'media/'        # 媒体文件 URL 前缀
MEDIA_ROOT = BASE_DIR / 'media'  # 媒体文件存储目录

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登录设置
LOGIN_URL = 'login'         # 登录页面 URL
LOGIN_REDIRECT_URL = 'car_list' # 登录成功后重定向 URL
LOGOUT_REDIRECT_URL = 'car_list'# 登出后重定向 URL

# 邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'     # SMTP 服务器
EMAIL_PORT = 587                    # SMTP 端口
EMAIL_USE_TLS = True               # 使用 TLS 加密
EMAIL_HOST_USER = 'your@email.com' # 邮箱账号
EMAIL_HOST_PASSWORD = 'password'   # 邮箱密码

# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# 会话设置
SESSION_COOKIE_AGE = 1209600  # 会话cookie过期时间（2周）
SESSION_SAVE_EVERY_REQUEST = True  # 每次请求都保存会话

# 安全设置
SECURE_SSL_REDIRECT = False  # 是否强制 HTTPS
CSRF_COOKIE_SECURE = False  # 是否仅通过 HTTPS 发送 CSRF cookie
SESSION_COOKIE_SECURE = False  # 是否仅通过 HTTPS 发送会话 cookie
