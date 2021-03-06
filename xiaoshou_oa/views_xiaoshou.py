#coding=utf-8
# Create your views here.
import StringIO
import json

import datetime
import urllib
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from XiaoShouOA import settings
from xiaoshou_oa.models import ProductType, ProductBrands, ProductModel, ProductOrder, Depatement, Gift, Office, Person
from xiaoshou_oa.tools import getResult, permission_required, client_login_required
from django.contrib.auth.models import User


@login_required
@permission_required
def userXiaoShouList(request):
    return render_to_response('oa/userxiaoshouList.html', RequestContext(request,
                                                                         {'depatementlist': Depatement.objects.all(),
                                                                          'giftlist': Gift.objects.all(),
                                                                          'productTypelist': ProductType.objects.all(),
                                                                          'productBrandslist': ProductBrands.objects.all(),
                                                                          'productModellist': ProductModel.objects.all().order_by(
                                                                              'brands'),
                                                                          'today': datetime.datetime.now()}))


def queryRecord(users, product, startdate, enddate, dategroup, productTypeid, giftid,officeids=None):
    query = ProductOrder.objects.filter(user__in=users).filter(product__in=product)
    query = query.filter(clientDate__gte=startdate).filter(clientDate__lte=enddate)
    if productTypeid:
        types = ProductType.objects.filter(pk__in=productTypeid)
        query = query.filter(type__in=types)
    if giftid:
        gifts = Gift.objects.filter(pk__in=giftid)
        query = query.filter(gift__in=gifts)
    if officeids:
        query=query.filter(office__in=officeids)
    query = query.order_by('clientDate').order_by('clientTime').order_by('office').order_by('user')

    # datadict={}
    # for order in query:
    #     if not datadict.has_key('%s_%s'%(order.clientDate,order.office_id)):
    #         datadict['%s_%s'%(order.clientDate,order.office_id)]=[]
    #         dategroup.append({'date':order.clientDate,'office':order.office,'query':datadict['%s_%s'%(order.clientDate,order.office_id)]})
    #     datadict['%s_%s'%(order.clientDate,order.office_id)].append(order)
    datelist = []
    officelist = []
    userlist = []
    productTypeList = []
    productList = []
    orderdict = {}
    for order in query:
        k = '%s-%s-%s-%s-%s' % (order.clientDate, order.office_id, order.user_id, order.type_id, order.product_id)
        if not orderdict.has_key(k):
            orderdict[k] = {'order': order, 'num': 0}
        orderdict[k]['num'] += 1
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
    datelist.sort(reverse=True)
    for date in datelist:

        for officeid in officelist:
            row = {}
            row['date'] = date
            row['officename'] = Office.objects.get(pk=officeid).name
            row['query'] = []
            phonenum=0
            for userid in userlist:
                for typeid in productTypeList:
                    for productid in productList:
                        k = '%s-%s-%s-%s-%s' % (date, officeid, userid, typeid, productid)
                        if not orderdict.has_key(k):
                            continue
                        porder = {}
                        porder['username'] = orderdict[k]['order'].user.username
                        if hasattr(getattr(getattr(orderdict[k]['order'].user.person, 'depate', ''), 'manager', ''),'get_full_name'):
                            porder['managername'] = getattr(getattr(orderdict[k]['order'].user.person, 'depate', ''), 'manager', '').get_full_name()
                        else:
                            porder['managername'] =u'';
                        porder['get_full_name'] = orderdict[k]['order'].user.get_full_name()
                        porder['ordernum'] = orderdict[k]['num']
                        porder['ordertypename'] = orderdict[k]['order'].type.name
                        porder['productname'] = orderdict[k]['order'].product.name
                        porder['productbrandsname'] = orderdict[k]['order'].product.brands.name
                        row['query'].append(porder)
                        phonenum+=orderdict[k]['num']
            row['totalnum']=phonenum
            dategroup.append(row)


def getDepartmentByDepartment(depates):
    d = set()
    for depat in Depatement.objects.filter(fatherDepart__in=depates):
        d.add(depat)
    return d


