from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .models import Car, Favorite

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('car_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def car_list(request):
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, car=car).exists()
    return render(request, 'cars/car_detail.html', {'car': car, 'is_favorite': is_favorite})

@login_required
def toggle_favorite(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)
    if not created:
        favorite.delete()
    return redirect('car_detail', car_id=car_id)

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('car')
    return render(request, 'cars/my_favorites.html', {'favorites': favorites})

def logout_view(request):
    logout(request)
    messages.success(request, '您已成功退出登录！')
    return redirect('car_list')
