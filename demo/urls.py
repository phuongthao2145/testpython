from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
app_name = "demo"
urlpatterns = [
    path('auth/login/', auth_views.LoginView.as_view(template_name='authticate/login.html'), name='login'),
    path('auth/logout', auth_views.LogoutView.as_view(template_name='authticate/logout.html'), name='logout'),
    #path('auth/register/', auth_views.register, name='register'),
    path('view/<str:f>', views.view, name='view'),
    #url(r'^view/(?P<f>f[0-9]+)$', views.view, name='view'),
    path('uploadfile', views.fileUploaderView, name='uploadfile'),
    url(r'^savedb/(?P<filename>.+)$', views.savedb, name='savedb'),
    path('search', views.search, name='search'),
    path('detail/<str:bn>', views.detail, name='detail'),
    path('', views.index, name='index'),

]