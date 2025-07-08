from django import forms
from .models import Event

class EventCreationForm(forms.ModelForm):
    class Meta:
        model  = Event
        fields = ['title', 'description', 'poster', 'venue', 'size', 'price']


class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'poster', 'venue', 'size', 'price']


