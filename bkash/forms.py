from django import forms

class BkashPaymentForm(forms.Form):
    phone_number = forms.CharField(label='bKash Number', max_length=15)
    transaction_id = forms.CharField(label='Transaction ID', max_length=100)
