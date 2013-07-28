#coding=utf-8
#author:u'王健'
#Date: 13-7-19
#Time: 下午9:01
from xiaoshou_oa.models import ProductType, ProductBrands, Gift, ProductModel, ProductOrder, DocumentKind, Document

__author__ = u'王健'

from django.contrib import admin

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name','flag','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    ordering = ('-name',)
class ProductBrandsAdmin(admin.ModelAdmin):
    list_display = ('name','flag','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    ordering = ('-name',)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('name','flag','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)
    ordering = ('-name',)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','flag','productModel')
    list_filter = ('productModel',)
    search_fields=('name','productModel')
    ordering = ('-name',)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name','flag','brands','isdel')
    list_filter = ('isdel','brands')
    search_fields=('name','brands')
    ordering = ('-brands',)

admin.site.register(ProductType,ProductTypeAdmin)
admin.site.register(ProductBrands,ProductBrandsAdmin)
admin.site.register(Gift,GiftAdmin)
admin.site.register(ProductModel,ProductModelAdmin)
admin.site.register(ProductOrder)

class DocumentKindAdmin(admin.ModelAdmin):
    list_display = ('name','isdel')
    list_filter = ('isdel',)
    search_fields=('name',)

admin.site.register(DocumentKind,DocumentKindAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title','kind','dateTime','author','show','isdel')
    list_filter = ('kind','dateTime','isdel',)
    search_fields=('title','kind__name',)

admin.site.register(Document,DocumentAdmin)



  