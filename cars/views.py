from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Car, Favorite, Post, Comment
from .forms import PostForm, CommentForm, CarForm

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

# 论坛相关视图
@login_required
def post_list(request):
    """论坛帖子列表"""
    posts = Post.objects.all()
    return render(request, 'forum/post_list.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    """帖子详情"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
        
    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def create_post(request):
    """创建新帖子"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    return render(request, 'forum/create_post.html', {'form': form})

# 搜索功能
def search(request):
    """搜索车辆和帖子"""
    query = request.GET.get('q', '')
    
    if query:
        # 搜索车辆
        cars = Car.objects.filter(
            Q(model__icontains=query) |
            Q(brand__icontains=query) |
            Q(name__icontains=query)
        )
        
        # 搜索帖子
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        cars = Car.objects.none()
        posts = Post.objects.none()
        
    return render(request, 'search/results.html', {
        'query': query,
        'cars': cars,
        'posts': posts
    })

def cars_by_year(request, year):
    """按年份显示车辆列表"""
    cars = Car.objects.filter(year=year)
    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'year': year
    })

@login_required
def add_car(request):
    """添加新车辆"""
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm()
    
    return render(request, 'cars/car_form.html', {
        'form': form,
        'title': '添加新车辆'
    })

@login_required
def edit_car(request, car_id):
    """编辑车辆信息"""
    car = get_object_or_404(Car, id=car_id)
    
    # 检查是否是车主
    if car.owner != request.user:
        return redirect('car_detail', car_id=car_id)
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car_id)
    else:
        form = CarForm(instance=car)
    
    return render(request, 'cars/car_form.html', {
        'form': form,
        'title': '编辑车辆信息',
        'car': car
    })

@login_required
def delete_car(request, car_id):
    """删除车辆"""
    car = get_object_or_404(Car, id=car_id)
    
    # 检查是否是车主
    if car.owner != request.user:
        return redirect('car_detail', car_id=car_id)
    
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    
    return render(request, 'cars/car_confirm_delete.html', {
        'car': car
    })
