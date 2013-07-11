from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
from XiaoShouOA import settings
from xiaoshou_oa.views import default, default2

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', default),
    url(r'^main$', default2),
    url(r'^oa/', include('xiaoshou_oa.urls')),

    (r'^accounts/login/$',login,{'template_name':'login.html'}),
     (r'^accounts/logout/$', logout,{'template_name':'logout.html'}),
     (r'^accounts/profile/$',default),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),


)