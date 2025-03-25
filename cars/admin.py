from django.contrib import admin
from .models import Car, Favorite

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'model', 'year', 'price', 'created_at')
    list_filter = ('brand', 'year')
    search_fields = ('brand', 'name', 'model')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('user', 'car')
    ordering = ('-created_at',)
