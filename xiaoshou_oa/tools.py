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

def getResult(success,message,result=None):
    return HttpResponse(json.dumps({'success':success,'message':message,'result':result}))