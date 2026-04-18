from django import forms

from core.form_utils import apply_bootstrap_styles

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contact_person', 'phone', 'email', 'city', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_styles(self)
