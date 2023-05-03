from django import forms

class SuperForm(forms.Form):
    def __init__(self, dynamic_fields, **kwargs) -> None:
        super().__init__(**kwargs)
        self.fields.update(dynamic_fields)

class SuperFormset(forms.BaseFormSet):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        #self.form_kwargs = form_kwargs