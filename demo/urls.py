from django.conf.urls import url
from . import views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
app_name = "demo"
urlpatterns = [
    path('auth/login/', auth_views.LoginView.as_view(template_name='authticate/login.html'), name='login'),
    path('auth/logout', auth_views.LogoutView.as_view(template_name='authticate/logout.html'), name='logout'),
    path('search', views.search, name='search'),
    path('city/<str:f>', views.city, name='city'),
    path('district/<str:f>', views.district, name='district'),
    path('province/<str:f>', views.province, name='province'),
    #url(r'^view/(?P<f>.+)$', views.view, name='view'),
    path('uploadfile', views.fileUploaderView, name='uploadfile'),
    url(r'^savedb/(?P<filename>.+)$', views.savedb, name='savedb'),
    path('detail/<str:bn>', views.detail, name='detail'),
    path('', views.index, name='index'),
    path('updatestatusF0/<int:id>', views.updateStatusF0, name='updateStatusF0'),
    path('updatestatus/<int:id>', views.updateStatus, name='updateStatus'),
    path('<str:f>', views.view, name='view'),

]