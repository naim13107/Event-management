from django.contrib import admin
from django.urls import path
from events.views import event_list, event_details, rsvp_event,CreateEvent,CreateCategory, show_category, DeleteEvent, UpdateEvent, OrganizerDashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('event-list/', event_list, name='event-list'),
    path('event-details/<int:event_id>/', event_details, name='event-details'),
    # path('create-event/', create_event, name='create-event'),
    path('create-event/', CreateEvent.as_view(), name='create-event'),
    path('categories/', show_category, name='categories'),
    # path('delete-event/<int:event_id>/', delete_event, name='delete-event'),
    path('delete-event/<int:event_id>/', DeleteEvent.as_view(), name='delete-event'),
    # path('update-event/<int:event_id>/', update_event, name='update-event'),
    path('update-event/<int:event_id>/', UpdateEvent.as_view(), name='update-event'),
    # path('organizer-dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('organizer-dashboard/', OrganizerDashboard.as_view(), name='organizer-dashboard'),
    path('create-category/', CreateCategory.as_view(), name='create-category'),
    path('rsvp/<int:event_id>/', rsvp_event, name='rsvp-event'),
   
]