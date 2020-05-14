from django.conf.urls import url
from django.contrib import admin
from baegotgupsik import views
 
urlpatterns = [
        url(r'^keyboard',views.keyboard),
        url(r'^admin/',admin.site.urls),
        url(r'^message',views.message),
        url(r'^crawl',views.crawl),
]
 
