#coding=utf-8
#author:u'王健'
#Date: 13-7-19
#Time: 下午9:01
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import  CheckboxSelectMultiple
from xiaoshou_oa.models import ProductType, ProductBrands, Gift, ProductModel, ProductOrder, DocumentKind, Document, DocumentImage, Choice, Topic, Examination, Person

__author__ = u'王健'

from django.contrib import admin


def make_deled(self, request, queryset):
        rows_updated=queryset.update(isdel=True)
        if rows_updated == 1:
            message_bit = "%s 条记录成功被设为删除状态。"%rows_updated
        self.message_user(request,message_bit)
make_deled.short_description = u"将所选的记录设为删除状态"


def make_opened(self, request, queryset):
        rows_updated=queryset.update(isdel=False)
        if rows_updated == 1:
            message_bit = "%s 条记录成功被设为使用状态。"%rows_updated
        self.message_user(request,message_bit)
make_opened.short_description = u"将所选的记录设为使用状态"

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name','flag','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    ordering = ('-name',)
    actions = [make_deled,make_opened]
class ProductBrandsAdmin(admin.ModelAdmin):
    list_display = ('name','flag','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    ordering = ('-name',)
    actions = [make_deled,make_opened]
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name','flag','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    ordering = ('-name',)
    actions = [make_deled,make_opened]
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','flag','productModel')
    list_filter = ('productModel',)
    search_fields=('name','productModel')
    ordering = ('-name',)
    actions = [make_deled,make_opened]
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name','flag','brands','isdel')
    list_filter = ('isdel','brands')
    search_fields=('name','brands')
    ordering = ('-brands',)
    actions = [make_deled,make_opened]

admin.site.register(ProductType,ProductTypeAdmin)
admin.site.register(ProductBrands,ProductBrandsAdmin)
admin.site.register(Gift,GiftAdmin)
admin.site.register(ProductModel,ProductModelAdmin)
admin.site.register(ProductOrder)

class DocumentKindAdmin(admin.ModelAdmin):
    list_display = ('name','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    actions = [make_deled,make_opened]

admin.site.register(DocumentKind,DocumentKindAdmin)


class DocumentImageAdmin(admin.TabularInline):
    model = DocumentImage
    extra = 1


class DocumentAdmin(admin.ModelAdmin):
    fields = ['title','kind','author','content','dateTime','show','isdel']
    list_display = ('title','kind','dateTime','author','show','isdel')
    list_filter = ('kind','dateTime','isdel',)
    search_fields=('title','kind__name',)
    actions = [make_deled,make_opened]
    inlines = (DocumentImageAdmin,)

admin.site.register(Document,DocumentAdmin)


class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 4


class TopicAdmin(admin.ModelAdmin):
    fields = ['title','isdel']
    list_display = ('title','isdel')
    list_filter = ('isdel',)
    search_fields=('title',)
    actions = [make_deled,make_opened]
    inlines = (ChoiceAdmin,)

admin.site.register(Topic,TopicAdmin)



class ExaminationForm(forms.ModelForm):
    users=User.objects.filter(is_staff=False).filter(is_active=True)
    userlist=Person.objects.filter(user__in=users)
    joins=forms.ModelMultipleChoiceField(queryset=userlist,widget=CheckboxSelectMultiple,label=u'参与考试者')
    topiclist=Topic.objects.filter(isdel=False)
    topics=forms.ModelMultipleChoiceField(queryset=topiclist,widget=CheckboxSelectMultiple,label=u'考试试题')
    class Meta:
        model = Examination
class ExaminationAdmin(admin.ModelAdmin):
    fields = ['name','dateTime','time','isdel','joins','topics']
    list_display = ('name','dateTime','time')
    list_filter = ('name','dateTime','time','isdel',)
    search_fields=('name','joins__username','joins__first_name')
    actions = [make_deled,make_opened]
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }
    form = ExaminationForm
    # inlines = (TopicExamAdmin,)

admin.site.register(Examination,ExaminationAdmin)





  