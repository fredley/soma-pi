from django import forms
from soma_pi.models import Station


class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = ('name','image','description','url',)
