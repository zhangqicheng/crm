from django.shortcuts import render,HttpResponse,redirect,reverse
from django.contrib import auth
from django.views import View
from django.db.models import Q
from django.http import QueryDict
from app01.forms import RegForm,CustomerForm,ConsultRecordFrom,EnrollmentListForm
from app01 import models
from utils.pager import PageInfo

#登录
def login(request):
    err_msg=''
    if request.method=='GET':
        return render(request,'login.html')
    else:
        #取出数据
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        #业务处理:验证用户存在
        user=auth.authenticate(request,username=username,password=password,email=email)
        if user is not None:
            #如果验证通过,记录登录状态，并返回首页
            auth.login(request,user)
            return redirect(reverse('index'))
        else:
            err_msg='用户名或密码错误'
            #承接上下文
            context={'error':err_msg}
            return render(request,'login.html',context)

#注册
def reg(request):
    if request.method=='GET':
        form_obj=RegForm()
        return render(request,'reg.html',{'form_obj':form_obj})
    else:
        form_obj=RegForm(request.POST)
        if form_obj.is_valid():
            #创建新用户

            #方法一
            form_obj.cleaned_data.pop('re_password')
            models.UserProfile.objects.create_user(**form_obj.cleaned_data)

            #方法二
            # obj=form_obj.save()
            # obj.set_password(obj.password)
            # obj.save()
            return redirect(reverse('login'))
        else:
            return render(request, 'reg.html', {'form_obj': form_obj})

#客户列表展示CBV
class CustomerList(View):
    def get(self,request):

        #搜索参数
        q=self.get_search_contion(['qq','name','date'])

        if request.path_info == reverse('customer'):
            '''如果识别出为我的客户路径，则自定义分页'''
            count = models.Customer.objects.filter(consultant__isnull=True).count()
            page_info = PageInfo(request.GET.get('page'), count, 4, request.path_info)
            customers = models.Customer.objects.filter(q,consultant__isnull=True)[page_info.start():page_info.end()]
        else:
            count = models.Customer.objects.filter(consultant=request.user).count()
            page_info = PageInfo(request.GET.get('page'), count, 4, request.path_info)
            customers = models.Customer.objects.filter(q,consultant=request.user)[page_info.start():page_info.end()]

        # 获取搜索条件
        query_params = self.get_query_params()

        # 承接上下文
        context = {
            'customers': customers,#显示的客户信息
            'page_info': page_info,#自定义分页
            'query_params':query_params,#获取搜索条件
        }
        return render(request, 'customer.html', context)

    def post(self,request):
        action=request.POST.get('action')
        if not hasattr(self,action):
            return HttpResponse('非法操作')

        ret=getattr(self,action)()
        return self.get(request)

    def multi_apply(self):
        '''共户变私户'''
        ids=self.request.POST.getlist('id')
        models.Customer.objects.filter(id__in=ids).update(consultant=self.request.user)

    def multi_pub(self):
        '''私户变公户'''
        ids=self.request.POST.getlist('id')
        models.Customer.objects.filter(id__in=ids).update(consultant=None)

    def get_search_contion(self,query_list):
        '''搜索'''
        query = self.request.GET.get('query', '')
        q=Q()
        q.connector='OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i),query)))
        return q

    def get_query_params(self):
        url=self.request.get_full_path()
        qd=QueryDict()
        qd._mutable=True
        qd['next']=url
        query_params=qd.urlencode()
        return query_params

#客户增加
def add_customer(request):
    if request.method=='GET':
        form_obj=CustomerForm()
        #承接上下文
        context={
            'form_obj':form_obj,
        }
        return render(request,'add_customer.html',context)
    else:
        form_obj=CustomerForm(request.POST)
        if form_obj.is_valid():
            #验证通过
            form_obj.save()
            return redirect(reverse('customer'))
        else:
            return render(request, 'add_customer.html',{'form_obj':form_obj})

