"""
Django URL 配置文件
主要功能：
1. 定义项目的所有 URL 路由规则
2. 将 URL 请求映射到对应的视图函数
3. 处理静态文件和媒体文件的访问
4. 配置管理后台路由
"""

from django.contrib import admin  # 导入 admin 模块用于后台管理
from django.urls import path, include  # 导入 URL 处理工具
from django.conf import settings  # 导入项目设置
from django.conf.urls.static import static  # 导入静态文件处理工具
from django.contrib.auth import views as auth_views
from . import views  # 确保导入视图
from cars.views import register, search, my_favorites, toggle_favorite  # 导入需要的视图函数

# URL 模式列表，定义所有的 URL 路由规则
urlpatterns = [
    # 后台管理界面的 URL 配置
    path('admin/', admin.site.urls),
    
    # 包含汽车应用的 URL 配置
    # 所有以 cars/ 开头的 URL 都会转到 cars.urls 处理
    path('cars/', include('cars.urls')),
    
    # 网站首页的 URL 配置
    path('', include('cars.urls')),  # 将根目录也指向cars.urls，这样就可以直接访问car_list
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', register, name='register'),  # 添加注册页面URL
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # 搜索URL配置
    path('search/', search, name='search'),
    
    # 收藏相关URL配置
    path('favorites/', my_favorites, name='my_favorites'),
    path('favorite/<int:car_id>/', toggle_favorite, name='toggle_favorite'),
]

# 开发环境下配置媒体文件的访问 URL
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# 配置错误页面的处理器
handler404 = 'car_collection.views.custom_404'  # 处理页面未找到错误
handler500 = 'car_collection.views.custom_500'  # 处理服务器内部错误
