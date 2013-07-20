#coding=utf-8
# Create your views here.
import json

import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import ProductType, ProductBrands, ProductModel, ProductOrder, Depatement, Gift, Office, Person
from xiaoshou_oa.tools import getResult, permission_required, client_login_required
from django.contrib.auth.models import User


@login_required
@permission_required
def userXiaoShouList(request):
    return render_to_response('oa/userxiaoshouList.html', RequestContext(request, { 'depatementlist':Depatement.objects.all(),'giftlist':Gift.objects.all(),'productTypelist':ProductType.objects.all(), 'productBrandslist':ProductBrands.objects.all(), 'productModellist':ProductModel.objects.all().order_by('brands'), 'today':datetime.datetime.now()}))


def queryRecord(users,product,startdate,enddate,dategroup,productTypeid,giftid):
    query = ProductOrder.objects.filter(user__in=users).filter(product__in=product)
    query = query.filter(clientDate__gte=startdate).filter(clientDate__lte=enddate)
    if productTypeid:
        types=ProductType.objects.filter(pk__in=productTypeid)
        query=query.filter(type__in=types)
    if giftid:
        gifts=Gift.objects.filter(pk__in=giftid)
        query=query.filter(gift__in=gifts)
    query = query.order_by('clientDate').order_by('clientTime').order_by('office').order_by('user')

    # datadict={}
    # for order in query:
    #     if not datadict.has_key('%s_%s'%(order.clientDate,order.office_id)):
    #         datadict['%s_%s'%(order.clientDate,order.office_id)]=[]
    #         dategroup.append({'date':order.clientDate,'office':order.office,'query':datadict['%s_%s'%(order.clientDate,order.office_id)]})
    #     datadict['%s_%s'%(order.clientDate,order.office_id)].append(order)
    datelist=[]
    officelist=[]
    userlist=[]
    productTypeList=[]
    productList=[]
    orderdict={}
    for order in query:
        k='%s-%s-%s-%s-%s'%(order.clientDate,order.office_id,order.user_id,order.type_id,order.product_id)
        if not orderdict.has_key(k):
            orderdict[k]={'order':order,'num':0}
        orderdict[k]['num']+=1
        if order.clientDate not in datelist:
            datelist.append(order.clientDate)
        if order.office_id not in officelist:
            officelist.append(order.office_id)
        if order.user_id not in userlist:
            userlist.append(order.user_id)
        if order.type_id not in productTypeList:
            productTypeList.append(order.type_id)
        if order.product_id not in productList:
            productList.append(order.product_id)
    for date in datelist:

        for officeid in officelist:
            row={}
            row['date']=date
            row['office']=Office.objects.get(pk=officeid)
            row['query']=[]
            for userid in userlist:
                for typeid in productTypeList:
                    for productid in productList:
                        k='%s-%s-%s-%s-%s'%(date,officeid,userid,typeid,productid)
                        if not orderdict.has_key(k):
                            continue
                        porder={}
                        porder['user']=orderdict[k]['order'].user
                        porder['order']=orderdict[k]
                        porder['product']=orderdict[k]['order'].product
                        row['query'].append(porder)
            dategroup.append(row)


def getDepartmentByDepartment(depates):
    d=set()
    for depat in Depatement.objects.filter(fatherDepart__in=depates):
        d.add(depat)
    return d


