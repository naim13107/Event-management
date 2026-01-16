from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from events.forms import EventForm,ParticipantForm
from django.contrib import messages
from events.models import Event,Participant,Category
from django.db.models import Q , Count
from django.utils import timezone

# Create your views here.

def event_list(request):
    query = request.GET.get('q')  

    events = Event.objects.select_related('category').prefetch_related('participants')
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))
    context = {'events': events}
    return render(request, 'event_list.html', context)

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event_details.html', {'event': event})

def create_event(request):
    event_form = EventForm()
    participant_form = ParticipantForm()
    
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid() :

            event = event_form.save()

            messages.success(request ,'Event created successfully')
            return redirect('create-event')
            
        

    context = {"event_form": event_form,
               "participant_form":participant_form}
    
    return render(request,'event_form.html',context)

def update_event(request,event_id):
    event = Event.objects.get(id = event_id)
    
    if event :
        event_form = EventForm(instance=event)

    if request.method == 'POST':
        event_form = EventForm(request.POST,instance=event)

        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event updated successfully")
            return redirect('update-event',event_id)
    context = {'event_form': event_form}
    return render(request,'event_form.html',context)    


def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
    else:
        messages.error(request, 'Invalid request method')
    
    return redirect('event-list') 

def show_participants(request):
    participants = Participant.objects.prefetch_related('event')
    return render(request,'participants.html',{'participants' : participants})

def add_participant(request):
    participant_form = ParticipantForm()

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        if participant_form.is_valid():
            participant = participant_form.save()  
            messages.success(request, f"Participant '{participant.name}' added successfully!")
            return redirect('add-participant')  

    
    return render(request, 'add_participant.html', {'participant_form':participant_form})

from django.shortcuts import render
from events.models import Category, Event

def show_category(request):
    type_name = request.GET.get('type', 'all')

    categories = Category.objects.prefetch_related('events')

    if type_name == 'all':
        events = Event.objects.select_related('category')
        selected_type = 'All Categories'
    else:
        category = categories.filter(name=type_name).first()
        events = category.events.all() if category else Event.objects.none()
        selected_type = category.name if category else 'Unknown Category'

    return render(request, 'category.html', {
        'categories': categories,
        'events': events,
        'selected_type': selected_type
    })


def organizer_dashboard(request):
    today = timezone.now().date()  

    stats = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events_count=Count('id', filter=Q(date__gte=today)),
        past_events_count=Count('id', filter=Q(date__lt=today))
    )
    total_participants = Participant.objects.count()  # Single query

    total_events = stats['total_events']
    upcoming_events_count = stats['upcoming_events_count']
    past_events_count = stats['past_events_count']

    filter_type = request.GET.get('filter', 'today')

    if filter_type == 'upcoming':
        events = Event.objects.filter(date__gte=today).order_by('date', 'time')
    elif filter_type == 'past':
        events = Event.objects.filter(date__lt=today).order_by('-date', '-time')
    elif filter_type == 'today':  
        events = Event.objects.filter(date=today).order_by('time')
    elif filter_type == 'participants':  
        events = Event.objects.filter(date=today).order_by('time')
    else :
        events=Event.objects.all()

  
    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'events': events,
        'filter_type': filter_type
    }

    return render(request, 'organizer_dashboard.html', context)