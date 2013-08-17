#coding=utf-8
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import QianDao, UserQianDao, Office, Person, Depatement
from xiaoshou_oa.tools import getResult, permission_required, client_login_required
from django.contrib.auth.models import User
from xiaoshou_oa.views_xiaoshou import getDepartmentByDepartment

import datetime
timezone=datetime.timedelta(hours =8)

@login_required
@permission_required
def qiandaoAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id = request.REQUEST.get('qiandaoid')
    qiandao = {}
    if id:
        qiandao = QianDao.objects.get(pk=id)
    return render_to_response('oa/qiandaoSave.html', RequestContext(request, {'qiandao': qiandao,'hour':range(24),'min':range(60)}))

@login_required
@permission_required
def check_qiandao(request):
    name = request.REQUEST.get('name')
    if name:
        count = QianDao.objects.filter(name=name).count()
        if count>0:
            return getResult(False,u'名称已经注册过了')
        else:
            return getResult(True,u'名称可用')

@login_required
@permission_required
def qiandaoSave(request):
    '''
    保存用户信息
    '''
    id = request.REQUEST.get('qiandaoid')
    name = request.REQUEST.get('name')
    needgps = request.REQUEST.get('needgps')
    needaddress = request.REQUEST.get('needaddress')
    needtime = request.REQUEST.get('needtime')
    type = request.REQUEST.get('type')
    hour = request.REQUEST.get('hour')
    min = request.REQUEST.get('min')
    if hour and  len(hour)==1:
        hour='0'+str(hour)
    if len(min)==1:
        min='0'+str(min)
    if id:
        qiandao = QianDao.objects.get(pk=id)
        msg=u'修改签到服务成功'
    else:
        qiandao = QianDao()
        msg=u'添加签到服务成功'
    qiandao.name = name
    if needgps=='1':
        qiandao.needGPS = True
    else:
        qiandao.needGPS = False
    if needaddress=='1':
        qiandao.needAddress = True
    else:
        qiandao.needAddress = False
    if needtime=='1':
        qiandao.needTime = True
    else:
        qiandao.needTime = False
    if hour:
        if type=='1':
            qiandao.type = True
        else:
            qiandao.type = False
        qiandao.standardtime='%s:%s'%(hour,min)
    qiandao.save()

    return getResult(True, msg, qiandao.id)


