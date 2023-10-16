from django.urls import path, include
from vendor import views
from accounts import views as AccountView

urlpatterns = [
    path('', AccountView.vendordashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile')
]
