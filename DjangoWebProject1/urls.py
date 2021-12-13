"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url

import django.contrib.auth.views
from django.views.generic.base import RedirectView

import app.forms
import app.views
from app  import views
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()
import app.views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


urlpatterns = [
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
   
    
    
    
    

    
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Войти',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^$', app.views.home, name='home'),
    url(r'^edit_order/(?P<id>\d+)/$', app.views.edit_order, name='edit_order'),
    url(r'^orders/$', app.views.orders, name='orders'),
    url(r'^edit/(?P<id>\d+)/$', app.views.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', app.views.delete, name='delete'),
    url(r'^users/$', app.views.users, name='users'),
    url(r'^empty/$', app.views.empty, name='empty'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^links$', app.views.links, name='links'),
    url(r'newpost', app.views.newpost, name='newpost'),
    url(r'newgame', app.views.newgame, name='newgame'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'registration$', app.views.registration, name='registration'),
    url(r'^blog/$', app.views.blog, name='blog'),
    url(r'^blog/(?P<parametr>\d+)/$', app.views.blogpost, name='blogpost'),
    url(r'^cart/',include('cart.urls', namespace = 'cart')),
    url(r'orders/',include('orders.urls', namespace = 'orders')),
    url(r'^', include('app.urls', namespace='app')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()