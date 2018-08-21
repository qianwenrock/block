from django.shortcuts import render,redirect
from post.models import Post
# Create your views here.
# 帖子列表操作
def post_list(request):
    return render(request, 'post_list.html' ,{})

# 创建帖子的操作
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 根据title和content创建帖子
        post = Post.objects.create(title=title, content=content)
        # 创建完成之后跳转到阅读页面
        return redirect('/post/read/?post_id=%s' %post.id)
    return render(request, 'create_post.html')

# 修改帖子的操作
def edit_post(request):
    return render(request, 'edit_post.html', {})

# 阅读帖子的操作
def read_post(request):
    # 获取post_id
    post_id = int(request.GET.get('post_id'))
    # 根据请求参数所携带的post_id查找到对应的post
    post = Post.objects.get(id=post_id)
    return render(request, 'read_post.html', {'post':post})

# 搜索帖子的操作
def search_post(request):
    return render(request, 'search_post.html', {})