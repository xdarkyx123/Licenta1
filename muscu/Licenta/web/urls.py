from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/',views.detail ,name='detail'),
    path('recommend/',views.recommend,name='recommend'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
       ]