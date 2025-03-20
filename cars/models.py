from django.db import models
from django.contrib.auth.models import User

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
