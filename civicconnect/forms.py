from django import forms


class RepresentativeForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Zip Code or Address', 'style': 'width:500px'}))

