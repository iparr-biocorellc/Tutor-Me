from django import forms
from .models import Availability


# class AvailabilityForm(forms.ModelForm):
#     class Meta:
#         model = Availability
#         fields = ('start', 'end')
#         widgets = {
#             'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'end': forms.DateTimeInput(attrs={'type': 'datetime-local'})
#         }

