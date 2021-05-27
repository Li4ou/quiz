from .views import *

from django.urls import path

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Registration.as_view(), name='registration'),
]
