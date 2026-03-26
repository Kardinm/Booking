from django.contrib import admin
from .models import Room, Booking, RoomFeatures


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'capacity', 'room_area', 'price_per_hour', 'price_per_day', 'is_active']
    list_filter = ['room_type', 'is_active']
    search_fields = ['name', 'description', 'room_type']
    list_editable = ['price_per_hour', 'price_per_day', 'is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'start_time', 'end_time', 'status', 'created_at']
    list_filter = ['status', 'room', 'created_at']
    search_fields = ['user__username', 'user__email', 'room__name']
    list_editable = ['status']


@admin.register(RoomFeatures)
class RoomFeaturesAdmin(admin.ModelAdmin):
    list_display = ['room', 'has_wifi', 'has_air_conditioning', 'has_heating', 'has_tv', 'has_kitchen', 'has_fridge', 'has_shower']
    list_filter = ['room']
