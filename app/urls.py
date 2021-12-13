from django.conf.urls import url
 
from . import views
 
urlpatterns = ([ 
    url(r'^my_orders/$', views.my_orders, name='my_orders'),
    url(r'^game_list$', views.game_list, name='game_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.game_list, name='game_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.game_detail, name='game_detail'),
    
    ])
