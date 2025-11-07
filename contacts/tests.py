from django.test import TestCase
from contacts.forms import ContactForm
from django.core.files.uploadedfile import SimpleUploadedFile
from contacts.forms import AddressFormSet
from contacts.models import Contact
from django.urls import reverse


class ContactFormFieldValidationTests(TestCase):
    def test_email_requires_example_domain(self):
        form = ContactForm(
            data={
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@gmail.com",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_contact_form_valid(db):
        from contacts.forms import ContactForm

        form = ContactForm(
            data={
                "first_name": "Linus",
                "last_name": "Torvalds",
                "email": "linus@example.com",
            }
        )
        assert form.is_valid()


class ContactFormCrossFieldTests(TestCase):
    def test_first_and_last_name_must_differ(self):
        form = ContactForm(
            data={"first_name": "Ada", "last_name": "Ada", "email": "ada@example.com"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)


class ContactFormSuccessTests(TestCase):
    def test_valid_form_is_accepted(self):
        form = ContactForm(
            data={
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
            }
        )
        self.assertTrue(form.is_valid())


class ContactFormAvatarTests(TestCase):
    def test_avatar_file_size_validation(self):
        big_file = SimpleUploadedFile(
            "avatar.jpg", b"x" * (2 * 1024 * 1024 + 1), content_type="image/jpeg"
        )
        form = ContactForm(
            data={
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
            },
            files={"avatar": big_file},
        )

        self.assertFalse(form.is_valid())
        self.assertIn("avatar", form.errors)


class AddressFormSetTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            first_name="Test", last_name="User", email="test@example.com"
        )

    def test_formset_valid(self):
        formset_data = {
            "address_set-TOTAL_FORMS": "1",
            "address_set-INITIAL_FORMS": "0",
            "address_set-MIN_NUM_FORMS": "0",
            "address_set-MAX_NUM_FORMS": "1000",
            "address_set-0-label": "Home",
            "address_set-0-line1": "123 Main St",
            "address_set-0-line2": "",
            "address_set-0-city": "Test City",
            "address_set-0-country": "USA",
        }

        formset = AddressFormSet(formset_data, instance=self.contact)
        self.assertTrue(formset.is_valid())


class TemplateErrorDisplayTests(TestCase):
    def test_bootstrap_error_rendering(self):
        response = self.client.post(
            reverse("contact_create"),
            {
                "first_name": "Ada",
                "last_name": "Ada",  # invalid, same as first
                "email": "ada@example.com",
            },
        )

        self.assertContains(response, "text-danger small")
        self.assertContains(response, "Last name must differ")
