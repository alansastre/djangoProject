from django import forms

from .models import Direction


class DirectionForm(forms.ModelForm):
    street = forms.CharField(label="Calle", widget=forms.TextInput(attrs={'class': 'form-control'}))
    province = forms.CharField(label="Provincia", widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(label="Código postal", widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(required=True, help_text="País de residencia", label="País", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Direction
        fields = ('street', 'province', 'postal_code', 'country')


