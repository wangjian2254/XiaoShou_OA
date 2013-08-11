#coding=utf-8
# Create your views here.
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import Examination, Score, Choice, Topic, Depatement, Person
from xiaoshou_oa.tools import getResult, client_login_required, permission_required
from xiaoshou_oa.views_xiaoshou import getDepartmentByDepartment


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
    for m in Examination.objects.filter(isdel=False).filter(joins=request.user.person).order_by('-dateTime'):
        d={'id':m.pk,'name':m.name,'dateTime':m.dateTime.strftime("%Y-%m-%d %H:%M"),'time':m.time}
        if str(m.pk) in kaoshiset:
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
    examindict={'id':examin.pk,'name':examin.name,'dateTime':examin.dateTime.strftime("%Y-%m-%d %H:%M"),'time':examin.time}
    sl=Score.objects.filter(user=request.user).filter(examination=examin).order_by('-id')[:1]
    if len(sl)>0:
        examindict['score']=sl[0].score
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
        try:
            s.save()
        except:
            return getResult(False,u'已经考过了，不能再考试。')
        result={'right':righttopic,'error':errortopic,'total':totaltopic,'score':score}
        return getResult(True,u'交卷成功',result)



@login_required
@permission_required
def getScoreQuery(request):
    '''
    查询考试统计
    '''
    return render_to_response('oa/kaoshiList.html', RequestContext(request,
                                                                             {'depatementlist': Depatement.objects.all(),
                                                                              'kaoshilist': Examination.objects.order_by('-id').all()}))


def queryRecord(users, product, dategroup):
    query = Score.objects.filter(user__in=users).filter(examination__in=product).order_by('-examination').order_by('id')

    productList = []
    userlist=[]
    orderdict = {}
    for order in query:
        k = '%s-%s' % (order.user_id, order.examination_id)

        orderdict[k]={'username':order.user.username,'get_full_name':order.user.get_full_name(),'score':order.score,'kaoshiname':order.examination.name,'kaoshi':order.examination_id}
        if hasattr(getattr(getattr(order.user.person, 'depate', ''), 'manager', ''),'get_full_name'):
            orderdict[k]['managername'] = getattr(getattr(order.user.person, 'depate', ''), 'manager', '').get_full_name()
        else:
            orderdict[k]['managername'] =u'';
        if order.examination not in productList:
            productList.append(order.examination)
        if order.user not in userlist:
            userlist.append(order.user)


    for examination in productList:
        row = {}
        row['name'] = examination.name
        row['query'] = []
        for user in userlist:
            k = '%s-%s' % (user.pk,examination.pk)
            if not orderdict.has_key(k):
                continue

            row['query'].append(orderdict[k])
        row['totalnum']=len(row['query'])
        dategroup.append(row)

def queryExcel(filename, dategroup, response):
    '''
    导出excel
    '''
    filename += u'.xls'
    response['Content-Disposition'] = (u'attachment;filename=%s' % filename).encode('utf-8')
    import xlwt
    from xlwt import Font, Alignment

    style1 = xlwt.XFStyle()
    font1 = Font()
    font1.height = 260
    font1.name = u'仿宋'
    style1.font = font1
    algn = Alignment()
    algn.horz = Alignment.HORZ_LEFT
    style1.alignment = algn
    style1.font = font1
    style0 = xlwt.XFStyle()
    algn0 = Alignment()
    algn0.horz = Alignment.HORZ_CENTER
    font = Font()
    font.height = 220
    font.bold = False
    font.name = u'仿宋'
    style0.alignment = algn0
    style0.font = font
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u"考试报表", cell_overwrite_ok=True)
    rownum = 0
    ws.write_merge(rownum, rownum, 0, 0, u'序号', style0)
    ws.write_merge(rownum, rownum, 1, 1, u'员工ID', style0)
    ws.write_merge(rownum, rownum, 2, 2, u'姓名', style0)
    ws.write_merge(rownum, rownum, 3, 3, u'得分', style0)
    ws.write_merge(rownum, rownum, 4, 4, u'主管', style0)
    rownum += 1
    datanum = 1
    for data in dategroup:
        ws.write_merge(rownum, rownum, 0, 4, u'考试：%s  人数：%s' % (data['name'],data['totalnum']), style1)
        rownum += 1
        for i, row in enumerate(data['query']):
            ws.write_merge(rownum, rownum, 0, 0, datanum, style0)
            ws.write_merge(rownum, rownum, 1, 1, row['username'], style0)
            ws.write_merge(rownum, rownum, 2, 2, row['get_full_name'], style0)
            ws.write_merge(rownum, rownum, 3, 3, row['score'], style0)
            ws.write_merge(rownum, rownum, 4, 4, row['managername'], style0)

            datanum += 1
            rownum += 1
    for i in range(5):
        ws.col(i).width = 256 * 10
    wb.save(response)

@login_required
@permission_required
def getScoreDetailQuery(request):
    '''
    查询考试统计
    '''
    depatementid = request.REQUEST.get('depatementid')

    kaoshiids = request.REQUEST.getlist('kaoshiid')
    filename = u'考试统计'

    if depatementid:
        d = []
        depatement = Depatement.objects.get(pk=depatementid)
        d.append(depatement)
        filename += u'_%s' % depatement.name
        for i in range(5):
            for depat in getDepartmentByDepartment(d):
                d.append(depat)

        users = []
        for u in Person.objects.filter(depate__in=d):
            users.append(u.user)


    else:
        users = User.objects.filter(is_superuser=False)
        filename += u'_所有人'
        # if productid:
    #     product = Product.objects.filter(pk__in=productid)
    # el
    if kaoshiids:
        productmodels = Examination.objects.filter(pk__in=kaoshiids)
    else:
        productmodels = []

    dategroup = []
    queryRecord(users, productmodels, dategroup)

    if request.REQUEST.get('isExcel'):
        response = HttpResponse(mimetype=u'application/ms-excel')

        queryExcel(filename, dategroup, response)
        return response
    return render_to_response('oa/userkaoshiListPage.html', RequestContext(request, {'query': dategroup}))



@client_login_required
def getAllKaoShi(request):
    '''
    获取所有我参与的考试
    '''
    kaoshilist=[]

    for m in Examination.objects.filter(isdel=False).order_by('-dateTime'):
        d={'id':m.pk,'name':m.name}
        kaoshilist.append(d)
    return getResult(True,u'下载数据成功',kaoshilist)


@client_login_required
def getScoreClient(request):
    '''
    手机查询考试统计
    '''
    depatementid = request.REQUEST.get('depatementid')

    kaoshiids = request.REQUEST.getlist('kaoshiid')

    if depatementid:
        d = []
        depatement = Depatement.objects.get(pk=depatementid)
        d.append(depatement)
        for i in range(5):
            for depat in getDepartmentByDepartment(d):
                d.append(depat)

        users = []
        for u in Person.objects.filter(depate__in=d):
            users.append(u.user)


    else:
        users = User.objects.filter(is_superuser=False)
    if kaoshiids:
        productmodels = Examination.objects.filter(pk__in=kaoshiids)
    else:
        productmodels = []

    dategroup = []
    resultList = []
    queryRecord(users, productmodels, dategroup)
    for data in dategroup:
        resultList.append({'date':u'考试：%s  人数：%s' % (data['name'], data['totalnum'])})
        for i, row in enumerate(data['query']):
            resultList.append(row)
    return getResult(True,u'获取数据成功',resultList)