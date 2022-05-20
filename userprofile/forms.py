from django.contrib.auth.models import User
from django import forms
from .models import Profile


# 登录表单，继承了 forms.Form 类
# 因为是登录而非注册所以用forms.Form
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    """用户注册表单"""
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    # def clean_password2()中的内容便是在验证密码是否一致了。
    # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")


# 个人主页表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
