#coding=utf-8
# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import Person, Depatement
from xiaoshou_oa.tools import getResult



@login_required
def depatementAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id=request.REQUEST.get('depatementid')
    depatement={}
    userlist=[]
    depatementlist=Depatement.objects.filter(isdel=False)

    if id:
        depatement=Depatement.objects.get(pk=id)
        personquery=Person.objects.filter(depate=depatement)
        userlist=User.objects.filter(person__in=personquery)
        depatementlist=depatementlist.exclude(id=depatement.id)
    return render_to_response('oa/depatementSave.html',RequestContext(request,{'depatement':depatement,'userlist':userlist, 'userall':User.objects.filter(is_superuser=False), 'depatementlist':depatementlist}))

@login_required
def depatementSave(request):
    '''
    保存用户信息
    '''
    id = request.REQUEST.get('depatementid')
    name = request.REQUEST.get('name')
    depatementfatherid = request.REQUEST.get('depatementfatherid')
    userid = request.REQUEST.get('managerid')


    if id:
        depate = Depatement.objects.get(pk=id)
        msg=u'修改职务信息成功'

    else:
        depate = Depatement()
        msg=u'添加职务信息成功'
    depate.name=name
    depate.save()
    if depatementfatherid:
        depatefather=Depatement.objects.get(pk=depatementfatherid)
        depate.fatherDepart=depatefather
        depate.save()
    if userid:
        user=User.objects.get(pk=userid)
        depate.manager=user
        depate.save()
        user.person.depate=depate
        user.person.save()
        user.save()

    return getResult(True,msg,depate.id)

@login_required
def depatementDelete(request):
    '''
    离职用户
    '''
    id=request.REQUEST.get('depatementid')
    if id:
        try:
            depate = Depatement.objects.get(pk=id)
            count=Person.objects.filter(depate=depate).count()
            if 0<count:
                return getResult(False,u'该职务还有属下，请先删除该职务底属下员工。')
            depate.isdel=True
            depate.save()
            return getResult(True,u'删除职务成功')
        except:
            return getResult(False,u'职务不存在')
    return getResult(False,u'请传递职务id')


@login_required
def depatementOpen(request):
    '''
    离职用户
    '''
    id=request.REQUEST.get('depatementid')
    if id:
        try:
            depate = Depatement.objects.get(pk=id)
            depate.isdel=False
            depate.save()
            return getResult(True,u'删除职务成功')
        except:
            return getResult(False,u'职务不存在')
    return getResult(False,u'请传递职务id')


@login_required
def depatementList(request):
    return render_to_response('oa/depatementList.html',RequestContext(request,{'depatementlist':Depatement.objects.all()}))


@login_required
def depatementPeopleDel(request):
    id=request.REQUEST.get('depatementid')
    userid=request.REQUEST.get('userid')
    if id:
        depatement=Depatement.objects.get(pk=id)
    else:
        return HttpResponseRedirect('/oa/depatementPeople/?type=1&depatementid=%s'%id)
    if userid:
        user=User.objects.get(pk=userid)
    else:
        return HttpResponseRedirect('/oa/depatementPeople/?type=2&depatementid=%s'%id)
    person=Person.objects.filter(depate=depatement).filter(user=user)[:1]
    if len(person):
        person=person[0]
    else:
        return HttpResponseRedirect('/oa/depatementPeople/?type=3&depatementid=%s'%id)
    if person.user.id==depatement.manager_id:
        return HttpResponseRedirect('/oa/depatementPeople/?type=4&depatementid=%s'%id)
    person.depate=None
    person.save()
    return HttpResponseRedirect('/oa/depatementPeople/?type=5&depatementid=%s'%id)

@login_required
def depatementPeopleAdd(request):
    id=request.REQUEST.get('depatementid')
    userid=request.REQUEST.get('userid')
    if id:
        depatement=Depatement.objects.get(pk=id)
    else:
        return HttpResponseRedirect('/oa/depatementPeople/?type=1&depatementid=%s'%id)
    if userid:
        user=User.objects.get(pk=userid)
    else:
        return HttpResponseRedirect('/oa/depatementPeople/?type=2&depatementid=%s'%id)
    person=Person.objects.filter(user=user)[:1]
    if len(person):
        person=person[0]
    else:
        return HttpResponseRedirect('/oa/depatementPeople/?type=3&depatementid=%s'%id)
    person.depate=depatement
    person.save()
    return HttpResponseRedirect('/oa/depatementPeople/?type=6&depatementid=%s'%id)



@login_required
def depatementPeople(request):
    id=request.REQUEST.get('depatementid')
    depatementlist=Depatement.objects.filter(isdel=False)
    type=request.REQUEST.get('type','')
    if id:
        depatement=Depatement.objects.get(pk=id)
    else:
        depatement=Depatement.objects.filter(isdel=False)[:1]
        if 0<len(depatement):
            depatement=depatement[0]
    emptyuserlist=Person.objects.filter(depate=None)
    userlist=Person.objects.filter(depate=depatement)
    return render_to_response('oa/depatementPeople.html',RequestContext(request,{'type':type, 'depatement':depatement, 'depatementlist':Depatement.objects.filter(isdel=False), 'emptyuserlist':emptyuserlist, 'userlist':userlist}))




