from django.urls import path

from . import views




urlpatterns = [
    path('', views.TasksView, name='tasks'),
    path('', include(frontend.urls))
]