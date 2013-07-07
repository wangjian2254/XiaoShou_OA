#coding=utf-8
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext


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
def userSave(request):
    id=request.REQUEST.get('userid')
    user={}
    if id:
        user=User.objects().get(id)
    return render_to_response('oa/saveUser.html',RequestContext(request,{'person':user}))