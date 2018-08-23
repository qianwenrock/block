from django.shortcuts import render,redirect
# 导入setting
from django.conf import settings
# django里面封装的有对密码的相关处理（加密）
from django.contrib.auth.hashers import make_password,check_password
from user.models import User
from user.forms import RegisterForm
from user.helper import get_wb_access_token,get_wb_user_show

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
            request.session['avatar'] = user.avatar
            # 跳转到用户信息模块 后面不需要跟着参数，因为参数存在session只要用户没退出都可用session
            return redirect('/user/info/')
        else:
           return render(request, 'register.html', {'error':form.errors})
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        # 获取到用户提交的昵称和密码
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            # 由于get会报错所有给他try下
            user = User.objects.get(nickname=nickname)
        except User.DoseNotExist:
            return render(request, 'login.html', {'error':'用户不存在','auth_url':settings.WB_AUTH_URL})
        # 用户存在 接着进行密码判断
        if check_password(password, user.password):
            # 记录用户的登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            # 因为每个页面都需要avata
            request.session['avatar'] = user.avatar
            # 跳转到用户信息模块 后面不需要跟着参数，因为参数存在session只要用户没退出都可用session
            return redirect('/user/info/')
        else:
            return render(request, 'login.html', {'error': '用户密码错误','auth_url':settings.WB_AUTH_URL})
    return render(request, 'login.html', {'auth_url':settings.WB_AUTH_URL})


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


def wb_callback(request):
    # 获取code
    code = request.GET.get('code')
    result = get_wb_access_token(code)
    # 对返回值进行判断
    if 'error' in result:
        # 将错误信息返回给页面
        return render(request, 'login.html', {'error': result['error'], 'auth_url': settings.WB_AUTH_URL})
    # 获取access_token 有了它就能调用微博的许多东西
    access_token = result['access_token']
    uid = result['uid']

    result = get_wb_user_show(access_token,uid)
    if 'error' in result:
        # 将错误信息返回给页面
        return render(request, 'login.html', {'error': result['error'], 'auth_url': settings.WB_AUTH_URL})
    # 现获取 如果获取不到则进行创建 get_or_create两个返回值，第二个是代表它进行的是获取还是创建过程
    user, created = User.objects.get_or_create(nickname=result['screen_name'])
    if created:
        user.plt_icon = result['avatar_large']
        user.save()

    # 设置用户登录状态
    request.session['uid'] = user.id
    request.session['nickname'] = user.nickname
    request.session['avatar'] = user.avatar
    return redirect('/user/info/')
