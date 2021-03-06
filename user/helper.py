import requests
from django.conf import settings
from django.shortcuts import redirect


def get_wb_access_token(code):
    # 由于需要在不修改全局变量的情况下对这个字典就行添加，所以对这个字典参数进行复制一份
    args =settings. WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    # 发送请求，这个respo就是微博给服务器的响应
    response = requests.post(settings.WB_ACCESS_TOKEN_API,data=args)
    # 判断返回状态码是否为200
    if response.status_code == 200:
        return response.json()
    else:
        return {'error':'Weibo server error'}

def get_wb_user_show(access_token, uid):
    '''获取微博个人信息'''
    args = settings.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = uid
    #发送get请求 获取响应
    response = requests.get(settings.WB_USER_SHOW_API, params=args)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Weibo server error'}

# 用来验证用户是否登录
def login_required(func):
    def wrapper(request):
        # 登录肯定有uid
        uid = request.session.get('uid')
        # 判断用户是否登录
        if uid is None:
            # 未登录,重定向到登录界面
            return redirect('/user/login/')
        else:
            # 已登录,进行后面的操作
            return func(request)
    return wrapper