@login_required
@permission_required
def userProductOrderQuery(request):
    '''
    查询用户销售记录

    '''
    depatementid = request.REQUEST.get('depatementid')
    productTypeid = request.REQUEST.getlist('productTypeid')
    giftid = request.REQUEST.getlist('giftid')
    productBrandsid = request.REQUEST.getlist('productBrandsid')
    productModelid = request.REQUEST.getlist('productModelid')
    # productid = request.REQUEST.getlist('productid')
    startdate = request.REQUEST.get('startdate')
    enddate = request.REQUEST.get('enddate')
    filename = ''
    if not startdate or not enddate:
        startdate = datetime.datetime.now().strftime('%Y-%m-%d')
        enddate = datetime.datetime.now().strftime('%Y-%m-%d')
        # startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    # enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    filename += u'%s_%s' % (startdate, enddate)
    if depatementid:
        d = []
        depatement = Depatement.objects.get(pk=depatementid)
        d.append(depatement)
        filename += u'_%s' % depatement.name
        for i in range(5):
            for depat in getDepartmentByDepartment(d):
                d.append(depat)

        users = [request.user]
        for u in Person.objects.filter(depate__in=d):
            users.append(u.user)


    else:
        users = User.objects.filter(is_superuser=False)
        filename += u'_所有人'
        # if productid:
    #     product = Product.objects.filter(pk__in=productid)
    # el
    if productModelid:
        productmodels = ProductModel.objects.filter(pk__in=productModelid)
        # product=Product.objects.filter(brands__in=productmodels)
    elif productBrandsid:
        productbrand = ProductBrands.objects.filter(pk__in=productBrandsid)
        productmodels = ProductModel.objects.filter(brands__in=productbrand)
        # product=Product.objects.filter(brands__in=productmodels)
    else:
        productmodels = []

    dategroup = []
    queryRecord(users, productmodels, startdate, enddate, dategroup, productTypeid, giftid)

    if request.REQUEST.get('isExcel'):
        response = HttpResponse(mimetype=u'application/ms-excel')

        queryExcel(filename, dategroup, response)
        return response
    return render_to_response('oa/userxiaoshouListPage.html', RequestContext(request, {'query': dategroup}))


def queryExcel(filename, dategroup, response):
    filename += u'.xls'
    response['Content-Disposition'] = (u'attachment;filename=%s' % filename).encode('utf-8')
    import xlwt
    from xlwt import Font, Alignment

    style1 = xlwt.XFStyle()
    font1 = Font()
    font1.height = 360
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
    font.height = 320
    font.bold = False
    font.name = u'仿宋'
    style0.alignment = algn0
    style0.font = font
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u"销售报表", cell_overwrite_ok=True)
    rownum = 0
    ws.write_merge(rownum, rownum, 0, 0, u'序号', style0)
    ws.write_merge(rownum, rownum, 1, 1, u'品牌', style0)
    ws.write_merge(rownum, rownum, 2, 2, u'型号', style0)
    ws.write_merge(rownum, rownum, 3, 3, u'类型', style0)
    ws.write_merge(rownum, rownum, 4, 4, u'数量', style0)
    ws.write_merge(rownum, rownum, 5, 5, u'账户', style0)
    ws.write_merge(rownum, rownum, 6, 6, u'姓名', style0)
    ws.write_merge(rownum, rownum, 7, 7, u'主管', style0)
    rownum += 1
    datanum = 1
    for data in dategroup:
        ws.write_merge(rownum, rownum, 0, 7, u'日期：%s   厅台：%s   总计：%s 台' % (data['date'], data['officename'],data['totalnum']), style1)
        rownum += 1
        for i, row in enumerate(data['query']):
            ws.write_merge(rownum, rownum, 0, 0, datanum, style0)
            ws.write_merge(rownum, rownum, 1, 1, row['productbrandsname'], style0)
            ws.write_merge(rownum, rownum, 2, 2, row['productname'], style0)
            ws.write_merge(rownum, rownum, 3, 3, row['ordertypename'], style0)
            ws.write_merge(rownum, rownum, 4, 4, row['ordernum'], style0)
            ws.write_merge(rownum, rownum, 5, 5, row['username'], style0)
            ws.write_merge(rownum, rownum, 6, 6, row['get_full_name'], style0)
            ws.write_merge(rownum, rownum, 7, 7, row['managername'], style0)
            datanum += 1
            rownum += 1
    for i in range(8):
        ws.col(i).width = 256 * 20
    wb.save(response)
    # wb.save(settings.STATIC_ROOT+'/upload/'+filename)


