from .models import SiteConfiguration, Profile


def site_configuration(request):
    return {
        "site_config": SiteConfiguration.load(),
        "profile": Profile.objects.first(),
    }
