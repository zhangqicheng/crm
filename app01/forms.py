from django import forms
from app01 import models
from django.core.exceptions import ValidationError

class BaseForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class':'form-control'})

#form表单注册
class RegForm(BaseForm):

    re_password=forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(),
        error_messages={'required':'密码不能为空'},
    )

    class Meta:
        model=models.UserProfile
        fields=['username','password','re_password','name','department','email']  #指定字段
        widgets={
            'username':forms.widgets.EmailInput(attrs={'class':'form-control'}),
            'password':forms.widgets.PasswordInput,
        }
        labels={
            'username':'用户名',
            'password':'密码',
            'department':'部门',
            'email':'邮箱',
        }
        error_messages={
            'username':{'required':'用户名不能为空'},
            'password': {'required': '密码不能为空'},
            'email': {'required': '邮件不能为空'},
            'name': {'required': '姓名不能为空'},
            'department': {'required': '部门不能为空'},
        }

    def clean(self):
        pwd=self.cleaned_data.get('password')
        re_pwd=self.cleaned_data.get('re_password')
        if pwd==re_pwd:
            return self.cleaned_data
        self.add_error('re_password','两次密码不一致')
        raise ValidationError('两次密码不一致')

#form客户表单
class CustomerForm(BaseForm):
    class Meta:
        model=models.Customer
        fields='__all__'
        widgets={
            'course':forms.widgets.SelectMultiple
        }

#跟进记录form
class ConsultRecordFrom(BaseForm):
    class Meta:
        model=models.ConsultRecord
        exclude=['delete_status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        customer_choice=[(i.id,i.name) for i in self.instance.consultant.customers.all()]
        customer_choice.insert(0,('','--------'))
        self.fields['customer'].widget.choices=customer_choice

#报名记录form
class EnrollmentListForm(BaseForm):
    class Meta:
        model=models.Enrollment
        exclude=['delete_status','contract_approved']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['customer'].widget.choices=[(self.instance.customer_id,self.instance.customer)]
        self.fields['enrolment_class'].widget.choices=[(i.id,i) for i in self.instance.customer.class_list.all()]


