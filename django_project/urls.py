from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from django_project.movies import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^movies/$', views.movie_read, name='movie_read'),
    url(r'^movies/create/$', views.movie_create, name='movie_create'),
    url(r'^movies/search/$', views.movie_search, name='movie_search'),
    url(r'^movies/(?P<pk>\d+)/update/$', views.movie_update, name='movie_update'),
    url(r'^movies/(?P<pk>\d+)/delete/$', views.movie_delete, name='movie_delete'),
    url(r'^movies/(?P<pk>\d+)/description/$', views.movie_description, name='movie_description'),
    url(r'^movies/(?P<pk>\d+)/description/upload_clear/$', views.remove_photo, name='remove_photo'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
