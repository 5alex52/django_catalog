from django import forms
from .models import Feedback

class AddFeedbackForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'required':'required', 'rows': 1, 'placeholder': "Алексей"}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'required':'required', 'class': 'art-stranger', 'rows': 1, 'placeholder': "+375 (**) ***-**-**"}))

    class Meta:
        model = Feedback
        fields = ['name', 'phone']
