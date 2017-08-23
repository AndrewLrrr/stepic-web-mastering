from django.conf.urls import url

from . import views

app_name = 'qa'
urlpatterns = [
    url(r'^$', views.new_questions, name='index'),
    url(r'^popular/?$', views.popular_questions, name='popular'),
    url(r'^ask/?$', views.question_ask, name='question_ask'),
    url(r'^question/(?P<pk>[0-9]+)/?$', views.question_detail, name='question_detail'),
    url(r'^signup/?$', views.user_singup, name='signup'),
    url(r'^login/?$', views.user_login, name='login'),
    url(r'^logout/?$', views.user_logout, name='logout'),
]
