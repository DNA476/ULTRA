from django import forms
from django.utils import timezone

from core.form_utils import apply_bootstrap_styles


class ReportPeriodForm(forms.Form):
    date_from = forms.DateField(
        label='Дата от',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    date_to = forms.DateField(
        label='Дата до',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        first_day = today.replace(day=1)
        self.fields['date_from'].initial = first_day
        self.fields['date_to'].initial = today
        apply_bootstrap_styles(self)

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from and date_to and date_to < date_from:
            self.add_error('date_to', 'Дата окончания не может быть раньше даты начала.')
        return cleaned_data
