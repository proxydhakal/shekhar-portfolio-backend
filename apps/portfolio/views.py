from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from .models import Profile, Skill, Project, Experience, Education, Certification, SiteConfiguration
from apps.blog.models import BlogPost
from .forms import ContactForm, NewsletterForm
from django.contrib import messages


def _email_context(request=None):
    """Shared context for HTML emails (theme, site name, URL)."""
    site_config = SiteConfiguration.load()
    ctx = {
        "site_name": getattr(site_config, "site_name", None) or "Shekhar Dhakal",
    }
    if request:
        ctx["site_url"] = request.build_absolute_uri("/")
    else:
        ctx["site_url"] = getattr(settings, "SITE_URL", None) or "#"
    return ctx


def index(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all().order_by("order")
    experiences = Experience.objects.all().order_by("order")
    education_list = Education.objects.all().order_by("order")
    certifications = Certification.objects.all().order_by("order")
    recent_posts = BlogPost.objects.filter(is_published=True).order_by("-created_at")[:3]

    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)

    contact_form = ContactForm()
    newsletter_form = NewsletterForm()

    if request.method == "POST":
        if "subscribe_newsletter" in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                subscriber = newsletter_form.save()
                subject = "[Newsletter] Welcome!"
                ctx = _email_context(request)
                ctx["email"] = subscriber.email
                html_message = render_to_string(
                    "portfolio/email/welcome_newsletter.html", ctx
                )
                plain_message = strip_tags(html_message)
                try:
                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [subscriber.email],
                        html_message=html_message,
                        fail_silently=True,
                    )
                    messages.success(
                        request, "Thanks for subscribing! Check your email for a confirmation."
                    )
                except Exception:
                    messages.warning(
                        request, "Subscribed successfully, but failed to send welcome email."
                    )
                return redirect("index")
            messages.error(request, "Invalid email or already subscribed.")
        else:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact = contact_form.save()
                # Send confirmation email to the user (HTML, theme-based)
                subject_confirm = "[Contact] We received your message"
                ctx = _email_context(request)
                ctx["name"] = contact.name
                ctx["subject"] = contact.subject
                ctx["date"] = timezone.localtime(contact.created_at).strftime("%Y-%m-%d")
                ctx["reference"] = f"CM-{contact.pk}"
                html_confirm = render_to_string(
                    "portfolio/email/contact_received.html", ctx
                )
                plain_confirm = strip_tags(html_confirm)
                try:
                    send_mail(
                        subject_confirm,
                        plain_confirm,
                        settings.DEFAULT_FROM_EMAIL,
                        [contact.email],
                        html_message=html_confirm,
                        fail_silently=True,
                    )
                except Exception:
                    pass
                messages.success(request, "Your message has been sent successfully!")
                return redirect("index")
            messages.error(request, "Please correct the errors in the contact form.")

    name_parts = (profile.name.split(None, 1) if profile and profile.name else None) or ["Shekhar", "Dhakal"]
    profile_first_name = name_parts[0]
    profile_last_name = name_parts[1] if len(name_parts) > 1 else ""

    context = {
        "profile": profile,
        "profile_first_name": profile_first_name,
        "profile_last_name": profile_last_name,
        "skills_by_category": skills_by_category,
        "skills_list": list(skills),
        "projects": projects,
        "experiences": experiences,
        "education_list": education_list,
        "certifications": certifications,
        "recent_posts": recent_posts,
        "contact_form": contact_form,
        "newsletter_form": newsletter_form,
    }
    return render(request, "portfolio/index.html", context)
