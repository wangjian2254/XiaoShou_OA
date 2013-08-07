#coding=utf-8
# Create your views here.
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import DocumentKind, Document, DocumentImage
from xiaoshou_oa.tools import getResult, client_login_required


def getAllMenu(request):
    '''
    获取所有栏目
    '''
    menus=[]
    for m in DocumentKind.objects.all():
        menus.append({"name":m.name ,"id":m.pk, "isdel":m.isdel})
    return getResult(True,u'下载数据成功',menus)

def getDocument(request):
    '''
    根据栏目获取文档
    '''
    menuid=request.REQUEST.get('menuid','')
    limit=request.REQUEST.get('limit',30)
    start=request.REQUEST.get('start',0)
    if menuid:
        menuid=int(menuid)
    if limit:
        limit=int(limit)
    if start:
        start=int(start)
    query=Document.objects.filter(isdel=False)
    if menuid:
        query = query.filter(kind=DocumentKind.objects.get(pk=menuid))
    documentlist=[]

    # documentid=[]
    for d in query[start:start+limit]:
        dic={'id':d.pk,'title':d.title,'kindName':d.kind.name,'kind':d.kind_id,'datetime':d.dateTime.strftime("%Y-%m-%d %H:%M"),'show':d.show}
        # dic['imglist']=[]
        # documentid.append(d.pk)
        documentlist.append(dic)
    # for img in DocumentImage.objects.filter(document__in=documentid).order_by('index'):
    #     documentdict['%s'%img.document_id]['imglist'].append({'url':img.get_img_url(),'index':img.index,'id':img.pk})
    result={'length':len(documentlist),'limit':limit,'end':start+len(documentlist),'result':documentlist,'total':query.count()}
    return getResult(True,u'下载数据成功',result)

def getDocumentContent(request):
    '''
    获取文档信息
    '''
    documentid=request.REQUEST.get('documentid','')
    if documentid:
        d=Document.objects.get(pk=documentid)
        docdict={'title':d.title,'kindName':d.kind.name,'kind':d.kind_id,'datetime':d.dateTime.strftime("%Y-%m-%d %H:%M"),'show':d.show}
        docdict['imglist']=[]
        for img in DocumentImage.objects.filter(document=d).order_by('index'):
            docdict['imglist'].append({'url':img.get_img_url(),'index':img.index,'id':img.pk})
        return getResult(True,u'下载数据成功',docdict)
    else:
        return getResult(True,u'文档不存在。',None)

def searchDocument(request):
    '''
    根据关键字查询文档，在标题中
    '''
    searchText=request.REQUEST.get('search','')
    limit=request.REQUEST.get('limit',30)
    start=request.REQUEST.get('start',0)
    if limit:
        limit=int(limit)
    if start:
        start=int(start)
    documentlist=[]
    if searchText:
        query=Document.objects.filter(title__contains=searchText).order_by('-dateTime')
        for d in query[start:start+limit]:
            dic={'title':d.title,'kindName':d.kind.name,'kind':d.kind_id,'datetime':d.dateTime.strftime("%Y-%m-%d %H:%M"),'show':d.show}
            documentlist.append(dic)
        result={'length':len(documentlist),'limit':limit,'end':start+len(documentlist),'result':documentlist,'total':query.count()}
        return getResult(True,u'查找数据成功',result)
    else:
        return getResult(False,u'查找数据失败,未提供查询关键字',None)