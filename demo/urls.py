from django.conf.urls import url
from . import views
from django.urls import path
app_name = "demo"
urlpatterns = [
    path('', views.fileUploaderView, name='index'),
    url(r'^savedb/(?P<filename>.+)$', views.savedb, name='savedb'),
    path('view/<str:f>', views.viewf, name='viewf'),
    path('search', views.search, name='search'),
    path('detail/<str:bn>', views.detail, name='detail'),
    path('view', views.view, name='view'),

]