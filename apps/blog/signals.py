"""
Send email to all newsletter subscribers when a new blog post is published.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def notify_subscribers_new_post(sender, instance, created, **kwargs):
    """When a new blog post is saved and published, email all active subscribers."""
    if not created or not instance.is_published:
        return
    from apps.portfolio.models import NewsletterSubscriber

    subscribers = list(NewsletterSubscriber.objects.filter(is_active=True).values_list("email", flat=True))
    if not subscribers:
        return

    site_url = getattr(settings, "SITE_URL", "") or ""
    post_url = (site_url.rstrip("/") + instance.get_absolute_url()) if site_url else instance.get_absolute_url()
    try:
        from apps.portfolio.models import SiteConfiguration
        site_config = SiteConfiguration.load()
        site_name = getattr(site_config, "site_name", None) or "Shekhar Dhakal"
    except Exception:
        site_name = "Shekhar Dhakal"

    ctx = {
        "site_name": site_name,
        "post_title": instance.title,
        "post_excerpt": (instance.excerpt or "")[:200],
        "post_url": post_url,
    }
    html_message = render_to_string("portfolio/email/new_article_notify.html", ctx)
    plain_message = strip_tags(html_message)
    subject = f"[Blog] New article: {instance.title}"

    for email in subscribers:
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception:
            pass
