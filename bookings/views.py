from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django import forms
from django.utils import timezone
 
from .models import Room, Booking, RoomFeatures
 
 
 
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
 
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        room = cleaned_data.get('room')
 
        if start_time and end_time:
            if room:
                overlapping = Booking.objects.filter(
                    room=room,
                    status__in=['pending', 'confirmed'],
                    start_time__lt=end_time,
                    end_time__gt=start_time,
                )
                if overlapping.exists():
                    raise forms.ValidationError('Кімната вже зайнята на обраний період.')
 
        return cleaned_data
 
 
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

 
def booking_create(request, pk=None):
    initial = {}
    if pk:
        room = get_object_or_404(Room, pk=pk, is_active=True)
        initial['room'] = room
 
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Бронювання успішно створено!')
            return redirect('my_bookings')
    else:
        form = BookingForm(initial=initial)
 
    return render(request, 'bookings/booking_create.html', {'form': form})
 
 
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
 
 