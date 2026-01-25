from django import forms
from .models import Event



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category','image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border rounded p-2 mt-5 w-full',
                'placeholder': 'Event name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border rounded p-2 mt-10 w-full',
                'rows': 4,
                'placeholder': 'Event description'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border rounded p-2 mt-10 w-full'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'border rounded p-2 mt-10 w-full'
            }),
            'location': forms.TextInput(attrs={
                'class': 'border rounded p-2 mt-10 w-full',
                'placeholder': 'Event location'
            }),
            'category': forms.Select(attrs={
                'class': 'border rounded p-2 mt-10 w-full'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'border rounded p-2 mt-10 w-full'
            }),
        }
    

# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = ['name', 'email','event']  
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'border rounded p-2 mt-5 w-full',
#                 'placeholder': 'Participant name'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'border rounded p-2 mt-5 w-full',
#                 'placeholder': 'Participant email'
#             }),
#             'event': forms.SelectMultiple(attrs={  
#                 'class': 'border rounded p-2 mt-5 w-full', 
#             }),
#         }

