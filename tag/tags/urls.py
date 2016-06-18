from django.conf.urls import url,include
from . import views as homeviews
from django.contrib.auth.urls import *
urlpatterns = [
url(r'^$', homeviews.homepage, name = "home"),
url(r'^accounts/profile/', homeviews.user_homepage, name = "profile"),
url(r'^signup/', homeviews.sign_up, name = "sign_up"),
url(r'^users/(?P<username>[\w]+)/', homeviews.user_homepage, name = "homepage"),
url(r'^tags/(?P<tagid>[\w]+)/', homeviews.tagpage, name = "taghomepage")
]
