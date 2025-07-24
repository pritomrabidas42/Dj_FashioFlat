from django import forms

class PurchaseForm(forms.Form):
    size = forms.ChoiceField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], widget=forms.Select(attrs={'class': 'form-select'}))
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
