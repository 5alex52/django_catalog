from dal import autocomplete
from django import forms

from .models import Feedback
from .models import Product


class AddFeedbackForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"required": "required", "rows": 1, "placeholder": "Алексей"}
        ),
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "required",
                "class": "art-stranger",
                "rows": 1,
                "placeholder": "+375 (__) ___-__-__",
            }
        ),
    )

    class Meta:
        model = Feedback
        fields = ["name", "phone"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "collection": autocomplete.ModelSelect2(
                url="collection-autocomplete",
                forward=["manufacturer"],
                attrs={
                    "data-theme": "admin-autocomplete",
                    "class": "unfold-admin-autocomplete",
                },
            ),
        }
