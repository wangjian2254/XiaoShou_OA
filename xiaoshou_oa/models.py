# coding=utf-8

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from xiaoshou_oa.tools import distance


class Depatement(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'职位后缀名称', help_text=u'部门的名称')
    manager = models.OneToOneField(User, blank=True,null=True, related_name=u'department_manager', verbose_name=u'管理者', help_text=u'部门管理者')
    fatherDepart = models.ForeignKey('Depatement', blank=True, null=True, related_name=u'department_father',
                                     verbose_name=u'父级部门', help_text=u'部门隶属关系')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')

    def __unicode__(self):
        return u'%s_%s' % (self.manager.get_full_name(), self.name)


class Person(models.Model):
    user = models.OneToOneField(User)
    sex = models.BooleanField(default=True, verbose_name=u'性别', help_text=u'性别')
    depate = models.ForeignKey(Depatement, blank=True,null=True, related_name=u'user_depate', verbose_name=u'隶属部门', help_text=u'员工隶属的部门')
    tel = models.CharField(max_length=15, verbose_name=u'电话')
    deviceid=models.CharField(max_length=100,unique=True,blank=True,null=True,verbose_name=u'手机唯一编码',help_text=u'手机的指纹')


class Office(models.Model):
    name = models.CharField(unique=True, max_length=30, verbose_name=u'厅台名称', help_text=u'厅台的名称')
    flag = models.CharField(unique=True, max_length=30, verbose_name=u'厅台字母缩写', help_text=u'厅台字母缩写，唯一')
    gps = models.CharField(blank=True, null=True, max_length=100, verbose_name=u'gps信息', help_text=u'厅台的gps信息')
    address = models.CharField(blank=True, null=True, max_length=100, verbose_name=u'街道地址', help_text=u'根据gps获取的街道信息')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    def __unicode__(self):
        return self.name

class QianDao(models.Model):
    name = models.CharField(unique=True, max_length=20, verbose_name=u'名称', help_text=u'签到服务的名称')
    standardtime=models.CharField(max_length=10,blank=True, null=True,verbose_name=u'标准时间')
    type=models.BooleanField(default=True,verbose_name=u'在标准时间前或后')
    needTime = models.BooleanField(default=True, verbose_name=u'每天唯一', help_text=u'是否每天唯一，按照最后一次签到信息')
    needGPS = models.BooleanField(default=True, verbose_name=u'需要GPS', help_text=u'是否GPS信息')
    needAddress = models.BooleanField(default=True, verbose_name=u'需要街道地址', help_text=u'是否需要街道信息')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')

    def hour(self):
        if self.standardtime:
            return int(self.standardtime.split(':')[0])
        else:
            return 0
    def min(self):
        if self.standardtime:
            return int(self.standardtime.split(':')[1])
        else:
            return 0
    def __unicode__(self):
        return self.name



class UserQianDao(models.Model):
    user = models.ForeignKey(User, verbose_name=u'签到人', help_text=u'发出签到信息的用户')
    qiandao = models.ForeignKey(QianDao, verbose_name=u'签到项目', help_text=u'进行签到的项目，上班、下班等等')
    dateTime = models.DateTimeField(auto_created=True, verbose_name=u'签到发生时间', help_text=u'提交到服务器上的时间')
    gps = models.CharField(blank=True, null=True, max_length=100, verbose_name=u'gps信息', help_text=u'手机端获取的gps信息')
    office = models.ForeignKey(Office, blank=True, null=True, verbose_name=u'签到厅台', help_text=u'签到的位置')
    address = models.CharField(blank=True, null=True, max_length=100, verbose_name=u'街道地址', help_text=u'根据gps获取的街道信息')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')

    def officeDistance(self):
        return distance(self.gps,self.office.gps)
    def addressHG(self):
        if self.officeDistance()>1000:
            return u'超过1000米'
        else:
            return u'千米内'
    def timeDistance(self):
        hour=str(self.dateTime.hour)
        minute=str(self.dateTime.minute)
        if len(hour)==1:
            hour='0'+hour
        if len(minute)==1:
            minute='0'+minute
        t='%s:%s'%(hour,minute)
        if t>self.qiandao.standardtime:
            if self.qiandao.type:
                return False
            else:
                return True
        elif t==self.qiandao.standardtime:
            return True
        else:
            if self.qiandao.type:
                return True
            else:
                return False



class DocumentKind(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=u'文档分类', help_text=u'文档的分类')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    def __unicode__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'文档标题', help_text=u'文档的标题')
    kind = models.ForeignKey(DocumentKind, verbose_name=u'文档分类')
    dateTime = models.DateTimeField(auto_created=True, verbose_name=u'创建时间', help_text=u'提交到服务器上的时间')
    author = models.ForeignKey(User, verbose_name=u'作者', help_text=u'创建文档的人')
    show = models.IntegerField(default=1, verbose_name=u'浏览次数', help_text=u'浏览文档的次数')
    content = models.TextField(blank=True, null=True, verbose_name=u'文档内容', help_text=u'文档内容的段')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    def __unicode__(self):
        return self.title

