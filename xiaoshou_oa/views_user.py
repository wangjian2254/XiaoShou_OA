#coding=utf-8
# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import Person, Depatement
from xiaoshou_oa.tools import getResult


@login_required
def default(request):
    return render_to_response('workframe.html',RequestContext(request))
@login_required
def top(request):
    return render_to_response('topnav.html',RequestContext(request))
@login_required
def menu(request):
    return render_to_response('menu.html',RequestContext(request))
@login_required
def welcome(request):
    return render_to_response('welcome.html',RequestContext(request,{'num':range(30)}))


@login_required
def userAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id=request.REQUEST.get('userid')
    user={}
    if id:
        user=User.objects().get(pk=id)
    return render_to_response('oa/userSave.html',RequestContext(request,{'person':user}))

@login_required
def userSave(request):
    '''
    保存用户信息
    '''
    id = request.REQUEST.get('userid')
    username = request.REQUEST.get('ygbh')
    fullname = request.REQUEST.get('truename')
    sex = request.REQUEST.get('sex')
    tel = request.REQUEST.get('tel')

    depate = request.REQUEST.get('bmid')

    if id:
        user = User.objects().get(pk=id)
        user.first_name=fullname
        user.is_active=True

        person=user.person
        if person:
            person=Person()
    else:
        user = User()
        user.username=username
        user.set_password('111111')
        user.first_name=fullname
        user.is_active=True
        person = Person()
    user.save()
    person.user=user
    if sex=='0':
        person.sex=True
    else:
        person.sex=False
    person.tel=tel
    if depate:
        try:
            depate=Depatement.objects.get(pk=depate)
        except:
            depate=None
            pass
    if depate:
        person.depate=depate
    person.save()

    return getResult(True,u'操作成功')

@login_required
def userDelete(request):
    '''
    离职用户
    '''
    id=request.REQUEST.get('userid')
    if id:
        try:
            user = User.objects().get(pk=id)
            user.is_active=False
            return getResult(True,u'设置用户离职成功')
        except:
            return getResult(False,u'用户不存在')
    return getResult(False,u'请传递用户id')


@login_required
def userList(request):
    return render_to_response('oa/userList.html',RequestContext(request,{}))
@login_required
def userListPage(request):
    username = request.REQUEST.get('ygbh')
    fullname = request.REQUEST.get('truename')
    depate = request.REQUEST.get('depate')

    userquery = User.objects.all()
    if username:
        userquery=userquery.filter(username__contains=username)
    if fullname:
        userquery = userquery.filter(first_name__contains=fullname)
    if depate:
        depatement=Depatement.objects.get(pk=depate)
        userquery = userquery.filter(person__in=Person.objects.filter(depate=depatement))
    return render_to_response('oa/userListPage.html',RequestContext(request,{'userlist':userquery}))


