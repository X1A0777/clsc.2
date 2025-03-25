from django.shortcuts import render

def custom_404(request, exception):
    """自定义404页面"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """自定义500页面"""
    return render(request, '500.html', status=500) 