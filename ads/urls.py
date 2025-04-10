from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('new_ad/', views.ad_form, name='new_ad'),
    path('success_new_ad/', views.success_new_ad, name='success_new_ad'),
    path('auth/', LoginView.as_view(template_name='auth.html'), name='auth'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('register', views.register, name='register'),
]
