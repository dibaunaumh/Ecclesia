from django.conf import settings
from django.contrib.sites.models import Site


def get_domain():
    """
    Returns the domain configured in django.contrib.sites
    """
    site = Site.objects.get(pk=settings.SITE_ID)
    return site.domain


def clear_whitespaces(s):
    return s.replace("\n", "").replace(" ", "")


# check if the story is in hebrew
def is_heb(s):
    for c in s:
        if ord(c) > 128:
            return True
    return False