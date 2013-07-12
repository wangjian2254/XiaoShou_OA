#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from xiaoshou_oa.views import top, menu, welcome
from xiaoshou_oa.views_depatement import depatementAdd, depatementList, depatementSave, depatementDelete, depatementOpen, depatementPeople, depatementPeopleDel, depatementPeopleAdd
from xiaoshou_oa.views_office import officeAdd, officeSave, check_office, officeList, officeDelete, officeOpen
from xiaoshou_oa.views_qiandao import qiandaoAdd, qiandaoSave, qiandaoDelete, qiandaoOpen, qiandaoList, check_qiandao
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

                        (r'^depatementAdd/$',depatementAdd),
                        (r'^depatementSave/$',depatementSave),
                        (r'^depatementList/$',depatementList),
                        (r'^depatementDelete/$',depatementDelete),
                        (r'^depatementOpen/$',depatementOpen),
                        (r'^depatementPeople/$',depatementPeople),
                        (r'^depatementPeopleAdd/$',depatementPeopleAdd),
                        (r'^depatementPeopleDel/$',depatementPeopleDel),

                        (r'^officeAdd/$',officeAdd),
                        (r'^officeSave/$',officeSave),
                        (r'^check_office/$',check_office),
                        (r'^officeList/$',officeList),
                        (r'^officeDelete/$',officeDelete),
                        (r'^officeOpen/$',officeOpen),

                        (r'^qiandaoAdd/$',qiandaoAdd),
                        (r'^check_qiandao/$',check_qiandao),
                        (r'^qiandaoSave/$',qiandaoSave),
                        (r'^qiandaoDelete/$',qiandaoDelete),
                        (r'^qiandaoOpen/$',qiandaoOpen),
                        (r'^qiandaoList/$',qiandaoList),
                       )