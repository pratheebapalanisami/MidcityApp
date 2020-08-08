from django import forms
from .models import Event, Volunteership
from django.db.models import F


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('user', 'created_at',)

    def is_valid(self):
        valid = super(CreateEventForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        event = super(CreateEventForm, self).save(commit=False)
        if commit:
            event.save()
        return event


class ApplyEventForm(forms.ModelForm):
    class Meta:
        model = Volunteership
        fields = ('event',)


class VolunteershipForm(forms.ModelForm):
    class Meta:
        model = Volunteership
        fields = ('attendance',)
