"""
Cars 应用的 URL 配置文件
处理所有与汽车相关的 URL 路由
"""

from django.urls import path
from . import views  # 导入当前应用的视图

urlpatterns = [
    # 根路径，直接显示车辆列表
    path('', 
         views.car_list, 
         name='car_list'),  # 使用 name 便于在模板中引用
    
    # 汽车列表页面
    path('list/', 
         views.car_list, 
         name='car_list'),  # 使用 name 便于在模板中引用
    
    # 汽车详情页面，接收 car_id 参数
    path('detail/<int:car_id>/',
         views.car_detail,
         name='car_detail'),
    
    # 添加新汽车的页面
    path('add/',
         views.add_car,
         name='add_car'),
    
    # 编辑汽车信息
    path('edit/<int:car_id>/',
         views.edit_car,
         name='edit_car'),
    
    # 删除汽车
    path('delete/<int:car_id>/',
         views.delete_car,
         name='delete_car'),
    
    # 论坛 URLs
    path('forum/', views.post_list, name='post_list'),
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/create/', views.create_post, name='create_post'),
    
    # 收藏相关URL
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('favorite/<int:car_id>/', views.toggle_favorite, name='toggle_favorite'),
]

# URL 使用示例：
"""
在模板中使用：
{% url 'cars:car_detail' car_id=1 %}

在视图中使用：
from django.urls import reverse
url = reverse('cars:car_detail', args=[1])
用户访问 xjy.pythonanywhere.com/cars/
↓
wsgi.py 接收请求
↓
settings.py 检查 ALLOWED_HOSTS
↓
urls.py 路由到 cars.urls
↓
cars/views.py 处理请求
↓
models.py 获取数据
↓
返回响应
""" 