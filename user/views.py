from django.shortcuts import render,redirect
# django里面封装的有对密码的相关处理（加密）
from django.contrib.auth.hashers import make_password,check_password
from user.models import User
from user.forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        # 生成对象 参数为字典形式，也就是传入的数据
        # 上传的图片是存在FILES中的
        form = RegisterForm(request.POST, request.FILES)
        # 判断输入的是否是有效的
        if form.is_valid():
            # 不仅可以将user提交到数据库中，还可以将图片保存到文件中去
            # 由于form和user表管理，所以有save方法
            user = form.save(commit=False)  #save先临时执行一下但是不立马保存到数据库中去
            user.password = make_password(user.password)
            user.save()
            #记录用户的登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            # 跳转到用户信息模块 后面不需要跟着参数，因为参数存在session只要用户没退出都可用session
            return redirect('/user/info/')
        else:
           return render(request, 'register.html', {'error':form.errors})
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    # 对session进行操作即可
    request.session.flush()
    return redirect('/user/register/')


def user_info(request):
    # 从session中获取用户的id
    uid = request.session.get('uid')
    # 根据用户id找到用户
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user':user})