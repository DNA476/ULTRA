from django import forms


BOOTSTRAP_CLASS = 'form-control'


def apply_bootstrap_styles(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.HiddenInput):
            continue
        if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
            css_class = 'form-check-input'
        elif isinstance(widget, forms.Select):
            css_class = 'form-select'
        elif isinstance(widget, forms.ClearableFileInput):
            css_class = 'form-control'
        else:
            css_class = BOOTSTRAP_CLASS

        existing = widget.attrs.get('class', '')
        widget.attrs['class'] = f'{existing} {css_class}'.strip()
