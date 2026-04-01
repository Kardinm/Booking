from django.contrib import admin
from .models import Room, Booking, RoomFeatures


class RoomFeaturesInline(admin.StackedInline):
    model = RoomFeatures
    can_delete = False
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'capacity', 'room_area',
                    'price_per_hour', 'price_per_day', 'is_active']
    list_filter = ['room_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price_per_hour', 'price_per_day', 'is_active']
    inlines = [RoomFeaturesInline]
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'room_type', 'description', 'is_active')
        }),
        ('Параметри', {
            'fields': ('capacity', 'room_area', 'price_per_hour', 'price_per_day')
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'start_time', 'end_time', 'status', 'created_at']
    list_filter = ['status', 'room', 'created_at']
    search_fields = ['user__username', 'user__email', 'room__name']
    list_editable = ['status']
    date_hierarchy = 'start_time'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RoomFeatures)
class RoomFeaturesAdmin(admin.ModelAdmin):
    list_display = ['room', 'has_wifi', 'has_air_conditioning', 'has_heating',
                    'has_tv', 'has_projector', 'has_whiteboard',
                    'has_kitchen', 'has_fridge', 'has_shower', 'has_parking']
    list_filter = ['has_wifi', 'has_projector', 'has_parking']