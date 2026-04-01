from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),

    path('booking/new/', views.booking_create, name='booking_create'),
    path('booking/new/<int:pk>/', views.booking_create, name='booking_create_for_room'),
    path('booking/my/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]