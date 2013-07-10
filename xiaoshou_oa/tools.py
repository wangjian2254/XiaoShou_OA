#coding=utf-8
#author:u'王健'
#Date: 13-7-10
#Time: 下午10:54
import json
from django.http import HttpResponse

__author__ = u'王健'



def getResult(success,message,result=None):
    return HttpResponse(json.dumps({'success':success,'message':message,'result':result}))