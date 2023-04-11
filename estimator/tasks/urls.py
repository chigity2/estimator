from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('complete/<int:id>', views.complete, name='complete'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('log', views.logs, name='log'),
    path('log/<int:id>/complete', views.complete_task, name='complete_task'),
    path('log/<int:id>/cancel', views.cancel_task, name='cancel_task'),
    path('log/dr', views.daily_recap, name='daily_recap'),
    path('profile', views.profile, name='profile')
]
