from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from urllib.parse import quote
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


@require_POST
def contact_submit(request):
    """AJAX: submit contact form. Returns JSON { success, message, errors? }."""
    form = ContactForm(request.POST)
    if not form.is_valid():
        errors = {k: v[0] for k, v in form.errors.items()}
        return JsonResponse({
            "success": False,
            "message": "Please correct the errors below.",
            "errors": errors,
        }, status=400)
    contact = form.save()
    subject_confirm = "[Contact] We received your message"
    ctx = _email_context(request)
    ctx["name"] = contact.name
    ctx["subject"] = contact.subject
    ctx["date"] = timezone.localtime(contact.created_at).strftime("%Y-%m-%d")
    ctx["reference"] = f"CM-{contact.pk}"
    html_confirm = render_to_string("portfolio/email/contact_received.html", ctx)
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
    return JsonResponse({
        "success": True,
        "message": "Your message has been sent successfully! We'll get back to you soon.",
    })


@require_POST
def newsletter_submit(request):
    """AJAX: submit newsletter subscription. Returns JSON { success, message }."""
    form = NewsletterForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "success": False,
            "message": "Invalid email or already subscribed.",
        }, status=400)
    subscriber = form.save()
    subject = "[Newsletter] Welcome!"
    ctx = _email_context(request)
    ctx["email"] = subscriber.email
    html_message = render_to_string("portfolio/email/welcome_newsletter.html", ctx)
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
        msg = "Thanks for subscribing! Check your email for a confirmation."
    except Exception:
        msg = "Subscribed successfully. We couldn't send the welcome email right now."
    return JsonResponse({"success": True, "message": msg})


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

    name_parts = (profile.name.split(None, 1) if profile and profile.name else None) or ["Shekhar", "Dhakal"]
    profile_first_name = name_parts[0]
    profile_last_name = name_parts[1] if len(name_parts) > 1 else ""

    # vCard QR code for "Scan to add contact" (VCF format)
    site_config = SiteConfiguration.load()
    full_name = (profile.name if profile and profile.name else None) or "Shekhar Dhakal"
    contact_email = getattr(site_config, "email", None) or ""
    contact_phone = getattr(site_config, "phone", None) or ""
    site_url = request.build_absolute_uri("/")
    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{full_name}",
    ]
    if contact_phone:
        vcard_lines.append(f"TEL:{contact_phone}")
    if contact_email:
        vcard_lines.append(f"EMAIL:{contact_email}")
    vcard_lines.append(f"URL:{site_url}")
    vcard_lines.append("END:VCARD")
    vcard_string = "\r\n".join(vcard_lines)
    qr_contact_url = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + quote(vcard_string)

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
        "qr_contact_url": qr_contact_url,
    }
    return render(request, "portfolio/index.html", context)
