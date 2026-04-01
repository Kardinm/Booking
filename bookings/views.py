from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django import forms
from django.utils import timezone

from .models import Room, Booking, RoomFeatures



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'start_time', 'end_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'notes': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control',
                       'placeholder': 'Додаткові коментарі...'}
            ),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        room = cleaned_data.get('room')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError('Час завершення має бути після початку бронювання.')

            if start_time < timezone.now():
                raise forms.ValidationError('Не можна бронювати на минулий час.')

            if room:
                overlapping = Booking.objects.filter(
                    room=room,
                    status__in=['pending', 'confirmed'],
                    start_time__lt=end_time,
                    end_time__gt=start_time,
                )
                if self.instance.pk:
                    overlapping = overlapping.exclude(pk=self.instance.pk)
                if overlapping.exists():
                    raise forms.ValidationError(
                        'Ця кімната вже зайнята на обраний період. Оберіть інший час.'
                    )
                

        return cleaned_data





def login_view(request):
    if request.user.is_authenticated:
        return redirect('room_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вітаємо, {user.username}!')
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('room_list')
        else:
            messages.error(request, 'Невірний логін або пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('room_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Реєстрація успішна! Вітаємо, {user.username}!')
            return redirect('room_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Ви успішно вийшли з системи.')
    return redirect('room_list')





def room_list(request):
    room_type = request.GET.get('room_type', '')
    rooms = Room.objects.filter(is_active=True)

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    return render(request, 'bookings/room_list.html', {
        'rooms': rooms,
        'room_types': Room.ROOM_TYPES,
        'selected_type': room_type,
    })


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk, is_active=True)
    features = getattr(room, 'features', None)

    upcoming_bookings = Booking.objects.filter(
        room=room,
        status__in=['pending', 'confirmed'],
        end_time__gte=timezone.now(),
    ).order_by('start_time')

    return render(request, 'bookings/room_detail.html', {
        'room': room,
        'features': features,
        'upcoming_bookings': upcoming_bookings,
    })





@login_required
def booking_create(request, pk=None):
    initial = {}
    preselected_room = None

    if pk:
        preselected_room = get_object_or_404(Room, pk=pk, is_active=True)
        initial['room'] = preselected_room

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Бронювання успішно створено! Очікуйте підтвердження.')
            return redirect('my_bookings')
        else:
            messages.error(request, 'Перевірте правильність введених даних.')
    else:
        form = BookingForm(initial=initial)

    return render(request, 'bookings/booking_create.html', {
        'form': form,
        'preselected_room': preselected_room,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-created_at')
    active_count = bookings.filter(status__in=['pending', 'confirmed']).count()
    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings,
        'active_count': active_count,
    })


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Бронювання скасовано.')
        else:
            messages.warning(request, 'Це бронювання не можна скасувати.')
    return redirect('my_bookings')