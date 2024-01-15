from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import lista_productos, detalle_producto, agregar_carrito


urlpatterns = [
	path('', views.feed, name='feed'),
	path('profile/', views.profile, name='profile'),
	path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile_photo/', views.edit_profile_photo, name='edit_profile_photo'),
	path('register/', views.register, name='register'),
	path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
	path('post/', views.post, name='post'),
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('productos/', lista_productos, name='lista_productos'), 
    path('productos/<int:producto_id>/', detalle_producto, name='detalle_producto'), 
    path('agregar-carrito/<int:producto_id>/', agregar_carrito, name='agregar_carrito'),
    

]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

