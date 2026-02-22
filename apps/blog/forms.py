from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl px-6 py-4 outline-none focus:border-primary text-slate-900 dark:text-white transition-all font-mono text-xs placeholder-slate-500",
                    "placeholder": "Full Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl px-6 py-4 outline-none focus:border-primary text-slate-900 dark:text-white transition-all font-mono text-xs placeholder-slate-500",
                    "placeholder": "Email",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl px-6 py-4 outline-none focus:border-primary text-slate-900 dark:text-white transition-all font-mono text-xs placeholder-slate-500",
                    "placeholder": "Message",
                    "rows": 4,
                }
            ),
        }
