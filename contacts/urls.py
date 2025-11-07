from django.urls import path
from . import views


urlpatterns = [
    path("contacts/", views.ContactListView.as_view(), name="contact_list"),
    path("contacts/new/", views.ContactCreateView.as_view(), name="contact_create"),
    path(
        "contacts/<int:pk>/edit/",
        views.ContactUpdateView.as_view(),
        name="contact_edit",
    ),
    path(
        "contacts/<int:pk>/addresses/",
        views.ContactAddressEditView.as_view(),
        name="contact_addresses",
    ),
    path(
        "contacts/new-ajax/",
        views.ContactCreateHTMXView.as_view(),
        name="contact_create_htmx",
    ),
    path(
        "contacts/new/ajax/",
        views.ContactCreateAJAXView.as_view(),
        name="contact_create_ajax",
    ),
]
