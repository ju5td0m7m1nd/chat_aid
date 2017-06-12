from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from recommendation import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recommend/(?P<user_input>.+)/$', views.Recommend.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
