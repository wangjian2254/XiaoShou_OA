#coding=utf-8
import urllib

__author__ = '王健'

from django import template
register=template.Library()

@register.filter(name='erweima')
def erweima(adminform,classname):
    s="{"
    for fieldset in adminform:
        for line in fieldset:
            for field in line:
                if field.field.name=='name' or field.field.name=='flag':
                    s+='"%s":"%s",'%(field.field.name,field.field.value())

    s+='"class":"%s"}'%classname
    return urllib.quote(s.encode('utf-8'))



