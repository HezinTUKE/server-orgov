from django import forms

class RegPhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=13, 
        required=True
    )

class RegSMSForm(forms.Form):
    phone = forms.CharField(
        max_length=5,
        required=True
    )

class RegLoginForm(forms.Form):
    username = forms.CharField(
        min_length=7,
        max_length=15,
        required=True
    )
    password = forms.CharField(
        min_length=8,
        max_length=15,
        required=True
    )