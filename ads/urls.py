from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('new_ad/', views.new_ad_form, name='new_ad'),
    path('auth/', LoginView.as_view(template_name='auth.html'), name='auth'),
    path('register/', views.register, name='register'),
    path('ad/<int:id>/', views.ad, name='ad'),
    path('ad/<int:id>/edit/', views.ad_edit, name='ad_edit'),
    path('no_access/', views.no_access, name='no_access'),
    path('ad/<int:id>/delete/', views.ad_delete, name='ad_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)