from django import forms
from .models import Apply_Pass

class ApplyPassForm(forms.ModelForm):
    class Meta:
        model = Apply_Pass
        exclude = ['passuser', ]