#客户编辑
def edit_customer(request,edit_id):
    obj = models.Customer.objects.filter(id=edit_id).first()
    if request.method=='GET':
        #查询对应id的客户信息
        form_obj=CustomerForm(instance=obj)
        return render(request,'edit_customer.html',{'form_obj':form_obj})
    else:
        #接收数据
        form_obj=CustomerForm(request.POST,instance=obj)
        if form_obj.is_valid():
            #如果验证通过
            form_obj.save()
            return redirect(reverse('my_customer'))
        else:
            return render(request,'edit_customer.html',{'form_obj':form_obj})

#展示跟进记录
class ConsultRecord(View):

    def get(self,request):
        all_consult_record=models.ConsultRecord.objects.filter(delete_status=False)
        return render(request,'consult_record_list.html',{'all_consult_record':all_consult_record})

#添加跟进记录
def add_consult_record(request):
    if request.method=='GET':
        obj=models.ConsultRecord(consultant=request.user)
        form_obj=ConsultRecordFrom(instance=obj)
        return render(request,'add_consult_record.html',{'form_obj':form_obj})
    else:
        form_obj=ConsultRecordFrom(request.POST)
        if form_obj.is_valid():
            #如果通过验证
            form_obj.save()
            return redirect(reverse('consult_record'))
        else:
            return render(request,'add_consult_record.html',{'form_obj':form_obj})

#编辑跟进记录
def edit_consult_record(request,edit_id):
    obj = models.ConsultRecord.objects.filter(id=edit_id).first()
    if request.method=='GET':
        form_obj=ConsultRecordFrom(instance=obj)
        return render(request, 'edit_consult_record.html', {'form_obj': form_obj})
    else:
        #接受数据
        form_obj=ConsultRecordFrom(request.POST,instance=obj)
        if form_obj.is_valid():
            #如果验证通过
            form_obj.save()
            return redirect(reverse('consult_record'))
        else:
            return render(request, 'add_consult_record.html', {'form_obj': form_obj})

#展示报名记录
class EnrollmentList(View):

    def get(self,request):
        count = models.Enrollment.objects.filter(customer__consultant=request.user).count()
        print(count)
        page_info = PageInfo(request.GET.get('page'), count, 4, request.path_info)
        enrollment_list = models.Enrollment.objects.filter(delete_status=False,customer__consultant=request.user)[page_info.start():page_info.end()]

        # 获取搜索条件
        query_params = self.get_query_params()

        context = {
            'enrollment_list': enrollment_list,  # 显示的报名记录
            'page_info': page_info,  # 自定义分页
            'query_params':query_params,
        }
        return render(request,'enrollment_list.html',context)

    def get_query_params(self):
        url=self.request.get_full_path()
        qd=QueryDict()
        qd._mutable=True
        qd['next']=url
        query_params=qd.urlencode()
        return query_params

#添加报名记录
def add_enrollment_list(request,customer_id):
    obj = models.Enrollment(customer_id=customer_id)
    if request.method=='GET':
        form_obj=EnrollmentListForm(instance=obj)
        return render(request,'enrollment.html',{'form_obj':form_obj})
    else:
        form_obj=EnrollmentListForm(data=request.POST,instance=obj)
        if form_obj.is_valid():
            #如果验证通过
            enrollment_obj=form_obj.save()
            enrollment_obj.customer.status='signed'
            enrollment_obj.customer.save()
            next=request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(reverse('my_customer'))
        else:
            return render(request, 'enrollment.html', {'form_obj': form_obj})

#编辑报名记录
def edit_enrollment_list(request,edit_id):
    obj = models.Enrollment.objects.filter(id=edit_id).first()
    if request.method=='GET':
        form_obj=EnrollmentListForm(instance=obj)
        return render(request,'enrollment.html',{'form_obj':form_obj})
    else:
        form_obj = EnrollmentListForm(data=request.POST, instance=obj)
        if form_obj.is_valid():
            #如果验证通过
            enrollment_obj=form_obj.save()
            enrollment_obj.customer.status='signed'
            enrollment_obj.customer.save()
            next=request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(reverse('enrollment_list'))

#首页
def index(request):
    return HttpResponse('ok')