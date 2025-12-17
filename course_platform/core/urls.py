from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('playlist/<int:id>/', views.playlist, name='playlist'),
    path('watch-video/<int:id>/', views.watch_video, name='watch_video'),
    path('teachers/', views.teachers, name='teachers'),
    path('teacher/<str:username>/', views.teacher_profile, name='teacher_profile'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
