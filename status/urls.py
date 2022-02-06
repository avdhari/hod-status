from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name="home"),
    path('base/', views.base_view, name="base"),
    path('register/', views.register_request, name="register"),
    path('new-progress/', views.new_progress, name="new-progress"),
    path('password-reset/', views.password_reset, name="password-reset"),
    path('users/', views.user_list_view, name="users"),
    path('users/<int:pk>', views.user_detail_view, name="user-detail"),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
