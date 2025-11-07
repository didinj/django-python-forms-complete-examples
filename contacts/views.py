from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.template.loader import render_to_string
from .forms import AddressFormSet, ContactForm
from .models import Contact


class ContactListView(ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    paginate_by = 10


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact_list")


class ContactAddressEditView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_with_addresses_form.html"
    success_url = reverse_lazy("contact_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["addresses"] = AddressFormSet(self.request.POST, instance=self.object)
        else:
            ctx["addresses"] = AddressFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        addresses = context["addresses"]

        if addresses.is_valid():
            self.object = form.save()
            addresses.instance = self.object
            addresses.save()
            messages.success(self.request, "Contact updated successfully.")
            return redirect(self.success_url)

        return self.form_invalid(form)


class ContactCreateHTMXView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_create_htmx.html"
    success_url = reverse_lazy("contact_list")

    def form_invalid(self, form):
        if self.request.headers.get("Hx-Request"):
            html = render_to_string(
                "contacts/_contact_form_partial.html",
                {"form": form},
                request=self.request,
            )
            return HttpResponse(html, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get("Hx-Request"):
            return HttpResponse(
                "<div class='alert alert-success'>Contact saved successfully!</div>"
            )
        return super().form_valid(form)


class ContactCreateAJAXView(CreateView):
    model = Contact
    form_class = ContactForm

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            html = render_to_string(
                "contacts/_contact_form_partial.html",
                {"form": form},
                request=self.request,
            )
            return JsonResponse({"ok": False, "form_html": html})
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"ok": True, "message": "Contact created successfully!"}
            )
        return super().form_valid(form)
