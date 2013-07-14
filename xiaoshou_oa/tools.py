#coding=utf-8
#author:u'王健'
#Date: 13-7-10
#Time: 下午10:54
import json
from django.http import HttpResponse

__author__ = u'王健'


def permission_required(func=None):
    def test(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return getResult(False,u'需要管理员权限')
    return test


def client_login_required(func=None):
    def test(request, *args, **kwargs):
        if not  request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return getResult(False,u'登录过期，需要重新登录。', None,404)
    return test

def getResult(success,message,result=None,status_code=200):
    '''
    200 正常返回 code
    404 登录过期，需要重新登录
    '''
    map={'success':success,'message':message, 'status_code':status_code}
    if result:
        map['result']=result
    return HttpResponse(json.dumps(map))