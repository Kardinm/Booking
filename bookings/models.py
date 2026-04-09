from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    ROOM_TYPES = [
        ('relax', 'Відпочинок/Перебування'),
        ('meeting', 'Переговорна кімната'),
        ('office', 'Офісне приміщення'),
        ('event', 'Приміщення для заходів'),
        ('studio', 'Фото/відео/аудіо студія'),
    ]

    name = models.CharField(max_length=200, verbose_name='Назва')

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        default='meeting',
        verbose_name='Тип приміщення'
    )

    capacity = models.PositiveIntegerField(verbose_name='Вмістимість')

    room_area = models.DecimalField(
        verbose_name='Площа', decimal_places=2, max_digits=7
    )

    address = models.CharField(max_length=300, blank=True, verbose_name='Адреса')

    price_per_hour = models.DecimalField(
        verbose_name='Ціна за годину (грн)', decimal_places=2, max_digits=8
    )
    price_per_day = models.DecimalField(
        verbose_name='Ціна за день (грн)', decimal_places=2, max_digits=8
    )

    description = models.TextField(blank=True, verbose_name='Опис')

    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        ordering = ['name']
        verbose_name = 'Приміщення'

    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"

    def get_type_icon(self):
        icons = {
            'relax': 'bi-cup-hot',
            'meeting': 'bi-people',
            'office': 'bi-briefcase',
            'event': 'bi-calendar-event',
            'studio': 'bi-camera-video',
        }
        return icons.get(self.room_type, 'bi-building')


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Користувач'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Приміщення'
    )

    start_time = models.DateTimeField(verbose_name='Початок бронювання')
    end_time = models.DateTimeField(verbose_name='Кінець бронювання')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    notes = models.TextField(blank=True, verbose_name='Коментар')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено')

    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Бронювання'

    def duration_hours(self):
        delta = self.end_time - self.start_time
        return round(delta.total_seconds() / 3600, 1)

    def get_status_badge(self):
        badge_map = {
            'pending': 'warning',
            'confirmed': 'success',
            'cancelled': 'secondary',
            'completed': 'primary',
        }
        return badge_map.get(self.status, 'light')


class RoomFeatures(models.Model):
    room = models.OneToOneField(
        'Room',
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Приміщення',
    )

    has_wifi = models.BooleanField(default=False, verbose_name='Wi-Fi')
    has_air_conditioning = models.BooleanField(default=False, verbose_name='Кондиціонер')
    has_heating = models.BooleanField(default=False, verbose_name='Опалення')
    has_tv = models.BooleanField(default=False, verbose_name='Телевізор')
    has_projector = models.BooleanField(default=False, verbose_name='Проєктор')
    has_whiteboard = models.BooleanField(default=False, verbose_name='Дошка')
    has_kitchen = models.BooleanField(default=False, verbose_name='Кухня')
    has_fridge = models.BooleanField(default=False, verbose_name='Холодильник')
    has_shower = models.BooleanField(default=False, verbose_name='Душ')
    has_parking = models.BooleanField(default=False, verbose_name='Паркінг')

    class Meta:
        verbose_name = 'Характеристики приміщення'


    def __str__(self):
        return f"Характеристики: {self.room.name}"

    def active_features(self):
        fields = [
            ('has_wifi', 'Wi-Fi', 'bi-wifi'),
            ('has_air_conditioning', 'Кондиціонер', 'bi-thermometer-snow'),
            ('has_heating', 'Опалення', 'bi-thermometer-sun'),
            ('has_tv', 'Телевізор', 'bi-tv'),
            ('has_projector', 'Проєктор', 'bi-projector'),
            ('has_whiteboard', 'Дошка', 'bi-easel'),
            ('has_kitchen', 'Кухня', 'bi-cup-straw'),
            ('has_fridge', 'Холодильник', 'bi-snow'),
            ('has_shower', 'Душ', 'bi-droplet'),
            ('has_parking', 'Паркінг', 'bi-p-square'),
        ]
        return [(label, icon) for field, label, icon in fields if getattr(self, field)]