@client_login_required
def userXiaoShouOrderUpdate(request):
    '''
    用户手机端上传销售记录
    '''
    id = request.REQUEST.get('id')
    productid = request.REQUEST.get('ProductModel')
    producttype = request.REQUEST.get('ProductType')
    productgifts = request.REQUEST.getlist('Gift')
    productoffice = request.REQUEST.get('Office')
    imie = request.REQUEST.get('imie')
    tel = request.REQUEST.get('tel', '')
    orderNumber = request.REQUEST.get('order')
    clientDate = request.REQUEST.get('clientDate')
    clientTime = request.REQUEST.get('clientTime')

    if not productid or not producttype or not productoffice or not imie or not orderNumber or not clientDate or not clientTime:
        return getResult(False, u'数据不足，请录入必要数据')
    if 0<ProductOrder.objects.filter(imie=imie).count():
        return getResult(False, u'设备IMIE重复，请扫描正确的条形码。')
    if not id:
        order = ProductOrder()
        order.user = request.user
        order.serverDate = datetime.datetime.now().strftime('%Y-%m-%d')
        order.clientDate = clientDate
        order.clientTime = clientTime
        msg = u'数据提交成功'

    else:
        order = ProductOrder.objects.get(pk=id)
        msg = u'数据修改成功'

    order.product = ProductModel.objects.get(flag=productid)
    order.type = ProductType.objects.get(flag=producttype)
    order.office = Office.objects.get(pk=productoffice)
    order.imie = imie
    order.tel = tel
    order.orderNumber = orderNumber


    order.save()
    for g in Gift.objects.filter(flag__in=productgifts):
        order.gift.add(g)
    order.save()

    return getResult(True, u'数据提交成功.', order.id)


@client_login_required
def userProductOrderClient(request):
    '''
    手机查询 销售统计信息
    '''
    userids = request.REQUEST.getlist('userids')
    officeids = request.REQUEST.getlist('officeids')
    productTypeid = request.REQUEST.getlist('productTypeid')
    productBrandsid = request.REQUEST.getlist('productBrandsid')
    productModelid = request.REQUEST.getlist('productModelid')
    startdate = request.REQUEST.get('startdate')
    enddate = request.REQUEST.get('enddate')
    if not startdate or not enddate:
        startdate = datetime.datetime.now().strftime('%Y-%m-%d')
        enddate = datetime.datetime.now().strftime('%Y-%m-%d')
        # startdate = datetime.datetime.strptime(startdate+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    # enddate = datetime.datetime.strptime(enddate+' 23:59:59', '%Y-%m-%d %H:%M:%S')
    if not userids:
        user = request.user
        if hasattr(user,'department_manager'):
            d = []
            depatement = user.department_manager
            d.append(depatement)
            for i in range(5):
                for depat in getDepartmentByDepartment(d):
                    d.append(depat)

            users = [request.user]
            for u in Person.objects.filter(depate__in=d):
                users.append(u.user)
        else:
            users = [user]
    else:
        users=User.objects.filter(pk__in=userids)

    if productModelid:
        productmodels = ProductModel.objects.filter(pk__in=productModelid)
        # product=Product.objects.filter(brands__in=productmodels)
    elif productBrandsid:
        productbrand = ProductBrands.objects.filter(pk__in=productBrandsid)
        productmodels = ProductModel.objects.filter(brands__in=productbrand)
        # product=Product.objects.filter(brands__in=productmodels)
    else:
        productmodels = ProductModel.objects.all()
    officelist=[]
    if officeids:
        officelist=Office.objects.filter(pk__in=officeids)

    dategroup = []
    queryRecord(users, productmodels, startdate, enddate, dategroup, productTypeid, None,officelist)
    resultList=[]
    for data in dategroup:
        resultList.append({'date':u'日期：%s   厅台：%s   总计：%s 台' % (data['date'], data['officename'],data['totalnum'])})
        for i, row in enumerate(data['query']):
            mapdata={'productbrandsname':row['productbrandsname'],'productname':row['productname'],'ordertypename':row['ordertypename'],'ordernum':row['ordernum'],'get_full_name':row['get_full_name'],'managername':row['managername']}
            resultList.append(mapdata)
    return getResult(True, u'获取数据成功', resultList)





