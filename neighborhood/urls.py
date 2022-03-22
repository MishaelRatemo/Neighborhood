from django.urls import  path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),    
    path('post/new', views.new_post, name='new_post'),
    path('view/post/<int:id>', views.view_post, name='view_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/<username>/edit', views.edit_profile, name='edit_profile'),    
    path('search/', views.search_business, name='search'),
    path('alerts/', views.alerts, name='alerts'),
    path('new/alert/', views.new_alert, name='new_alert'),    
    path('business/', views.shops, name='business'),
    path('new/business/', views.new_shop, name='new_business'), 
    path('logout', views.logout, name='logout'),
]