from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    contact = models.ForeignKey(
        Contact, related_name="addresses", on_delete=models.CASCADE
    )
    label = models.CharField(max_length=20, help_text="Home, Work, etc.")
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.label}: {self.line1}, {self.city}"
