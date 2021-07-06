from django import forms
from .models import Apply_Pass, District, TimeLimit, MovementReason, MovementType

class Apply_PassForm(forms.ModelForm):
    class Meta:
        model = Apply_Pass
        fields = ['location_from', 'where_to', 'district', 'thana', 'journey_date', 'time_limit', 'movement_type', 'movement_reason' ]
        widgets = {
            'location_from' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your location'}),
            'where_to' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your destination'}),
            'district' : forms.Select(attrs={'class':'form-control', 'empty':'Select District'}),
            'thana' : forms.TextInput(attrs={'class':'form-control'}),
            'journey_date' : forms.DateInput(attrs={'class':'form-control', 'type':'datetime-local'}),
            'time_limit' : forms.Select(attrs={'class':'form-control'}),
            'movement_type' : forms.Select(attrs={'class':'form-control'}),
            'movement_reason' : forms.Select(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.all()
        self.fields['district'].empty_label = "Select District"

        self.fields['time_limit'].queryset = TimeLimit.objects.all()
        self.fields['time_limit'].empty_label = "How long you stay there ?"

        self.fields['movement_type'].queryset = MovementType.objects.all()
        self.fields['movement_type'].empty_label = "Movement Type"
        
        self.fields['movement_reason'].queryset = MovementReason.objects.all()
        self.fields['movement_reason'].empty_label = "Movement Reason"

