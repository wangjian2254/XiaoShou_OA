#coding=utf-8
import urllib

__author__ = '王健'

from django import template
register=template.Library()

@register.filter(name='erweima')
def erweima(adminform,object_name):
    flag=True
    s=u"{"
    for fieldset in adminform:
        for line in fieldset:
            for field in line:
                if   field.field.name=='flag':
                    s+=u'"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False
                elif  object_name=='ProductModel' and  field.field.name=='name':
                    s+=u'"%s":"%s",'%(field.field.name,adminform.form.instance)
                    if field.field.value():
                        flag=False
                elif field.field.name=='':
                    s+=u'"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False
    s+=u'"class":"%s"}'%object_name
    if not flag:
        return u'''<a href="http://qr.liantu.com/api.php?text=%s"><img src="http://qr.liantu.com/api.php?text=%s" border="0"/></a>'''%(urllib.quote(s.encode('utf-8')),urllib.quote(s.encode('utf-8')))
    return u'保存后才可以生成二维码'


