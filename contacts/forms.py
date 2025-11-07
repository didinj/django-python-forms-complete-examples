from django import forms
from .models import Address, Contact
from django.core.exceptions import ValidationError


AddressFormSet = forms.inlineformset_factory(
    Contact,
    Address,
    fields=["label", "line1", "line2", "city", "country"],
    extra=1,
    can_delete=True,
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "avatar", "notes"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ada",
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Lovelace",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "ada@example.com",
                    "class": "form-control",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Additional information...",
                    "class": "form-control",
                }
            ),
        }

    # Cross-field validation example
    def clean(self):
        cleaned = super().clean()
        fn = cleaned.get("first_name", "").strip()
        ln = cleaned.get("last_name", "").strip()
        if fn and ln and fn == ln:
            self.add_error("last_name", "Last name must be different from first name.")
        return cleaned

    # Apply Bootstrap classes automatically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {"class": "form-control", "placeholder": "Enter details..."}
                )
            else:
                field.widget.attrs.update({"class": "form-control"})

    def clean_avatar(self):
        file = self.cleaned_data.get("avatar")
        if not file:
            return file

        if file.size > 2 * 1024 * 1024:  # 2 MB
            raise ValidationError("Avatar must be under 2MB.")

        if not file.content_type.startswith("image/"):
            raise ValidationError("Please upload a valid image file.")

        return file
