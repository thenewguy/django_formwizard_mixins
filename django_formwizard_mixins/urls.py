from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_formwizard_mixins.views.mixins.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', mixin_demo_wizard_view, name=MIXIN_DEMO_WIZARD_DONE_URL_NAME),
    url(r'^(?P<step>.+)/$', mixin_demo_wizard_view, name=MIXIN_DEMO_WIZARD_STEP_URL_NAME),
)
