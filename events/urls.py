from django.contrib import admin
from django.urls import path
from events.views import event_list,event_details,create_event,show_participants,add_participant,show_category,delete_event,update_event,organizer_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event-list/', event_list, name='event-list'),
    path('event-details/<int:event_id>/', event_details, name='event-details'),
    path('create-event/', create_event, name='create-event'),
    path('participants/', show_participants, name='participants'),
    path('add-participant/',add_participant,name='add-participant'),
    path('categories/',show_category, name='categories'),
    path('delete-event/<int:event_id>/', delete_event, name='delete-event'),
    path('update-event/<int:event_id>/', update_event, name='update-event'),
    path('organizer-dashboard/',organizer_dashboard,name='organizer-dashboard'),

]