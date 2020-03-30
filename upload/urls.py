from django.conf.urls import url

from upload import views

urlpatterns = [
    url(r'^avatar$', views.avatar),
    url(r'^dynamicImg$', views.dynamicImg),
    url(r'^dynamicImgByUrl$', views.dynamicImgByUrl),

]