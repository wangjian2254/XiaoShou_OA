#coding=utf-8
# Create your views here.
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import Examination, Score, Choice, Topic
from xiaoshou_oa.tools import getResult, client_login_required


@client_login_required
def getMyKaoShi(request):
    '''
    获取所有我参与的考试
    '''
    kaoshilist=[]
    kaoshidict={}
    kaoshilist_nonescore=[]
    for m in Score.objects.filter(user=request.user).order_by('-id'):
        kaoshidict['%s'%m.examination_id]=m.score
    kaoshiset=kaoshidict.keys()
    for m in Examination.objects.filter(isdel=False).filter(joins=request.user):
        d={'name':m.name,'dateTime':m.dateTime.strftime("%Y-%m-%d %H:%M"),'time':m.time}
        if m.pk in kaoshiset:
            d['score']=kaoshidict['%s'%m.pk]
            kaoshilist.append(d)
        else:
            kaoshilist_nonescore.append(d)
    result={'kaoshilist':kaoshilist,'kaoshilist_nonescore':kaoshilist_nonescore}
    return getResult(True,u'下载数据成功',result)


@client_login_required
def getExamination(request):
    '''
    根据考试获取所有考题，开始考试
    '''
    examinationid=request.REQUEST.get('examinationid','')

    examin=Examination.objects.get(pk=examinationid)
    if examin.isdel:
        return getResult(False,u'考试已经被删除。')
    examindict={'name':examin.name,'dateTime':examin.dateTime.strftime("%Y-%m-%d %H:%M"),'time':examin.time}
    examindict['topics']=[]
    topicsdict={}
    topicslist=[]
    for t in examin.topics.filter(isdel=False).all():
        tdic={'title':t.title,'id':t.pk,'choicelist':[]}
        topicslist.append(t)
        examindict['topics'].append(tdic)
        topicsdict['%s'%t.pk]=tdic
    for c in Choice.objects.filter(topic__in=topicslist).order_by('index'):
        topicsdict['%s'%c.topic_id]['choicelist'].append({'id':c.pk,'content':c.content,'isright':c.isright,'index':c.index})
    return getResult(True,u'下载数据成功',examindict)

@client_login_required
def getScore(request):
    '''
    根据答案生成得分，并存储
    '''
    examid=request.REQUEST.get('examinationid','')
    examin=Examination.objects.get(pk=examid)
    if examin.isdel:
        return getResult(False,u'考试已经被删除。')
    value=request.REQUEST.get('value','')
    try:
        if value:
            value=json.loads(value)
    except:
        value=None
    if value:
        totaltopic=len(value.keys())
        righttopic=0
        errortopic=0
        for choice in Choice.objects.filter(topic__in=value.keys()).filter(isright=True):
            if str(value.get('%s'%choice.topic_id,''))==str(choice.pk):
                righttopic+=1
            else:
                errortopic+=1
        score=int(int(righttopic)*1.0/int(totaltopic)*100)
        s=Score()
        s.user=request.user
        s.examination=examin
        s.score=score
        s.save()
        result={'right':righttopic,'error':errortopic,'total':totaltopic,'score':score}
        return getResult(True,u'交卷成功',result)


