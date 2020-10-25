from django import forms


class RepresentativeForm(forms.Form):
    address = forms.CharField()