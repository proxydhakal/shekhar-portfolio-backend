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
                    "class": "w-full bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-white/5 rounded-2xl px-8 py-5 outline-none focus:border-primary transition-all font-mono text-xs text-slate-900 dark:text-slate-100 placeholder-slate-500",
                    "placeholder": "NAME",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-white/5 rounded-2xl px-8 py-5 outline-none focus:border-primary transition-all font-mono text-xs text-slate-900 dark:text-slate-100 placeholder-slate-500",
                    "placeholder": "EMAIL",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "w-full bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-white/5 rounded-2xl px-8 py-5 outline-none focus:border-primary transition-all font-mono text-xs text-slate-900 dark:text-slate-100 placeholder-slate-500",
                    "placeholder": "SUBJECT",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "w-full bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-white/5 rounded-2xl px-8 py-5 outline-none focus:border-primary transition-all font-mono text-xs text-slate-900 dark:text-slate-100 placeholder-slate-500",
                    "placeholder": "HOW_CAN_I_HELP?",
                    "rows": 4,
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
                    "class": "w-full bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl px-6 py-4 outline-none focus:border-primary text-slate-900 dark:text-white transition-all font-mono text-xs placeholder-slate-500",
                    "placeholder": "dev@example.com",
                }
            ),
        }
