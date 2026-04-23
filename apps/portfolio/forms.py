import re
from django import forms
from django.core.exceptions import ValidationError
from .models import ContactMessage, NewsletterSubscriber

# Patterns that indicate XSS / script injection (reject input containing these)
XSS_PATTERN = re.compile(
    r'(<script|</script|javascript:|on\w+\s*=|\bexpression\s*\(|vbscript:|data\s*:)',
    re.IGNORECASE
)


def validate_no_xss(value):
    """Reject content that looks like XSS or script injection."""
    if value and XSS_PATTERN.search(value):
        raise ValidationError("Invalid characters or content not allowed.")


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        # ModelForm uses ORM .save() — parameterized queries (SQL injection safe)
        # All string fields use validators below and templates auto-escape (XSS safe)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your full name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "hello@company.com",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Project inquiry / job / collaboration",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-input resize-none",
                    "placeholder": "Tell me about your project or opportunity...",
                    "rows": 5,
                }
            ),
        }

    def clean_name(self):
        value = self.cleaned_data.get("name") or ""
        validate_no_xss(value)
        return value.strip()

    def clean_subject(self):
        value = self.cleaned_data.get("subject") or ""
        validate_no_xss(value)
        return value.strip()

    def clean_message(self):
        value = self.cleaned_data.get("message") or ""
        validate_no_xss(value)
        return value.strip()


class NewsletterForm(forms.ModelForm):
    # EmailField is validated by Django; ORM used (SQL injection safe)
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input text-sm",
                    "style": "max-width:220px; padding: 10px 14px;",
                    "placeholder": "Subscribe to newsletter",
                }
            ),
        }
