from django.urls import path
from authuser import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
