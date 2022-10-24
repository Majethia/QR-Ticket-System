from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('import/', views.import_data),
]
