from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .forms import AdFilterView, CustomLoginView

urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('auth/', CustomLoginView.as_view(), name='auth'),
    path('register/', views.register, name='register'),
    path('new_ad/', views.new_ad_form, name='new_ad'),
    path('ad/<int:id>/', views.ad, name='ad'),
    path('ad/<int:id>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<int:id>/delete/', views.ad_delete, name='ad_delete'),
    path('ad/<int:id>/exchange/', views.ad_exсhange, name='ad_exсhange'),
    path('exchange/<int:id>/', views.exchange, name='exchange'),
    path('exchange/<int:id>/update/', views.exchange_update, name='exchange_update'),
    path('no_access/', views.no_access, name='no_access'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)