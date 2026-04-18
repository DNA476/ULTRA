from django import forms

from core.form_utils import apply_bootstrap_styles

from .models import EmployeeProfile


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['user', 'role', 'phone', 'hire_date', 'is_active', 'notes']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_styles(self)
