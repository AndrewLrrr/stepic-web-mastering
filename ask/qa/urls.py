from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.new_questions, name='new_questions'),
    url(r'^popular/?$', views.popular_questions, name='popular_questions'),
    url(r'^question/(?P<pk>[0-9]+)/?$', views.question_detail, name='question_detail'),
    url(r'^login/?$', views.test, name='login'),
    url(r'^signup/?$', views.test, name='signup'),
    url(r'^ask/?$', views.test, name='ask'),
    url(r'^new/?$', views.test, name='new'),
]