@login_required
@permission_required
def qiandaoDelete(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('qiandaoid')
    if id:
        try:
            qiandao = QianDao.objects.get(pk=id)

            qiandao.isdel = True
            qiandao.save()
            return getResult(True, u'删除签到服务成功')
        except:
            return getResult(False, u'签到服务不存在')
    return getResult(False, u'请传递签到服务id')

@login_required
@permission_required
def qiandaoOpen(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('qiandaoid')
    if id:
        try:
            qiandao = QianDao.objects.get(pk=id)

            qiandao.isdel = False
            qiandao.save()
            return getResult(True, u'开通签到服务成功')
        except:
            return getResult(False, u'签到服务不存在')
    return getResult(False, u'请传递签到服务id')


@login_required
@permission_required
def qiandaoList(request):
    return render_to_response('oa/qiandaoList.html', RequestContext(request, {'qiandaolist': QianDao.objects.all()}))




@login_required
@permission_required
def userQianDaoList(request):
    return render_to_response('oa/userqiandaoList.html', RequestContext(request, { 'depatementlist':Depatement.objects.all(), 'qiandaolist':QianDao.objects.all(), 'today':datetime.datetime.utcnow()+timezone}))


def queryRecord(users,qiandao,startdate,enddate,dategroup):
    query = UserQianDao.objects.filter(user__in=users).filter(qiandao__in=qiandao)
    query = query.filter(dateTime__gte=startdate).filter(dateTime__lte=enddate)
    query = query.order_by('dateTime').order_by('office').order_by('user')

    datadict={}
    datelist=[]
    userlist=[]
    dateformate='%Y-%m-%d'
    date=None
    for uqd in query:
        date = uqd.dateTime.strftime(dateformate)
        if date not in datelist:
            datelist.append(date)
        if uqd.user_id not in userlist:
            userlist.append(uqd.user_id)
        if not datadict.has_key('%s-%s-%s'%(date,uqd.user_id,uqd.qiandao_id)):
            datadict['%s-%s-%s'%(date,uqd.user_id,uqd.qiandao_id)]=[]
        datadict['%s-%s-%s'%(date,uqd.user_id,uqd.qiandao_id)].append(uqd)
    datelist.sort(reverse=True)
    for date in datelist:
        row={}
        row['date']=date
        row['rowspan']=3+len(qiandao)
        row['rowspan2']=3+len(qiandao)*5
        row['query']=[]
        for u in users:
            if u.id not in userlist and u.is_active==False:
                continue
            userrow={}
            userrow['user']={'username':getattr(u,'username',''),'get_full_name':getattr(u,'first_name',''),}
            userrow['qiandaolist']=[]
            for qd in qiandao:
                if datadict.has_key('%s-%s-%s'%(date,u.id,qd.id)):
                    oo=datadict['%s-%s-%s'%(date,u.id,qd.id)]
                    l=[]
                    for o in oo:
                        q={'qiandaoname':o.qiandao.name,'officename':getattr(getattr(o,'office',''),'name',''),'officegps':getattr(getattr(o,'office',''),'gps',''),'address':getattr(o,'address',''),'dateTime':o.dateTime.strftime('%H:%M'),'gpsdistance':o.officeDistance(),'time':o.timeDistance()}
                        l.append(q)
                    userrow['qiandaolist'].append(l)
                else:
                    userrow['qiandaolist'].append([])
            row['query'].append(userrow)
        dategroup.append(row)



@login_required
@permission_required
def userQianDaoQuery(request):
    '''
    查询用户签到信息

    '''
    filename=''
    depatementid = request.REQUEST.get('depatementid')
    qiandaoid = request.REQUEST.getlist('qiandaoid')
    mi = request.REQUEST.get('mi',800)
    try:
        mi=int(mi)
    except:
        pass
    startdate = request.REQUEST.get('startdate')
    enddate = request.REQUEST.get('enddate')
    if not startdate or not enddate:
        startdate=(datetime.datetime.utcnow()+timezone).strftime('%Y-%m-%d')
        enddate=(datetime.datetime.utcnow()+timezone).strftime('%Y-%m-%d')
    filename+='%s_%s'%(startdate,enddate)
    startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    if depatementid:
        d=[]
        depatement=Depatement.objects.get(pk=depatementid)
        filename+=u'_%s'%depatement.fullname()
        d.append(depatement)

        for i in range(5):
            for depat in getDepartmentByDepartment(d):
                d.append(depat)

        users=[request.user]
        for u in Person.objects.filter(depate__in=d):
            users.append(u.user)
    else:
        users=User.objects.filter(is_superuser=False)
        filename+=u'_所有人'
    if qiandaoid:
        qiandao = QianDao.objects.filter(pk__in=qiandaoid)
    else:
        qiandao=[]
    dategroup=[]
    queryRecord(users,qiandao,startdate,enddate,dategroup)

    isExcel=request.REQUEST.get('isExcel',None)
    if isExcel:
        response=HttpResponse(mimetype=u'application/ms-excel')
        qiandaoXls(filename,qiandao,dategroup,mi,response)
        return response
            # return HttpResponseRedirect(settings.STATIC_URL+'upload/%s'%urllib.quote(filename.encode('utf-8')))
    return render_to_response('oa/userqiandaoListPage.html', RequestContext(request, {'query': dategroup,'qiandao':qiandao,'mi':mi}))

def qiandaoXls(filename,qiandao,dategroup,mi,response):
    import uuid
    filename+=u'.xls'
    response['Content-Disposition'] = (u'attachment;filename=%s'%filename).encode('utf-8')
    import xlwt
    from xlwt import Font,Alignment
    style1=xlwt.XFStyle()
    font1=Font()
    font1.height=320
    font1.name=u'仿宋'
    style1.font=font1
    algn=Alignment()
    algn.horz=Alignment.HORZ_RIGHT
    style1.alignment=algn
    style0=xlwt.XFStyle()
    algn0=Alignment()
    algn0.horz=Alignment.HORZ_CENTER
    algn0.vert=Alignment.VERT_CENTER
    font=Font()
    font.height=320
    font.bold=False
    font.name=u'仿宋'
    style0.alignment=algn0
    style0.font=font
    style3=xlwt.XFStyle()
    algn3=Alignment()
    algn3.horz=Alignment.HORZ_CENTER
    font3=Font()
    font3.height=320
    font3.bold=False
    font1.name=u'仿宋'
    style3.alignment=algn3
    style3.font=font3
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour =2
    style3.pattern=pattern
    wb=xlwt.Workbook()
    style2=xlwt.XFStyle()
    algn2=Alignment()
    algn2.horz=Alignment.HORZ_LEFT
    font2=Font()
    font2.height=350
    font2.bold=True
    font1.name=u'仿宋'
    style2.alignment=algn2
    style2.font=font2
    wb=xlwt.Workbook()
    ws=wb.add_sheet(u"签到报表",cell_overwrite_ok=True)
    rownum=2
    usernum=1
    ws.write_merge(0,1,0,0,u'序号',style2)
    ws.write_merge(0,1,1,1,u'员工ID',style2)
    ws.col(1).width=0x0d00 +3000
    ws.write_merge(0,1,2,2,u'姓名',style2)
    ws.col(2).width=0x0d00 +3000
    for i,q in enumerate(qiandao):
        ws.write_merge(0,0,5*i+3,5*i+6,q.name,style2)
        ws.write_merge(1,1,5*i+3,5*i+3,u'厅台',style2)
        ws.col(5*i+3).width=0x0d00 + 7000
        ws.write_merge(1,1,5*i+4,5*i+4,u'地址',style2)
        ws.col(5*i+4).width=0x0d00 + 9000
        ws.write_merge(1,1,5*i+5,5*i+5,u'时间',style2)
        ws.write_merge(1,1,5*i+6,5*i+6,u'位置判断',style2)
        ws.col(6).width=0x0d00 +3000
        ws.write_merge(1,1,5*i+7,5*i+7,u'时间判读',style2)
        ws.col(7).width=0x0d00 +3000
    for data in dategroup:
        ws.write_merge(rownum,rownum,0,data['rowspan2'],u'日期：%s'%(data['date'],),style2)
        rownum+=1
        tempnum=0
        for query in data['query']:
            for i,rows in enumerate(query['qiandaolist']):
                for j,row in enumerate(rows):
                    ws.write_merge(rownum+j,rownum+j,3+i*5+0,3+i*5+0,row['officename'],style0)
                    ws.write_merge(rownum+j,rownum+j,3+i*5+1,3+i*5+1,row['address'],style0)
                    ws.write_merge(rownum+j,rownum+j,3+i*5+2,3+i*5+2,row['dateTime'],style0)
                    if row['officegps']:
                        if row['gpsdistance']<mi:
                            ws.write_merge(rownum+j,rownum+j,3+i*5+3,3+i*5+3,u'合格',style0)
                        else:
                            ws.write_merge(rownum+j,rownum+j,3+i*5+3,3+i*5+3,u'不合格',style3)
                    else:
                        ws.write_merge(rownum+j,rownum+j,3+i*5+3,3+i*5+3,u'0',style0)
                    if row['time']:
                        ws.write_merge(rownum+j,rownum+j,3+i*5+4,3+i*5+4,u'合格',style0)
                    else:
                        ws.write_merge(rownum+j,rownum+j,3+i*5+4,3+i*5+4,u'不合格',style3)
                    if tempnum<j:
                        tempnum=j
            ws.write_merge(rownum,rownum+tempnum,0,0,usernum,style0)
            ws.write_merge(rownum,rownum+tempnum,1,1,query['user']['username'],style0)
            ws.write_merge(rownum,rownum+tempnum,2,2,query['user']['get_full_name'],style0)

            rownum+=tempnum+1
            usernum+=1


    wb.save(response)
    # return filename


@client_login_required
def userQianDaoQueryClient(request):
    '''
    手机查询 签到信息
    '''
    qiandaoid = request.REQUEST.getlist('qiandaoid')
    mi = request.REQUEST.get('mi',500)
    try:
        mi=int(mi)
    except:
        pass
    startdate = request.REQUEST.get('startdate','2013-07-01')
    enddate = request.REQUEST.get('enddate','2013-07-29')
    if not startdate or not enddate:
        startdate=(datetime.datetime.utcnow()+timezone).strftime('%Y-%m-%d')
        enddate=(datetime.datetime.utcnow()+timezone).strftime('%Y-%m-%d')
    startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    user=request.user


    if hasattr(user,'department_manager'):
        d=[]
        depatement=user.department_manager
        d.append(depatement)

        for i in range(5):
            for depat in getDepartmentByDepartment(d):
                d.append(depat)

        users=[request.user]
        for u in Person.objects.filter(depate__in=d):
            users.append(u.user)
    else:
        users=[user]

    if qiandaoid:
        qiandao = QianDao.objects.filter(pk__in=qiandaoid)
    else:
        qiandao=QianDao.objects.all()
    dategroup=[]
    queryRecord(users,qiandao,startdate,enddate,dategroup)
    resultList=[]
    for data in dategroup:
        resultList.append({'date':u'日期：%s'%data['date']})
        for query in data['query']:
            for i,rows in enumerate(query['qiandaolist']):
                for j,row in enumerate(rows):

                    mapdata={'qiandaoname':row['qiandaoname'],'get_full_name':query['user']['get_full_name'],'officename':row['officename'],'dateTime':row['dateTime']}
                    if row['officegps']:
                        if row['gpsdistance']<mi:
                            mapdata['gps']=u'合格'
                        else:
                            mapdata['gps']=u'不合格'
                    else:
                        mapdata['gps']=u'缺少数据'
                    if row['time']:
                        mapdata['time']=u'合格'
                    else:
                        mapdata['time']=u'不合格'
                    resultList.append(mapdata)

    return getResult(True,u'获取数据成功',resultList)


@client_login_required
def userqiandaoUploadClient(request):
    '''
    手机端提交签到信息
    '''
    user=request.user
    id = request.REQUEST.get('qiandaoid')
    if id:
        try:
            qiandao = QianDao.objects.get(pk=id)
        except:
            return getResult(False, u'签到服务不存在')
    else:
        return getResult(False, u'请传递签到服务id')
    gps = request.REQUEST.get('gps')
    if gps=='null,null':
        return getResult(False, u'GPS信息不正确')
    address = request.REQUEST.get('address')
    officeid = request.REQUEST.get('officeid')
    userQianDao = UserQianDao()
    userQianDao.user = user
    userQianDao.qiandao = qiandao
    # userQianDao.dateTime=datetime.datetime.utcnow()
    if gps:
        userQianDao.gps = gps
    if address:
        userQianDao.address = address
    if officeid:
        userQianDao.office=Office.objects.get(pk=officeid)
    else:
        return getResult(False,u'请选择签到厅台信息')
    userQianDao.save()
    return getResult(True, u'提交签到信息成功',{'time':userQianDao.dateTime.strftime("%Y-%m-%d %H:%M:%S"),'id':id})



@client_login_required
def qiandaoListClient(request):
    l = []
    for qiandao in QianDao.objects.all():
        if qiandao.isdel:
            l.append({'id':qiandao.id, 'isdel':qiandao.isdel})
        else:
            l.append({'id':qiandao.id, 'name':qiandao.name, 'needTime':qiandao.needTime, 'needGPS':qiandao.needGPS, 'needAddress':qiandao.needAddress, 'isdel':qiandao.isdel})

    return getResult(True, u'更新签到服务成功', l)



