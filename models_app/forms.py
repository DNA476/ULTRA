from django import forms

from core.form_utils import apply_bootstrap_styles

from .models import ModelCard, ModelPhoto


class ModelCardForm(forms.ModelForm):
    class Meta:
        model = ModelCard
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'phone',
            'email',
            'city',
            'height',
            'bust',
            'waist',
            'hips',
            'shoe_size',
            'hair_color',
            'eye_color',
            'experience',
            'category',
            'status',
            'main_photo',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'experience': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_styles(self)

    def clean_height(self):
        height = self.cleaned_data['height']
        if height < 120 or height > 230:
            raise forms.ValidationError('Рост должен быть в диапазоне 120-230 см.')
        return height

    def clean_bust(self):
        return self._clean_measurement('bust', 'Объем груди')

    def clean_waist(self):
        return self._clean_measurement('waist', 'Талия')

    def clean_hips(self):
        return self._clean_measurement('hips', 'Бедра')

    def clean_shoe_size(self):
        shoe_size = self.cleaned_data.get('shoe_size')
        if shoe_size is not None and (shoe_size < 30 or shoe_size > 50):
            raise forms.ValidationError('Размер обуви должен быть в диапазоне 30-50.')
        return shoe_size

    def _clean_measurement(self, field_name, label):
        value = self.cleaned_data[field_name]
        if value < 40 or value > 160:
            raise forms.ValidationError(f'{label} должен быть в диапазоне 40-160 см.')
        return value


class ModelPhotoForm(forms.ModelForm):
    class Meta:
        model = ModelPhoto
        fields = ['model', 'image', 'caption']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_styles(self)
