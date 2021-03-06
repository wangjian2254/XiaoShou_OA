#coding=utf-8
'''
Created on 2011-3-19

@author: 王健
'''
from django.conf.urls import patterns
from xiaoshou_oa.views import top, menu, welcome
from xiaoshou_oa.views_depatement import depatementAdd, depatementList, depatementSave, depatementDelete, depatementOpen, depatementPeople, depatementPeopleDel, depatementPeopleAdd
from xiaoshou_oa.views_kaoshi import getMyKaoShi, getExamination, getScore, getScoreClient, getScoreDetailQuery, getScoreQuery, getAllKaoShi
from xiaoshou_oa.views_office import officeAdd, officeSave, check_office, officeList, officeDelete, officeOpen, calculateOffice, officeListClient, setGPSoffice
from xiaoshou_oa.views_qiandao import qiandaoAdd, qiandaoSave, qiandaoDelete, qiandaoOpen, qiandaoList, check_qiandao, userQianDaoList, userQianDaoQuery, userqiandaoUploadClient, userQianDaoQueryClient, qiandaoListClient
from xiaoshou_oa.views_user import userSave, userAdd, userList, userListPage, check_username, userDelete, userOpen, userPassword, clientLogin, userDeviceid, userListClient, userPWD, userPWD_get
from xiaoshou_oa.views_wendang import getAllMenu, getDocument, getDocumentContent, searchDocument
from xiaoshou_oa.views_xiaoshou import userProductOrderQuery, userXiaoShouList, userXiaoShouOrderUpdate, userProductOrderClient


urlpatterns = patterns('^oa/$',
                       (r'^top/$', top),
                       (r'^menu/$', menu),
                       (r'^welcome/$', welcome),
                        (r'^clientLogin/$',clientLogin),

                        (r'^check_username/$',check_username),
                        (r'^userAdd/$',userAdd),
                        (r'^userSave/$',userSave),
                        (r'^userDelete/$',userDelete),
                        (r'^userOpen/$',userOpen),
                        (r'^userPassword/$',userPassword),
                        (r'^userDeviceid/$',userDeviceid),
                        (r'^userList/$',userList),
                        (r'^userListPage/$',userListPage),
                         (r'^userPWD/$',userPWD),
                        (r'^userPWD_get/$',userPWD_get),


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
                        (r'^calculateOffice/$',calculateOffice),
                        (r'^setGPSoffice/$',setGPSoffice),

                        (r'^qiandaoAdd/$',qiandaoAdd),
                        (r'^check_qiandao/$',check_qiandao),
                        (r'^qiandaoSave/$',qiandaoSave),
                        (r'^qiandaoDelete/$',qiandaoDelete),
                        (r'^qiandaoOpen/$',qiandaoOpen),
                        (r'^qiandaoList/$',qiandaoList),


                        (r'^userQianDaoList/$',userQianDaoList),
                        (r'^userQianDaoQuery/$',userQianDaoQuery),

                        (r'^userXiaoShouList/$',userXiaoShouList),
                        (r'^userProductOrderQuery/$',userProductOrderQuery),



                        (r'^getScoreDetailQuery/$',getScoreDetailQuery),
                        (r'^getScoreQuery/$',getScoreQuery),



                        # 手机端接口
                        (r'^userqiandaoUploadClient/$',userqiandaoUploadClient),
                        (r'^userQianDaoQueryClient/$',userQianDaoQueryClient),
                        (r'^userProductOrderClient/$',userProductOrderClient),
                        (r'^qiandaoListClient/$',qiandaoListClient),
                        (r'^officeListClient/$',officeListClient),
                        (r'^userXiaoShouOrderUpdate/$',userXiaoShouOrderUpdate),
                        (r'^userListClient/$',userListClient),

                        # 文档接口
                        (r'^getAllMenu/$',getAllMenu),
                        (r'^getDocument/$',getDocument),
                        (r'^getDocumentContent/$',getDocumentContent),
                        (r'^searchDocument/$',searchDocument),
                        # 考试接口
                        (r'^getMyKaoShi/$',getMyKaoShi),
                        (r'^getExamination/$',getExamination),
                        (r'^getAllKaoShi/$',getAllKaoShi),
                        (r'^getScore/$',getScore),
                        (r'^getScoreClient/$',getScoreClient),

                       )