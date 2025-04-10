from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('new_ad/', views.new_ad_form, name='new_ad'),
    path('success_new_ad/', views.success_new_ad, name='success_new_ad'),
    path('auth/', LoginView.as_view(template_name='auth.html'), name='auth'),
    path('register/', views.register, name='register'),
    path('ad/', views.ad, name='ad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)