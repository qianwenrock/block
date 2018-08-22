from django import forms

from user.models import User

# 字段太多就会导致和数据库的交互过于频繁，另外通过一个form类解决此问题
class RegisterForm(forms.ModelForm):
   class Meta:
       # 关联的表
       model = User
       # 关联的字段
       fields = ['nickname', 'password', 'icon', 'age', 'sex']
   # 验证的密码字段
   password2 = forms.CharField(max_length=128)
   # 固定搭配 需要对那个字段进行清洗 就将那个字段放到clean后面（就是用来检查数据的）
   # def clean_password(self):
   #     # 取得关联字段数据  全放在clean中
   #     cleaned_data = super().clean()
   #     # 判断密码长度是否小于6位数
   #     if len(cleaned_data.get('password')) < 6:
   #         # 抛异常，最终显示到error信息中
   #         raise forms.ValidationError('弱口令')


   def clean_password2(self):
       # 取得关联字段数据  字段全在clean中
       cleaned_data = super().clean()
       # 分别获取两次的密码 进行比对
       password =  cleaned_data.get('password')
       password2 = cleaned_data.get('password2')
       # 判断两次密码是否相等
       if password != password2:
           # 抛异常，最终显示到error信息中
           raise forms.ValidationError('两次密码不一致')