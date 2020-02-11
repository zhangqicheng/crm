"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('index/',views.index,name='index'),
    path('reg/',views.reg,name='reg'),
    path('customer/',views.CustomerList.as_view(),name='customer'),#公共客户列表
    path('my_customer/',views.CustomerList.as_view(),name='my_customer'),#私有客户列表
    path('customer/add/',views.add_customer,name='add_customer'),
    re_path('customer/edit/(\w+)/',views.edit_customer,name='edit_customer'),

    #展示跟进记录
    path('consult_record_list/',views.ConsultRecord.as_view(),name='consult_record'),
    #添加跟进记录
    path('consult_record_list/add/',views.add_consult_record,name='add_consult_record'),
    #编辑跟进记录
    re_path('consult_record_list/edit/(\d+)$',views.edit_consult_record,name='edit_consult_record'),

    #展示报名记录
    re_path('enrollment_list/',views.EnrollmentList.as_view(),name='enrollment_list'),
    #添加报名记录
    re_path('enrollment_list/add/(\d+)/',views.add_enrollment_list,name='add_enrollment'),
    #编辑报名记录
    re_path('enrollment_list/edit/(\d+)/',views.edit_enrollment_list,name='edit_enrollment'),
]
