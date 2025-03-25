from django.db import models # 导入模型基类 
from django.contrib.auth.models import User # 导入用户模型，用于关联车主

class Car(models.Model):
    name = models.CharField(max_length=200, verbose_name='车名')
    brand = models.CharField(max_length=100, verbose_name='品牌')
    model = models.CharField(max_length=100, verbose_name='型号')
    year = models.IntegerField(verbose_name='年份')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    description = models.TextField(verbose_name='描述')
    image = models.ImageField(upload_to='cars/', verbose_name='图片')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20,
        choices=[
            ('SPORTS', '跑车'),
            ('SUV', 'SUV'),
            ('SEDAN', '轿车'),
            ('HATCHBACK', '掀背车')
        ],
        verbose_name='车型',
        default='SEDAN'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='车主')

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"

    class Meta:
        verbose_name = '车辆'
        verbose_name_plural = '车辆'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='车辆')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('user', 'car')

# 论坛帖子模型
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='作者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '帖子'
        verbose_name_plural = '帖子列表'

# 评论模型
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='帖子'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='作者'
    )
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论列表'
