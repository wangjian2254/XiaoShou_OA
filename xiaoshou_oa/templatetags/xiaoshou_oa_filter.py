#coding=utf-8
import urllib

__author__ = '王健'

from django import template
register=template.Library()

@register.filter(name='erweima')
def erweima(adminform,classname):
    flag=True
    s="{"
    for fieldset in adminform:
        for line in fieldset:
            for field in line:
                if field.field.name=='name' or field.field.name=='flag':
                    s+='"%s":"%s",'%(field.field.name,field.field.value())
                    if field.field.value():
                        flag=False
    s+='"class":"%s"}'%classname
    if not flag:
        return '''<a href="http://qr.liantu.com/api.php?text=%s"><img src="http://qr.liantu.com/api.php?text=%s" border="0"/></a>'''%(urllib.quote(s.encode('utf-8')),urllib.quote(s.encode('utf-8')))
    return u'保存后才可以生成二维码'


