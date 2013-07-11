#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from xiaoshou_oa.views import top, menu, welcome
from xiaoshou_oa.views_user import userSave, userAdd, userList, userListPage, check_username, userDelete, userOpen, userPassword


urlpatterns = patterns('^oa/$',
                       (r'^top/$', top),
                       (r'^menu/$', menu),
                       (r'^welcome/$', welcome),
                        (r'^check_username/$',check_username),
                        (r'^userAdd/$',userAdd),
                        (r'^userSave/$',userSave),
                        (r'^userDelete/$',userDelete),
                        (r'^userOpen/$',userOpen),
                        (r'^userPassword/$',userPassword),
                        (r'^userList/$',userList),
                        (r'^userListPage/$',userListPage),
                       )