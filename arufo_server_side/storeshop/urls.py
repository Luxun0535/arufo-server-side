from django.conf.urls import include, url
from django.contrib import admin
import storeshop.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sign/', storeshop.views.sign,name="sign"),
    url(r'^notify_verify/', storeshop.views.notify_verify,name="notify_verify"),
    url(r'^Exchange_prop/', storeshop.views.Exchange_prop,name="Exchange_prop"),
]
