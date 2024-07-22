from django.contrib import admin
from django.urls import path
from client.views import login, callback, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('profile/', profile, name='profile'),
]

