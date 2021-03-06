#coding=utf-8
# Create your views here.
from django.contrib.auth import  login as auth_login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from xiaoshou_oa.models import Person, Depatement
from xiaoshou_oa.tools import getResult, permission_required, client_login_required
from xiaoshou_oa.views_xiaoshou import getDepartmentByDepartment


@login_required
@permission_required
def userAdd(request):
    '''
    添加、修改用户信息
    离职用户
    '''
    id = request.REQUEST.get('userid')
    user = {}
    if id:
        user = User.objects.get(pk=id)
    return render_to_response('oa/userSave.html', RequestContext(request, {'person': user, 'depatementlist':Depatement.objects.filter(isdel=False)}))

@login_required
@permission_required
def check_username(request):
    username = request.REQUEST.get('username')
    count=User.objects.filter(username=username).count()
    if count>0:
        return getResult(False,u'用户名已经注册过了')
    else:
        return getResult(True,u'用户名可用')
@login_required
@permission_required
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
        user = User.objects.get(pk=id)
        user.first_name = fullname
        user.is_active = True

        person = user.person
        if not person:
            person = Person()
    else:
        user = User()
        user.username = username
        user.set_password('111111')
        user.first_name = fullname
        user.is_active = True
        person = Person()
        count=User.objects.filter(username=username).count()
        if count>0:
            return getResult(False,u'用户名已经注册过了')
    user.save()
    person.user = user
    if sex == '0':
        person.sex = True
    else:
        person.sex = False
    person.tel = tel
    if depate:
        try:
            depate = Depatement.objects.get(pk=depate)
        except:
            depate = None
            pass
    if depate:
        person.depate = depate
    else:
        person.depate = None

    person.save()
    if id:
        message = u'修改成功'
    else:
        message = u'添加成功'
    return getResult(True, message, user.id)


@login_required
@permission_required
def userOpen(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('userid')
    if id:
        try:
            user = User.objects.get(pk=id)

            # if user.is_active:
            user.is_active = True
            msg=u'开通用户成功'
            # else:
            # user.is_active = False
            # msg=u'设置用户离职成功'
            user.save()
            return getResult(True,msg )
        except:
            return getResult(False, msg)
    return getResult(False, u'请传递用户id')

@login_required
@permission_required
def userDelete(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('userid')
    if id:
        try:
            user = User.objects.get(pk=id)
            user.is_active = False
            user.save()
            return getResult(True, u'设置用户离职成功')
        except:
            return getResult(False, u'用户不存在')
    return getResult(False, u'请传递用户id')

@login_required
@permission_required
def userPassword(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('userid')
    if id:
        try:
            user = User.objects.get(pk=id)
            user.set_password('111111')
            user.save()
            return getResult(True, u'重置用户密码成功')
        except:
            return getResult(False, u'用户不存在')
    return getResult(False, u'请传递用户id')

@login_required
@permission_required
def userPWD_get(request):
    '''
    修改用户密码
    '''
    id = request.REQUEST.get('userid')
    user = {}
    if id:
        user = User.objects.get(pk=id)
    return render_to_response('oa/userPWD.html', RequestContext(request, {'person': user}))


@login_required
@permission_required
def userPWD(request):
    '''
    离职用户
    '''
    id = request.REQUEST.get('userid')
    password = request.REQUEST.get('password')
    if id:
        try:
            user = User.objects.get(pk=id)
            user.set_password(password)
            user.save()
            return getResult(True, u'重置用户密码成功')
        except:
            return getResult(False, u'用户不存在')
    return getResult(False, u'请传递用户id')

@login_required
@permission_required
def userDeviceid(request):
    '''
    重置用户设备
    '''
    id = request.REQUEST.get('userid')
    if id:
        try:
            user = User.objects.get(pk=id)
            user.person.deviceid=None
            user.person.save()
            return getResult(True, u'注销用户设备指纹成功，用户可以使用新的设备。')
        except:
            return getResult(False, u'用户不存在')
    return getResult(False, u'请传递用户id')


@login_required
@permission_required
def userList(request):
    return render_to_response('oa/userList.html', RequestContext(request, { 'depatelist' : Depatement.objects.all()}))


@login_required
@permission_required
def userListPage(request):
    username = request.REQUEST.get('ygbh')
    fullname = request.REQUEST.get('truename')
    depate = request.REQUEST.get('depate')
    isdel = request.REQUEST.get('isdel')

    userquery = User.objects.filter(is_superuser=False)
    if username:
        userquery = userquery.filter(username__contains=username)
    if fullname:
        userquery = userquery.filter(first_name__contains=fullname)
    if isdel=='1':
        userquery = userquery.filter(is_active=False)
    else:
        userquery = userquery.filter(is_active=True)
    if depate:
        depatement = Depatement.objects.get(pk=depate)
        userquery = userquery.filter(person__in=Person.objects.filter(depate=depatement))
    return render_to_response('oa/userListPage.html', RequestContext(request, {'userlist': userquery}))


def clientLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if username:
            userlist = User.objects.filter(username=username)[:1]
            if len(userlist)>0:
                user=userlist[0]
                if not user.is_active:
                    return getResult(False,u'用户已经离职，不能在使用本系统。')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():


            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return getResult(True,u'登录成功')
        else:
            return getResult(False,u'用户名密码错误')



@client_login_required
def userListClient(request):
    '''
    手机查询 用户下属
    '''

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
    l=[]
    for u in users:
        l.append({'fullname':u.get_full_name(),'id':u.pk,'username':u.username,'allname':u'%s:%s'%(u.username,u.get_full_name())})
    return getResult(True,u'获取到所有下属',l)