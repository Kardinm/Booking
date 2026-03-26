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

    room_area = models.DecimalField(verbose_name='Площа', decimal_places=2, max_digits=5)

    price_per_hour = models.DecimalField( verbose_name='Ціна за годину', decimal_places=2, max_digits=5)
    price_per_day = models.DecimalField(verbose_name='Ціна за день', decimal_places=2, max_digits=5)

    description = models.TextField(blank=True, verbose_name='Опис')

    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        ordering = ['name']
    


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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено')
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.room.name} - {self.user.username} ({self.start_time.date()})"


class RoomFeatures(models.Model):
    room = models.OneToOneField(
        'Room',
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Приміщення',
    )

    
    has_wifi = models.BooleanField(
        default=False,
        verbose_name='Wi-Fi',
    )
   
    
    has_air_conditioning = models.BooleanField(
        default=False,
        verbose_name='Кондиціонер',
    )
    
    has_heating = models.BooleanField(
        default=False,
        verbose_name='Опалення',
    )
    
    
    has_tv = models.BooleanField(
        default=False,
        verbose_name='Телевізор',
    )


    has_kitchen = models.BooleanField(
        default=False,
        verbose_name='Кухня',
    )
    
    has_fridge = models.BooleanField(
        default=False,
        verbose_name='Холодильник',
    )
    


    
    has_shower = models.BooleanField(
        default=False,
        verbose_name='Душ',
    )
    
    
#----------------------------------------




