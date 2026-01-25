from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from events.forms import EventForm
from django.contrib import messages
from events.models import Event, Category
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists() or user.is_superuser

def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser



def event_list(request):
    query = request.GET.get('q')  

    events = Event.objects.select_related('category').prefetch_related('participants')
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))
    context = {'events': events}
    return render(request, 'event_list.html', context)

@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), id=event_id)
    return render(request, 'event_details.html', {'event': event})

@user_passes_test(is_organizer)
def create_event(request):
    event_form = EventForm()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event created successfully')
            return redirect('event-list')
    return render(request, 'event_form.html', {"event_form": event_form})

@user_passes_test(is_organizer)
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_form = EventForm(instance=event)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event updated successfully")
            return redirect('event-list')
    return render(request, 'event_form.html', {'event_form': event_form})

@user_passes_test(is_organizer)
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
    return redirect('event-list')



@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.participants.all():
        event.participants.remove(user)
        messages.info(request, f"You have withdrawn from {event.name}.")
    else:
        event.participants.add(user)
        messages.success(request, f"RSVP successful! A confirmation email is being sent.")

    return redirect('event-details', event_id=event.id)





@user_passes_test(is_organizer)
def organizer_dashboard(request):
    today = timezone.now().date()  
    stats = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events_count=Count('id', filter=Q(date__gte=today)),
        past_events_count=Count('id', filter=Q(date__lt=today))
    )
    
    total_participants = User.objects.exclude(is_superuser=True).count()

    filter_type = request.GET.get('filter', 'today')
    if filter_type == 'upcoming':
        events = Event.objects.filter(date__gte=today).order_by('date')
    elif filter_type == 'past':
        events = Event.objects.filter(date__lt=today).order_by('-date')
    else:
        events = Event.objects.all()

    context = {
        **stats,
        'total_participants': total_participants,
        'events': events,
        'filter_type': filter_type
    }
    return render(request, 'organizer_dashboard.html', context)


@user_passes_test(is_admin)
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Category.objects.create(name=name, description=description)
            messages.success(request, f"Category '{name}' created successfully!")
            return redirect('/users/admin-dashboard/?view=categories')
    return render(request, 'dashboard/create_category.html')


@user_passes_test(is_organizer)
def show_category(request):
    categories = Category.objects.annotate(event_count=Count('events'))
    type_name = request.GET.get('type', 'all')
    
    if type_name == 'all':
        events = Event.objects.all()
    else:
        events = Event.objects.filter(category__name=type_name)

    return render(request, 'category.html', {
        'categories': categories,
        'events': events,
        'selected_type': type_name
    })