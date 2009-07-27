from django.conf import settings
from django.contrib.sites.models import Site


def get_domain():
    """
    Returns the domain configured in django.contrib.sites
    """
    site = Site.objects.get(pk=settings.SITE_ID)
    return site.domain