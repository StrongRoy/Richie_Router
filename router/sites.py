# encoding:utf-8
# Author:Richie
# Date:12/14/2017
from django.shortcuts import HttpResponse, render
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class ModelRouter:
    list_display = None
    list_display_links = None

    def __init__(self, model, router_site):
        self.model = model
        self.router_site = router_site

    def changelist_view(self, request):
        opts = self.model._meta
        app_name = opts.app_label

        data_list = self.model.objects.all()

        def head():
            if not self.list_display:
                yield opts.model_name
            else:
                for field_name in self.list_display:
                    if isinstance(field_name, str):
                        val = opts.get_field(field_name).verbose_name
                    else:
                        val = field_name(self, flag=True)
                    yield val

        head_list = head()

        def inner():
            for obj in data_list:
                def inner_loop():
                    if not self.list_display:
                        yield obj
                    else:
                        for field_name in self.list_display:
                            if isinstance(field_name, str):
                                val = getattr(obj, field_name)
                            else:
                                val = field_name(self, obj)
                            yield val

                yield inner_loop()

        new_data_list = inner()

        return render(request, 'router/changelist.html', {'head_list': head_list, 'new_data_list': new_data_list})

    def add_view(self, request):
        return HttpResponse('添加页面')

    def delete_view(self, request, object_id):
        return HttpResponse('删除页面')

    def change_view(self, request, object_id):
        return HttpResponse('修改页面')

    def get_urls(self):
        from django.conf.urls import url
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/del/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()


class RouterSite:
    def __init__(self, name='router'):
        self.name = name
        self._registry = {}

    def register(self, model_or_iterable, model_router=None, **options):
        if not model_router:
            model_router = ModelRouter

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered with admin.' % model.__name__
                )

            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            self._registry[model] = model_router(model, self)

    def unregister(self, model_or_iterable):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]

    def get_urls(self):
        from django.conf.urls import url, include
        urlpatterns = []
        for model_class, model_router in self._registry.items():
            info = model_class._meta.app_label, model_class._meta.model_name
            urlpatterns += [
                url(r'^%s/%s/' % info, include(model_router.urls)), ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'router', self.name


site = RouterSite()
