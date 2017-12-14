
from router.decorators import register
from router.sites import RouterSite,ModelRouter, site

from django.utils.module_loading import autodiscover_modules

__all__ = [
    "register","RouterSite","ModelRouter", "site",
]


def autodiscover():
    autodiscover_modules('router', register_to=site)
