from django.conf.urls import url,include
from . import views as homeviews
from django.contrib.auth.urls import *
from django.conf import settings
from django.conf.urls.static import static
import django.views.defaults

urlpatterns = [
url('^login/', homeviews.login_user, name = "login"),
url(r'^$', homeviews.homepage, name = "home"),
url(r'^profile/', homeviews.user_homepage, name = "profile"),
url(r'^signup/', homeviews.sign_up, name = "sign_up"),
url(r'^users/(?P<username>[\w]+)/', homeviews.view_homepage, name = "homepage"),
url(r'^tags/(?P<tagid>[\w]+)/', homeviews.tagpage, name = "taghomepage"),
url(r'^addfriends/', homeviews.addfriends, name = "addfriends"),
url(r'^removefriend/(?P<removevar>[\w]+)/', homeviews.removefriend, name = "removefriend"),
url(r'^edit/', homeviews.editprofile, name = "editprofile"),
url(r'^pass/(?P<username>[\w]+)/(?P<tagid>[0-9]+)', homeviews.pass_tag, name = "pass_tag"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
