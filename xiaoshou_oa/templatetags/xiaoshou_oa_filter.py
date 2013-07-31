#coding=utf-8
import urllib
from xiaoshou_oa.models import ProductType

__author__ = '王健'

from django import template
register=template.Library()


@register.filter(name='erweima')
def erweima(adminform,object_name):
    flag=True
    isModel=False
    s=u"{"
    for fieldset in adminform:
        for line in fieldset:
            for field in line:
                if   field.field.name=='flag':
                    s+=u'"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False
                elif  object_name=='ProductModel' and  field.field.name=='name':
                    try:
                        s+=u'"%s":"%s",'%(field.field.name,adminform.form.instance)
                        if field.field.value():
                            flag=False
                            isModel=True

                    except:
                        pass
                elif field.field.name=='name':
                    s+=u'"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False

    if isModel:
        slist=[]
        for type in ProductType.objects.filter(isdel=False):
            slist.append(s+u'"type":"%s","typename":"%s","class":"%s"}'%(type.flag,type.name,object_name))
        erweistr=u''
        for er in slist:
            erweistr+=u'''<a href="http://qr.liantu.com/api.php?text=%s"><img src="http://qr.liantu.com/api.php?text=%s" border="0"/></a><a href="https://chart.googleapis.com/chart?cht=qr&chs=300x300&choe=UTF-8&chld=L|2&chl=%s"><img src="https://chart.googleapis.com/chart?cht=qr&chs=300x300&choe=UTF-8&chld=L|2&chl=%s" border="0"/></a>'''%(urllib.quote(er.encode('utf-8')),urllib.quote(er.encode('utf-8')),urllib.quote(er.encode('utf-8')),urllib.quote(er.encode('utf-8')))
        return erweistr
    s+=u'"class":"%s"}'%object_name
    if not flag:
        return u'''<a href="http://qr.liantu.com/api.php?text=%s"><img src="http://qr.liantu.com/api.php?text=%s" border="0"/></a><a href="https://chart.googleapis.com/chart?cht=qr&chs=300x300&choe=UTF-8&chld=L|2&chl=%s"><img src="https://chart.googleapis.com/chart?cht=qr&chs=300x300&choe=UTF-8&chld=L|2&chl=%s" border="0"/></a>'''%(urllib.quote(s.encode('utf-8')),urllib.quote(s.encode('utf-8')),urllib.quote(s.encode('utf-8')),urllib.quote(s.encode('utf-8')))
    return u'保存后才可以生成二维码'


