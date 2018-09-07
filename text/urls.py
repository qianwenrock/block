"""text URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin


from post import views as post_views
from user import views as user_views

urlpatterns = [
    # 帖子的url
    # 添加默认
    url(r'^$', post_views.post_list),
    # 帖子列表
    url(r'^post/list/', post_views.post_list),
    # 创建帖子
    url(r'^post/create/', post_views.create_post),
    # 修改帖子
    url(r'^post/edit/', post_views.edit_post),
    # 阅读帖子
    url(r'^post/read/', post_views.read_post),
    # 搜索帖子
    url(r'^post/search/', post_views.search_post),
    # 帖子排行
    url(r'^post/top10/', post_views.top10),

    # 用户的url
    #
    url(r'^user/register/', user_views.register),
    url(r'^user/login/', user_views.login),
    url(r'^user/logout/', user_views.logout),
    url(r'^user/info/', user_views.user_info),

    # 第三方登录接口
    url(r'^weibo/callback/', user_views.wb_callback)
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
