# encoding:utf-8
# Author:Richie
# Date:12/14/2017

def register(*models, **kwargs):
    """
    Registers the given model(s) classes and wrapped ModelAdmin class with
    admin site:

    @register(Author)
    class AuthorAdmin(admin.ModelAdmin):
        pass

    A kwarg of `site` can be passed as the admin site, otherwise the default
    admin site will be used.
    """
    from router import ModelRouter
    from router.sites import site,RouterSite
    # from django.contrib.admin.sites import site, AdminSite

    def _model_admin_wrapper(model_router):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        router_site= kwargs.pop('site', site)

        if not isinstance(router_site, RouterSite):
            raise ValueError('site must subclass AdminSite')

        if not issubclass(model_router, ModelRouter):
            raise ValueError('Wrapped class must subclass ModelAdmin.')

        router_site.register(models, model_router=model_router)

        return model_router
    return _model_admin_wrapper