@login_required
@permission_required
def userProductOrderQuery(request):
    '''
    查询用户签到信息

    '''
    depatementid = request.REQUEST.get('depatementid')
    productTypeid = request.REQUEST.getlist('productTypeid')
    giftid = request.REQUEST.getlist('giftid')
    productBrandsid = request.REQUEST.getlist('productBrandsid')
    productModelid = request.REQUEST.getlist('productModelid')
    # productid = request.REQUEST.getlist('productid')
    startdate = request.REQUEST.get('startdate')
    enddate = request.REQUEST.get('enddate')
    if not startdate or not enddate:
        startdate=datetime.datetime.now().strftime('%Y-%m-%d')
        enddate=datetime.datetime.now().strftime('%Y-%m-%d')
    # startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    # enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    if depatementid:
        d=[]
        depatement=Depatement.objects.get(pk=depatementid)
        d.append(depatement)

        for i in range(5):
            for depat in getDepartmentByDepartment(d):
                d.append(depat)

        users=[]
        for u in Person.objects.filter(depate__in=d):
            users.append(u.user)


    else:
        users=User.objects.filter(is_superuser=False)
    # if productid:
    #     product = Product.objects.filter(pk__in=productid)
    # el
    if productModelid:
        productmodels=ProductModel.objects.filter(pk__in=productModelid)
        # product=Product.objects.filter(brands__in=productmodels)
    elif productBrandsid:
        productbrand=ProductBrands.objects.filter(pk__in=productBrandsid)
        productmodels=ProductModel.objects.filter(brands__in=productbrand)
        # product=Product.objects.filter(brands__in=productmodels)
    else:
        productmodels=ProductModel.objects.all()



    dategroup=[]
    queryRecord(users,productmodels,startdate,enddate,dategroup,productTypeid,giftid)
    return render_to_response('oa/userxiaoshouListPage.html', RequestContext(request, {'query': dategroup}))

#
# @client_login_required
# def userProductOrderClient(request):
#     '''
#     手机查询 签到信息
#     '''
#     qiandaoid = request.REQUEST.get('qiandaoid','').split(',')
#     qiandaoid.remove('')
#     startdate = request.REQUEST.get('startdate')
#     enddate = request.REQUEST.get('enddate')
#     if not startdate or not enddate:
#         raise Http404
#     startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
#     enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
#     user=request.user
#     users=[user]
#     d=[]
#     for i in range(5):
#         u=getUserByDepartment(users,d)
#         users.extend(u)
#
#     if qiandaoid:
#         qiandao = QianDao.objects.filter(pk__in=qiandaoid)
#     else:
#         qiandao=[]
#     dategroup=[]
#     queryRecord(users,qiandao,startdate,enddate,dategroup)
#     querylist=[]
#     for datedict in dategroup:
#         querylist.append({'date':datedict['date'], 'query':[]})
#         for uqd in datedict['query']:
#             querylist[-1]['query'].append({'id':uqd.pk, 'userid':uqd.user.pk ,'username':uqd.user.username, 'truename':uqd.user.get_full_name, 'dateTime':uqd.dateTime.strftime('%H:%M'), 'gps':uqd.gps, 'address':uqd.address, 'officeid':uqd.office.pk, 'office':uqd.office.name})
#     return getResult(True,u'获取数据成功',querylist)
#
#
# @client_login_required
# def userProductOrderUploadClient(request):
#     '''
#     手机端提交签到信息
#     '''
#     user=request.user
#     id = request.REQUEST.get('qiandaoid')
#     if id:
#         try:
#             qiandao = QianDao.objects.get(pk=id)
#         except:
#             return getResult(False, u'签到服务不存在')
#     else:
#         return getResult(False, u'请传递签到服务id')
#     gps = request.REQUEST.get('gps')
#     if gps=='null,null':
#         return getResult(False, u'GPS信息不正确')
#     address = request.REQUEST.get('address')
#     officeid = request.REQUEST.get('officeid')
#     userQianDao = UserQianDao()
#     userQianDao.user = user
#     userQianDao.qiandao = qiandao
#     if gps:
#         userQianDao.gps = gps
#     if address:
#         userQianDao.address = address
#     if officeid:
#         userQianDao.office=Office.objects.get(pk=officeid)
#     else:
#         return getResult(False,u'请选择签到厅台信息')
#     userQianDao.dateTime=datetime.datetime.now()
#     userQianDao.save()
#     return getResult(True, u'提交签到信息成功',{'time':userQianDao.dateTime.strftime("%Y-%m-%d %H:%M:%S"),'id':id})
#
#
#
# @client_login_required
# def qiandaoListClient(request):
#     l = []
#     for qiandao in QianDao.objects.all():
#         if qiandao.isdel:
#             l.append({'id':qiandao.id, 'isdel':qiandao.isdel})
#         else:
#             l.append({'id':qiandao.id, 'name':qiandao.name, 'needTime':qiandao.needTime, 'needGPS':qiandao.needGPS, 'needAddress':qiandao.needAddress, 'isdel':qiandao.isdel})
#
#     return getResult(True, u'更新签到服务成功', l)



