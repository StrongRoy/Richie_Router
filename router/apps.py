from django.apps import AppConfig


class RouterConfig(AppConfig):
    name = 'router'

    def ready(self):
        self.module.autodiscover()