class DocumentImage(models.Model):
    img = models.ImageField(blank=True, null=True, upload_to='media/upload/images', verbose_name=u'图片')
    document = models.ForeignKey(Document, verbose_name=u'隶属文档')
    index = models.IntegerField(verbose_name=u'排序')

class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'题目', help_text=u'选择题的题目')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    def __unicode__(self):
        return self.title

class Choice(models.Model):
    content = models.CharField(max_length=100, verbose_name=u'选项', help_text=u'选择题的选项')
    index = models.IntegerField(verbose_name=u'索引', help_text=u'选项索引')
    isright = models.BooleanField(default=False, verbose_name=u'是否正确', help_text=u'是否是正确答案')
    topic = models.ForeignKey(Topic, verbose_name=u'题目', help_text=u'隶属题目')
    def __unicode__(self):
        return self.content

class Examination(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'考试名称', help_text=u'给考试起个名字，方便查询')
    dateTime = models.DateTimeField(auto_created=True, verbose_name=u'创建时间', help_text=u'提交到服务器上的时间')
    joins = models.ManyToManyField(User, verbose_name=u'参与考试的用户', help_text=u'参与考试的员工')
    topics = models.ManyToManyField(Topic, verbose_name=u'试卷的考题', help_text=u'组成试卷的考题')
    time = models.IntegerField(verbose_name=u'考试时间', help_text=u'单位为分钟')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    def __unicode__(self):
        return self.name

class Score(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    examination = models.ForeignKey(Examination, verbose_name=u'考试')
    score = models.IntegerField(verbose_name=u'得分')
    def __unicode__(self):
        return u'%s-%s'%(self.user,self.score)

class ProductType(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'类型', help_text=u'合约、裸机……')
    flag = models.CharField(max_length=50,unique=True, verbose_name=u'唯一标记', help_text=u'从其他系统导入的数据的id')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')

    class Admin():
        pass
    class Meta():
        verbose_name=u'机器类型（合约、裸机）'
    def __unicode__(self):
        return self.name


class ProductBrands(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'品牌', help_text=u'')
    flag = models.CharField(max_length=50,unique=True, verbose_name=u'唯一标记', help_text=u'从其他系统导入的数据的id')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')

    class Admin():
        pass
    class Meta():
        verbose_name=u'品牌'
    def __unicode__(self):
        return self.name



class Gift(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'礼物名称', help_text=u'礼物的名称')
    flag = models.CharField(max_length=50,unique=True, verbose_name=u'唯一标记', help_text=u'从其他系统导入的数据的id')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    class Admin():
        pass
    class Meta():
        verbose_name=u'礼物'
    def __unicode__(self):
        return self.name



class ProductModel(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'机型名称', help_text=u'')
    flag = models.CharField(max_length=50,unique=True, verbose_name=u'唯一标记', help_text=u'从其他系统导入的数据的id')
    brands = models.ForeignKey(ProductBrands, verbose_name=u'机型的品牌', help_text=u'品牌的机型')
    isdel = models.BooleanField(default=False, verbose_name=u'是否删除', help_text=u'不再使用')
    class Admin():
        pass
    class Meta():
        verbose_name=u'机型'
    def __unicode__(self):
        return u'%s-%s'%(self.name,self.brands.name)

#
#
# class Product(models.Model):
#     name = models.CharField(max_length=30, verbose_name=u'产品名称', help_text=u'产品的名称')
#     flag = models.CharField(max_length=50, verbose_name=u'唯一标记', help_text=u'从其他系统导入的数据的id')
#     productModel = models.ForeignKey(ProductModel, verbose_name=u'机型', help_text=u'机器型号')
#     class Admin():
#         pass
#     class Meta():
#         verbose_name=u'产品'
#     def __unicode__(self):
#         return self.name



class ProductOrder(models.Model):
    product = models.ForeignKey(ProductModel, verbose_name=u'终端')
    type = models.ForeignKey(ProductType, verbose_name=u'合约类型')
    gift = models.ManyToManyField(Gift,null=True,blank=True, verbose_name=u'配套礼品')
    user = models.ForeignKey(User, verbose_name=u'用户')
    office = models.ForeignKey(Office, verbose_name=u'厅台')
    imie = models.CharField(max_length=30, unique=True, verbose_name=u'imie', help_text=u'每个手机唯一')
    tel = models.CharField(max_length=15,null=True,blank=True, verbose_name=u'客户手机号', help_text=u'客户的联系方式')
    orderNumber = models.CharField(max_length=50, verbose_name=u'订单id', help_text=u'同一次提交，保持一致')

    serverDate = models.CharField(max_length=10, verbose_name=u'服务器端日期', help_text=u'2013-06-07')
    clientDate = models.CharField(max_length=10, verbose_name=u'客户端日期', help_text=u'2013-07-09')
    clientTime = models.CharField(max_length=10, verbose_name=u'客户端时间', help_text=u'14:30')










