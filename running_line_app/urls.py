from django.urls import path
from . import views

app_name = 'running_line_app'

urlpatterns = [
    path('<str:text>', views.generate_running_line, name='generate_running_line'),
    path('', views.generate, name='generate_page'),
]