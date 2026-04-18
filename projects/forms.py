from django import forms

from core.form_utils import apply_bootstrap_styles

from .models import Participation, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'client',
            'project_type',
            'description',
            'start_date',
            'end_date',
            'status',
            'budget',
            'responsible_employee',
            'notes',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_styles(self)

    def clean_budget(self):
        budget = self.cleaned_data['budget']
        if budget < 0:
            raise forms.ValidationError('Бюджет / выручка не может быть отрицательным.')
        return budget

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'Дата окончания не может быть раньше даты начала.')
        return cleaned_data


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['project', 'model', 'status', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if self.project:
            self.fields['project'].initial = self.project
            self.fields['project'].widget = forms.HiddenInput()
        apply_bootstrap_styles(self)

    def clean(self):
        cleaned_data = super().clean()
        project = self.project or cleaned_data.get('project')
        model = cleaned_data.get('model')
        if project and model:
            exists = Participation.objects.filter(project=project, model=model)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                self.add_error('model', 'Эта модель уже назначена на выбранный проект.')
        return cleaned_data
