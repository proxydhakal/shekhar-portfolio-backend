from .models import SiteConfiguration, Profile
from .forms import NewsletterForm


def site_configuration(request):
    return {
        "site_config": SiteConfiguration.load(),
        "profile": Profile.objects.first(),
        "newsletter_form": NewsletterForm(),
    }
