#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from xiaoshou_oa.views_user import top, menu, welcome, userSave


urlpatterns = patterns('^oa/$',
                       (r'^top/$', top),
                       (r'^menu/$', menu),
                       (r'^welcome/$', welcome),
                        (r'^userSave/$',userSave),
                       )