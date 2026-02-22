from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("newsletter/submit/", views.newsletter_submit, name="newsletter_submit"),
]
